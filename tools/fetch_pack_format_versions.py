"""
Refreshes pack_format_versions.json by fetching the misode/mcmeta version index
and pre-resolving each (data_pack_version, data_pack_version_minor) pair seen in
stable releases to the first and last MC release ids using it.

Usage:
    py fetch_pack_format_versions.py

Output:
    pack_format_versions.json — dict
    { "<major>.<minor>": {"first": "<MC version>", "last": "<MC version>"} }.
    Read offline by _pack_meta.resolve_supported_mc_versions so the rest of the
    tooling never has to hit the network at run time. Run this script whenever
    the datapack's targeted pack format changes (or when a new MC release ships
    that you want the tooling to know about).
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

VERSIONS_INDEX_URL = (
    "https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/versions/data.min.json"
)

SCRIPT_DIR = Path(__file__).resolve().parent
OUT_FILE = SCRIPT_DIR / "pack_format_versions.json"


def main() -> None:
    print(f"Fetching version index from {VERSIONS_INDEX_URL} ...")
    try:
        with urllib.request.urlopen(VERSIONS_INDEX_URL, timeout=15) as resp:
            versions = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        sys.exit(f"Failed to fetch mcmeta version index: {e}")

    # Stable releases only, sorted newest-first.
    stable = [v for v in versions if v.get("stable")]
    stable.sort(key=lambda v: v.get("release_time", ""), reverse=True)

    # For each (major, minor) seen in stable releases, resolve "last" to the latest
    #  stable MC release with major matching AND minor <= ours, and "first" to the
    #  earliest stable MC release with exactly that format, so the offline lookup
    #  is a plain dict get
    seen = sorted({(v["data_pack_version"], v.get("data_pack_version_minor", 0)) for v in stable})
    out: dict[str, dict[str, str]] = {}
    for major, minor in seen:
        candidates = [v for v in stable
                      if v["data_pack_version"] == major
                      and v.get("data_pack_version_minor", 0) <= minor]
        exact = [v for v in candidates if v.get("data_pack_version_minor", 0) == minor]
        if not candidates or not exact:
            continue
        out[f"{major}.{minor}"] = {"first": exact[-1]["id"], "last": candidates[0]["id"]}

    # Add snapshots for the next-release cycle: any snapshot whose pack format
    #  exceeds the highest released pack format. One entry per unique (major,
    #  minor), spanning that pack format's earliest to most recent snapshot id.
    #  Snapshots whose pack format is already covered by a stable release are
    #  skipped (the stable entry takes precedence)
    if stable:
        max_stable = max((v["data_pack_version"], v.get("data_pack_version_minor", 0)) for v in stable)
    else:
        max_stable = (-1, -1)
    unreleased = [v for v in versions
                  if not v.get("stable")
                  and (v["data_pack_version"], v.get("data_pack_version_minor", 0)) > max_stable]
    unreleased.sort(key=lambda v: v.get("release_time", ""), reverse=True)
    for v in unreleased:
        key = f"{v['data_pack_version']}.{v.get('data_pack_version_minor', 0)}"
        if key not in out:
            out[key] = {"first": v["id"], "last": v["id"]}
        else:
            # Newest-first order, so each later match is an earlier snapshot
            out[key]["first"] = v["id"]

    # Sort entries by pack format ascending so the file reads predictably.
    out = dict(sorted(out.items(), key=lambda kv: tuple(int(p) for p in kv[0].split("."))))
    OUT_FILE.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_FILE.name} ({len(out)} entries)")


if __name__ == "__main__":
    main()
