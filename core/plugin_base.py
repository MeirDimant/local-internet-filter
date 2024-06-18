from abc import ABC, abstractmethod
from core.singleton_pattern import SingletonABCMeta
from core.iflow import IFlow


class PluginBase(metaclass=SingletonABCMeta):
    @abstractmethod
    def title() -> str:
        """Return the title of the plugin."""
        pass

    def onRequest(self, flow: IFlow) -> bool:
        """Process the request. Return False to stop further processing."""
        pass

    def onResponce(self, flow: IFlow) -> bool:
        """Process the response. Return False to stop further processing."""
        pass
