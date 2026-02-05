import unittest
from unittest import mock

from core import detector
from core.detector import ToolInfo, tool_requires_npm


class TestDetector(unittest.TestCase):
    def test_get_installed_version_prefers_version_command(self):
        tool = ToolInfo(
            id="t",
            name="t",
            package="pkg",
            category="c",
            version_command="tool --version",
        )
        with mock.patch("core.detector.get_installed_version_custom", return_value="1.2.3") as mock_custom, \
             mock.patch("core.detector.get_installed_version_npm", return_value="9.9.9") as mock_npm:
            result = detector.get_installed_version(tool)
            self.assertEqual(result, "1.2.3")
            mock_custom.assert_called_once()
            mock_npm.assert_not_called()

    def test_get_installed_version_fallback_to_npm(self):
        tool = ToolInfo(
            id="t",
            name="t",
            package="pkg",
            category="c",
            version_command="tool --version",
        )
        with mock.patch("core.detector.get_installed_version_custom", return_value=None) as mock_custom, \
             mock.patch("core.detector.get_installed_version_npm", return_value="1.0.0") as mock_npm:
            result = detector.get_installed_version(tool)
            self.assertEqual(result, "1.0.0")
            mock_custom.assert_called_once()
            mock_npm.assert_called_once()

    def test_split_command_handles_quotes(self):
        cmd = r'"C:\Program Files\Tool\tool.exe" --version'
        parts = detector._split_command(cmd)
        self.assertEqual(parts[0], r"C:\Program Files\Tool\tool.exe")
        self.assertIn("--version", parts)

    def test_tool_requires_npm(self):
        tool_no_package = ToolInfo(id="t1", name="t1", package="", category="c")
        self.assertFalse(tool_requires_npm(tool_no_package))

        tool_with_version_cmd = ToolInfo(
            id="t2", name="t2", package="pkg", category="c", version_command="tool --version"
        )
        self.assertFalse(tool_requires_npm(tool_with_version_cmd))

        tool_with_repo = ToolInfo(
            id="t3", name="t3", package="pkg", category="c", github_repo="org/repo"
        )
        self.assertFalse(tool_requires_npm(tool_with_repo))

        tool_requires = ToolInfo(id="t4", name="t4", package="pkg", category="c")
        self.assertTrue(tool_requires_npm(tool_requires))


if __name__ == "__main__":
    unittest.main()
