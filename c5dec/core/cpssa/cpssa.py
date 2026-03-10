"""
C5-DEC CAD — Cyber-Physical System Security Assessment (CPSSA) module.

Builds on and provides support for OWASP pytm, threagile and pyfair

1. create_threat_model(project_path, output_path, format, arc_folder, specs_path) → str
   Reads Doorstop architecture (ARC/HARC/LARC) artifacts from a C5-DEC
   project and produces a Threagile-compatible YAML threat-model template,
   a pytm Python script, or a pytm JSON file.  For pytm formats only ARC
   items are processed; an optional *specs_path* lets the caller supply the
   Doorstop specs root directly (bypassing auto-discovery).

2. generate_cpssa_report(threat_model_path, output_path) → str
   Consumes a Threagile-style threat model YAML and generates a structured
   CPSSA Markdown report suitable for Quarto / DocEngine publishing.

3. generate_dfd(project_path, output_path, arc_folder) → str
   Derives a PlantUML Data Flow Diagram from Doorstop architecture items
   (ARC/HARC/LARC) and, when pyTM (pytm) is installed.

4. run_quantitative_risk_analysis(threat_model_path, output_path) → str
   Runs a FAIR-based Monte Carlo simulation (via pyfair) for each abuse
   case and produces an Annualised Loss Expectancy (ALE) summary.

"""

import json
import os
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import pyfair
import yaml

from c5dec import common
import c5dec.settings as c5settings

logger = common.logger(__name__)

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

_DFD_ELEMENT_COLORS = {
    "process": "#AED6F1",
    "external": "#A9DFBF",
    "datastore": "#FAD7A0",
    "boundary": "#E8DAEF",
}

# Supported output formats for create_threat_model
_THREAT_MODEL_FORMATS = ("threagile", "pytm-python", "pytm-json")

# Path to the external Threagile schema-to-ARC mapping file.
_THREAGILE_MAPPINGS_FILE = Path(__file__).parent / "threagile-mappings.yml"

# Cached mappings (loaded lazily from threagile-mappings.yml).
_THREAGILE_MAPPINGS: Optional[Dict[str, Dict[str, str]]] = None


def _load_threagile_mappings() -> Dict[str, Dict[str, str]]:
    """Load and cache the Threagile schema mapping tables.

    Returns the full mapping dict read from ``threagile-mappings.yml``.
    Each top-level key is a mapping section (e.g. ``protocol``,
    ``authentication``) and each value is a ``{arc_value: threagile_value}``
    dict.
    """
    global _THREAGILE_MAPPINGS  # noqa: PLW0603
    if _THREAGILE_MAPPINGS is not None:
        return _THREAGILE_MAPPINGS

    if not _THREAGILE_MAPPINGS_FILE.is_file():
        logger.warning(
            "Threagile mappings file not found: %s — using empty mappings",
            _THREAGILE_MAPPINGS_FILE,
        )
        _THREAGILE_MAPPINGS = {}
        return _THREAGILE_MAPPINGS

    try:
        with open(_THREAGILE_MAPPINGS_FILE, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
        # Normalise keys to lowercase strings.
        _THREAGILE_MAPPINGS = {}
        for section, mapping in raw.items():
            if isinstance(mapping, dict):
                _THREAGILE_MAPPINGS[str(section)] = {
                    str(k).lower().strip(): str(v)
                    for k, v in mapping.items()
                }
        logger.debug(
            "Loaded Threagile mappings from %s (%d sections)",
            _THREAGILE_MAPPINGS_FILE, len(_THREAGILE_MAPPINGS),
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not read %s: %s", _THREAGILE_MAPPINGS_FILE, exc)
        _THREAGILE_MAPPINGS = {}

    return _THREAGILE_MAPPINGS


def _map_threagile(section: str, value: str, default: str) -> str:
    """Look up *value* in a Threagile mapping *section*.

    Returns *default* when the section or value is not found.
    """
    mappings = _load_threagile_mappings()
    section_map = mappings.get(section, {})
    return section_map.get(value.lower().strip(), default)


# Convenience accessors for the most commonly used mapping sections.
def _map_protocol(raw: str) -> str:
    return _map_threagile("protocol", raw, "unknown-protocol")


def _map_authentication(raw: str) -> str:
    return _map_threagile("authentication", raw, "none")


def _map_authorization(raw: str) -> str:
    return _map_threagile("authorization", raw, "none")


def _map_technology(raw_type: str) -> str:
    return _map_threagile("technology", raw_type, "unknown-technology")


def _map_asset_type(raw_type: str) -> str:
    return _map_threagile("asset_type", raw_type, "process")


def _map_encryption(raw: str) -> str:
    return _map_threagile("encryption", raw, "none")


def _map_machine(raw: str) -> str:
    return _map_threagile("machine", raw, "physical")


def _map_size(raw: str) -> str:
    return _map_threagile("size", raw, "component")


def _map_confidentiality(raw: str) -> str:
    return _map_threagile("confidentiality", raw, "internal")


def _map_integrity(raw: str) -> str:
    return _map_threagile("integrity", raw, "operational")


def _map_availability(raw: str) -> str:
    return _map_threagile("availability", raw, "operational")


def _map_trust_boundary_type(raw: str) -> str:
    return _map_threagile("trust_boundary_type", raw, "network-on-prem")


def _map_data_format(raw: str) -> str:
    return _map_threagile("data_format", raw, "file")


def _sanitise_name(raw: str, max_len: int = 60) -> str:
    """Collapse multi-line text into a single-line label and truncate.

    Strips leading Markdown heading markers (``#``), folds all whitespace
    (including newlines) into single spaces, and limits the result to
    *max_len* characters.  The returned string is safe for embedding in
    generated Python source or PlantUML diagrams.
    """
    text = raw.strip()
    # Remove leading Markdown heading markers
    while text.startswith("#"):
        text = text.lstrip("#").strip()
    # Fold all runs of whitespace (newlines, tabs, spaces) into one space
    text = " ".join(text.split())
    if len(text) > max_len:
        text = text[:max_len]
    return text


def _escape_py_str(value: str) -> str:
    """Escape *value* so it can be placed inside a Python double-quoted string.

    Handles the five characters that would otherwise break or alter a
    ``"..."`` literal: backslash, double-quote, newline, carriage-return,
    and tab.
    """
    out = []  # type: List[str]
    for ch in value:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return "".join(out)


# Mapping from Doorstop ARC/SWD ``type`` field to pytm element class name.
_TYPE_TO_PYTM_CLASS: Dict[str, str] = {
    # → pytm.Server
    "server": "Server",
    "web-server": "Server",
    "app-server": "Server",
    "scada-server": "Server",
    # → pytm.Process
    "process": "Process",
    "service": "Process",
    "api": "Process",
    "lambda": "Lambda",
    "plc": "Process",
    "hmi": "Process",
    "workstation": "Process",
    "jump-server": "Process",
    "module": "Process",
    "library": "Process",
    "cli": "Process",
    # → pytm.Datastore
    "datastore": "Datastore",
    "database": "Datastore",
    "historian": "Datastore",
    "repo": "Datastore",
    # → pytm.Actor
    "actor": "Actor",
    "user": "Actor",
    "operator": "Actor",
    "external": "Actor",
    # → pytm.ExternalEntity
    "firewall": "ExternalEntity",
    "gateway": "ExternalEntity",
    "rtu": "ExternalEntity",
    "switch": "ExternalEntity",
    "router": "ExternalEntity",
}

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _read_doorstop_items(doc_path: Path) -> List[Dict[str, Any]]:
    """Read all active Doorstop items from a document directory.

    Supports both the Markdown-with-YAML-frontmatter format
    (``itemformat: markdown``, files named ``*.md``) and the legacy
    plain-YAML format (``*.yml``).  The ``.doorstop.yml`` config file
    itself is always skipped.
    """
    items: List[Dict[str, Any]] = []
    if not doc_path.is_dir():
        return items

    # Collect candidate files: .md first (markdown itemformat), then .yml
    candidate_files = sorted(doc_path.glob("*.md")) + sorted(doc_path.glob("*.yml"))

    # Known sidecar filenames that live alongside Doorstop items but are not
    # items themselves.  Skip them unconditionally.
    _SIDECAR_FILENAMES = {
        "threat-actors.yml",
        "assumptions.yml",
    }

    for item_file in candidate_files:
        # Skip hidden files and the Doorstop config file
        if item_file.name.startswith("."):
            continue
        if item_file.suffix == ".yml" and "doorstop" in item_file.name.lower():
            continue
        if item_file.name.lower() in _SIDECAR_FILENAMES:
            continue

        try:
            with open(item_file, "r", encoding="utf-8") as fh:
                raw = fh.read()

            if item_file.suffix == ".md":
                # Parse YAML frontmatter delimited by --- ... ---
                data: Dict[str, Any] = {}
                body = raw
                if raw.startswith("---"):
                    parts = raw.split("---", 2)
                    if len(parts) >= 3:
                        fm = yaml.safe_load(parts[1])
                        if isinstance(fm, dict):
                            data = fm
                        body = parts[2].strip()
                # Store Markdown body as the item text
                if "text" not in data:
                    data["text"] = body
            else:
                loaded = yaml.safe_load(raw)
                data = loaded if isinstance(loaded, dict) else {}

            if data.get("active", True) is False:
                continue
            data["_uid"] = item_file.stem.upper()
            items.append(data)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not read %s: %s", item_file, exc)

    return items


def _doorstop_text(item: Dict[str, Any]) -> str:
    """Return the plain text from a Doorstop item (handles block scalars)."""
    text = item.get("text", "") or ""
    return str(text).strip()


# Default architecture document folder names (tried in order during auto-discovery)
_ARC_FOLDER_NAMES = ("arc", "harc", "larc")


def _find_arc_dir(
    specs_root: Optional[Path],
    arc_folder: Optional[str] = None,
) -> Optional[Path]:
    """Locate the architecture items directory.

    When *arc_folder* is given (a full filesystem path supplied by the user)
    the function returns that path directly.  A ``*doorstop.yml`` file is not
    required, but if one is found in the directory a DEBUG note is logged.

    When *arc_folder* is ``None`` the function searches *specs_root* for a
    subdirectory whose name matches one of :data:`_ARC_FOLDER_NAMES` **and**
    which contains a ``.doorstop.yml`` file (the authoritative Doorstop
    document marker).  Returns ``None`` when no matching directory is found.
    """
    if arc_folder is not None:
        candidate = Path(arc_folder).resolve()
        if not candidate.is_dir():
            logger.warning("Specified arc_folder does not exist: %s", candidate)
            return None
        # Fuzzy check: log if a *doorstop.yml file is present (not required)
        doorstop_files = list(candidate.glob("*doorstop.yml"))
        if doorstop_files:
            logger.debug(
                "Doorstop config found in user-supplied arc_folder: %s",
                doorstop_files[0],
            )
        return candidate

    if not specs_root:
        return None

    for d in sorted(specs_root.iterdir()):
        if not d.is_dir():
            continue
        if d.name.lower() not in _ARC_FOLDER_NAMES:
            continue
        if (d / ".doorstop.yml").exists():
            return d

    return None


def _find_specs_root(project_path: Path) -> Optional[Path]:
    """Locate the Doorstop specs root within a project.

    Checks the standard candidate paths in order and returns the first
    directory that either contains a ``.doorstop.yml`` file itself or has
    at least one immediate subdirectory that does.  The presence of
    ``.doorstop.yml`` is the authoritative Doorstop document marker.
    """
    for candidate in [
        project_path / "docs" / "specs",
        project_path / "specs",
        project_path,
    ]:
        if not candidate.is_dir():
            continue
        # Candidate is itself a Doorstop document root
        if (candidate / ".doorstop.yml").exists():
            return candidate
        # Candidate is a specs root whose children are Doorstop documents
        if any(
            d.is_dir() and (d / ".doorstop.yml").exists()
            for d in candidate.iterdir()
            if d.is_dir()
        ):
            return candidate
    return None


# NOTE: _collect_doorstop_items was removed — SRS item collection is no
# longer supported.  Use :func:`_collect_arc_items` to collect architecture
# items only.


def _pytm_class_for_item(item: Dict[str, Any]) -> str:
    """Return the pytm element class name for a Doorstop ARC/SWD item.

    Uses the ``type`` field first, then falls back to keyword heuristics on
    the item text.
    """
    raw_type = (item.get("type") or "").lower().strip()
    if raw_type in _TYPE_TO_PYTM_CLASS:
        return _TYPE_TO_PYTM_CLASS[raw_type]

    # Keyword heuristics on text
    text = _doorstop_text(item).lower()
    if any(kw in text for kw in ("database", "storage", "repository", "store", "historian")):
        return "Datastore"
    if any(kw in text for kw in ("user", "operator", "external actor", "third-party")):
        return "Actor"
    if any(kw in text for kw in ("server", "web server", "application server")):
        return "Server"
    if any(kw in text for kw in ("firewall", "gateway", "router", "switch")):
        return "ExternalEntity"
    return "Process"


def _dfd_kind_for_item(item: Dict[str, Any]) -> str:
    """Return a DFD element kind (``process``, ``external``, ``datastore``)
    for a Doorstop ARC/SWD item, using the ``type`` field and keyword
    heuristics.
    """
    pytm_cls = _pytm_class_for_item(item)
    if pytm_cls in ("Actor",):
        return "external"
    if pytm_cls in ("Datastore",):
        return "datastore"
    if pytm_cls in ("ExternalEntity",):
        return "external"
    return "process"


def _collect_links(item: Dict[str, Any]) -> List[str]:
    """Extract normalised Doorstop link UIDs from an item.

    Note: this function reads the Doorstop ``links`` field which is reserved
    for upward traceability (child → parent document).  Use
    :func:`_collect_flows` to derive data-flow edges between ARC items.
    """
    uids: List[str] = []
    for link in item.get("links", []) or []:
        if isinstance(link, dict):
            uid = (link.get("uid") or str(link)).upper()
        else:
            uid = str(link).upper()
        uids.append(uid)
    return uids


# Architecture-document UID prefixes used by the _collect_flows fallback.
_ARC_UID_PREFIXES = ("ARC-", "HARC-", "LARC-")


def _collect_flows(item: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return outgoing data-flow descriptors for a Doorstop ARC item.

    Reads the ``flows`` field (list of dicts) when present.  Each entry must
    have at least a ``target`` key (the destination UID); all other keys are
    optional and fall back to sensible defaults:

    .. code-block:: yaml

        flows:
          - target: ARC-006
            protocol: OPC-UA
            port: 4840
            encrypted: false
            authentication: none

    When ``flows`` is absent the function falls back to the legacy behaviour:
    it reads every entry in the Doorstop ``links`` field whose UID starts with
    an architecture-document prefix (``ARC-``, ``HARC-``, ``LARC-``) and
    constructs a minimal flow dict using the item-level ``protocol`` and
    ``port`` fields.  This backward-compatibility path means items that have
    not yet been migrated to the ``flows`` field continue to produce data-flow
    edges automatically.

    Parameters
    ----------
    item : dict
        A Doorstop item dict as returned by :func:`_read_doorstop_items`.

    Returns
    -------
    list of dict
        Each dict has the keys
        ``target`` (str, uppercased UID),
        ``protocol`` (str),
        ``port`` (int, -1 when absent),
        ``encrypted`` (bool),
        ``authentication`` (str).
    """
    # --- Primary: use the dedicated `flows` field ---
    raw_flows = item.get("flows")
    if raw_flows:
        result: List[Dict[str, Any]] = []
        for f in raw_flows:
            if not isinstance(f, dict):
                # Plain string shorthand: treat as target UID only
                f = {"target": str(f)}
            target = str(f.get("target") or "").upper().strip()
            if not target:
                continue
            result.append({
                "target": target,
                "protocol": str(f.get("protocol") or "").strip(),
                "port": int(f.get("port") or -1),
                "encrypted": bool(f.get("encrypted", False)),
                "authentication": str(f.get("authentication") or "none").strip(),
                "authorization": str(f.get("authorization") or "none").strip(),
                "vpn": bool(f.get("vpn", False)),
                "readonly": bool(f.get("readonly", False)),
                "data_assets_sent": f.get("data_assets_sent") or [],
                "data_assets_received": f.get("data_assets_received") or [],
            })
        return result

    # --- Fallback: derive from `links` filtering to ARC-prefixed UIDs only ---
    result = []
    item_proto = str(item.get("protocol") or "").strip()
    item_port = int(item.get("port") or -1)
    item_encrypted = bool(item.get("is_encrypted", False))
    for link in item.get("links", []) or []:
        if isinstance(link, dict):
            uid = (link.get("uid") or str(link)).upper()
        else:
            uid = str(link).upper()
        if any(uid.startswith(pfx) for pfx in _ARC_UID_PREFIXES):
            result.append({
                "target": uid,
                "protocol": item_proto,
                "port": item_port,
                "encrypted": item_encrypted,
                "authentication": "none",
                "authorization": "none",
            })
    return result


def _read_threat_actors(arc_dir: Path) -> List[Dict[str, Any]]:
    """Read threat actors from ``threat-actors.yml`` in the ARC directory.

    Returns an empty list when the file does not exist, allowing graceful
    degradation when the sidecar has not yet been created.
    """
    path = arc_dir / "threat-actors.yml"
    if not path.is_file():
        logger.debug("No threat-actors.yml found in %s", arc_dir)
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        actors = data.get("threat_actors", [])
        if not isinstance(actors, list):
            logger.warning(
                "threat-actors.yml: expected 'threat_actors' list, got %s",
                type(actors),
            )
            return []
        logger.debug("Loaded %d threat actor(s) from %s", len(actors), path)
        return actors
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not read %s: %s", path, exc)
        return []


def _read_assumptions(arc_dir: Path) -> List[Dict[str, Any]]:
    """Read documented assumptions from ``assumptions.yml`` in the ARC directory.

    Returns an empty list when the file does not exist.
    """
    path = arc_dir / "assumptions.yml"
    if not path.is_file():
        logger.debug("No assumptions.yml found in %s", arc_dir)
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        assumptions = data.get("assumptions", [])
        if not isinstance(assumptions, list):
            logger.warning(
                "assumptions.yml: expected 'assumptions' list, got %s",
                type(assumptions),
            )
            return []
        logger.debug("Loaded %d assumption(s) from %s", len(assumptions), path)
        return assumptions
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not read %s: %s", path, exc)
        return []


def _build_pytm_model_dict(
    project_name: str,
    arc_items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Build a dictionary representation of a pytm threat model.

    This intermediate dict is used both for generating a Python script and
    for serialising to JSON.  Only architecture (ARC/HARC/LARC) items are
    used as elements; SRS and SWD items are not processed.
    """
    elements: List[Dict[str, Any]] = []
    element_ids: Dict[str, int] = {}  # uid -> index
    boundaries: Dict[str, Dict[str, Any]] = {}  # zone -> boundary dict

    # ---- elements from architecture items ----
    for item in arc_items:
        uid = item.get("_uid", "UNKNOWN")
        raw_header = item.get("header", "") or _doorstop_text(item)[:60] or uid
        header = _sanitise_name(raw_header)
        pytm_cls = _pytm_class_for_item(item)
        zone = (item.get("zone") or "").strip()
        elem: Dict[str, Any] = {
            "uid": uid,
            "name": header,
            "pytm_class": pytm_cls,
            "zone": zone,
            "description": _sanitise_name(_doorstop_text(item), max_len=300),
            "os": item.get("os") or item.get("os_version") or "",
            "port": item.get("port", -1),
            "protocol": item.get("protocol") or "",
            "vendor": item.get("vendor") or "",
            "model": item.get("model") or "",
            # Security controls inferred from item fields
            "is_encrypted": bool(item.get("is_encrypted", False)),
            "has_access_control": bool(item.get("has_access_control", False)),
            "authenticates_source": bool(item.get("authenticates_source", False)),
            "stores_pii": bool(item.get("stores_pii", False)),
            "is_sql": bool(item.get("is_sql", False)),
            "safety_rated": bool(item.get("safety_rated", False)),
            "source": "ARC",
        }
        element_ids[uid] = len(elements)
        elements.append(elem)

        if zone and zone not in boundaries:
            boundaries[zone] = {
                "name": f"{zone} Zone",
                "zone": zone,
                "elements": [],
            }
        if zone:
            boundaries[zone]["elements"].append(uid)

    # ---- dataflows from `flows` field between architecture items ----
    dataflows: List[Dict[str, Any]] = []
    all_element_uids = set(element_ids.keys())
    for item in arc_items:
        src_uid = item.get("_uid", "UNKNOWN")
        if src_uid not in all_element_uids:
            continue
        for flow in _collect_flows(item):
            dst_uid = flow["target"]
            if dst_uid in all_element_uids and dst_uid != src_uid:
                dataflows.append({
                    "source": src_uid,
                    "sink": dst_uid,
                    "name": f"{src_uid} -> {dst_uid}",
                    "protocol": flow["protocol"],
                    "port": flow["port"],
                    "encrypted": flow["encrypted"],
                    "authentication": flow["authentication"],
                })

    return {
        "name": f"C5-DEC CPSSA — {project_name}",
        "description": (
            f"Threat model auto-generated from Doorstop ARC artifacts. "
            f"{len(arc_items)} architecture item(s)."
        ),
        "date": str(date.today()),
        "elements": elements,
        "boundaries": list(boundaries.values()),
        "dataflows": dataflows,
        "abuse_cases": {
            "Unauthorized Data Access": (
                "An attacker gains unauthorized access to confidential data assets."
            ),
            "Denial of Service": (
                "An attacker floods the system to exhaust available resources."
            ),
        },
    }


def _render_pytm_python(model_dict: Dict[str, Any], output_path: Path) -> str:
    """Render a pytm threat model as an executable Python script."""
    lines: List[str] = [
        '#!/usr/bin/env python3',
        '"""',
        f'pytm threat model — {model_dict["name"]}',
        '',
        f'Auto-generated by C5-DEC CAD on {model_dict["date"]}.',
        '',
        'Usage:',
        '  python <this_file> --dfd | dot -Tpng -o dfd.png',
        '  python <this_file> --seq | java -Djava.awt.headless=true -jar plantuml.jar -p > seq.png',
        '  python <this_file> --list',
        '  python <this_file> --json output.json',
        '  python <this_file> --report docs/basic_template.md',
        '"""',
        '',
        'from pytm import (',
        '    TM, Actor, Boundary, Dataflow, Datastore, ExternalEntity,',
        '    Lambda, Process, Server,',
        ')',
        '',
        '',
        f'tm = TM("{_escape_py_str(model_dict["name"])}")',
        f'tm.description = """{_escape_py_str(model_dict["description"])}"""',
        f'tm.isOrdered = True',
        '',
        '# ' + '=' * 70,
        '# Trust boundaries (derived from Doorstop ARC zone fields)',
        '# ' + '=' * 70,
        '',
    ]

    # Boundaries
    boundary_var_names: Dict[str, str] = {}
    for bd in model_dict.get("boundaries", []):
        zone = bd["zone"]
        var = f'boundary_{zone.lower().replace("-", "_").replace(" ", "_")}'
        boundary_var_names[zone] = var
        lines.append(f'{var} = Boundary("{_escape_py_str(bd["name"])}")')
    lines.append('')

    # Elements
    lines += [
        '# ' + '=' * 70,
        '# Elements (derived from Doorstop ARC and SWD items)',
        '# ' + '=' * 70,
        '',
    ]
    elem_var_names: Dict[str, str] = {}
    for elem in model_dict.get("elements", []):
        uid = elem["uid"]
        var = uid.lower().replace("-", "_")
        elem_var_names[uid] = var
        cls = elem["pytm_class"]
        name = _escape_py_str(elem["name"])

        lines.append(f'{var} = {cls}("{name}")')
        if elem.get("description"):
            desc_escaped = _escape_py_str(
                _sanitise_name(elem["description"], max_len=200)
            )
            lines.append(f'{var}.description = "{desc_escaped}"')
        if elem.get("os"):
            lines.append(f'{var}.OS = "{_escape_py_str(str(elem["os"]))}"')
        if elem.get("port") and elem["port"] != -1:
            lines.append(f'{var}.port = {elem["port"]}')
        if elem.get("protocol"):
            lines.append(f'{var}.protocol = "{_escape_py_str(str(elem["protocol"]))}"')

        # Security controls
        if elem.get("is_encrypted"):
            lines.append(f'{var}.controls.isEncrypted = True')
        if elem.get("has_access_control"):
            lines.append(f'{var}.controls.hasAccessControl = True')
        if elem.get("authenticates_source"):
            lines.append(f'{var}.controls.authenticatesSource = True')

        # Datastore-specific
        if cls == "Datastore":
            if elem.get("stores_pii"):
                lines.append(f'{var}.storesPII = True')
            if elem.get("is_sql"):
                lines.append(f'{var}.isSQL = True')

        # Boundary assignment
        zone = elem.get("zone", "")
        if zone and zone in boundary_var_names:
            lines.append(f'{var}.inBoundary = {boundary_var_names[zone]}')

        lines.append('')

    # Dataflows
    lines += [
        '# ' + '=' * 70,
        '# Data flows (derived from Doorstop links between architecture items)',
        '# ' + '=' * 70,
        '',
    ]
    for i, df in enumerate(model_dict.get("dataflows", [])):
        src_var = elem_var_names.get(df["source"])
        sink_var = elem_var_names.get(df["sink"])
        if src_var and sink_var:
            flow_name = _escape_py_str(df["name"])
            flow_var = f'flow_{i}'
            lines.append(f'{flow_var} = Dataflow({src_var}, {sink_var}, "{flow_name}")')
            if df.get("protocol"):
                lines.append(f'{flow_var}.protocol = "{_escape_py_str(str(df["protocol"]))}"')
            if df.get("port") and df["port"] != -1:
                lines.append(f'{flow_var}.dstPort = {df["port"]}')
            lines.append('')

    # Footer
    lines += [
        '',
        '',
        'if __name__ == "__main__":',
        '    tm.process()',
        '',
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    return str(output_path.resolve())


def _render_pytm_json(model_dict: Dict[str, Any], output_path: Path) -> str:
    """Render the intermediate pytm model dictionary as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(model_dict, fh, indent=2, ensure_ascii=False)
    return str(output_path.resolve())


# ---------------------------------------------------------------------------
# pytm-only ARC item collector (no SRS)
# ---------------------------------------------------------------------------

def _collect_arc_items(
    specs_root: Optional[Path],
    arc_folder: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Collect only architecture (ARC/HARC/LARC) items.

    When *arc_folder* is provided it is used directly (no ``.doorstop.yml``
    required).  When *specs_root* is provided without *arc_folder* the
    function calls :func:`_find_arc_dir` for auto-discovery.  Returns an
    empty list when neither argument resolves to a valid directory.
    """
    arc_dir = _find_arc_dir(specs_root, arc_folder)
    if arc_dir is None:
        logger.warning(
            "No architecture document folder found (tried names: %s). "
            "Pass --arc-folder to specify the path explicitly.",
            ", ".join(_ARC_FOLDER_NAMES),
        )
        return []
    arc_items = _read_doorstop_items(arc_dir)
    logger.debug(
        "Collected %d ARC items from '%s' (arc_folder=%s)",
        len(arc_items), arc_dir, arc_folder or "<auto>",
    )
    return arc_items


# ---------------------------------------------------------------------------
# 1. Create Threat Model (CPSSA Step 1)
# ---------------------------------------------------------------------------

# Excel sheet names (used by Threagile) are limited to 31 characters.
_THREAGILE_ID_MAX_LEN = 31


def _safe_threagile_id(raw: str, max_len: int = _THREAGILE_ID_MAX_LEN) -> str:
    """Return a Threagile-safe ID: lowercase, hyphens only, max *max_len* chars.

    Threagile requires IDs that contain only letters, digits, and hyphens.
    Threagile also passes IDs as Excel sheet names, which are limited to
    31 characters — so we enforce that limit here.
    """
    safe = raw.lower().replace("_", "-").replace(" ", "-")
    safe = "".join(c for c in safe if c.isalnum() or c == "-")
    return safe[:max_len]


def create_threat_model(
    project_path: Path,
    output_path: Optional[Path] = None,
    format: str = "threagile",
    arc_folder: Optional[str] = None,
) -> str:
    """Generate a threat-model template from Doorstop architecture artifacts.

    Only ARC (architecture) items are processed for all output formats.

    Supported formats
    -----------------
    ``threagile`` (default)
        Threagile-compatible YAML.  Output file: ``threat-model.yml``.
    ``pytm-python``
        Executable Python script using the OWASP pytm library.
        Output file: ``threat-model-pytm.py``.
    ``pytm-json``
        JSON representation of the pytm model.
        Output file: ``threat-model-pytm.json``.

    Architecture folder discovery
    -----------------------------
    When *arc_folder* is ``None`` the function searches the Doorstop specs
    root for the first subdirectory named ``arc``, ``harc``, or ``larc``
    (case-insensitive) that also contains a ``.doorstop.yml`` file.
    When *arc_folder* is provided it must be a full filesystem path to the
    directory containing the architecture item files (``.yml`` or ``.md``);
    a ``.doorstop.yml`` file is not required in that case.

    Parameters
    ----------
    project_path : Path
        Root directory of a C5-DEC SSDLC project.
    output_path : Path, optional
        Destination file.  When omitted the default depends on *format*.
    format : str
        One of ``"threagile"``, ``"pytm-python"``, ``"pytm-json"``.
    arc_folder : str, optional
        Full path to the directory containing architecture item files.
        When omitted, auto-discovery is used (looks for ``arc``, ``harc``,
        or ``larc`` folder with ``.doorstop.yml``).

    Returns
    -------
    str
        Absolute path to the written threat-model file.

    Raises
    ------
    common.C5decError
        If the project path does not exist or *format* is invalid.
    """
    format = format.lower().strip()
    if format not in _THREAT_MODEL_FORMATS:
        raise common.C5decError(
            f"Unsupported threat model format '{format}'. "
            f"Choose one of: {', '.join(_THREAT_MODEL_FORMATS)}"
        )

    project_path = Path(project_path).resolve()
    if not project_path.is_dir():
        raise common.C5decError(f"Project path not found: {project_path}")

    # -------- Collect ARC items (all formats) --------
    specs_root = _find_specs_root(project_path)
    if specs_root is None and arc_folder is None:
        logger.warning(
            "No Doorstop specs root found under '%s'. "
            "Use --arc-folder to specify the path explicitly.",
            project_path,
        )
    arc_items = _collect_arc_items(specs_root, arc_folder)

    # -------- pytm formats --------
    if format in ("pytm-python", "pytm-json"):
        model_dict = _build_pytm_model_dict(
            project_path.name, arc_items,
        )
        if format == "pytm-python":
            output_path = (
                Path(output_path) if output_path
                else project_path / "threat-model-pytm.py"
            ).resolve()
            result = _render_pytm_python(model_dict, output_path)
        else:
            output_path = (
                Path(output_path) if output_path
                else project_path / "threat-model-pytm.json"
            ).resolve()
            result = _render_pytm_json(model_dict, output_path)

        logger.info(
            "pytm threat model written (%s): %s (%d elements, %d dataflows)",
            format, result, len(model_dict["elements"]),
            len(model_dict["dataflows"]),
        )
        return result

    # -------- Threagile YAML format (default) --------

    # Locate the ARC directory so we can read sidecar files
    # (threat-actors.yml, assumptions.yml) that live alongside the
    # architecture item files.
    arc_dir_for_sidecars = _find_arc_dir(specs_root, arc_folder)
    threat_actors: List[Dict[str, Any]] = (
        _read_threat_actors(arc_dir_for_sidecars) if arc_dir_for_sidecars else []
    )
    model_assumptions: List[Dict[str, Any]] = (
        _read_assumptions(arc_dir_for_sidecars) if arc_dir_for_sidecars else []
    )

    # Collect all unique data-asset names declared across architecture items.
    # Each unique name becomes one entry in the Threagile `data_assets` section.
    _raw_data_asset_names: List[str] = []
    for _item in arc_items[:40]:
        for _name in (_item.get("data_assets") or []):
            _raw_data_asset_names.append(str(_name).strip())
    _unique_data_assets = sorted(set(_raw_data_asset_names))
    data_assets_dict: Dict[str, Any] = {}
    for _name in _unique_data_assets:
        _da_id = _safe_threagile_id(_name)
        if _da_id:
            data_assets_dict[_da_id] = {
                "id": _da_id,
                "description": _name,
                "usage": "business",
                "tags": [],
                "origin": "internal",
                "owner": "TBD",
                "quantity": "many",
                "confidentiality": "confidential",
                "integrity": "critical",
                "availability": "operational",
                "justification_cia_rating": "TBD — classify according to business context",
            }
    # Always include a generic user-data asset as a baseline
    if "user-data" not in data_assets_dict:
        data_assets_dict["user-data"] = {
            "id": "user-data",
            "description": "User-supplied input data",
            "usage": "business",
            "tags": [],
            "origin": "user",
            "owner": "TBD",
            "quantity": "few",
            "confidentiality": "confidential",
            "integrity": "critical",
            "availability": "operational",
            "justification_cia_rating": "TBD",
        }

    output_path = (
        Path(output_path) if output_path else project_path / "threat-model.yml"
    ).resolve()

    # Build Threagile-compatible YAML skeleton
    # Map of asset_id -> technical asset dict (also tracks communication links per asset)
    technical_assets: Dict[str, Any] = {}
    asset_id_lookup: Dict[str, str] = {}  # UID -> asset_id (lowercase, hyphens only)
    for item in arc_items[:40]:
        uid = item.get("_uid", "UNKNOWN")
        header = item.get("header", "") or _doorstop_text(item)[:60] or uid
        # Threagile IDs: letters, numbers, hyphens only, max 31 chars (Excel sheet name limit)
        asset_id = _safe_threagile_id(uid)
        item_type = (item.get("type") or "").lower()
        zone = (item.get("zone") or "").strip()

        # Map Doorstop type to valid Threagile asset type via external mapping
        ta_type = _map_asset_type(item_type)

        # Infer Threagile technology from type via external mapping
        tech = _map_technology(item_type)

        # Map encryption — prefer explicit ``encryption`` field on the item;
        # fall back to boolean ``is_encrypted`` for backward compat.
        raw_enc = str(item.get("encryption") or "").strip()
        if raw_enc:
            encryption = _map_encryption(raw_enc)
        else:
            encryption = "transparent" if item.get("is_encrypted") else "none"

        # Map machine — prefer explicit ``machine`` field
        raw_machine = str(item.get("machine") or "").strip()
        if raw_machine:
            machine = _map_machine(raw_machine)
        else:
            machine = "physical" if item_type in ("plc", "rtu", "hmi", "workstation") else "virtual"

        # Map size — prefer explicit ``size`` field
        size = _map_size(str(item.get("size") or "").strip()) if item.get("size") else "component"

        # Map CIA ratings — prefer explicit fields from ARC item
        confidentiality = _map_confidentiality(
            str(item.get("confidentiality") or "").strip()
        ) if item.get("confidentiality") else "confidential"
        integrity = _map_integrity(
            str(item.get("integrity") or "").strip()
        ) if item.get("integrity") else "critical"
        availability = _map_availability(
            str(item.get("availability") or "").strip()
        ) if item.get("availability") else "critical"

        # Map data_formats_accepted from ARC item
        raw_formats = item.get("data_formats_accepted") or []
        data_formats = [
            _map_data_format(str(f).strip())
            for f in raw_formats
            if str(f).strip()
        ] or ["json"]

        asset_id_lookup[uid] = asset_id
        technical_assets[asset_id] = {
            "id": asset_id,
            "description": header,
            "type": ta_type,
            "usage": "business",
            "used_as_client_by_human": item_type in ("workstation", "hmi", "jump-server"),
            "out_of_scope": bool(item.get("out_of_scope", False)),
            "justification_out_of_scope": str(item.get("justification_out_of_scope") or ""),
            "size": size,
            "technology": tech,
            "tags": [uid] + ([zone] if zone else []),
            "internet": bool(item.get("internet", False)),
            "machine": machine,
            "encryption": encryption,
            "owner": item.get("vendor") or "TBD",
            "confidentiality": confidentiality,
            "integrity": integrity,
            "availability": availability,
            "justification_cia_rating": str(item.get("justification_cia_rating") or "TBD"),
            "multi_tenant": bool(item.get("multi_tenant", False)),
            "redundant": bool(item.get("redundancy") or item.get("redundant", False)),
            "custom_developed_parts": bool(item.get("custom_developed_parts", False)),
            "data_assets_processed": [
                _safe_threagile_id(str(n).strip())
                for n in (
                    item.get("data_assets")
                    or item.get("data_assets_processed")
                    or []
                )
                if _safe_threagile_id(str(n).strip())
            ],
            "data_assets_stored": [
                _safe_threagile_id(str(n).strip())
                for n in (item.get("data_assets_stored") or [])
                if _safe_threagile_id(str(n).strip())
            ],
            "data_formats_accepted": data_formats,
            "communication_links": {},
        }

    # Populate communication_links from data flows between assets.
    # Uses the `flows` field on each ARC item (with fallback to ARC-prefix links).
    flow_counter = 0
    for item in arc_items[:40]:
        src_uid = item.get("_uid", "")
        if src_uid not in asset_id_lookup:
            continue
        src_asset_id = asset_id_lookup[src_uid]
        for flow in _collect_flows(item):
            dst_uid = flow["target"]
            if dst_uid in asset_id_lookup and dst_uid != src_uid:
                dst_asset_id = asset_id_lookup[dst_uid]
                raw_proto = (flow["protocol"] or "https").strip()
                # When the flow is explicitly encrypted, prefer an -encrypted variant
                if flow["encrypted"] and not raw_proto.lower().endswith("-encrypted"):
                    enc_variant = raw_proto.lower() + "-encrypted"
                    if _map_protocol(enc_variant) != "unknown-protocol":
                        raw_proto = enc_variant
                threagile_proto = _map_protocol(raw_proto)
                threagile_auth = _map_authentication(flow["authentication"])
                threagile_authz = _map_authorization(
                    str(flow.get("authorization") or "none")
                )
                link_id = f"flow-{flow_counter}"
                technical_assets[src_asset_id]["communication_links"][link_id] = {
                    "target": dst_asset_id,
                    "description": f"Data flow from {src_uid} to {dst_uid}",
                    "protocol": threagile_proto,
                    "authentication": threagile_auth,
                    "authorization": threagile_authz,
                    "tags": [src_uid, dst_uid],
                    "vpn": bool(flow.get("vpn", False)),
                    "ip_filtered": bool(item.get("has_access_control", False)),
                    "readonly": bool(flow.get("readonly", False)),
                    "usage": "business",
                    "data_assets_sent": [
                        _safe_threagile_id(str(n).strip())
                        for n in (flow.get("data_assets_sent") or [])
                        if _safe_threagile_id(str(n).strip())
                    ],
                    "data_assets_received": [
                        _safe_threagile_id(str(n).strip())
                        for n in (flow.get("data_assets_received") or [])
                        if _safe_threagile_id(str(n).strip())
                    ],
                    "diagram_tweak_weight": 1,
                }
                flow_counter += 1

    threat_model: Dict[str, Any] = {
        "threagile_version": "1.0.0",
        "title": f"C5-DEC CPSSA — {project_path.name}"[:80],
        "date": str(date.today()),
        "author": {
            "name": "C5-DEC CAD (auto-generated)",
            "homepage": "https://github.com/AbstractionsLab/c5dec",
        },
        "management_summary_comment": (
            "Auto-generated threat model template. Review and complete all "
            "TBD fields before running Threagile risk analysis."
        ),
        "business_criticality": "important",
        "business_overview": {
            "description": (
                f"System: {project_path.name}. "
                f"Contains {len(arc_items)} architecture item(s)."
            ),
            "images": [],
        },
        "technical_overview": {
            "description": (
                "Architecture derived from Doorstop ARC/HARC/LARC documents. "
                "Review trust boundaries and data-flow paths."
            ),
            "images": [],
        },
        "questions": {q: "" for q in [
            "Within which network segments are the technical assets running?",
            "Which external entities interact with the system?",
            "What data classifications apply to stored and processed data?",
        ]},
        "abuse_cases": {
            "Unauthorized Data Access": (
                "An attacker gains unauthorized access to confidential data assets."
            ),
            "Denial of Service": (
                "An attacker floods the system to exhaust available resources."
            ),
        },
        # Threat actors sourced from threat-actors.yml in the ARC directory.
        # Add entries by creating/editing that sidecar file.
        "threat_actors": threat_actors,
        # Documented assumptions sourced from assumptions.yml in the ARC directory.
        "assumptions": model_assumptions,
        "security_requirements": {},
        "tags_available": [],  # populated after all assets and boundaries are built
        "data_assets": data_assets_dict,
        "trust_boundaries": {
            "internet-boundary": {
                "id": "internet-boundary",
                "description": "Internet perimeter trust boundary",
                "type": "network-on-prem",
                "tags": [],
                "technical_assets_inside": [],
                "trust_boundaries_nested": [],
            },
        },
        "shared_runtimes": {},
        "individual_risk_categories": {},
        "risk_tracking": {},
        "technical_assets": technical_assets,
    }

    # Add zone-based trust boundaries from architecture items
    zones_seen: Dict[str, List[str]] = {}
    for item in arc_items:
        zone = (item.get("zone") or "").strip()
        uid = item.get("_uid", "UNKNOWN")
        if zone and uid in asset_id_lookup:
            zones_seen.setdefault(zone, []).append(asset_id_lookup[uid])
    for zone, ids in zones_seen.items():
        # Sanitise zone name: Threagile ID rules + 31-char Excel sheet name limit
        bd_id = _safe_threagile_id(f"{zone}-zone")
        threat_model["trust_boundaries"][bd_id] = {
            "id": bd_id,
            "description": f"{zone} zone trust boundary",
            "type": _map_trust_boundary_type(zone.lower()),
            "tags": [zone],
            "technical_assets_inside": ids,
            "trust_boundaries_nested": [],
        }

    # Rebuild tags_available as the union of every tag value actually used
    # anywhere in the model (asset tags, communication-link tags, trust-boundary
    # tags).  Threagile validates that every referenced tag appears in this list.
    all_tags_used: set = set()
    for asset_data in technical_assets.values():
        for tag in (asset_data.get("tags") or []):
            all_tags_used.add(str(tag))
        for link_data in (asset_data.get("communication_links") or {}).values():
            for tag in (link_data.get("tags") or []):
                all_tags_used.add(str(tag))
    for bd_data in threat_model["trust_boundaries"].values():
        if isinstance(bd_data, dict):
            for tag in (bd_data.get("tags") or []):
                all_tags_used.add(str(tag))
    all_tags_used.discard("")
    threat_model["tags_available"] = sorted(all_tags_used)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        yaml.dump(
            threat_model,
            fh,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    logger.info(
        "Threat model written: %s (%d assets, %d communication links)",
        output_path, len(technical_assets), flow_counter,
    )
    return str(output_path)


# ---------------------------------------------------------------------------
# 2. Generate CPSSA Report (CPSSA Step 2)
# ---------------------------------------------------------------------------

_CPSSA_REPORT_SECTIONS = [
    "Executive Summary",
    "System Description",
    "Assets and Dependencies",
    "Threat Landscape",
    "Attack Scenarios",
    "Risk Assessment",
    "Recommended Controls",
    "Residual Risk",
    "Conclusion",
]

_STRIDE_CATEGORIES = {
    "Spoofing": "Authentication",
    "Tampering": "Integrity",
    "Repudiation": "Non-repudiation",
    "Information Disclosure": "Confidentiality",
    "Denial of Service": "Availability",
    "Elevation of Privilege": "Authorization",
}


def generate_cpssa_report(
    threat_model_path: Path,
    output_path: Optional[Path] = None,
) -> str:
    """Generate a structured CPSSA Markdown report from a threat model YAML.

    Parameters
    ----------
    threat_model_path : Path
        Path to a Threagile-compatible threat model YAML.
    output_path : Path, optional
        Destination Markdown file. Defaults to ``cpssa-report.md`` next to
        the threat model.

    Returns
    -------
    str
        Absolute path to the written Markdown report.

    Raises
    ------
    common.C5decError
        If the threat model file cannot be read.
    """
    threat_model_path = Path(threat_model_path).resolve()
    if not threat_model_path.is_file():
        raise common.C5decError(f"Threat model not found: {threat_model_path}")

    try:
        with open(threat_model_path, "r", encoding="utf-8") as fh:
            model: Dict[str, Any] = yaml.safe_load(fh) or {}
    except Exception as exc:
        raise common.C5decError(
            f"Cannot parse threat model '{threat_model_path}': {exc}"
        ) from exc

    output_path = (
        Path(output_path) if output_path
        else threat_model_path.parent / "cpssa-report.md"
    ).resolve()

    title = model.get("title", "CPSSA Report")
    report_date = model.get("date", str(date.today()))
    author = model.get("author", {})
    author_name = author.get("name", "Unknown") if isinstance(author, dict) else str(author)
    biz_summary = model.get("management_summary_comment", "")
    biz_overview = (model.get("business_overview") or {}).get("description", "")
    tech_overview = (model.get("technical_overview") or {}).get("description", "")
    assets: Dict[str, Any] = model.get("technical_assets") or {}
    data_assets: Dict[str, Any] = model.get("data_assets") or {}
    security_reqs: Dict[str, Any] = model.get("security_requirements") or {}
    abuse_cases: Dict[str, Any] = model.get("abuse_cases") or {}
    trust_boundaries: Dict[str, Any] = model.get("trust_boundaries") or {}
    report_threat_actors: List[Dict[str, Any]] = (
        model.get("threat_actors") or []
    )
    report_assumptions: List[Dict[str, Any]] = (
        model.get("assumptions") or []
    )

    lines: List[str] = [
        f"# {title}",
        "",
        f"**Date:** {report_date}  ",
        f"**Author:** {author_name}  ",
        f"**Classification:** CONFIDENTIAL  ",
        "",
        "---",
        "",
    ]

    # 1. Executive summary
    lines += [
        "## 1. Executive summary",
        "",
        biz_summary or "_[Auto-generated — complete this section.]_",
        "",
    ]

    # 2. System description
    lines += [
        "## 2. System description",
        "",
        "### Business overview",
        "",
        biz_overview or "_[Complete this section.]_",
        "",
        "### Technical overview",
        "",
        tech_overview or "_[Complete this section.]_",
        "",
    ]

    # 3. Assets and dependencies
    lines += ["## 3. Assets and dependencies", "", "### Technical assets", ""]
    if assets:
        lines += [
            "| ID | Description | Confidentiality | Integrity | Availability |",
            "|----|-------------|-----------------|-----------|--------------|",
        ]
        for aid, asset in assets.items():
            if not isinstance(asset, dict):
                continue
            lines.append(
                f"| `{aid}` | {asset.get('description', '')} "
                f"| {asset.get('confidentiality', '')} "
                f"| {asset.get('integrity', '')} "
                f"| {asset.get('availability', '')} |"
            )
        lines.append("")
    else:
        lines += ["_No technical assets defined in threat model._", ""]

    lines += ["### Data assets", ""]
    if data_assets:
        lines += [
            "| ID | Description | Confidentiality |",
            "|----|-------------|-----------------|",
        ]
        for did, da in data_assets.items():
            if not isinstance(da, dict):
                continue
            lines.append(f"| `{did}` | {da.get('description', '')} | {da.get('confidentiality', '')} |")
        lines.append("")

    lines += ["### Trust boundaries", ""]
    for bid, tb in trust_boundaries.items():
        if not isinstance(tb, dict):
            continue
        lines += [f"- **{bid}** ({tb.get('type', '')}): {tb.get('description', '')}", ""]

    # 4. Threat landscape
    lines += [
        "## 4. Threat landscape",
        "",
        "The following STRIDE threat categories were considered during the assessment:",
        "",
    ]
    for threat, property_ in _STRIDE_CATEGORIES.items():
        lines.append(f"- **{threat}** (targets *{property_}*)")
    lines.append("")

    # 4.1 Threat actors & personas
    lines += ["### 4.1 Threat actors and personas", ""]
    if report_threat_actors:
        lines += [
            "| ID | Name | Capability | Access | Motivation |",
            "|----|------|-----------|--------|-----------||",
        ]
        for actor in report_threat_actors:
            if not isinstance(actor, dict):
                continue
            lines.append(
                f"| `{actor.get('id', 'N/A')}` "
                f"| {actor.get('name', '')} "
                f"| {actor.get('capability', '')} "
                f"| {actor.get('access', '')} "
                f"| {actor.get('motivation', '')} |"
            )
        lines.append("")
        for actor in report_threat_actors:
            if not isinstance(actor, dict):
                continue
            desc = actor.get("description", "")
            if desc:
                lines += [f"**{actor.get('name', actor.get('id', 'Actor'))}**: {desc.strip()}", ""]
    else:
        lines += [
            "_No threat actors defined. Create `threat-actors.yml` in the ARC directory "
            "to populate this section._",
            "",
        ]

    # 4.2 Documented assumptions
    lines += ["### 4.2 Documented assumptions", ""]
    if report_assumptions:
        lines += [
            "| ID | Assumption | Verified |",
            "|----|-----------|---------||",
        ]
        for assumption in report_assumptions:
            if not isinstance(assumption, dict):
                continue
            verified = "✅" if assumption.get("verified") else "⚠️ TBD"
            text = str(assumption.get("text", "")).replace("\n", " ")
            lines.append(
                f"| `{assumption.get('id', 'N/A')}` | {text} | {verified} |"
            )
        lines.append("")
    else:
        lines += [
            "_No documented assumptions found. Create `assumptions.yml` in the ARC "
            "directory to populate this section._",
            "",
        ]

    # 5. Attack scenarios
    lines += ["## 5. Attack scenarios", ""]
    if abuse_cases:
        for scenario, description in abuse_cases.items():
            lines += [f"### {scenario}", "", description, ""]
    else:
        lines += ["_No abuse cases defined. Complete using STRIDE analysis._", ""]

    # 6. Risk assessment
    lines += [
        "## 6. Risk assessment",
        "",
        "| Scenario | Likelihood | Impact | Risk Level | Notes |",
        "|----------|------------|--------|------------|-------|",
    ]
    for scenario in (list(abuse_cases.keys()) if abuse_cases else ["Example scenario"]):
        lines.append(f"| {scenario} | TBD | TBD | TBD | |")
    lines.append("")

    # 7. Security requirements
    lines += ["## 7. Security requirements", ""]
    if security_reqs:
        for uid, req_text in list(security_reqs.items())[:20]:
            snippet = str(req_text)[:120].replace("\n", " ")
            lines.append(f"- **{uid}**: {snippet}")
        lines.append("")
    else:
        lines += ["_No security requirements extracted from Doorstop._", ""]

    # 8. Recommended controls
    lines += [
        "## 8. Recommended controls",
        "",
        "| Control ID | Description | Addresses | Priority |",
        "|------------|-------------|-----------|----------|",
        "| CTRL-001 | _[Complete]_ | _[STRIDE categories]_ | HIGH |",
        "",
    ]

    # 9. Residual risk
    lines += [
        "## 9. Residual risk",
        "",
        "_Document accepted residual risks and their business justification._",
        "",
    ]

    # 10. Conclusion
    lines += [
        "## 10. Conclusion",
        "",
        "_Summarise assessment findings and next steps._",
        "",
        "---",
        "",
        "_Report generated by C5-DEC CAD CPSSA module._",
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    logger.info("CPSSA report written: %s", output_path)
    return str(output_path)


# ---------------------------------------------------------------------------
# 3. Generate Data Flow Diagram (CPSSA Step 3)
# ---------------------------------------------------------------------------

_PLANTUML_ELEMENT_STYLES = {
    "process":   'component "{label}" as {id} #AED6F1',
    "external":  'actor "{label}" as {id} #A9DFBF',
    "datastore": 'database "{label}" as {id} #FAD7A0',
}


def generate_dfd(
    project_path: Path,
    output_path: Optional[Path] = None,
    arc_folder: Optional[str] = None,
) -> str:
    """Generate a PlantUML Data Flow Diagram from Doorstop architecture items.

    Element IDs, asset-type classification (``process`` / ``external`` /
    ``datastore``), trust-boundary IDs, data-flow labels, and the 40-item
    cap all match the Threagile output produced by
    :func:`create_threat_model` so that the two artefacts are
    cross-referenceable.  Specifically:

    * Element IDs are generated with :func:`_safe_threagile_id` (lowercase,
      hyphens, max 31 chars), identical to the Threagile ``technical_assets``
      keys.
    * Asset type follows Threagile's ``ta_type`` logic: ``datastore``,
      ``external-entity``, or ``process``; rendered in PlantUML as
      ``database``, ``actor``, or ``component`` respectively.
    * Trust-boundary rectangle IDs use
      ``_safe_threagile_id("<zone>-zone")``.
    * Flow arrows are labelled ``flow-N [protocol]`` matching Threagile
      ``communication_links`` keys and protocol values.
    * At most 40 architecture items are processed (same cap as
      ``create_threat_model``).

    Links between architecture items are rendered as directed data-flow
    arrows.  Zone-based trust boundaries from the items are rendered as
    PlantUML ``rectangle`` groupings.  SWD (software-design) items are not
    processed.

    Parameters
    ----------
    project_path : Path
        Root directory of a C5-DEC SSDLC project.
    output_path : Path, optional
        Destination ``.puml`` file.  Defaults to
        ``<project_path>/cpssa-dfd.puml``.
    arc_folder : str, optional
        Full path to the directory containing architecture item files.
        When omitted, auto-discovery is used.

    Returns
    -------
    str
        Absolute path to the written PlantUML file.

    Raises
    ------
    common.C5decError
        If the project path does not exist.
    """
    project_path = Path(project_path).resolve()
    if not project_path.is_dir():
        raise common.C5decError(f"Project path not found: {project_path}")

    output_path = (
        Path(output_path) if output_path else project_path / "cpssa-dfd.puml"
    ).resolve()

    specs_root = _find_specs_root(project_path)
    arc_items = _collect_arc_items(specs_root, arc_folder)
    # Cap at 40 items — same limit as create_threat_model (Threagile format)
    all_items = arc_items[:40]

    if not specs_root and not arc_folder:
        logger.warning("No Doorstop specs root found under '%s'.", project_path)

    # ---------- build element map ----------
    # IDs and type classification mirror create_threat_model's Threagile output
    # so that both artefacts are cross-referenceable.
    elements: Dict[str, Dict[str, str]] = {}
    for item in all_items:
        uid = item.get("_uid", "UNKNOWN")
        header = item.get("header", "") or _doorstop_text(item)[:60] or uid
        # Use the same Threagile-safe ID as create_threat_model
        eid = _safe_threagile_id(uid)
        label = header.replace('"', "'")
        # Threagile ta_type classification (matches create_threat_model exactly)
        item_type = (item.get("type") or "").lower()
        if item_type in ("datastore", "database", "historian", "repo"):
            kind = "datastore"
        elif item_type in (
            "actor", "user", "operator", "external",
            "firewall", "gateway", "router", "switch", "rtu",
        ):
            kind = "external"
        else:
            kind = "process"
        zone = (item.get("zone") or "").strip()
        elements[uid] = {"id": eid, "label": label, "kind": kind, "zone": zone}

    # ---------- collect data flows ----------
    # Flows carry the Threagile protocol and a sequential link_id (flow-N)
    # matching communication_links keys in create_threat_model's YAML output.
    # Tuple layout: (src_uid, dst_uid, proto, link_id, encrypted, authentication)
    flows: List[Tuple[str, str, str, str, bool, str]] = []
    flow_counter = 0
    for item in all_items:
        uid = item.get("_uid", "UNKNOWN")
        if uid not in elements:
            continue
        for flow in _collect_flows(item):
            dst_uid = flow["target"]
            if dst_uid in elements and dst_uid != uid:
                raw_proto = (flow["protocol"] or "https").strip()
                # Prefer encrypted variant when the flow is encrypted
                if flow["encrypted"] and not raw_proto.lower().endswith("-encrypted"):
                    enc_variant = raw_proto.lower() + "-encrypted"
                    if _map_protocol(enc_variant) != "unknown-protocol":
                        raw_proto = enc_variant
                threagile_proto = _map_protocol(raw_proto)
                link_id = f"flow-{flow_counter}"
                flows.append((
                    uid, dst_uid, threagile_proto, link_id,
                    flow["encrypted"], flow["authentication"],
                ))
                flow_counter += 1

    # ---------- group elements into zone boundaries ----------
    zones: Dict[str, List[str]] = {}
    no_zone: List[str] = []
    for uid, el in elements.items():
        zone = el.get("zone", "")
        if zone:
            zones.setdefault(zone, []).append(uid)
        else:
            no_zone.append(uid)

    # ---------- render PlantUML ----------
    puml_lines: List[str] = [
        "@startuml cpssa-dfd",
        "skinparam componentStyle rectangle",
        "skinparam defaultTextAlignment center",
        "skinparam ArrowColor #555555",
        "",
        "title Data Flow Diagram — " + project_path.name,
        "",
    ]

    def _render_element(uid: str) -> str:
        el = elements[uid]
        style = _PLANTUML_ELEMENT_STYLES.get(el["kind"], _PLANTUML_ELEMENT_STYLES["process"])
        return style.format(id=el["id"], label=el["label"])

    # Render zone-grouped elements inside rectangles
    # Rectangle IDs use _safe_threagile_id("<zone>-zone") to match
    # the trust_boundaries keys in create_threat_model's Threagile YAML.
    for zone, uids in sorted(zones.items()):
        zone_bd_id = _safe_threagile_id(f"{zone}-zone")
        puml_lines.append(f'rectangle "{zone} Zone" as {zone_bd_id} #E8DAEF {{')
        for uid in uids:
            puml_lines.append("  " + _render_element(uid))
        puml_lines.append("}")
        puml_lines.append("")

    # Render elements without a zone
    for uid in no_zone:
        puml_lines.append(_render_element(uid))

    if flows:
        puml_lines.append("")
        # Label each arrow with its Threagile link_id, normalised protocol,
        # encryption status, and authentication so the DFD matches Threagile's
        # communication_links annotations.
        for src_uid, dst_uid, proto, link_id, encrypted, authentication in flows:
            src_id = elements[src_uid]["id"]
            dst_id = elements[dst_uid]["id"]
            enc_label = "enc" if encrypted else "no-enc"
            auth_label = authentication if authentication and authentication != "none" else "no-auth"
            puml_lines.append(
                f'"{src_id}" --> "{dst_id}" : {link_id}\\n'
                f'[{proto} / {enc_label} / {auth_label}]'
            )

    puml_lines.append("")
    puml_lines.append("@enduml")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(puml_lines) + "\n")

    logger.info(
        "DFD written: %s (%d elements, %d flows, %d zones)",
        output_path, len(elements), len(flows), len(zones),
    )

    return str(output_path)

# ---------------------------------------------------------------------------
# 4. Quantitative Risk Analysis — FAIR / pyfair (CPSSA Step 5)
# ---------------------------------------------------------------------------

_DEFAULT_FAIR_LEF = {"low": 1, "mode": 5, "high": 20}
_DEFAULT_FAIR_LM = {"low": 10_000, "mode": 100_000, "high": 1_000_000}

# Advanced FAIR tree node defaults (used as placeholders in the template).
# Users uncomment and calibrate these to replace the simple LEF/LM inputs.
_DEFAULT_FAIR_TEF = {"low": 10, "mode": 50, "high": 200}
_DEFAULT_FAIR_CONTACT = {"low": 100, "mode": 500, "high": 2_000}
_DEFAULT_FAIR_ACTION = {"low": 0.05, "mode": 0.1, "high": 0.3}
_DEFAULT_FAIR_VULN = {"low": 0.1, "mode": 0.3, "high": 0.7}
_DEFAULT_FAIR_TC = {"low": 0.3, "mode": 0.5, "high": 0.8}
_DEFAULT_FAIR_CS = {"low": 0.2, "mode": 0.4, "high": 0.6}
_DEFAULT_FAIR_PL = {"low": 5_000, "mode": 50_000, "high": 500_000}
_DEFAULT_FAIR_SL = {"low": 5_000, "mode": 50_000, "high": 500_000}
_DEFAULT_FAIR_SLEF = {"low": 0.1, "mode": 0.3, "high": 0.7}
_DEFAULT_FAIR_SLEM = {"low": 10_000, "mode": 50_000, "high": 500_000}

# Mapping from short YAML key → pyfair ``input_data`` node name.
_FAIR_NODE_MAP: Dict[str, str] = {
    "lef": "Loss Event Frequency",
    "tef": "Threat Event Frequency",
    "contact": "Contact Frequency",
    "action": "Probability of Action",
    "vulnerability": "Vulnerability",
    "tc": "Threat Capability",
    "cs": "Control Strength",
    "lm": "Loss Magnitude",
    "pl": "Primary Loss",
    "sl": "Secondary Loss",
    "slef": "Secondary Loss Event Frequency",
    "slem": "Secondary Loss Event Magnitude",
}


# Type alias for FAIR PERT parameter dicts (values may be int or float).
_FairPert = Dict[str, Any]


def _fmt_pert(d: _FairPert) -> str:
    """Format a PERT dict ``{low, mode, high}`` as a compact YAML string."""
    return "{low: %s, mode: %s, high: %s}" % (d["low"], d["mode"], d["high"])


def generate_fair_input_template(
    threat_model_path: Path,
    output_path: Optional[Path] = None,
) -> str:
    """Generate a FAIR parameters YAML template from a threat model.

    Reads the abuse cases (and, for pytm JSON, synthesises element-based
    scenarios when none exist) and produces a YAML file with per-scenario
    FAIR calibration placeholders that the user can populate before
    running :func:`run_quantitative_risk_analysis`.

    The template exposes the **full FAIR model tree** so that users can
    choose the decomposition level that best matches their data:

    * **Simple** (default, active): ``lef`` + ``lm``.
    * **LEF decomposition**: replace ``lef`` with ``tef`` +
      ``vulnerability``, or go deeper with ``contact`` + ``action``
      (→ TEF) and/or ``tc`` + ``cs`` (→ Vulnerability).
    * **LM decomposition**: replace ``lm`` with ``pl`` + ``sl``, or
      go deeper with ``pl`` + ``slef`` + ``slem``.

    Advanced parameters are included as commented-out YAML lines; the
    user uncomments the level they want and removes the parent node.

    Parameters
    ----------
    threat_model_path : Path
        Path to a Threagile YAML or pytm JSON threat model.
    output_path : Path, optional
        Destination YAML file.  Defaults to
        ``<model_dir>/fair-params.yml``.

    Returns
    -------
    str
        Absolute path to the written FAIR parameters template.

    Raises
    ------
    common.C5decError
        If the threat model cannot be read or contains no abuse cases.
    """
    threat_model_path = Path(threat_model_path).resolve()
    if not threat_model_path.is_file():
        raise common.C5decError(f"Threat model not found: {threat_model_path}")

    is_json = threat_model_path.suffix.lower() == ".json"
    try:
        with open(threat_model_path, "r", encoding="utf-8") as fh:
            if is_json:
                model: Dict[str, Any] = json.load(fh)
            else:
                model = yaml.safe_load(fh) or {}
    except Exception as exc:
        raise common.C5decError(f"Cannot parse threat model: {exc}") from exc

    abuse_cases: Dict[str, Any] = model.get("abuse_cases") or {}

    # For pytm JSON models without explicit abuse_cases, synthesise scenarios
    if not abuse_cases and is_json:
        elements = model.get("elements") or []
        for elem in elements:
            name = elem.get("name") or elem.get("uid") or "Unknown Element"
            abuse_cases[f"Compromise of {name}"] = (
                f"An attacker compromises the {name} component, "
                f"leading to loss of confidentiality, integrity or availability."
            )

    if not abuse_cases:
        raise common.C5decError(
            "No abuse cases found in threat model — add entries under 'abuse_cases'."
        )

    output_path = (
        Path(output_path) if output_path
        else threat_model_path.parent / "fair-params.yml"
    ).resolve()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ---- Build the file manually so we can embed YAML comments ----
    # Header
    lines: List[str] = [
        "# FAIR calibration parameters for CPSSA quantitative risk analysis",
        "#",
        f"# Generated from: {threat_model_path.name}",
        f"# Date: {date.today()}",
        "#",
        "# FAIR model tree (pyfair):",
        "#",
        "#   Risk = LEF × LM",
        "#",
        "#   LEF (Loss Event Frequency)",
        "#     └─ TEF (Threat Event Frequency) × Vulnerability",
        "#          ├─ TEF = Contact Frequency × Probability of Action",
        "#          └─ Vulnerability = f(Threat Capability, Control Strength)",
        "#",
        "#   LM  (Loss Magnitude)",
        "#     └─ Primary Loss + Secondary Loss",
        "#          └─ Secondary Loss = SLEF × SLEM",
        "#",
        "# Instructions:",
        "#   1. Choose the decomposition level that matches the data you have.",
        "#      The simplest option (lef + lm) is active by default.",
        "#      To use a finer decomposition, uncomment the child nodes and",
        "#      remove (or comment out) the parent node.",
        "#   2. Calibrate the PERT distribution bounds (low / mode / high):",
        "#        - lef  : loss events per year",
        "#        - tef  : threat events per year (whether or not they cause loss)",
        "#        - contact : threat actor contacts per year (positive number)",
        "#        - action  : probability the actor acts on contact (0–1)",
        "#        - vulnerability : probability a threat event causes loss (0–1)",
        "#        - tc   : relative threat capability (0–1)",
        "#        - cs   : relative control strength (0–1)",
        "#        - lm   : monetary impact per loss event (€)",
        "#        - pl   : primary/direct monetary loss (€)",
        "#        - sl   : secondary/indirect monetary loss (€)",
        "#        - slef : probability of each secondary loss type (0–1)",
        "#        - slem : monetary amount per secondary loss type (€)",
        "#   3. Delete scenarios you want to use defaults for (or leave",
        "#      them as-is to use the placeholder values).",
        "#   4. Run the analysis:",
        f"#      c5dec cpssa risk-analysis --model {threat_model_path.name} "
        f"--fair-params {output_path.name}",
        "#",
        "",
    ]

    # ---- Helper to render a defaults/scenario block ----
    def _render_fair_block(indent: str) -> List[str]:
        """Return YAML lines for one FAIR parameter block.

        Active (simple): lef + lm.
        Commented-out: all advanced decomposition nodes.
        """
        blk: List[str] = [
            # -- LEF side (active) --
            f"{indent}lef: {_fmt_pert(_DEFAULT_FAIR_LEF)}",
            f"{indent}# --- Advanced LEF decomposition (uncomment to replace lef) ---",
            f"{indent}# tef: {_fmt_pert(_DEFAULT_FAIR_TEF)}",
            f"{indent}# vulnerability: {_fmt_pert(_DEFAULT_FAIR_VULN)}",
            f"{indent}# --- Further TEF decomposition (uncomment to replace tef) ---",
            f"{indent}# contact: {_fmt_pert(_DEFAULT_FAIR_CONTACT)}",
            f"{indent}# action: {_fmt_pert(_DEFAULT_FAIR_ACTION)}",
            f"{indent}# --- Further Vulnerability decomposition (uncomment to replace vulnerability) ---",
            f"{indent}# tc: {_fmt_pert(_DEFAULT_FAIR_TC)}",
            f"{indent}# cs: {_fmt_pert(_DEFAULT_FAIR_CS)}",
            # -- LM side (active) --
            f"{indent}lm: {_fmt_pert(_DEFAULT_FAIR_LM)}",
            f"{indent}# --- Advanced LM decomposition (uncomment to replace lm) ---",
            f"{indent}# pl: {_fmt_pert(_DEFAULT_FAIR_PL)}",
            f"{indent}# sl: {_fmt_pert(_DEFAULT_FAIR_SL)}",
            f"{indent}# --- Further SL decomposition (uncomment to replace sl) ---",
            f"{indent}# slef: {_fmt_pert(_DEFAULT_FAIR_SLEF)}",
            f"{indent}# slem: {_fmt_pert(_DEFAULT_FAIR_SLEM)}",
        ]
        return blk

    # ---- defaults section ----
    lines.append("defaults:")
    lines.extend(_render_fair_block("  "))
    lines.append("")

    # ---- scenarios section ----
    lines.append("scenarios:")
    for scenario_name, description in abuse_cases.items():
        desc_text = (
            str(description)[:200] if isinstance(description, str) else ""
        )
        # Quote the scenario name for YAML safety
        safe_name = scenario_name.replace('"', '\\"')
        lines.append(f'  "{safe_name}":')
        lines.append(f"    description: \"{desc_text}\"")
        lines.extend(_render_fair_block("    "))
    lines.append("")

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    logger.info(
        "FAIR input template written: %s (%d scenarios)",
        output_path, len(abuse_cases),
    )
    return str(output_path)


def _extract_fair_nodes(params: Dict[str, Any]) -> Dict[str, _FairPert]:
    """Extract recognised FAIR node dicts from a parameter block.

    Returns a dict whose keys are short node names (e.g. ``"lef"``,
    ``"tef"``, ``"tc"``) and values are ``{low, mode, high}`` dicts.
    Only keys present in *params* that are also valid FAIR node names
    (see :data:`_FAIR_NODE_MAP`) are included.
    """
    nodes: Dict[str, _FairPert] = {}
    for key in _FAIR_NODE_MAP:
        val = params.get(key)
        if isinstance(val, dict) and {"low", "mode", "high"} <= val.keys():
            nodes[key] = val
    return nodes


def _supply_fair_inputs(
    fm: Any,
    params: Dict[str, _FairPert],
    calibration_defaults: Dict[str, _FairPert],
) -> Dict[str, _FairPert]:
    """Supply ``input_data`` calls on a :class:`FairModel`.

    Chooses the finest decomposition level available in *params* for
    both the LEF and LM branches of the FAIR model tree.  Falls back to
    ``calibration_defaults`` for ``lef`` / ``lm`` when no data at all
    is provided for a branch.

    Returns
    -------
    dict
        The effective FAIR node parameters that were supplied (useful
        for reporting).
    """
    supplied: Dict[str, _FairPert] = {}

    def _input(key: str) -> None:
        """Call ``fm.input_data`` for *key* and record it."""
        d = params[key]
        fm.input_data(_FAIR_NODE_MAP[key], low=d["low"], mode=d["mode"], high=d["high"])
        supplied[key] = d

    # ---- LEF side ----
    lef_decomposed = False

    # TEF sub-tree: Contact × Action → TEF
    if "contact" in params and "action" in params:
        _input("contact")
        _input("action")
        lef_decomposed = True
    elif "tef" in params:
        _input("tef")
        lef_decomposed = True

    # Vulnerability sub-tree: TC vs CS → Vulnerability
    if "tc" in params and "cs" in params:
        _input("tc")
        _input("cs")
        lef_decomposed = True
    elif "vulnerability" in params:
        _input("vulnerability")
        lef_decomposed = True

    if not lef_decomposed:
        # Fall back to LEF directly
        if "lef" not in params:
            params["lef"] = calibration_defaults.get("lef", _DEFAULT_FAIR_LEF)
        _input("lef")

    # ---- LM side ----
    lm_decomposed = False

    if "pl" in params:
        _input("pl")
        lm_decomposed = True

    # Secondary loss: SLEF × SLEM → SL
    if "slef" in params and "slem" in params:
        _input("slef")
        _input("slem")
        lm_decomposed = True
    elif "sl" in params:
        _input("sl")
        lm_decomposed = True

    if not lm_decomposed:
        # Fall back to LM directly
        if "lm" not in params:
            params["lm"] = calibration_defaults.get("lm", _DEFAULT_FAIR_LM)
        _input("lm")

    return supplied


def run_quantitative_risk_analysis(
    threat_model_path: Path,
    output_path: Optional[Path] = None,
    simulations: int = 10_000,
    fair_params_path: Optional[Path] = None,
) -> str:
    """Run a FAIR-based quantitative risk analysis using pyfair.

    For each abuse case in the threat model a ``FairModel`` is created.
    The function supports the **full FAIR model tree**, so users can
    supply parameters at any decomposition level:

    * **LEF side** — ``lef`` directly, or ``tef`` + ``vulnerability``,
      or ``contact`` + ``action`` (→ TEF) and/or ``tc`` + ``cs``
      (→ Vulnerability).
    * **LM side** — ``lm`` directly, or ``pl`` + ``sl``, or ``pl`` +
      ``slef`` + ``slem``.

    Calibration parameters can be supplied in three ways (checked in
    order of precedence):

    1. **Dedicated FAIR parameters file** (*fair_params_path*) — a YAML
       file mapping scenario names to their PERT bounds.  Generate one
       with :func:`generate_fair_input_template`.
    2. **Inline in threat model** — each abuse case value can be a dict
       with any combination of FAIR node keys.
    3. **Fallback defaults** — conservative ``lef`` + ``lm`` placeholders
       when no calibration data is available.  A warning is emitted for
       each scenario that uses defaults.

    Both Threagile YAML and pytm JSON threat models are accepted.

    A Monte Carlo simulation is run, results are exported to CSV, and a
    Markdown summary table (mean ALE, 95th-percentile ALE, maximum) is
    written alongside.

    Parameters
    ----------
    threat_model_path : Path
        Path to a Threagile YAML or pytm JSON threat model.
    output_path : Path, optional
        Destination directory for output files.  Defaults to the parent
        directory of the threat model.
    simulations : int
        Number of Monte Carlo iterations (default: 10 000).
    fair_params_path : Path, optional
        Path to a YAML file with per-scenario FAIR calibration parameters.
        Generate a template with ``c5dec cpssa fair-input --model <model>``.

    Returns
    -------
    str
        Absolute path to the Markdown summary file.

    Raises
    ------
    common.C5decError
        If *pyfair* is not installed or the threat model cannot be read.
    """
    try:
        from pyfair import FairModel, FairMetaModel  # type: ignore
    except ImportError:
        raise common.C5decError(
            "pyfair is not installed. Run: poetry add pyfair"
        )

    threat_model_path = Path(threat_model_path).resolve()
    if not threat_model_path.is_file():
        raise common.C5decError(f"Threat model not found: {threat_model_path}")

    # Auto-detect format
    is_json = threat_model_path.suffix.lower() == ".json"
    try:
        with open(threat_model_path, "r", encoding="utf-8") as fh:
            if is_json:
                model: Dict[str, Any] = json.load(fh)
            else:
                model = yaml.safe_load(fh) or {}
    except Exception as exc:
        raise common.C5decError(f"Cannot parse threat model: {exc}") from exc

    # ---- Load FAIR calibration parameters ----
    # Each entry maps a scenario name → {node_key: {low, mode, high}}.
    fair_calibration: Dict[str, Dict[str, _FairPert]] = {}
    calibration_defaults: Dict[str, _FairPert] = {
        "lef": dict(_DEFAULT_FAIR_LEF),
        "lm": dict(_DEFAULT_FAIR_LM),
    }

    # Source 1: dedicated FAIR parameters file (highest precedence)
    if fair_params_path is not None:
        fair_params_path = Path(fair_params_path).resolve()
        if not fair_params_path.is_file():
            raise common.C5decError(
                f"FAIR parameters file not found: {fair_params_path}"
            )
        try:
            with open(fair_params_path, "r", encoding="utf-8") as fh:
                fair_params: Dict[str, Any] = yaml.safe_load(fh) or {}
        except Exception as exc:
            raise common.C5decError(
                f"Cannot parse FAIR parameters file: {exc}"
            ) from exc

        # Override defaults if provided
        if "defaults" in fair_params:
            defaults_block = fair_params["defaults"]
            # Accept any recognised FAIR node key as a default
            for key in _FAIR_NODE_MAP:
                if key in defaults_block and isinstance(defaults_block[key], dict):
                    calibration_defaults[key] = defaults_block[key]

        # Per-scenario overrides — extract all FAIR node keys
        for scenario_name, params in (fair_params.get("scenarios") or {}).items():
            nodes = _extract_fair_nodes(params)
            if nodes:
                fair_calibration[scenario_name] = nodes
        logger.info(
            "Loaded FAIR calibration from '%s': %d scenario-specific params, "
            "default keys: %s",
            fair_params_path, len(fair_calibration),
            list(calibration_defaults.keys()),
        )

    # Extract abuse cases — works for both Threagile and pytm JSON
    abuse_cases: Dict[str, Any] = model.get("abuse_cases") or {}

    # Source 2: inline FAIR parameters in abuse case values (dict form)
    for scenario_name, case_value in abuse_cases.items():
        if scenario_name in fair_calibration:
            continue  # dedicated file takes precedence
        if isinstance(case_value, dict):
            nodes = _extract_fair_nodes(case_value)
            if nodes:
                fair_calibration[scenario_name] = nodes

    # For pytm JSON models without explicit abuse_cases, synthesise one
    # scenario per element so the analysis still runs.
    if not abuse_cases and is_json:
        elements = model.get("elements") or []
        if elements:
            for elem in elements:
                name = elem.get("name") or elem.get("uid") or "Unknown Element"
                abuse_cases[f"Compromise of {name}"] = (
                    f"An attacker compromises the {name} component, "
                    f"leading to loss of confidentiality, integrity or availability."
                )
            logger.info(
                "No abuse_cases in pytm JSON; synthesised %d element-based scenarios.",
                len(abuse_cases),
            )

    if not abuse_cases:
        raise common.C5decError(
            "No abuse cases found in threat model — add entries under 'abuse_cases'."
        )

    out_dir = (
        Path(output_path) if output_path else threat_model_path.parent
    ).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build one FairModel per scenario
    # Each entry: (scenario_name, FairModel, supplied_nodes_dict)
    fair_models: List[Tuple[str, Any, Dict[str, _FairPert]]] = []
    scenarios_using_defaults: List[str] = []

    for scenario_name in abuse_cases:
        fm = FairModel(name=scenario_name, n_simulations=simulations)

        if scenario_name in fair_calibration:
            scenario_params = dict(fair_calibration[scenario_name])
        else:
            scenario_params = {}
            scenarios_using_defaults.append(scenario_name)

        supplied = _supply_fair_inputs(fm, scenario_params, calibration_defaults)
        fm.calculate_all()
        fair_models.append((scenario_name, fm, supplied))

    if scenarios_using_defaults:
        logger.warning(
            "%d scenario(s) use default FAIR parameters (results are illustrative "
            "only — calibrate via --fair-params or inline abuse_case dicts): %s",
            len(scenarios_using_defaults),
            ", ".join(scenarios_using_defaults),
        )

    meta = FairMetaModel(
        name="CPSSA Risk Analysis",
        models=[fm for _, fm, _ in fair_models],
    )
    meta.calculate_all()

    i = 1
    for _, fm, _ in fair_models:
        # Create report comparing individual model vs metamodel.
        fsr = pyfair.FairSimpleReport([fm, meta])
        html_file_name = str(out_dir / f"cpssa-risk-{i}.html")
        fsr.to_html(html_file_name)
        i += 1

    # Export raw results to CSV
    csv_path = out_dir / "cpssa-risk-results.csv"
    results_df = meta.export_results()
    results_df.to_csv(csv_path, index=False)

    # Build Markdown summary
    summary_path = out_dir / "cpssa-risk-summary.md"
    md_lines = [
        "# CPSSA quantitative risk summary",
        "",
        f"**Source model:** {threat_model_path.name}  ",
        f"**Date:** {date.today()}  ",
        f"**Simulations:** {simulations:,}  ",
        "",
    ]

    if scenarios_using_defaults:
        md_lines += [
            "> **Warning:** The following scenarios use default placeholder "
            "FAIR parameters and their results should be treated as illustrative "
            "only. Provide calibrated values via a FAIR parameters file "
            "(`--fair-params`) or inline in the threat model's `abuse_cases`.",
            ">",
            "> " + ", ".join(f"*{s}*" for s in scenarios_using_defaults),
            "",
        ]

    # ---- Input parameters table ----
    # Build dynamic columns based on which FAIR nodes were supplied.
    all_supplied_keys: List[str] = []
    for _, _, supplied in fair_models:
        for k in supplied:
            if k not in all_supplied_keys:
                all_supplied_keys.append(k)

    col_headers = [_FAIR_NODE_MAP.get(k, k).upper() for k in all_supplied_keys]
    md_lines += [
        "## Input parameters",
        "",
        "| Scenario | " + " | ".join(f"{h} (low/mode/high)" for h in col_headers) + " | Calibrated? |",
        "|----------" + "|--------------------" * len(col_headers) + "|-------------|",
    ]

    for scenario_name, _, supplied in fair_models:
        calibrated = "yes" if scenario_name not in scenarios_using_defaults else "no (defaults)"
        cells: List[str] = []
        for k in all_supplied_keys:
            if k in supplied:
                d = supplied[k]
                # Format large numbers with commas, small with plain
                vals = []
                for v_key in ("low", "mode", "high"):
                    v = d[v_key]
                    vals.append(f"{v:,}" if isinstance(v, int) and v >= 1_000 else str(v))
                cells.append("/".join(vals))
            else:
                cells.append("—")
        md_lines.append(
            f"| {scenario_name} | " + " | ".join(cells) + f" | {calibrated} |"
        )

    md_lines += [
        "",
        "## Annualised loss expectancy (ALE)",
        "",
        "| Scenario | Mean ALE | 95th Percentile | Max |",
        "|----------|----------|-----------------|-----|",
    ]

    for scenario_name, fm, _ in fair_models:
        try:
            individual_results = fm.export_results()
            risk_col = next(
                (c for c in individual_results.columns if "risk" in c.lower()), None
            )
            if risk_col:
                risk_data = individual_results[risk_col]
                md_lines.append(
                    f"| {scenario_name} "
                    f"| {risk_data.mean():,.0f} "
                    f"| {risk_data.quantile(0.95):,.0f} "
                    f"| {risk_data.max():,.0f} |"
                )
            else:
                md_lines.append(f"| {scenario_name} | N/A | N/A | N/A |")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not extract risk data for '%s': %s", scenario_name, exc)
            md_lines.append(f"| {scenario_name} | error | error | error |")

    md_lines += [
        "",
        f"Full results exported to: `{csv_path.name}`",
        "",
        "_Generated by C5-DEC CAD CPSSA module (pyfair)._",
    ]

    with open(summary_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md_lines) + "\n")

    logger.info(
        "Quantitative risk analysis written: %s (CSV: %s, %d scenarios, "
        "%d using defaults)",
        summary_path, csv_path, len(fair_models), len(scenarios_using_defaults),
    )
    return str(summary_path)