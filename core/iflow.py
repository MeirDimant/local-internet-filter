from abc import ABC


class IFlow(ABC):
    def __init__(self):
        pass

    def get_content(self) -> str:
        pass

    def set_content(self) -> None:
        pass

    def get_request(self) -> object:
        pass

    def make_response(self, status, data, content_type) -> None:
        pass

    def get_cookie(self, key: str) -> str:
        pass

    def set_cookie(self, key: str, value: str) -> None:
        pass