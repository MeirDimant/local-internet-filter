import json
import os
from .auth_plugin import AuthPlugin
from core.iflow import IFlow
from core.plugin_base import PluginBase

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT = "text/plain"


class SettingsPlugin(PluginBase):

    def __init__(self) -> None:
        self.auth = AuthPlugin()

    def title(self):
        return 'Settings'

    def serve_files(self, flow: IFlow, path: str):
        root = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'assets/settings_ui/build')
        file_path = os.path.join(root, path)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            ext = os.path.splitext(path)[1]
            types = {'.html': 'text/html',
                     '.js': 'application/javascript', '.css': 'text/css'}
            flow.make_response(
                200, content, {"Content-Type": types.get(ext, 'application/octet-stream')})
        else:
            flow.make_response(404, b"File not found!", {
                "Content-Type": "text/plain"})

    def onRequest(self, flow: IFlow) -> bool:
        host = flow.get_host()

        if host == "settings.it":
            self.serve_files(
                flow, flow.get_request().path.lstrip("/") or "index.html")

        return True
