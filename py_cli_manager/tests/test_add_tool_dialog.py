import unittest

from gui.add_tool_dialog import make_tool_id


class TestMakeToolId(unittest.TestCase):
    def test_make_tool_id_scoped(self):
        self.assertEqual(make_tool_id("@org/pkg"), "@org/pkg")

    def test_make_tool_id_unscoped(self):
        self.assertEqual(make_tool_id("foo"), "foo")


if __name__ == "__main__":
    unittest.main()
