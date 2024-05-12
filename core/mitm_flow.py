from core.iflow import IFlow
from mitmproxy import http


class MitmFlow(IFlow):
    def __init__(self, flow_of_mitmproxy):
        self.flow_of_mitmproxy = flow_of_mitmproxy

    def kill(self, status=403, txt="Unauthorized request!", ct="text/plain"):
        self.flow_of_mitmproxy.response = http.Response.make(
            status, txt, {"Content-Type": ct})

    def get_host(self):
        return self.flow_of_mitmproxy.request.pretty_host

    def get_request(self):
        return self.flow_of_mitmproxy.request

    def get_response(self):
        return self.flow_of_mitmproxy.response

    def make_response(self, status, data, content_type):
        self.flow_of_mitmproxy.response = http.Response.make(
            status, data, content_type)

    def get_cookie(self, key: str) -> str:
        cookie_value = self.flow_of_mitmproxy.request.cookies.get(key, None)
        return cookie_value

    def make_response_with_cookie(self, status, data, content_type, key: str, value: str) -> None:
        res = http.Response.make(status, data, content_type)
        res.headers["set-cookie"] = key + "=" + value

        self.flow_of_mitmproxy.response = res
