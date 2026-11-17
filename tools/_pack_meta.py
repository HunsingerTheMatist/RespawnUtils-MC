"""Shared helpers for reading pack.mcmeta and resolving the supported MC versions.
The MC-version lookup is offline, backed by pack_format_versions.json (refresh
that file via fetch_pack_format_versions.py, which is the only script in this
project that hits the network for version data).

pack_format_versions.json indexes DATA PACK formats only. Resource pack formats
are numbered independently and their values collide with data pack ones, so
only ever pass these functions a data pack directory.
"""
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VERSIONS_FILE = SCRIPT_DIR / "pack_format_versions.json"


def _parse_format(fmt) -> tuple[int, int]:
    """Turns an int or a `[major, minor]` list into `(major, minor)`, with minor
    defaulting to 0."""
    if isinstance(fmt, list):
        return int(fmt[0]), int(fmt[1]) if len(fmt) > 1 else 0
    return int(fmt), 0


def read_pack_format_range(root: Path) -> tuple[tuple[int, int], tuple[int, int]]:
    """Reads the lowest and highest pack formats pack.mcmeta declares, as
    `((major, minor), (major, minor))`. Each end comes from `pack.min_format` /
    `pack.max_format` when present (MC 1.21.9+), otherwise from the legacy
    `pack.supported_formats` range, otherwise from `pack.pack_format`."""
    pack_mcmeta = root / "pack.mcmeta"
    if not pack_mcmeta.is_file():
        sys.exit(f"pack.mcmeta not found at {pack_mcmeta}")
    pack = json.loads(pack_mcmeta.read_text(encoding="utf-8"))["pack"]

    # Legacy ranges are an int, a [min, max] list or {min_inclusive, max_inclusive}
    supported = pack.get("supported_formats")
    if isinstance(supported, dict):
        legacy = (supported["min_inclusive"], supported["max_inclusive"])
    elif isinstance(supported, list):
        legacy = (min(supported), max(supported))
    elif supported is not None:
        legacy = (supported, supported)
    else:
        legacy = (None, None)

    low = pack.get("min_format", legacy[0] if legacy[0] is not None else pack.get("pack_format"))
    high = pack.get("max_format", legacy[1] if legacy[1] is not None else pack.get("pack_format"))
    if low is None or high is None:
        sys.exit("pack.mcmeta declares no pack format (min_format/max_format, "
                 "supported_formats or pack_format).")
    return _parse_format(low), _parse_format(high)


def _lookup(versions: dict, fmt: tuple[int, int], end: str) -> str:
    """Returns the `end` ('first' or 'last') MC release id for a pack format.
    Same-major matching is fuzzy along the minor axis: prefer the lowest minor >=
    ours (forward), fall back to the highest minor < ours if no forward entry
    exists. Errors out if no entry with the same major exists."""
    major, minor = fmt
    same_major: dict[int, dict] = {}
    for key, value in versions.items():
        k_major, k_minor = (int(p) for p in key.split("."))
        if k_major == major:
            same_major[k_minor] = value

    if not same_major:
        sys.exit(f"No entry with pack format major {major} in {VERSIONS_FILE.name}. "
                 f"pack.mcmeta targets a pack format outside the offline index; "
                 f"run fetch_pack_format_versions.py to refresh.")

    forward = [m for m in same_major if m >= minor]
    entry = same_major[min(forward)] if forward else same_major[max(same_major)]
    if not isinstance(entry, dict):
        sys.exit(f"{VERSIONS_FILE.name} is in an old format; run "
                 f"fetch_pack_format_versions.py to refresh it.")
    return entry[end]


def resolve_supported_mc_versions(root: Path) -> tuple[str, str]:
    """Returns the earliest and latest MC release ids (e.g. '1.21.6', '1.21.8')
    covered by pack.mcmeta's pack format range. Lookup is offline against
    pack_format_versions.json; errors out if it is missing or stale, in which
    case run fetch_pack_format_versions.py to refresh."""
    low, high = read_pack_format_range(root)
    if not VERSIONS_FILE.is_file():
        sys.exit(f"{VERSIONS_FILE.name} not found at {VERSIONS_FILE}. "
                 f"Run fetch_pack_format_versions.py first.")
    versions = json.loads(VERSIONS_FILE.read_text(encoding="utf-8"))
    return _lookup(versions, low, "first"), _lookup(versions, high, "last")
