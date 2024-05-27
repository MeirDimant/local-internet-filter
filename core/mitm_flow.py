from core.iflow import IFlow
from mitmproxy import http


class MitmFlow(IFlow):
    def __init__(self, flow_of_mitmproxy):
        """
        Initialize MitmFlow with a mitmproxy flow object.
        
        :param flow_of_mitmproxy: The flow object from mitmproxy.
        """
        self.flow_of_mitmproxy = flow_of_mitmproxy

    def kill(self, status=403, txt="Unauthorized request!", ct="text/plain"):
        """
        Kill the request by setting a custom response.
        
        :param status: HTTP status code, defaults to 403.
        :param txt: Response text, defaults to "Unauthorized request!".
        :param ct: Content type, defaults to "text/plain".
        """
        self.flow_of_mitmproxy.response = http.Response.make(
            status, txt, {"Content-Type": ct})

    def get_host(self):
        """Get the host from the request."""
        return self.flow_of_mitmproxy.request.pretty_host

    def get_request(self):
        """Get the request object from the flow."""
        return self.flow_of_mitmproxy.request

    def get_response(self):
        """Get the response object from the flow."""
        return self.flow_of_mitmproxy.response

    def make_response(self, status, data, content_type):
        """
        Create a response with the given status, data, and content type.
        
        :param status: HTTP status code.
        :param data: Response data.
        :param content_type: Content type of the response.
        """
        self.flow_of_mitmproxy.response = http.Response.make(
            status, data, content_type)

    def get_cookie(self, key: str) -> str:
        """Get a cookie value from the request."""
        cookie_value = self.flow_of_mitmproxy.request.cookies.get(key, None)
        return cookie_value

    def make_response_with_cookie(self, status, data, content_type, key: str, value: str) -> None:
        """
        Create a response with a set cookie.
        
        :param status: HTTP status code.
        :param data: Response data.
        :param content_type: Content type of the response.
        :param key: Cookie key.
        :param value: Cookie value.
        """
        res = http.Response.make(status, data, content_type)
        res.headers["set-cookie"] = key + "=" + value

        self.flow_of_mitmproxy.response = res
