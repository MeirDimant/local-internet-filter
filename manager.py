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

    def onRequest(self):
        for plugin in self.plugins:
            if hasattr(plugin, 'onRequest'):
                flag = plugin.onRequest(self.flow)
                if (not flag):
                    break

    def onResponse(self):
        for plugin in self.plugins:
            if hasattr(plugin, 'onResponse'):
                flag = plugin.onResponse(self.flow)
                if (not flag):
                    break
