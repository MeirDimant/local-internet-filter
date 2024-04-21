import unittest
from unittest.mock import patch, MagicMock
from plugins.settings_plugin import SettingsPlugin

class TestSettingsPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = SettingsPlugin()

    @patch('os.path.exists')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=b'content')
    def test_serve_files_existing(self, mock_open, mock_join, mock_exists):
        # Setup
        mock_exists.return_value = True
        mock_join.side_effect = lambda *args: '/'.join(args)
        flow = MagicMock()
        flow.make_response = MagicMock()

        # Action
        self.plugin.serve_files(flow, 'index.html')

        # Assert
        flow.make_response.assert_called_with(200, b'content', {'Content-Type': 'text/html'})

    @patch('os.path.exists')
    @patch('os.path.join')
    def test_serve_files_non_existing(self, mock_join, mock_exists):
        # Setup
        mock_exists.return_value = False
        mock_join.side_effect = lambda *args: '/'.join(args)
        flow = MagicMock()
        flow.make_response = MagicMock()

        # Action
        self.plugin.serve_files(flow, 'nonexistent.html')

        # Assert
        flow.make_response.assert_called_with(404, b"File not found!", {"Content-Type": "text/plain"})

    def test_onRequest_valid_host(self):
        # Setup
        flow = MagicMock()
        flow.get_host.return_value = "settings.it"
        flow.get_request.return_value = MagicMock(path="/index.html")
        self.plugin.serve_files = MagicMock()

        # Action
        result = self.plugin.onRequest(flow)

        # Assert
        self.plugin.serve_files.assert_called_with(flow, "index.html")
        self.assertTrue(result)

    def test_onRequest_invalid_host(self):
        # Setup
        flow = MagicMock()
        flow.get_host.return_value = "notsettings.it"

        # Action
        result = self.plugin.onRequest(flow)

        # Assert
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
