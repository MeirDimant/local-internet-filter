from abc import ABC, abstractmethod
from core.singleton_pattern import SingletonABCMeta
from core.iflow import IFlow


class PluginBase(metaclass=SingletonABCMeta):
    @abstractmethod
    def title() -> str:
        """Return the title of the plugin."""
        pass

    def on_request(self, flow: IFlow) -> bool:
        """Process the request. Return False to stop further processing."""
        pass

    def on_responce(self, flow: IFlow) -> bool:
        """Process the response. Return False to stop further processing."""
        pass
