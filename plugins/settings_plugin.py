import json
import os
from .auth_plugin import AuthPlugin
from core.iflow import IFlow
from core.plugin_base import PluginBase

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT = "text/plain"

def is_static_file(path):
    """Check if the requested path is for a static file."""
    static_extensions = ['.html', '.css', '.js', '.png', '.jpg', '.gif', '.woff', '.woff2', '.ttf', '.eot', '.json', '.ico']
    return any(path.endswith(ext) for ext in static_extensions)


class SettingsPlugin(PluginBase):

    def __init__(self) -> None:
        self.auth = AuthPlugin()

    def title(self):
        return 'Settings'

    def serve_files(self, flow: IFlow, path: str):
        """Serve static files"""

        # Determine the root directory for static files
        root = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'assets/settings_ui/build')
        file_path = os.path.join(root, path)

        # Check if the requested file exists and serve it
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            # Extract the file extension
            ext = os.path.splitext(path)[1]
            # Define a dictionary to map file extensions to their respective MIME types
            types = {'.html': 'text/html',
                     '.js': 'application/javascript', '.css': 'text/css'}
            flow.make_response(
                200, content, {"Content-Type": types.get(ext, 'application/octet-stream')})
        else:
            flow.make_response(404, b"File not found!", {
                "Content-Type": "text/plain"})

    def onRequest(self, flow: IFlow) -> bool:
        host = flow.get_host()
        path = flow.get_request().path

        # If the user trys to reach "setting.it" the plugin will return the static files of the UI
        if host == "settings.it":
            if path == "/" or is_static_file(path):
                self.serve_files(flow, path.lstrip("/") or "index.html")

        return True
