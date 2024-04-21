from core.mitm_flow import MitmFlow
from manager import Manager
from plugins.plugins_management import PluginsManagement
import debugpy

debugpy.listen(("127.0.0.1", 5678))
print("Waiting for debugger attach")
debugpy.wait_for_client()

plugin_management = PluginsManagement()
plugin_management.set_plugins_instances()


class Runner():

    def request(self, flow):
        self.mitm_flow = MitmFlow(flow)
        self.manager = Manager(
            plugin_management.request_plugins_instances, self.mitm_flow)
        self.manager.onRequest()

    def response(self, flow):
        self.mitm_flow = MitmFlow(flow)
        self.manager = Manager(
            plugin_management.response_plugins_instances, self.mitm_flow)
        self.manager.onResponse()


addons = [Runner()]
