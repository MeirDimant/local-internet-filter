from core.mitm_flow import MitmFlow
from manager import Manager
from plugins.plugins_management import PluginsManagement
import debugpy

# Setting mitmproxy to listen to debug connection
debugpy.listen(("127.0.0.1", 5678))
print("Waiting for debugger attach")
debugpy.wait_for_client()

# Initialize the plugin management
plugin_management = PluginsManagement()
# Initialize and setting the plugin instances in the plugin management
plugin_management.set_plugins_instances()


class Runner():

    def request(self, flow):
        # Create a MitmFlow instance with the mitmproxy flow object
        self.mitm_flow = MitmFlow(flow)
        # Initialize the Manager with request plugins and the current MitmFlow
        self.manager = Manager(
            plugin_management.request_plugins_instances, self.mitm_flow)
        self.manager.on_request()

    def response(self, flow):
        self.mitm_flow = MitmFlow(flow)
        self.manager = Manager(
            plugin_management.response_plugins_instances, self.mitm_flow)
        self.manager.on_response()


# Add an instance of Runner to the mitmproxy addons list
addons = [Runner()]
