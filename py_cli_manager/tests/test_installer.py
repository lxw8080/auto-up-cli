import unittest
from unittest import mock

from core.installer import install_tool
from core.detector import ToolInfo, InstallType


class TestInstaller(unittest.TestCase):
    def test_install_tool_npm_fallback_uses_alt(self):
        tool = ToolInfo(id="t", name="t", package="pkg", category="c", install_type=InstallType.NPM)

        with mock.patch("core.installer.install_package_npm", return_value=(False, "fail")) as mock_npm, \
             mock.patch("core.installer.get_alt_install_command", return_value="echo alt") as mock_alt, \
             mock.patch("core.installer._run_install_command", return_value=(True, "ok")) as mock_run:
            success, _ = install_tool(tool)

            self.assertTrue(success)
            mock_npm.assert_called_once()
            mock_alt.assert_called_once()
            mock_run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
