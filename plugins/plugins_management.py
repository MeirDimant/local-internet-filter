import importlib
import json
import os
import re
from werkzeug.utils import secure_filename
from core.iflow import IFlow
from core.plugin_base import PluginBase
from dal_db import DalDB

# HTTP status codes and content types
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT = "text/plain"


def normalize_name(db_name):
    """
    Convert the plugin name from the DB format ("Plugin Name") to a filename ("plugin_name")
    and class name ("PluginName").
    """
    file_name = db_name.lower().replace(" ", "_")
    class_name = ''.join(word.title() for word in db_name.split())
    return file_name, class_name


def load_plugins(plugin_names):
    """
    Dynamically load and instantiate plugins based on a plugins list.
    """
    plugins = []
    for db_name in plugin_names:
        file_name, class_name = normalize_name(db_name)
        module = importlib.import_module(f'plugins.{file_name}')
        plugin_class = getattr(module, class_name)
        plugins.append(plugin_class())
    return plugins

# This plugin manages two types of lists the lists of the plugins names and the lists of the plugins instances
# Both types of lists are divided into request plugins and response plugins
# The request plugins are plugins that run on the user's request and the response when the user get a response
# The plugins instances are initiated based on the lists of the plugin names and in the same order as they
# are in the lists


class PluginsManagement(PluginBase):

    def __init__(self) -> None:
        """
        Initialize PluginsManagement with database access and plugin lists.
        """
        self.db = DalDB()  # Initialize database access
        # Fetch all plugins names from the database
        self.plugins_list = self.db.fetch_all('plugins')

        self.request_plugins_list = []
        self.response_plugins_list = []

        self.request_plugins_instances = []
        self.response_plugins_instances = []

        # If no plugins are in the database, populate with all the existing plugins in the directory
        if not self.plugins_list:
            self.initialize_plugins_from_directory()

        # Fetch the plugins lists form the DB and assign them to request_plugins_list and response_plugins_list
        self.fetch_plugins_list()

    def title(self) -> str:
        return "Plugins Management"

    def initialize_plugins_from_directory(self):
        """
        Initialize plugins lists from the directory if there are no lists in the database.
        """
        plugins_dir = os.path.join(os.path.dirname(__file__))
        plugin_files = os.listdir(plugins_dir)
        plugins_list = [os.path.splitext(file)[0] for file in plugin_files if file.endswith(
            '.py') and not file.startswith('__init__')]

        formatted_plugins_list = [plugin.replace(
            '_', ' ').title() for plugin in plugins_list]

        self.db.insert(
            'plugins', {'request_plugins_list': formatted_plugins_list})
        self.db.insert(
            'plugins', {'response_plugins_list': formatted_plugins_list})

    def set_plugins_instances(self):
        """
        Load and set instances of request and response plugins.
        """
        self.request_plugins_instances = load_plugins(
            self.request_plugins_list)
        self.response_plugins_instances = load_plugins(
            self.response_plugins_list)

    def fetch_plugins_list(self):
        """
        Fetch the list of plugins from the database 
        and assign it to request_plugins_list and response_plugins_list.
        """
        self.plugins_list = self.db.fetch_all('plugins')

        for item in self.plugins_list:
            if 'request_plugins_list' in item:
                self.request_plugins_list = item['request_plugins_list']
            if 'response_plugins_list' in item:
                self.response_plugins_list = item['response_plugins_list']

    def update_and_refresh_plugins(self, new_request_plugins_list, new_response_plugins_list):
        """
        Update the plugin lists in the database and refresh the request_plugins_list and response_plugins_list.
        """
        self.db.update('plugins', {
            'request_plugins_list': new_request_plugins_list}, 'request_plugins_list', self.request_plugins_list)
        self.db.update('plugins', {'response_plugins_list': new_response_plugins_list},
                       'response_plugins_list', self.response_plugins_list)

        self.fetch_plugins_list()

    def _handle_request(self, method: str, flow: IFlow):
        if method == "GET":
            self._handle_get(flow)
        elif method == "POST":
            self._handle_post(flow)
        elif method == "PUT":
            self._handle_put(flow)
        elif method == "DELETE":
            self._handle_delete(flow)

    def _handle_get(self, flow):
        """Handles GET requests."""
        # returns to the user the plugins lists
        response_content = json.dumps(self.plugins_list)
        flow.make_response(HTTP_OK, response_content, {
                           "Content-Type": CONTENT_TYPE_JSON})

    def _handle_post(self, flow):
        """Handles POST requests with file upload.
        Adding new plugins."""
        # Decode the raw content of the request and extract the filename and its content using a regex pattern
        raw_data = flow.get_request().content.decode()
        pattern = r'filename="(.+\.py)"\s+Content-Type:\s+text/x-python\s+(.*?)\s+-----------------------------'
        match = re.search(pattern, raw_data, re.DOTALL)

        # if the file is valid, extract the filename and file content, save the file, and update the plugin lists
        if match:
            filename = match.group(1)
            file_content = match.group(2).strip()
            file_path = os.path.join(os.path.dirname(__file__), filename)

            # Write the extracted content to a file
            with open(file_path, 'w') as file:
                file.write(file_content)
                print(f"File saved as {filename}")

            # Create a plugin name from the filename
            plugin_name = filename[:-3].replace('_', ' ').title()

            # Update the request and response plugin lists with the new plugin
            new_request_plugins_list = self.request_plugins_list + \
                [plugin_name]
            new_response_plugins_list = self.response_plugins_list + \
                [plugin_name]

            # Update the lists in the database
            self.update_and_refresh_plugins(
                new_request_plugins_list, new_response_plugins_list)

            # Reload the instances to include the new plugin
            self.set_plugins_instances()

            response_content = "File uploaded successfully."
            flow.make_response(HTTP_OK, response_content, {
                "Content-Type": CONTENT_TYPE_TEXT})  # Send a success response
        else:
            # If no match is found, send an error response
            flow.make_response(HTTP_BAD_REQUEST, "Invalid file", {
                "Content-Type": CONTENT_TYPE_TEXT})

    def _handle_put(self, flow):
        """Handles PUT requests.
        Updating the plugins lists"""
        new_plugins_list = json.loads(
            flow.get_request().content.decode())

        request_plugins_list = new_plugins_list.get('request_plugins_list')
        response_plugins_list = new_plugins_list.get('response_plugins_list')

        self.update_and_refresh_plugins(
            request_plugins_list, response_plugins_list)

        self.set_plugins_instances()

        flow.make_response(HTTP_OK, "Plugins list updated successfully", {
                           "Content-Type": CONTENT_TYPE_TEXT})

    def _handle_delete(self, flow):
        """Handles DELETE requests to remove a plugin."""
        request_data = json.loads(flow.get_request().content.decode())
        plugin_name = request_data.get('plugin_name')

        # Format the filename base on the plugin name
        filename = plugin_name.replace(' ', '_').lower() + '.py'
        file_path = os.path.join(os.path.dirname(__file__), filename)

        # Check if file exists
        if not os.path.exists(file_path):
            flow.make_response(HTTP_BAD_REQUEST, "Plugin file does not exist", {
                               "Content-Type": CONTENT_TYPE_TEXT})
            return

        # Remove the plugin file
        os.remove(file_path)

        # Update plugin lists and database
        new_request_plugins_list = [
            plugin for plugin in self.request_plugins_list if plugin != plugin_name]
        new_response_plugins_list = [
            plugin for plugin in self.response_plugins_list if plugin != plugin_name]

        self.update_and_refresh_plugins(
            new_request_plugins_list, new_response_plugins_list)

        # Reload the instances to exclude the removed plugin
        self.set_plugins_instances()

        flow.make_response(HTTP_OK, f"Plugin '{plugin_name}' removed successfully.", {
                           "Content-Type": CONTENT_TYPE_TEXT})

    def on_request(self, flow: IFlow) -> bool:
        host = flow.get_host()
        normalized_host = host[len("www."):] if host.startswith(
            "www.") else host

        if normalized_host == "settings.it":
            req = flow.get_request()
            if req.path.endswith("/api/plugins"):
                self._handle_request(req.method, flow)

            return True
