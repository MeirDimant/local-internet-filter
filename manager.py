from typing import List
from core.iflow import IFlow
from core.plugin_base import PluginBase


class Manager():

    def __init__(self,  plugins: List[PluginBase], flow: IFlow):
        self.plugins = plugins
        self.flow = flow

        print('Starting with the following plugins')
        for plugin in self.plugins:
            print(plugin.title())

    def on_request(self):
        """
        Execute the onRequest method for each plugin in the list.
        Stops execution if a plugin's onRequest method returns False.
        """
        for plugin in self.plugins:
            if hasattr(plugin, 'on_request'):
                flag = plugin.on_request(self.flow)
                if (not flag):
                    break

    def on_response(self):
        """
        Execute the onResponse method for each plugin in the list.
        Stops execution if a plugin's onResponse method returns False.
        """
        for plugin in self.plugins:
            if hasattr(plugin, 'on_response'):
                flag = plugin.on_response(self.flow)
                if (not flag):
                    break
