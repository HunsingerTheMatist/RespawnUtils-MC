"""
Builds the distributable Respawn Utils zip into builds/:
  RespawnUtils-v<version>-mc<MC versions>-build<n>.zip
where:
  - version is parsed from load.mcfunction's `Version` setter and stripped to
    its first contiguous numeric+dot run (e.g. 'beta 1.0' -> '1.0').
  - MC versions is the supported range, earliest to latest (e.g.
    '1.21.6-1.21.8'), or a single version when both ends match. It is resolved
    offline from pack.mcmeta via _pack_meta.resolve_supported_mc_versions
    (refresh the lookup with fetch_pack_format_versions.py). Year-based ids like
    '26.2.1' are trimmed to major.minor; legacy '1.x.y' ids are kept whole,
    since 1.21.x patch releases often have different pack formats.
  - build # is tracked in build_info.json: increments on each run while the
    version is unchanged, resets to 1 when the version changes.

Predicates are written with the 26.3+ `"type"` condition key. The build adds a
copy of each one using the older `"condition"` key under the CONDITION_KEY_OVERLAY
directory, which pack.mcmeta applies for formats 71-120 (MC 1.21.5-26.2).
"""
import argparse
import json
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from _pack_meta import resolve_supported_mc_versions

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent  # repo root (one level up from tools/)
BUILD_INFO_FILE = SCRIPT_DIR / "build_info.json"
BUILDS_DIR = ROOT / "builds"

LOAD_MCFUNCTION = ROOT / "data" / "respawn" / "function" / "load.mcfunction"
PREDICATE_DIR = ROOT / "data" / "respawn" / "predicate"

# Overlay directory holding the generated `"condition"` key predicates. Must
#  match the overlay entry's "directory" in pack.mcmeta
CONDITION_KEY_OVERLAY = "condition_key"

# Condition types the key conversion can walk, and the fields holding their
#  nested conditions
CONDITION_CHILDREN = {
    "any_of": "terms",
    "all_of": "terms",
    "inverted": "term",
    "location_check": None,
}

# Repo-root entries that make up the pack. Folders are walked recursively.
#  Anything not listed here is excluded from the build
REQUIRED = ["pack.mcmeta", "data", "LICENSE"]
OPTIONAL = ["pack.png", "README.md"]


def parse_version() -> str:
    """Reads load.mcfunction's `data modify storage respawn:data Version set
    value "..."` line and strips the value to its first contiguous numeric+dot
    run (e.g. 'beta 1.0' -> '1.0'). Errors out if the setter line or a numeric
    component is missing."""
    if not LOAD_MCFUNCTION.is_file():
        sys.exit(f"load.mcfunction not found at {LOAD_MCFUNCTION}")
    text = LOAD_MCFUNCTION.read_text(encoding="utf-8")
    setter = re.search(r'storage respawn:data Version set value "([^"]*)"', text)
    if not setter:
        sys.exit("Could not find the Version setter line in load.mcfunction.")
    raw = setter.group(1)
    numeric = re.search(r'[0-9]+(?:\.[0-9]+)*', raw)
    if not numeric:
        sys.exit(f"Version {raw!r} contains no numeric component.")
    return numeric.group(0)


def short_mc_version(full: str) -> str:
    """Shortens an MC release id for the zip name: legacy '1.x.y' ids stay as
    they are (e.g. '1.21.6'), year-based ids like '26.2.1' or '26.2-snapshot-6'
    are trimmed to major.minor (e.g. '26.2')."""
    if full.startswith("1."):
        m = re.match(r'^1\.[0-9]+(?:\.[0-9]+)?', full)
    else:
        m = re.match(r'^[0-9]+\.[0-9]+', full)
    if not m:
        sys.exit(f"MC version {full!r} doesn't start with major.minor.")
    return m.group(0)


def update_build_info(version: str) -> int:
    """Reads build_info.json (creating it on first run), bumps the build number
    if the version is unchanged or resets to 1 if it changed, writes the file
    back, and returns the new build number."""
    if BUILD_INFO_FILE.is_file():
        info = json.loads(BUILD_INFO_FILE.read_text(encoding="utf-8"))
    else:
        info = {}

    if info.get("latest_version") == version:
        info["build_number"] = int(info.get("build_number", 0)) + 1
    else:
        info["latest_version"] = version
        info["build_number"] = 1

    BUILD_INFO_FILE.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    return info["build_number"]


def collect_files() -> dict:
    """Gathers the pack's files as {path in the zip: source path}, from the
    REQUIRED entries and whichever OPTIONAL ones exist."""
    entries = REQUIRED + [e for e in OPTIONAL if (ROOT / e).exists()]
    files = {}
    for entry in entries:
        src = ROOT / entry
        if not src.exists():
            sys.exit(f"Required entry missing from the repo root: {entry}")
        if src.is_file():
            files[entry] = src
            continue
        for sub in sorted(src.rglob("*")):
            # .gitkeep only exists to keep empty dirs in git, so it isn't pack content
            if sub.is_file() and sub.name != ".gitkeep":
                files[sub.relative_to(ROOT).as_posix()] = sub
    return files


def to_condition_key(cond: dict, source: str) -> dict:
    """Returns a copy of a `"type"` key condition using the `"condition"` key,
    converting its nested conditions too. Other keys are copied unchanged, so a
    block state such as a slab's `"type": "top"` is left alone. Errors out on a
    condition without a `"type"` key or of a type CONDITION_CHILDREN lacks."""
    if "type" not in cond:
        sys.exit(f"{source}: condition without a \"type\" key: {json.dumps(cond)[:80]}")
    kind = cond["type"].removeprefix("minecraft:")
    if kind not in CONDITION_CHILDREN:
        sys.exit(f"{source}: condition type {cond['type']!r} needs adding to CONDITION_CHILDREN.")
    children = CONDITION_CHILDREN[kind]
    out = {}
    for key, value in cond.items():
        if key == "type":
            out["condition"] = value
        elif key == children == "terms":
            out[key] = [to_condition_key(c, source) for c in value]
        elif key == children == "term":
            out[key] = to_condition_key(value, source)
        else:
            out[key] = value
    return out


def condition_key_overlay() -> dict:
    """Generates the CONDITION_KEY_OVERLAY copy of every predicate as {path in the
    zip: bytes}. Errors out if pack.mcmeta has no overlay entry for that
    directory."""
    meta = json.loads((ROOT / "pack.mcmeta").read_text(encoding="utf-8"))
    dirs = [e.get("directory") for e in meta.get("overlays", {}).get("entries", [])]
    if CONDITION_KEY_OVERLAY not in dirs:
        sys.exit(f"pack.mcmeta has no overlay entry for directory {CONDITION_KEY_OVERLAY!r}.")
    files = {}
    for src in sorted(PREDICATE_DIR.glob("*.json")):
        rel = src.relative_to(ROOT).as_posix()
        converted = to_condition_key(json.loads(src.read_text(encoding="utf-8")), rel)
        text = json.dumps(converted, indent=4) + "\n"
        files[f"{CONDITION_KEY_OVERLAY}/{rel}"] = text.replace("\n", "\r\n").encode("utf-8")
    return files


def build_pack(zip_path: Path, verbose: bool) -> int:
    """Zips the files 'collect_files' gathers plus the generated
    'condition_key_overlay' files. Returns the file count."""
    if zip_path.exists():
        zip_path.unlink()

    files = collect_files()
    generated = condition_key_overlay()
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zf:
        for rel, src in files.items():
            zf.write(src, rel)
            if verbose:
                print(f"  {rel}")
        for rel, data in generated.items():
            zf.writestr(rel, data)
            if verbose:
                print(f"  {rel} (generated)")
    return len(files) + len(generated)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the distributable Respawn Utils zip.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print every file as it's added to the zip.")
    args = parser.parse_args()

    version = parse_version()
    first, last = (short_mc_version(v) for v in resolve_supported_mc_versions(ROOT))
    mc_version = first if first == last else f"{first}-{last}"
    build = update_build_info(version)

    BUILDS_DIR.mkdir(exist_ok=True)
    zip_name = f"RespawnUtils-v{version}-mc{mc_version}-build{build}.zip"
    if args.verbose:
        print(zip_name)
    written = build_pack(BUILDS_DIR / zip_name, args.verbose)
    print(f"Wrote builds/{zip_name} ({written} files)")


if __name__ == "__main__":
    main()
