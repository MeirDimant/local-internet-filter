from abc import ABC, abstractmethod
from core.singleton_pattern import SingletonABCMeta
from core.iflow import IFlow


class PluginBase(metaclass=SingletonABCMeta):
    @abstractmethod
    def title() -> str:
        pass

    def onRequest(self, flow: IFlow) -> bool:
        pass

    def onResponce(self, flow: IFlow) -> bool:
        pass
