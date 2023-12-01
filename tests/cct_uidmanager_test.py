import unittest
from unittest.mock import MagicMock
import sys
import os
# Add the parent directory to the sys.path so modules can be imported
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from c5dec.core.cct import UniqueIDManager  # Replace 'your_module' with the actual module name
from c5dec.common import C5decError

class TestUniqueIDManager(unittest.TestCase):

    def setUp(self):
        """Set up test environment with a custom separator and count width."""
        self.uid_manager = UniqueIDManager(separator='-', count_width=3)

    def test_get_next_id(self):
        """Test generating unique IDs with the specified separator and count width."""
        id1 = self.uid_manager.next("prefix")
        id2 = self.uid_manager.next("prefix")
        id3 = self.uid_manager.next("another_prefix")

        self.assertEqual(id1, "prefix-001")
        self.assertEqual(id2, "prefix-002")
        self.assertEqual(id3, "another_prefix-001")

    def test_singleton_property(self):
        """Ensure only one UniqueIDManager instance exists at a time."""
        uid_manager1 = UniqueIDManager()
        uid_manager2 = UniqueIDManager()
        self.assertIs(uid_manager1, uid_manager2)

    def test_custom_config_update(self):
        """Verify that configuration can be updated on subsequent instantiations."""
        uid_manager = UniqueIDManager(separator="p", count_width=4)
        uid = uid_manager.next("test")
        self.assertEqual(uid, "testp0001")
        
        # Update the configuration.
        uid_manager = UniqueIDManager(separator="-", count_width=2)
        uid = uid_manager.next("test")
        self.assertEqual(uid, "test-02")

    def test_configurabilty(self):
        """Check that separator and count_width can be configured."""
        UniqueIDManager.reset()
        uid_manager = UniqueIDManager(separator="@", count_width=4)
        uid = uid_manager.next("PreFix")
        self.assertEqual(uid, "PreFix@0001")

    def test_counter_reset(self):
        """Ensure counters reset after the UniqueIDManager instance is reset."""
        self.uid_manager.next("prefix")
        UniqueIDManager.reset()
        new_uid_manager = UniqueIDManager()
        uid = new_uid_manager.next("prefix")
        self.assertEqual(uid, "prefix-1")

    def test_prefix_isolation(self):
        """Ensure counters for different prefixes do not overlap."""
        self.uid_manager.next("prefixA")
        uid = self.uid_manager.next("prefixB")
        self.assertEqual(uid, "prefixB-001")

    def test_reset(self):
        """Verify instances before and after reset are different."""
        uid_manager = UniqueIDManager()
        UniqueIDManager.reset()
        new_uid_manager = UniqueIDManager()
        self.assertIsNot(uid_manager, new_uid_manager)

    def test_boundary(self):
        """Test boundary condition for unique ID generation."""
        for _ in range(999):
            self.uid_manager.next("prefix")
        uid = self.uid_manager.next("prefix")
        self.assertEqual(uid, "prefix-1000")

    def test_invalid_separator(self):
        with self.assertRaises(C5decError):
            UniqueIDManager(separator='invalid')  # Ex: a separator longer than one character

    def test_negative_count_width(self):
        with self.assertRaises(C5decError):
            UniqueIDManager(count_width=-1)

    def test_non_integer_count_width(self):
        with self.assertRaises(C5decError):
            UniqueIDManager(count_width="a")

    def test_maximum_count_width(self):
        # This isn't a true edge case since there isn't a defined max width.
        # However, it tests a large count width for demonstrative purposes.
        uid_manager = UniqueIDManager(count_width=10)
        uid = uid_manager.next("prefix")
        self.assertEqual(uid, "prefix-0000000001")

    def test_minimum_count_width(self):
        uid_manager = UniqueIDManager(count_width=1)
        uid = uid_manager.next("prefix")
        self.assertEqual(uid, "prefix-1")

    def tearDown(self):
        """Clean up after each test by resetting the UniqueIDManager instance."""
        UniqueIDManager.reset()

if __name__ == '__main__':
    unittest.main()


