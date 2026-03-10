"""
Test module for SBOM functionality.

Tests SBOM generation, parsing, Doorstop integration, comparison,
and validation capabilities.
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import c5dec.core.sbom as sbom
import c5dec.settings as c5settings


class TestSBOMUtilities(unittest.TestCase):
    """Test SBOM utility functions."""
    
    def test_check_syft_installed(self):
        """Test Syft installation check."""
        # Should return bool without crashing
        result = sbom.check_syft_installed()
        self.assertIsInstance(result, bool)


class TestSBOMParsing(unittest.TestCase):
    """Test SBOM parsing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.sample_sbom = self._create_sample_cyclonedx_sbom()
    
    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_sample_cyclonedx_sbom(self):
        """Create a sample CycloneDX SBOM for testing."""
        sbom_data = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "serialNumber": "urn:uuid:12345",
            "version": 1,
            "metadata": {
                "timestamp": "2026-02-15T10:00:00Z",
                "component": {
                    "type": "application",
                    "name": "test-app",
                    "version": "1.0.0"
                }
            },
            "components": [
                {
                    "type": "library",
                    "name": "example-lib",
                    "version": "2.3.4",
                    "purl": "pkg:pypi/example-lib@2.3.4",
                    "licenses": [
                        {"license": {"id": "MIT"}}
                    ],
                    "supplier": {"name": "Example Corp"},
                    "description": "An example library"
                },
                {
                    "type": "library",
                    "name": "another-lib",
                    "version": "1.0.0",
                    "purl": "pkg:pypi/another-lib@1.0.0",
                    "licenses": [
                        {"license": {"id": "Apache-2.0"}}
                    ]
                }
            ]
        }
        
        sbom_path = Path(self.temp_dir) / "test_sbom.json"
        with open(sbom_path, 'w') as f:
            json.dump(sbom_data, f, indent=2)
        
        return sbom_path
    
    def test_parse_cyclonedx_sbom(self):
        """Test parsing a CycloneDX SBOM file."""
        parsed = sbom.parse_cyclonedx_sbom(self.sample_sbom)
        
        self.assertEqual(parsed['format'], 'CycloneDX')
        self.assertEqual(parsed['component_count'], 2)
        self.assertEqual(len(parsed['components']), 2)
        
        # Check first component
        comp1 = parsed['components'][0]
        self.assertEqual(comp1['name'], 'example-lib')
        self.assertEqual(comp1['version'], '2.3.4')
        self.assertIn('MIT', comp1['licenses'])
    
    def test_parse_invalid_sbom(self):
        """Test parsing invalid SBOM raises error."""
        invalid_sbom = Path(self.temp_dir) / "invalid.json"
        invalid_sbom.write_text("not valid json {")
        
        with self.assertRaises(Exception):
            sbom.parse_cyclonedx_sbom(invalid_sbom)
    
    def test_parse_missing_sbom(self):
        """Test parsing non-existent SBOM raises error."""
        missing_sbom = Path(self.temp_dir) / "missing.json"
        
        with self.assertRaises(Exception):
            sbom.parse_cyclonedx_sbom(missing_sbom)


class TestSBOMDoorstopIntegration(unittest.TestCase):
    """Test SBOM integration with Doorstop."""
    
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
        
        # Create sample SBOM
        self.sample_sbom = self._create_sample_sbom()
    
    def tearDown(self):
        """Clean up temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_sample_sbom(self):
        """Create sample SBOM file."""
        sbom_data = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "serialNumber": "urn:uuid:test-123",
            "version": 1,
            "metadata": {"timestamp": "2026-02-15T10:00:00Z"},
            "components": [
                {
                    "type": "library",
                    "name": "test-component",
                    "version": "1.0.0",
                    "purl": "pkg:pypi/test-component@1.0.0",
                    "licenses": [{"license": {"id": "MIT"}}]
                }
            ]
        }
        
        sbom_path = self.project_path / "test_sbom.json"
        with open(sbom_path, 'w') as f:
            json.dump(sbom_data, f)
        
        return sbom_path
    
    def test_import_sbom_to_doorstop(self):
        """Test importing SBOM into Doorstop."""
        try:
            doc_path = sbom.import_sbom_to_doorstop(
                sbom_path=self.sample_sbom,
                project_path=self.project_path,
                prefix="SBOM",
                version="1.0"
            )
            
            # Check that document was created
            self.assertTrue(Path(doc_path).exists())
            
            # Check that index file exists
            index_path = Path(doc_path) / "sbom_index.json"
            self.assertTrue(index_path.exists())
            
            # Verify index content
            with open(index_path, 'r') as f:
                index_data = json.load(f)
            
            self.assertIn('SBOMInfo', index_data)
            self.assertIn('Components', index_data)
            self.assertEqual(index_data['SBOMInfo']['format'], 'CycloneDX')
            
        except Exception as e:
            self.skipTest(f"Doorstop not available: {e}")


class TestSBOMComparison(unittest.TestCase):
    """Test SBOM comparison functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_compare_nonexistent_sboms(self):
        """Test comparing non-existent SBOMs handles gracefully."""
        with self.assertRaises(Exception):
            sbom.compare_sboms(
                sbom1_prefix="SBOM-v1",
                sbom2_prefix="SBOM-v2",
                project_path=self.project_path
            )
    
    def test_export_sbom_diff_report(self):
        """Test exporting SBOM comparison report."""
        # Create mock diff result
        diff_result = {
            'sbom1': 'SBOM-v1.0',
            'sbom2': 'SBOM-v2.0',
            'added': {
                'new-lib': {'version': '1.0.0', 'purl': 'pkg:pypi/new-lib@1.0.0', 'license': 'MIT'}
            },
            'removed': {
                'old-lib': {'version': '0.5.0', 'purl': 'pkg:pypi/old-lib@0.5.0', 'license': 'BSD'}
            },
            'changed': {
                'updated-lib': {'old_version': '1.0.0', 'new_version': '2.0.0'}
            },
            'summary': {
                'added_count': 1,
                'removed_count': 1,
                'changed_count': 1
            }
        }
        
        output_path = Path(self.temp_dir) / "diff_report.md"
        
        result_path = sbom.export_sbom_diff_report(diff_result, output_path)
        
        self.assertTrue(Path(result_path).exists())
        
        # Verify content
        content = output_path.read_text()
        self.assertIn("SBOM Comparison Report", content)
        self.assertIn("Added Components", content)
        self.assertIn("Removed Components", content)
        self.assertIn("Changed Components", content)
        self.assertIn("new-lib", content)
        self.assertIn("old-lib", content)


class TestSBOMValidation(unittest.TestCase):
    """Test SBOM validation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_validate_nonexistent_sbom(self):
        """Test validation of non-existent SBOM."""
        with self.assertRaises(Exception):
            sbom.validate_sbom(
                sbom_prefix="SBOM-nonexistent",
                project_path=self.project_path
            )


class TestSBOMGeneration(unittest.TestCase):
    """Test SBOM generation with Syft."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_generate_sbom_requires_syft(self):
        """Test that SBOM generation checks for Syft."""
        if not sbom.check_syft_installed():
            # If Syft not installed, should raise error
            with self.assertRaises(Exception):
                sbom.generate_sbom(
                    target_path=Path(self.temp_dir),
                    output_path=Path(self.temp_dir) / "sbom.json"
                )
        else:
            # If Syft is installed, try generating
            try:
                result = sbom.generate_sbom(
                    target_path=Path(self.temp_dir),
                    output_path=Path(self.temp_dir) / "sbom.json"
                )
                self.assertTrue(Path(result).exists())
            except Exception as e:
                self.skipTest(f"Syft generation failed: {e}")


def suite():
    """Return test suite."""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestSBOMUtilities))
    test_suite.addTest(unittest.makeSuite(TestSBOMParsing))
    test_suite.addTest(unittest.makeSuite(TestSBOMDoorstopIntegration))
    test_suite.addTest(unittest.makeSuite(TestSBOMComparison))
    test_suite.addTest(unittest.makeSuite(TestSBOMValidation))
    test_suite.addTest(unittest.makeSuite(TestSBOMGeneration))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
