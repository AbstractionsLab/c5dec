"""
Test module for CPSSA (Cyber-Physical System Security Assessment) functionality.

Tests helper utilities, threat model generation, DFD generation, CPSSA report
generation, FAIR input template generation, and quantitative risk analysis.
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from typing import List, Optional

import yaml

import c5dec.core.cpssa.cpssa as cpssa_mod
from c5dec.core.cpssa import (
    create_threat_model,
    generate_cpssa_report,
    generate_dfd,
    generate_fair_input_template,
    run_quantitative_risk_analysis,
)
from c5dec import common

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

def _write_arc_item(arc_dir: Path, uid: str, data: dict) -> None:
    """Write a Doorstop ARC item as a YAML file."""
    item_file = arc_dir / f"{uid}.yml"
    with open(item_file, "w", encoding="utf-8") as fh:
        yaml.dump(data, fh, default_flow_style=False, allow_unicode=True)


def _create_minimal_project(tmp_dir: Path, arc_items: Optional[List[dict]] = None) -> Path:
    """Create a minimal C5-DEC project with an ARC Doorstop document."""
    specs = tmp_dir / "docs" / "specs"
    arc_dir = specs / "arc"
    arc_dir.mkdir(parents=True)
    # Doorstop marker
    (arc_dir / ".doorstop.yml").write_text(
        "settings:\n  prefix: ARC\n  sep: '-'\n  digits: 3\n"
    )

    items = arc_items or [
        {
            "uid": "ARC-001",
            "active": True,
            "header": "SCADA Server",
            "type": "scada-server",
            "zone": "OT",
            "text": "Main SCADA server controlling industrial processes.",
            "protocol": "OPC-UA",
            "port": 4840,
            "is_encrypted": False,
            "has_access_control": True,
        },
        {
            "uid": "ARC-002",
            "active": True,
            "header": "Historian DB",
            "type": "historian",
            "zone": "OT",
            "text": "Time-series historian database for process data.",
            "protocol": "ODBC",
            "port": 1433,
            "is_encrypted": True,
            "flows": [
                {
                    "target": "ARC-001",
                    "protocol": "OPC-UA",
                    "port": 4840,
                    "encrypted": False,
                    "authentication": "none",
                }
            ],
        },
        {
            "uid": "ARC-003",
            "active": True,
            "header": "Engineering Workstation",
            "type": "workstation",
            "zone": "IT",
            "text": "Engineering workstation for configuration and monitoring.",
            "protocol": "SSH",
            "port": 22,
        },
    ]

    for item in items:
        uid = item.pop("uid")
        _write_arc_item(arc_dir, uid, item)

    return tmp_dir


# ---------------------------------------------------------------------------
# 1. Helper utility tests
# ---------------------------------------------------------------------------

class TestSanitiseName(unittest.TestCase):
    def test_strips_heading_markers(self):
        result = cpssa_mod._sanitise_name("## My Component")
        self.assertEqual(result, "My Component")

    def test_folds_whitespace(self):
        result = cpssa_mod._sanitise_name("  Hello\n  World  ")
        self.assertEqual(result, "Hello World")

    def test_truncates_at_max_len(self):
        long_str = "A" * 100
        result = cpssa_mod._sanitise_name(long_str, max_len=20)
        self.assertEqual(len(result), 20)

    def test_empty_string(self):
        result = cpssa_mod._sanitise_name("")
        self.assertEqual(result, "")

    def test_multiple_heading_markers(self):
        result = cpssa_mod._sanitise_name("### Section Title")
        self.assertEqual(result, "Section Title")


class TestEscapePyStr(unittest.TestCase):
    def test_escapes_double_quote(self):
        result = cpssa_mod._escape_py_str('say "hello"')
        self.assertEqual(result, 'say \\"hello\\"')

    def test_escapes_backslash(self):
        result = cpssa_mod._escape_py_str("C:\\path")
        self.assertEqual(result, "C:\\\\path")

    def test_escapes_newline(self):
        result = cpssa_mod._escape_py_str("line1\nline2")
        self.assertEqual(result, "line1\\nline2")

    def test_escapes_tab(self):
        result = cpssa_mod._escape_py_str("col1\tcol2")
        self.assertEqual(result, "col1\\tcol2")

    def test_plain_string_unchanged(self):
        result = cpssa_mod._escape_py_str("simple text")
        self.assertEqual(result, "simple text")


class TestSafeThreagileId(unittest.TestCase):
    def test_lowercases_input(self):
        result = cpssa_mod._safe_threagile_id("MY-COMPONENT")
        self.assertEqual(result, "my-component")

    def test_replaces_underscore_with_hyphen(self):
        result = cpssa_mod._safe_threagile_id("my_comp")
        self.assertEqual(result, "my-comp")

    def test_replaces_space_with_hyphen(self):
        result = cpssa_mod._safe_threagile_id("my comp")
        self.assertEqual(result, "my-comp")

    def test_strips_non_alnum_non_hyphen(self):
        result = cpssa_mod._safe_threagile_id("comp@2.0!")
        self.assertEqual(result, "comp20")

    def test_truncates_to_31_chars(self):
        long_str = "a" * 50
        result = cpssa_mod._safe_threagile_id(long_str)
        self.assertEqual(len(result), 31)

    def test_arc_uid_produces_stable_id(self):
        result = cpssa_mod._safe_threagile_id("ARC-001")
        self.assertEqual(result, "arc-001")


class TestDoorstopText(unittest.TestCase):
    def test_returns_text_field(self):
        item = {"text": "hello world"}
        self.assertEqual(cpssa_mod._doorstop_text(item), "hello world")

    def test_strips_whitespace(self):
        item = {"text": "  hello  "}
        self.assertEqual(cpssa_mod._doorstop_text(item), "hello")

    def test_missing_text_returns_empty(self):
        self.assertEqual(cpssa_mod._doorstop_text({}), "")

    def test_none_text_returns_empty(self):
        item = {"text": None}
        self.assertEqual(cpssa_mod._doorstop_text(item), "")


class TestPytmClassForItem(unittest.TestCase):
    def test_server_type(self):
        self.assertEqual(cpssa_mod._pytm_class_for_item({"type": "server"}), "Server")

    def test_database_type(self):
        self.assertEqual(cpssa_mod._pytm_class_for_item({"type": "database"}), "Datastore")

    def test_actor_type(self):
        self.assertEqual(cpssa_mod._pytm_class_for_item({"type": "actor"}), "Actor")

    def test_firewall_type(self):
        self.assertEqual(cpssa_mod._pytm_class_for_item({"type": "firewall"}), "ExternalEntity")

    def test_process_type(self):
        self.assertEqual(cpssa_mod._pytm_class_for_item({"type": "process"}), "Process")

    def test_unknown_type_with_storage_keyword_falls_back_to_datastore(self):
        item = {"type": "unknown", "text": "This is a repository for data storage"}
        self.assertEqual(cpssa_mod._pytm_class_for_item(item), "Datastore")

    def test_unknown_type_defaults_to_process(self):
        item = {"type": "xyz", "text": "A generic component"}
        self.assertEqual(cpssa_mod._pytm_class_for_item(item), "Process")

    def test_historian_type(self):
        self.assertEqual(cpssa_mod._pytm_class_for_item({"type": "historian"}), "Datastore")


class TestDfdKindForItem(unittest.TestCase):
    def test_actor_maps_to_external(self):
        self.assertEqual(cpssa_mod._dfd_kind_for_item({"type": "actor"}), "external")

    def test_datastore_maps_to_datastore(self):
        self.assertEqual(cpssa_mod._dfd_kind_for_item({"type": "datastore"}), "datastore")

    def test_firewall_maps_to_external(self):
        self.assertEqual(cpssa_mod._dfd_kind_for_item({"type": "firewall"}), "external")

    def test_server_maps_to_process(self):
        self.assertEqual(cpssa_mod._dfd_kind_for_item({"type": "server"}), "process")


class TestCollectLinks(unittest.TestCase):
    def test_string_links_uppercased(self):
        item = {"links": ["arc-001", "srs-002"]}
        links = cpssa_mod._collect_links(item)
        self.assertEqual(links, ["ARC-001", "SRS-002"])

    def test_dict_links_extracted(self):
        item = {"links": [{"uid": "arc-003"}]}
        links = cpssa_mod._collect_links(item)
        self.assertEqual(links, ["ARC-003"])

    def test_empty_links(self):
        self.assertEqual(cpssa_mod._collect_links({}), [])

    def test_none_links(self):
        self.assertEqual(cpssa_mod._collect_links({"links": None}), [])


class TestCollectFlows(unittest.TestCase):
    def test_flows_field_used_when_present(self):
        item = {
            "flows": [
                {"target": "arc-002", "protocol": "HTTPS", "port": 443, "encrypted": True, "authentication": "certificate"}
            ]
        }
        flows = cpssa_mod._collect_flows(item)
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0]["target"], "ARC-002")
        self.assertEqual(flows[0]["protocol"], "HTTPS")
        self.assertTrue(flows[0]["encrypted"])

    def test_flows_defaults_to_empty_when_no_flows_or_links(self):
        self.assertEqual(cpssa_mod._collect_flows({}), [])

    def test_links_fallback_for_arc_prefixed_uids(self):
        item = {
            "links": [{"uid": "ARC-005"}, {"uid": "SRS-001"}],
            "protocol": "SSH",
            "port": 22,
        }
        flows = cpssa_mod._collect_flows(item)
        # Only ARC-prefixed links should be converted to flows.
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0]["target"], "ARC-005")
        self.assertEqual(flows[0]["protocol"], "SSH")

    def test_string_shorthand_in_flows(self):
        item = {"flows": ["ARC-003"]}
        flows = cpssa_mod._collect_flows(item)
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0]["target"], "ARC-003")

    def test_flow_with_missing_target_skipped(self):
        item = {"flows": [{"protocol": "HTTP"}]}
        flows = cpssa_mod._collect_flows(item)
        self.assertEqual(flows, [])


class TestFmtPert(unittest.TestCase):
    def test_integer_values(self):
        result = cpssa_mod._fmt_pert({"low": 1, "mode": 5, "high": 20})
        self.assertIn("low: 1", result)
        self.assertIn("mode: 5", result)
        self.assertIn("high: 20", result)

    def test_float_values(self):
        result = cpssa_mod._fmt_pert({"low": 0.1, "mode": 0.3, "high": 0.7})
        self.assertIn("0.1", result)


class TestExtractFairNodes(unittest.TestCase):
    def test_extracts_lef_and_lm(self):
        params = {
            "lef": {"low": 1, "mode": 5, "high": 20},
            "lm": {"low": 10000, "mode": 100000, "high": 1000000},
        }
        nodes = cpssa_mod._extract_fair_nodes(params)
        self.assertIn("lef", nodes)
        self.assertIn("lm", nodes)

    def test_ignores_incomplete_pert_dicts(self):
        params = {"lef": {"low": 1, "mode": 5}}  # missing "high"
        nodes = cpssa_mod._extract_fair_nodes(params)
        self.assertNotIn("lef", nodes)

    def test_ignores_unknown_keys(self):
        params = {"unknown_key": {"low": 1, "mode": 2, "high": 3}}
        nodes = cpssa_mod._extract_fair_nodes(params)
        self.assertEqual(nodes, {})


# ---------------------------------------------------------------------------
# 2. File-reading helpers
# ---------------------------------------------------------------------------

class TestReadDoorstopItems(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.arc_dir = Path(self.tmp) / "arc"
        self.arc_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_reads_yaml_items(self):
        item_data = {
            "active": True,
            "header": "Test Component",
            "type": "server",
            "text": "A test server.",
        }
        (self.arc_dir / "ARC-001.yml").write_text(
            yaml.dump(item_data, default_flow_style=False)
        )
        items = cpssa_mod._read_doorstop_items(self.arc_dir)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["_uid"], "ARC-001")
        self.assertEqual(items[0]["header"], "Test Component")

    def test_reads_markdown_items_with_frontmatter(self):
        md_content = (
            "---\n"
            "active: true\n"
            "header: Markdown Component\n"
            "type: process\n"
            "---\n"
            "This is the item text body.\n"
        )
        (self.arc_dir / "ARC-002.md").write_text(md_content)
        items = cpssa_mod._read_doorstop_items(self.arc_dir)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["header"], "Markdown Component")
        self.assertIn("This is the item text body.", items[0]["text"])

    def test_skips_inactive_items(self):
        item_data = {"active": False, "header": "Inactive", "type": "server"}
        (self.arc_dir / "ARC-001.yml").write_text(yaml.dump(item_data))
        items = cpssa_mod._read_doorstop_items(self.arc_dir)
        self.assertEqual(items, [])

    def test_skips_doorstop_config_file(self):
        (self.arc_dir / ".doorstop.yml").write_text(
            "settings:\n  prefix: ARC\n"
        )
        item_data = {"active": True, "header": "Real Item", "type": "server"}
        (self.arc_dir / "ARC-001.yml").write_text(yaml.dump(item_data))
        items = cpssa_mod._read_doorstop_items(self.arc_dir)
        self.assertEqual(len(items), 1)

    def test_skips_sidecar_files(self):
        (self.arc_dir / "threat-actors.yml").write_text(
            "threat_actors:\n  - name: Attacker\n"
        )
        (self.arc_dir / "assumptions.yml").write_text(
            "assumptions:\n  - id: A1\n    text: Assumption one\n"
        )
        item_data = {"active": True, "header": "Component", "type": "server"}
        (self.arc_dir / "ARC-001.yml").write_text(yaml.dump(item_data))
        items = cpssa_mod._read_doorstop_items(self.arc_dir)
        self.assertEqual(len(items), 1)

    def test_returns_empty_for_nonexistent_dir(self):
        items = cpssa_mod._read_doorstop_items(Path("/nonexistent/path"))
        self.assertEqual(items, [])


class TestFindSpecsRoot(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.project = Path(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_finds_docs_specs(self):
        specs = self.project / "docs" / "specs"
        arc = specs / "arc"
        arc.mkdir(parents=True)
        (arc / ".doorstop.yml").write_text("settings:\n  prefix: ARC\n")
        result = cpssa_mod._find_specs_root(self.project)
        self.assertIsNotNone(result)
        self.assertEqual(result.resolve(), specs.resolve())

    def test_returns_none_when_no_specs(self):
        result = cpssa_mod._find_specs_root(self.project)
        self.assertIsNone(result)


class TestFindArcDir(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.specs = Path(self.tmp) / "specs"
        self.specs.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_finds_arc_folder_by_name(self):
        arc = self.specs / "arc"
        arc.mkdir()
        (arc / ".doorstop.yml").write_text("settings:\n  prefix: ARC\n")
        result = cpssa_mod._find_arc_dir(self.specs)
        self.assertIsNotNone(result)
        self.assertEqual(result.resolve(), arc.resolve())

    def test_finds_harc_folder_by_name(self):
        harc = self.specs / "harc"
        harc.mkdir()
        (harc / ".doorstop.yml").write_text("settings:\n  prefix: HARC\n")
        result = cpssa_mod._find_arc_dir(self.specs)
        self.assertIsNotNone(result)
        self.assertEqual(result.resolve(), harc.resolve())

    def test_returns_none_when_no_doorstop_yml(self):
        arc = self.specs / "arc"
        arc.mkdir()
        # No .doorstop.yml
        result = cpssa_mod._find_arc_dir(self.specs)
        self.assertIsNone(result)

    def test_explicit_arc_folder_used_directly(self):
        arc = self.specs / "custom-arc"
        arc.mkdir()
        result = cpssa_mod._find_arc_dir(None, arc_folder=str(arc))
        self.assertIsNotNone(result)
        self.assertEqual(result.resolve(), arc.resolve())

    def test_explicit_arc_folder_nonexistent_returns_none(self):
        result = cpssa_mod._find_arc_dir(None, arc_folder="/nonexistent/arc")
        self.assertIsNone(result)

    def test_returns_none_for_none_specs_root(self):
        result = cpssa_mod._find_arc_dir(None)
        self.assertIsNone(result)


class TestReadThreatActors(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.arc_dir = Path(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # TST-013
    def test_reads_threat_actors(self):
        actors_data = {
            "threat_actors": [
                {"id": "TA-001", "name": "Insider Threat", "capability": "high"},
            ]
        }
        (self.arc_dir / "threat-actors.yml").write_text(
            yaml.dump(actors_data, default_flow_style=False)
        )
        actors = cpssa_mod._read_threat_actors(self.arc_dir)
        self.assertEqual(len(actors), 1)
        self.assertEqual(actors[0]["name"], "Insider Threat")

    def test_returns_empty_when_file_missing(self):
        actors = cpssa_mod._read_threat_actors(self.arc_dir)
        self.assertEqual(actors, [])


class TestReadAssumptions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.arc_dir = Path(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_reads_assumptions(self):
        assumptions_data = {
            "assumptions": [
                {"id": "ASM-001", "text": "Network segmentation is in place.", "verified": True},
            ]
        }
        (self.arc_dir / "assumptions.yml").write_text(
            yaml.dump(assumptions_data, default_flow_style=False)
        )
        assumptions = cpssa_mod._read_assumptions(self.arc_dir)
        self.assertEqual(len(assumptions), 1)
        self.assertEqual(assumptions[0]["id"], "ASM-001")

    def test_returns_empty_when_file_missing(self):
        assumptions = cpssa_mod._read_assumptions(self.arc_dir)
        self.assertEqual(assumptions, [])


# ---------------------------------------------------------------------------
# 3. create_threat_model tests
# ---------------------------------------------------------------------------

class TestCreateThreatModelThreagile(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.project = _create_minimal_project(Path(self.tmp))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # TST-013
    def test_generates_threat_model_file(self):
        out = create_threat_model(self.project)
        self.assertTrue(os.path.isfile(out))

    def test_output_is_valid_yaml(self):
        out = create_threat_model(self.project)
        with open(out, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        self.assertIsInstance(data, dict)

    def test_threat_model_contains_expected_keys(self):
        out = create_threat_model(self.project)
        with open(out, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        for key in ("threagile_version", "title", "technical_assets", "trust_boundaries"):
            self.assertIn(key, data, f"Missing key: {key}")

    def test_technical_assets_include_arc_items(self):
        out = create_threat_model(self.project)
        with open(out, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        assets = data.get("technical_assets", {})
        self.assertGreater(len(assets), 0)

    def test_default_output_path(self):
        out = create_threat_model(self.project)
        self.assertEqual(Path(out).name, "threat-model.yml")

    def test_custom_output_path(self):
        out_file = Path(self.tmp) / "custom-model.yml"
        out = create_threat_model(self.project, output_path=out_file)
        self.assertEqual(Path(out).resolve(), out_file.resolve())
        self.assertTrue(out_file.exists())

    def test_invalid_format_raises_error(self):
        with self.assertRaises(common.C5decError):
            create_threat_model(self.project, format="invalid-format")

    def test_nonexistent_project_raises_error(self):
        with self.assertRaises(common.C5decError):
            create_threat_model(Path("/nonexistent/project"))

    def test_zone_based_trust_boundaries_created(self):
        out = create_threat_model(self.project)
        with open(out, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        # ARC items have zones "OT" and "IT" — trust boundaries should appear
        boundaries = data.get("trust_boundaries", {})
        boundary_ids = list(boundaries.keys())
        # At least the default internet boundary + zone boundaries
        self.assertGreater(len(boundaries), 1)
        boundary_ids_lower = [b.lower() for b in boundary_ids]
        self.assertTrue(any("ot" in b for b in boundary_ids_lower))

    def test_communication_links_from_flows(self):
        out = create_threat_model(self.project)
        with open(out, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        # ARC-002 has a flow to ARC-001, so there should be ≥1 communication link
        total_links = sum(
            len(asset.get("communication_links", {}))
            for asset in data["technical_assets"].values()
        )
        self.assertGreater(total_links, 0)

    def test_tags_available_populated(self):
        out = create_threat_model(self.project)
        with open(out, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        # tags_available must be a list and non-empty when items have tags
        self.assertIsInstance(data.get("tags_available"), list)


class TestCreateThreatModelPytmPython(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.project = _create_minimal_project(Path(self.tmp))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_generates_python_script(self):
        out = create_threat_model(self.project, format="pytm-python")
        self.assertTrue(os.path.isfile(out))
        self.assertTrue(out.endswith(".py"))

    def test_generated_script_contains_pytm_imports(self):
        out = create_threat_model(self.project, format="pytm-python")
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("from pytm import", content)

    def test_generated_script_references_elements(self):
        out = create_threat_model(self.project, format="pytm-python")
        content = Path(out).read_text(encoding="utf-8")
        # ARC items should appear as pytm element assignments
        self.assertIn("= Server(", content)
        self.assertIn("= Datastore(", content)


class TestCreateThreatModelPytmJson(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.project = _create_minimal_project(Path(self.tmp))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_generates_json_file(self):
        out = create_threat_model(self.project, format="pytm-json")
        self.assertTrue(os.path.isfile(out))
        self.assertTrue(out.endswith(".json"))

    def test_generated_json_is_valid(self):
        out = create_threat_model(self.project, format="pytm-json")
        with open(out, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertIsInstance(data, dict)

    def test_generated_json_contains_elements(self):
        out = create_threat_model(self.project, format="pytm-json")
        with open(out, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertIn("elements", data)
        self.assertGreater(len(data["elements"]), 0)

    def test_generated_json_contains_dataflows(self):
        out = create_threat_model(self.project, format="pytm-json")
        with open(out, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        # ARC-002 → ARC-001 flow should produce one dataflow entry
        self.assertIn("dataflows", data)
        self.assertGreater(len(data["dataflows"]), 0)


class TestCreateThreatModelExplicitArcFolder(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.project = Path(self.tmp)
        # Arc items placed outside the standard docs/specs path
        self.arc_dir = self.project / "custom-arc"
        self.arc_dir.mkdir()
        item = {
            "active": True,
            "header": "Custom Component",
            "type": "server",
            "text": "A component in a custom arc folder.",
        }
        (self.arc_dir / "ARC-001.yml").write_text(
            yaml.dump(item, default_flow_style=False)
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_explicit_arc_folder_used(self):
        out = create_threat_model(
            self.project, arc_folder=str(self.arc_dir)
        )
        with open(out, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        assets = data.get("technical_assets", {})
        self.assertEqual(len(assets), 1)


# ---------------------------------------------------------------------------
# 4. generate_cpssa_report tests
# ---------------------------------------------------------------------------

def _create_minimal_threat_model(tmp_dir: Path) -> Path:
    """Write a minimal Threagile-compatible YAML threat model to disk."""
    model = {
        "threagile_version": "1.0.0",
        "title": "Test CPSSA Report",
        "date": "2026-03-06",
        "author": {"name": "TestAuthor"},
        "management_summary_comment": "Test summary.",
        "business_overview": {"description": "Test business overview."},
        "technical_overview": {"description": "Test technical overview."},
        "technical_assets": {
            "arc-001": {
                "id": "arc-001",
                "description": "Test Server",
                "confidentiality": "confidential",
                "integrity": "critical",
                "availability": "critical",
                "communication_links": {},
            }
        },
        "data_assets": {
            "user-data": {
                "id": "user-data",
                "description": "User data",
                "confidentiality": "confidential",
            }
        },
        "trust_boundaries": {
            "internet-boundary": {
                "id": "internet-boundary",
                "type": "network-on-prem",
                "description": "Internet perimeter",
            }
        },
        "abuse_cases": {
            "Unauthorized Access": "An attacker gains unauthorized access.",
            "Denial of Service": "An attacker causes unavailability.",
        },
        "security_requirements": {},
        "threat_actors": [
            {
                "id": "TA-001",
                "name": "External Attacker",
                "capability": "high",
                "access": "remote",
                "motivation": "financial",
                "description": "Motivated by financial gain.",
            }
        ],
        "assumptions": [
            {"id": "ASM-001", "text": "Network segmentation in place.", "verified": True}
        ],
    }
    model_path = tmp_dir / "threat-model.yml"
    with open(model_path, "w", encoding="utf-8") as fh:
        yaml.dump(model, fh, default_flow_style=False, allow_unicode=True, sort_keys=False)
    return model_path


class TestGenerateCpssaReport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp_dir = Path(self.tmp)
        self.model_path = _create_minimal_threat_model(self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_generates_markdown_file(self):
        out = generate_cpssa_report(self.model_path)
        self.assertTrue(os.path.isfile(out))
        self.assertTrue(out.endswith(".md"))

    def test_report_contains_title(self):
        out = generate_cpssa_report(self.model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("Test CPSSA Report", content)

    def test_report_contains_stride_section(self):
        out = generate_cpssa_report(self.model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("Spoofing", content)
        self.assertIn("Tampering", content)

    def test_report_contains_technical_assets_table(self):
        out = generate_cpssa_report(self.model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("arc-001", content)
        self.assertIn("Test Server", content)

    def test_report_contains_abuse_cases(self):
        out = generate_cpssa_report(self.model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("Unauthorized Access", content)
        self.assertIn("Denial of Service", content)

    def test_report_contains_threat_actors(self):
        out = generate_cpssa_report(self.model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("External Attacker", content)

    def test_report_contains_assumptions(self):
        out = generate_cpssa_report(self.model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("ASM-001", content)

    def test_nonexistent_model_raises_error(self):
        with self.assertRaises(common.C5decError):
            generate_cpssa_report(Path("/nonexistent/model.yml"))

    def test_custom_output_path(self):
        out_file = self.tmp_dir / "my-report.md"
        out = generate_cpssa_report(self.model_path, output_path=out_file)
        self.assertEqual(Path(out).resolve(), out_file.resolve())
        self.assertTrue(out_file.exists())

    def test_default_output_name(self):
        out = generate_cpssa_report(self.model_path)
        self.assertEqual(Path(out).name, "cpssa-report.md")


# ---------------------------------------------------------------------------
# 5. generate_dfd tests
# ---------------------------------------------------------------------------

class TestGenerateDfd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.project = _create_minimal_project(Path(self.tmp))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_generates_plantuml_file(self):
        out = generate_dfd(self.project)
        self.assertTrue(os.path.isfile(out))
        self.assertTrue(out.endswith(".puml"))

    def test_output_is_valid_plantuml(self):
        out = generate_dfd(self.project)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("@startuml", content)
        self.assertIn("@enduml", content)

    def test_dfd_contains_arc_elements(self):
        out = generate_dfd(self.project)
        content = Path(out).read_text(encoding="utf-8")
        # ARC items should produce component/database/actor entries
        self.assertTrue(
            any(kw in content for kw in ("component", "database", "actor"))
        )

    def test_dfd_contains_zone_boundaries(self):
        out = generate_dfd(self.project)
        content = Path(out).read_text(encoding="utf-8")
        # OT and IT zones should produce rectangle groupings
        self.assertIn("rectangle", content)
        self.assertIn("OT Zone", content)

    def test_dfd_contains_dataflow_arrows(self):
        out = generate_dfd(self.project)
        content = Path(out).read_text(encoding="utf-8")
        # ARC-002 flows to ARC-001
        self.assertIn("-->", content)

    def test_default_output_name(self):
        out = generate_dfd(self.project)
        self.assertEqual(Path(out).name, "cpssa-dfd.puml")

    def test_custom_output_path(self):
        out_file = Path(self.tmp) / "my-dfd.puml"
        out = generate_dfd(self.project, output_path=out_file)
        self.assertEqual(Path(out).resolve(), out_file.resolve())
        self.assertTrue(out_file.exists())

    def test_nonexistent_project_raises_error(self):
        with self.assertRaises(common.C5decError):
            generate_dfd(Path("/nonexistent/project"))

    def test_explicit_arc_folder(self):
        arc_dir = self.project / "docs" / "specs" / "arc"
        out = generate_dfd(self.project, arc_folder=str(arc_dir))
        self.assertTrue(os.path.isfile(out))


# ---------------------------------------------------------------------------
# 6. generate_fair_input_template tests
# ---------------------------------------------------------------------------

class TestGenerateFairInputTemplate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp_dir = Path(self.tmp)
        self.model_path = _create_minimal_threat_model(self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_generates_yaml_file(self):
        out = generate_fair_input_template(self.model_path)
        self.assertTrue(os.path.isfile(out))
        self.assertTrue(out.endswith(".yml"))

    def test_output_contains_defaults_section(self):
        out = generate_fair_input_template(self.model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("defaults:", content)

    def test_output_contains_scenarios_section(self):
        out = generate_fair_input_template(self.model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("scenarios:", content)

    def test_abuse_cases_appear_as_scenarios(self):
        out = generate_fair_input_template(self.model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("Unauthorized Access", content)
        self.assertIn("Denial of Service", content)

    def test_output_contains_lef_and_lm_defaults(self):
        out = generate_fair_input_template(self.model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("lef:", content)
        self.assertIn("lm:", content)

    def test_default_output_name(self):
        out = generate_fair_input_template(self.model_path)
        self.assertEqual(Path(out).name, "fair-params.yml")

    def test_custom_output_path(self):
        out_file = self.tmp_dir / "my-fair-params.yml"
        out = generate_fair_input_template(self.model_path, output_path=out_file)
        self.assertEqual(Path(out).resolve(), out_file.resolve())

    def test_nonexistent_model_raises_error(self):
        with self.assertRaises(common.C5decError):
            generate_fair_input_template(Path("/nonexistent/model.yml"))

    def test_model_without_abuse_cases_raises_error(self):
        empty_model = self.tmp_dir / "empty-model.yml"
        empty_model.write_text(
            yaml.dump({"threagile_version": "1.0.0", "title": "Empty"}, default_flow_style=False)
        )
        with self.assertRaises(common.C5decError):
            generate_fair_input_template(empty_model)

    def test_pytm_json_model_generates_template(self):
        # Build a minimal pytm JSON model
        pytm_model = {
            "name": "Test pytm model",
            "elements": [{"uid": "ARC-001", "name": "Test Server", "pytm_class": "Server"}],
            "abuse_cases": {
                "Server Compromise": "Attacker compromises the test server."
            },
        }
        json_model_path = self.tmp_dir / "model.json"
        json_model_path.write_text(json.dumps(pytm_model))
        out = generate_fair_input_template(json_model_path)
        self.assertTrue(os.path.isfile(out))
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("Server Compromise", content)

    def test_pytm_json_without_abuse_cases_synthesises_scenarios(self):
        pytm_model = {
            "name": "Test pytm model",
            "elements": [
                {"uid": "ARC-001", "name": "Server A", "pytm_class": "Server"},
                {"uid": "ARC-002", "name": "DB B", "pytm_class": "Datastore"},
            ],
        }
        json_model_path = self.tmp_dir / "model-no-cases.json"
        json_model_path.write_text(json.dumps(pytm_model))
        out = generate_fair_input_template(json_model_path)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("Server A", content)


# ---------------------------------------------------------------------------
# 7. run_quantitative_risk_analysis tests
# ---------------------------------------------------------------------------

class TestRunQuantitativeRiskAnalysis(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp_dir = Path(self.tmp)
        self.model_path = _create_minimal_threat_model(self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_generates_markdown_summary(self):
        out = run_quantitative_risk_analysis(self.model_path, simulations=100)
        self.assertTrue(os.path.isfile(out))
        self.assertTrue(out.endswith(".md"))

    def test_generates_csv_results(self):
        run_quantitative_risk_analysis(self.model_path, simulations=100)
        csv_path = self.model_path.parent / "cpssa-risk-results.csv"
        self.assertTrue(csv_path.exists())

    def test_summary_contains_scenario_names(self):
        out = run_quantitative_risk_analysis(self.model_path, simulations=100)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("Unauthorized Access", content)

    def test_summary_contains_ale_table(self):
        out = run_quantitative_risk_analysis(self.model_path, simulations=100)
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("Annualised loss expectancy", content)

    def test_custom_output_dir(self):
        out_dir = self.tmp_dir / "results"
        out = run_quantitative_risk_analysis(
            self.model_path, output_path=out_dir, simulations=100
        )
        self.assertTrue(out_dir.exists())
        self.assertTrue(os.path.isfile(out))

    def test_nonexistent_model_raises_error(self):
        with self.assertRaises(common.C5decError):
            run_quantitative_risk_analysis(Path("/nonexistent/model.yml"))

    def test_model_without_abuse_cases_raises_error(self):
        empty_model = self.tmp_dir / "empty.yml"
        empty_model.write_text(
            yaml.dump({"title": "Empty"}, default_flow_style=False)
        )
        with self.assertRaises(common.C5decError):
            run_quantitative_risk_analysis(empty_model, simulations=100)

    def test_with_fair_params_file(self):
        # Write a minimal FAIR params file
        fair_params = {
            "defaults": {
                "lef": {"low": 1, "mode": 3, "high": 10},
                "lm": {"low": 5000, "mode": 50000, "high": 500000},
            },
            "scenarios": {
                "Unauthorized Access": {
                    "description": "Test",
                    "lef": {"low": 2, "mode": 5, "high": 15},
                    "lm": {"low": 10000, "mode": 100000, "high": 1000000},
                }
            },
        }
        params_path = self.tmp_dir / "fair-params.yml"
        with open(params_path, "w", encoding="utf-8") as fh:
            yaml.dump(fair_params, fh, default_flow_style=False)

        out = run_quantitative_risk_analysis(
            self.model_path,
            simulations=100,
            fair_params_path=params_path,
        )
        content = Path(out).read_text(encoding="utf-8")
        self.assertIn("Unauthorized Access", content)

    def test_nonexistent_fair_params_raises_error(self):
        with self.assertRaises(common.C5decError):
            run_quantitative_risk_analysis(
                self.model_path,
                simulations=100,
                fair_params_path=Path("/nonexistent/params.yml"),
            )

    def test_pytm_json_model_analysis(self):
        # Build a pytm JSON scenario for analysis
        pytm_model = {
            "name": "Test pytm model",
            "elements": [{"uid": "ARC-001", "name": "Test Server", "pytm_class": "Server"}],
            "abuse_cases": {
                "Server Compromise": "Attacker compromises the test server."
            },
        }
        json_model = self.tmp_dir / "model.json"
        json_model.write_text(json.dumps(pytm_model))
        out = run_quantitative_risk_analysis(json_model, simulations=100)
        self.assertTrue(os.path.isfile(out))


# ---------------------------------------------------------------------------
# 8. Threagile mapping tests
# ---------------------------------------------------------------------------

class TestThreagileMappers(unittest.TestCase):
    def test_map_protocol_known_value(self):
        result = cpssa_mod._map_protocol("https")
        self.assertNotEqual(result, "unknown-protocol")

    def test_map_protocol_unknown_value_returns_default(self):
        result = cpssa_mod._map_protocol("totally-unknown-proto-xyz")
        self.assertEqual(result, "unknown-protocol")

    def test_map_authentication_known_value(self):
        result = cpssa_mod._map_authentication("none")
        self.assertIsInstance(result, str)

    def test_map_asset_type_server(self):
        result = cpssa_mod._map_asset_type("server")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_map_encryption_none(self):
        result = cpssa_mod._map_encryption("none")
        self.assertIsInstance(result, str)

    def test_load_threagile_mappings_returns_dict(self):
        mappings = cpssa_mod._load_threagile_mappings()
        self.assertIsInstance(mappings, dict)


# ---------------------------------------------------------------------------
# 9. Build pytm model dict tests
# ---------------------------------------------------------------------------

class TestBuildPytmModelDict(unittest.TestCase):
    def _make_item(self, uid, header, item_type="server", zone=""):
        return {
            "_uid": uid,
            "header": header,
            "type": item_type,
            "zone": zone,
            "text": f"Description of {header}.",
            "protocol": "HTTPS",
            "port": 443,
        }

    def test_elements_created_for_each_arc_item(self):
        items = [
            self._make_item("ARC-001", "Web Server"),
            self._make_item("ARC-002", "Historian", "historian"),
        ]
        model = cpssa_mod._build_pytm_model_dict("TestProject", items)
        self.assertEqual(len(model["elements"]), 2)

    def test_dataflows_created_from_flows_field(self):
        items = [
            {
                "_uid": "ARC-001",
                "header": "Server A",
                "type": "server",
                "zone": "",
                "text": "Server",
                "flows": [{"target": "ARC-002", "protocol": "HTTPS", "port": 443}],
            },
            self._make_item("ARC-002", "Server B"),
        ]
        model = cpssa_mod._build_pytm_model_dict("TestProject", items)
        self.assertGreater(len(model["dataflows"]), 0)

    def test_boundaries_created_for_zones(self):
        items = [
            self._make_item("ARC-001", "IT Component", zone="IT"),
            self._make_item("ARC-002", "OT Component", zone="OT"),
        ]
        model = cpssa_mod._build_pytm_model_dict("TestProject", items)
        zones = {b["zone"] for b in model["boundaries"]}
        self.assertIn("IT", zones)
        self.assertIn("OT", zones)

    def test_model_name_includes_project_name(self):
        model = cpssa_mod._build_pytm_model_dict("MyProject", [])
        self.assertIn("MyProject", model["name"])


if __name__ == "__main__":
    unittest.main()
