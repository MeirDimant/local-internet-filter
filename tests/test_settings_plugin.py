from plugins.settings_plugin import SettingsPlugin
import unittest
from unittest.mock import Mock, patch
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestSettingsPlugin(unittest.TestCase):

    def setUp(self):
        # The singleton instance of SettingsPlugin
        self.plugin = SettingsPlugin()
        # A mock for IFlow
        self.mock_flow = Mock()

    def test_onRequest_valid_host(self):
        # Setup the mock to simulate a request to 'settings.it'
        self.mock_flow.get_host.return_value = 'settings.it'
        # Mock the get_request method to return a request object with path set to 'index.html'
        self.mock_flow.get_request.return_value.path = 'index.html'

        with patch.object(self.plugin, 'serve_files') as mock_serve_files:
            self.plugin.on_request(self.mock_flow)
            mock_serve_files.assert_called_once_with(
                self.mock_flow, 'index.html')

    def test_serve_files_existing_file(self):
        # Mock os.path.exists to return True for existing file
        with patch('os.path.exists', return_value=True), \
                patch('builtins.open', unittest.mock.mock_open(read_data='data')), \
                patch('os.path.join', return_value="path/to/an/existing/file"):
            self.plugin.serve_files(self.mock_flow, 'index.html')
            # Check response was made with correct status and content-type
            self.mock_flow.make_response.assert_called_once_with(
                200, 'data', {'Content-Type': 'text/html'})

    def test_serve_files_non_existing_file(self):
        # Setup non-existing file scenario
        self.mock_flow.make_response.reset_mock()
        with patch('os.path.exists', return_value=False):
            self.plugin.serve_files(self.mock_flow, 'nonexistent.html')
            self.mock_flow.make_response.assert_called_once_with(
                404, b"File not found!", {"Content-Type": "text/plain"})


# This allows running the tests from the command line
if __name__ == '__main__':
    unittest.main()
