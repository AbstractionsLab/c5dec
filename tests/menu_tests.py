from c5dec.frontend.tui.foundation.menu import Menu
import unittest


class MenuTest(unittest.TestCase):
    def test_add_function(self):
        a.add_function("f1", test_function)
        self.assertTrue("f1" in a.functions.keys())
        self.assertTrue(test_function in a.functions.values())

    def test_add_menu(self):
        a.add_menu("A")
        self.assertTrue("A" in a.submenus.keys())
        self.assertTrue(isinstance(a.submenus["A"], Menu))
        self.assertEqual(a.submenus["A"].name, "A")

    def test_get_submenu(self):
        self.assertEqual(
            a.get_submenu("A"), 
            list(a.submenus.values())[0]
            )
        self.assertTrue(isinstance(a.get_submenu("A"), Menu))

    def test_get_nested_submenu(self):
        a.add_menu("B")
        a.get_submenu("B").add_menu("S1")
        self.assertEqual(
            a.get_nested_submenu(["B", "S1"]).name, 
            list(a.get_submenu("B").submenus.values())[-1].name
            )

    def test_get_path(self):
        a.add_menu("P1")
        a.get_submenu("P1").add_menu("P2")
        a.get_nested_submenu(["P1","P2"]).add_menu("P3")
        self.assertEqual(
            a.get_nested_submenu(["P1", "P2", "P3"]).get_path(), 
            ["main","P1", "P2"]
            )

    def test_get_all_submenus(self):
        a.add_menu("B")
        a.get_submenu("B").add_menu("C")
        self.assertEqual(
            [i.name for i in a.get_all_submenus()],
            ["A", "B", "C"]
            )


def test_function():
    pass

a = Menu("main")

if __name__ == "__main__":
    unittest.main()