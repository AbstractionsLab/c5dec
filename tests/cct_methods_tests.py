import unittest
from unittest.mock import MagicMock, patch, call
import sys
import os
# Add the parent directory to the sys.path so modules can be imported
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from lxml import etree
import c5dec.core.cct as cct

os.chdir(parent_dir + "/c5dec")

class TestCheckHierarchical(unittest.TestCase):

    def setUp(self):
        componentA = MagicMock(cct.AComponent(_id="compA_id", _name="compA_name"))
        # set a mock return value for the function get_hierarchical_tree
        componentA.get_hierarchical_tree.return_value = ["compb_id"]
        cct.Index.update("compA_id", componentA)
        componentB = MagicMock(cct.AComponent(_id="compB_id", _name="compB_name"))
        componentB.get_hierarchical_tree.return_value = []
        cct.Index.update("compB_id", componentB)
        componentC = MagicMock(cct.AComponent(_id="compC_id", _name="compC_name"))
        componentC.get_hierarchical_tree.return_value = ["compa_id", "compb_id"]
        cct.Index.update("compC_id", componentC)
        componentD = MagicMock(cct.AComponent(_id="compD_id", _name="compD_name"))
        componentD.get_hierarchical_tree.return_value = []
        cct.Index.update("compD_id", componentD)

    def test_check_hierarchical(self):
        component_ids = set(['compa_id', 'compd_id'])
        is_valid = cct.check_hierarchical('compa_id', component_ids)
        self.assertFalse(is_valid)

    def test_check_hierarchical_redundant(self):
        component_ids = set(['compa_id', 'compb_id'])
        is_valid = cct.check_hierarchical('compa_id', component_ids)
        self.assertTrue(is_valid)

    def test_check_hierarchical_redundant_inverted(self):
        component_ids = set(['compa_id', 'compb_id'])
        is_valid = cct.check_hierarchical('compb_id', component_ids, inverted=True)
        self.assertTrue(is_valid)

    def test_check_hierarchical_redundant_non_adjecent(self):
        # tests if cases like CompC > CompA > CompB are correctly detected.
        component_ids = set(['compc_id', 'compb_id'])
        is_valid = cct.check_hierarchical('compc_id', component_ids)
        self.assertTrue(is_valid)

    def test_check_hierarchical_redundant_non_adjecent_inverted(self):
        # tests if cases like CompC > CompA > CompB are correctly detected.
        component_ids = set(['compc_id', 'compb_id'])
        is_valid = cct.check_hierarchical('compb_id', component_ids, inverted=True)
        self.assertTrue(is_valid)

    def tearDown(self):
        cct.Index.clear()

class TestCheckDependencies(unittest.TestCase):

    def setUp(self):
        # set up components
        componentA = MagicMock(cct.AComponent(_id="compA_id", _name="compA_name"))
        componentA.get_dependency_pool.return_value = ["compb_id"]
        cct.Index.update("compA_id", componentA)
        componentB = MagicMock(cct.AComponent(_id="compB_id", _name="compB_name"))
        componentB.get_dependency_pool.return_value = []
        cct.Index.update("compB_id", componentB)
        componentC = MagicMock(cct.AComponent(_id="compC_id", _name="compC_name"))
        componentC.get_dependency_pool.return_value = [("compa_id", "compb_id")]
        cct.Index.update("compC_id", componentC)
        componentD = MagicMock(cct.AComponent(_id="compD_id", _name="compD_name"))
        componentD.get_dependency_pool.return_value = []
        cct.Index.update("compD_id", componentD)

    def test_check_dependencies(self):
        # valid set
        component_ids = set(['compa_id', 'compb_id'])
        is_valid = cct.check_dependencies('compa_id', component_ids)
        self.assertFalse(is_valid)

    def test_check_dependencies_invalid(self):
        component_ids = set(['compa_id'])
        is_valid = cct.check_dependencies('compa_id', component_ids)
        self.assertTrue(is_valid)

    def test_valid_or_dependencies(self):
        component_ids_1 = set(['compc_id', 'compa_id', 'compb_id'])
        component_ids_2 = set(['compc_id', 'compb_id'])

        is_valid_1  = cct.check_dependencies('compc_id', component_ids_1)
        is_valid_2 = cct.check_dependencies('compc_id', component_ids_2)

        self.assertTrue(all([not is_valid_1, not is_valid_2]))

    @patch.object(cct, 'check_hierarchical')
    def test_check_hierarchical_dependencies(self, mock_check_h):
        # CompD hierarchical to compB
        mock_check_h.return_value = True
        component_ids = set(["compa_id", "compd_id"])
        is_valid = cct.check_dependencies('compa_id', component_ids)
        self.assertFalse(is_valid)

    def test_check_hierarchical_or_dependecies(self):
        # same logic as before no need for additional unit test
        pass

    def tearDown(self):
        cct.Index.clear()

class TestValidateDependencies(unittest.TestCase):

    def setUp(self):
        componentA = MagicMock(cct.AComponent(_id="compA_id", _name="compA_name"))
        componentA.get_dependency_pool.return_value = ["compb_id"]
        componentA.get_hierarchical_tree.return_value = []
        cct.Index.update("compA_id", componentA)
        componentB = MagicMock(cct.AComponent(_id="compB_id", _name="compB_name"))
        componentB.get_dependency_pool.return_value = []
        componentB.get_hierarchical_tree.return_value = []
        cct.Index.update("compB_id", componentB)
        componentC = MagicMock(cct.AComponent(_id="compC_id", _name="compC_name"))
        componentC.get_dependency_pool.return_value = [("compa_id", "compd_id")]
        componentC.get_hierarchical_tree.return_value = []
        cct.Index.update("compC_id", componentC)
        componentD = MagicMock(cct.AComponent(_id="compD_id", _name="compD_name"))
        componentD.get_dependency_pool.return_value = []
        componentD.get_hierarchical_tree.return_value = ["compb_id"]
        cct.Index.update("compD_id", componentD)

    def test_validate_dependencies_valid_set(self):
        component_ids = set(["compa_id", "compb_id"])
        is_valid, valid_set = cct.validate_dependencies(component_ids)
        self.assertTrue(is_valid)
        self.assertEqual(valid_set, component_ids)
    
    def test_validate_dependencies_invalid_set(self):
        component_ids = set(["compa_id"])
        is_valid, valid_set = cct.validate_dependencies(component_ids)
        self.assertFalse(is_valid)
        self.assertEqual(valid_set, set(["compa_id", "compb_id"]))

    def test_validate_dependencies_redundante_set(self):
        component_ids = set(["compd_id", "compb_id"])
        is_valid, valid_set = cct.validate_dependencies(component_ids)
        self.assertFalse(is_valid)
        self.assertEqual(valid_set, set(["compd_id"]))

    def test_validate_dependencies_hierarchical_dependency(self):
        component_ids = set(["compa_id", "compd_id"])
        is_valid, valid_set = cct.validate_dependencies(component_ids)
        self.assertTrue(is_valid)
        self.assertEqual(valid_set, component_ids)
    
    def test_validate_dependencies_non_adjacent_hierarchy(self):
        componentE = MagicMock(cct.AComponent(_id="compE_id", _name="compE_name"))
        componentE.get_dependency_pool.return_value = []
        componentE.get_hierarchical_tree.return_value = ["compd_id", "compb_id"]
        cct.Index.update("compE_id", componentE)

        component_ids = set(["compe_id", "compb_id"])
        is_valid, valid_set = cct.validate_dependencies(component_ids)
        self.assertFalse(is_valid)
        self.assertEqual(valid_set, set(["compe_id"]))

    def tearDown(self):
        cct.Index.clear()

class TestEvalIndexOperations(unittest.TestCase):

    def setUp(self):
        

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_save_index(self, mock_open):
        index = {'key': 'value'}
        save_index(index, '/path/to')
        mock_open.assert_called_once_with('/path/to/index.json', 'w')
        mock_open().write.assert_called_once_with(json.dumps(index, indent=4))

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=json.dumps({'key': 'value'}))
    def test_load_index(self, mock_open):
        expected_index = {'key': 'value'}
        index = load_index('/path/to')
        mock_open.assert_called_once_with('/path/to/index.json', 'r')
        self.assertEqual(index, expected_index)

if __name__ == '__main__':
    unittest.main()

"""TODO
- doorstop Index methods
- create eval checklist methods
- climethods
"""

if __name__ == '__main__':
    unittest.main()
