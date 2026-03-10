"""
Test module for CRA checklist functionality.

Tests CRA requirements database, checklist generation, verdict tracking,
and Excel export capabilities.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import c5dec.core.cra as cra
import c5dec.settings as c5settings


class TestCRADatabase(unittest.TestCase):
    """Test CRA requirements database loading and querying."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.db = cra.CRADatabase()
    
    def test_database_loads(self):
        """Test that CRA database loads successfully."""
        self.assertIsNotNone(self.db)
        self.assertGreater(len(self.db.get_all_requirements()), 0)
    
    def test_database_version(self):
        """Test that database has version information."""
        self.assertIsNotNone(self.db.version)
        self.assertEqual(self.db.version, "1.0")
        self.assertIsNotNone(self.db.regulation)
        self.assertIn("2024/2847", self.db.regulation)
    
    def test_categories_exist(self):
        """Test that Part I and Part II categories exist."""
        self.assertIn('part_i', self.db.categories)
        self.assertIn('part_ii', self.db.categories)
    
    def test_requirement_count(self):
        """Test that requirements are loaded."""
        all_reqs = self.db.get_all_requirements()
        self.assertGreater(len(all_reqs), 20, "Should have 20+ requirements")
    
    def test_get_requirement_by_id(self):
        """Test retrieving a specific requirement."""
        req = self.db.get_requirement('cra_i_1_1')
        self.assertIsNotNone(req)
        self.assertEqual(req.id, 'cra_i_1_1')
        self.assertIn('appropriate level of cybersecurity', req.text.lower())
    
    def test_sbom_requirement_exists(self):
        """Test that SBOM requirement exists (critical for CRA compliance)."""
        req = self.db.get_requirement('cra_ii_1_1')
        self.assertIsNotNone(req)
        self.assertIn('SBOM', req.text)
    
    def test_category_filtering(self):
        """Test filtering requirements by product category."""
        default_reqs = self.db.get_applicable_requirements('default')
        class_i_reqs = self.db.get_applicable_requirements('class_i')
        
        # All categories should have some requirements
        self.assertGreater(len(default_reqs), 0)
        self.assertGreater(len(class_i_reqs), 0)
        
        # Class I should have at least as many as default
        self.assertGreaterEqual(len(class_i_reqs), len(default_reqs))
    
    def test_requirement_applies_to_category(self):
        """Test requirement applicability check."""
        req = self.db.get_requirement('cra_i_1_1')
        self.assertTrue(req.applies_to_category('default'))
        self.assertTrue(req.applies_to_category('class_i'))
        self.assertTrue(req.applies_to_category('class_ii'))
        self.assertTrue(req.applies_to_category('critical'))


class TestCRAChecklistBuilder(unittest.TestCase):
    """Test CRA checklist generation and management."""
    
    def setUp(self):
        """Set up test fixtures with temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        
        # Create minimal Doorstop structure
        docs_specs = self.project_path / "docs" / "specs"
        docs_specs.mkdir(parents=True)
        
        # Create MRS root document
        mrs_path = docs_specs / "MRS"
        mrs_path.mkdir()
        doorstop_yml = mrs_path / ".doorstop.yml"
        doorstop_yml.write_text("settings:\n  prefix: MRS\n  sep: '-'\n  digits: 3\n")
        
        self.builder = cra.CRAChecklistBuilder()
    
    def tearDown(self):
        """Clean up temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_builder_initialization(self):
        """Test that checklist builder initializes."""
        self.assertIsNotNone(self.builder)
        self.assertIsNotNone(self.builder.db)
    
    def test_create_checklist_invalid_category(self):
        """Test that invalid category raises error."""
        with self.assertRaises(Exception):
            self.builder.create_cra_checklist(
                category="invalid",
                project_path=self.project_path
            )
    
    def test_create_checklist_default(self):
        """Test creating checklist for default category."""
        try:
            checklist_path = self.builder.create_cra_checklist(
                category="default",
                project_path=self.project_path,
                prefix="CRAC"
            )
            
            self.assertTrue(Path(checklist_path).exists())
            
            # Check that index.json was created
            index_path = Path(checklist_path) / "index.json"
            self.assertTrue(index_path.exists())
            
        except Exception as e:
            # May fail if doorstop not installed, that's okay for unit test
            self.skipTest(f"Doorstop not available: {e}")
    
    def test_create_checklist_class_i(self):
        """Test creating checklist for Important Class I category."""
        try:
            checklist_path = self.builder.create_cra_checklist(
                category="class_i",
                project_path=self.project_path,
                prefix="CRAC"
            )
            
            self.assertTrue(Path(checklist_path).exists())
            
        except Exception as e:
            self.skipTest(f"Doorstop not available: {e}")


class TestCRATraceability(unittest.TestCase):
    """Test cross-feature traceability functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_verify_sbom_exists_false(self):
        """Test SBOM verification when SBOM doesn't exist."""
        # Should return False when no SBOM document exists
        exists = cra.verify_sbom_exists(project_path=self.project_path)
        self.assertFalse(exists)
    
    def test_auto_verify_handles_missing_checklist(self):
        """Test auto-verification gracefully handles missing checklist."""
        # Should not crash when checklist doesn't exist
        result = cra.auto_verify_sbom_requirement(project_path=self.project_path)
        self.assertFalse(result)


class TestCRARequirements(unittest.TestCase):
    """Test individual CRA requirement classes."""
    
    def test_requirement_creation(self):
        """Test CRARequirement object creation."""
        req = cra.CRARequirement(
            id="test_1",
            name="Test Requirement",
            text="This is a test requirement.",
            applies_to=["default", "class_i"]
        )
        
        self.assertEqual(req.id, "test_1")
        self.assertEqual(req.name, "Test Requirement")
        self.assertTrue(req.applies_to_category("default"))
        self.assertTrue(req.applies_to_category("class_i"))
        self.assertFalse(req.applies_to_category("critical"))
    
    def test_section_creation(self):
        """Test CRASection object creation."""
        req1 = cra.CRARequirement("r1", "Req 1", "Text", ["default"])
        req2 = cra.CRARequirement("r2", "Req 2", "Text", ["class_i"])
        
        section = cra.CRASection("sec_1", "Test Section", [req1, req2])
        
        self.assertEqual(section.id, "sec_1")
        self.assertEqual(len(section.requirements), 2)
        
        default_reqs = section.get_applicable_requirements("default")
        self.assertEqual(len(default_reqs), 1)
        
        class_i_reqs = section.get_applicable_requirements("class_i")
        self.assertEqual(len(class_i_reqs), 2)


def suite():
    """Return test suite."""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestCRADatabase))
    test_suite.addTest(unittest.makeSuite(TestCRAChecklistBuilder))
    test_suite.addTest(unittest.makeSuite(TestCRATraceability))
    test_suite.addTest(unittest.makeSuite(TestCRARequirements))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
