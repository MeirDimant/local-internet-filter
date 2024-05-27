import json
import re
from core.iflow import IFlow
from core.plugin_base import PluginBase
from typing import Dict, Any
from contenttype import ContentType

from dal_db import DalDB

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT = "text/plain"


class FilterContent(PluginBase):
    def __init__(self) -> None:
        self.db = DalDB()
        result = self.db.fetch_all('contents')
        self.contents = result if result is not None else []

    def title(self) -> str:
        return "Filter Content"

    def handle_request(self, method: str, flow: Any):
        """Dispatch request based on HTTP method."""
        if method == "GET":
            self.handle_get(flow)
        elif method == "POST":
            self.handle_post(flow)
        elif method == "PUT":
            self.handle_put(flow)
        elif method == "DELETE":
            self.handle_delete(flow)

    def handle_get(self, flow: Any):
        """Return list of all content objects."""
        response_content = json.dumps(self.contents)
        flow.make_response(HTTP_OK, response_content, {
                           "Content-Type": CONTENT_TYPE_JSON})

    def handle_post(self, flow: Any):
        """Create a new content object."""
        try:
            content_data = json.loads(flow.get_request().content.decode())

            domain_name = content_data.get('domain_name', '').strip()
            content = content_data.get('content', '').strip()

            if not domain_name or not content:
                flow.make_response(HTTP_BAD_REQUEST, "Domain name cannot be empty and Content must contain regular expression patterns", {
                                   "Content-Type": CONTENT_TYPE_TEXT})
                return

            existing_contents = self.db.search(
                'contents', 'domain_name', domain_name)

            if existing_contents:
                existing_content = existing_contents[0]
                content_list = existing_content['content']

                if content not in content_list:
                    content_list.append(content)
                    self.db.update(
                        'contents', {'content': content_list}, 'domain_name', domain_name)
            else:
                self.db.insert(
                    'contents', {'domain_name': domain_name, 'content': [content]})

            result = self.db.fetch_all('contents')
            self.contents = result
            flow.make_response(HTTP_OK, "Content added successfully", {
                "Content-Type": CONTENT_TYPE_TEXT})

        except Exception as e:
            print(e)
            flow.make_response(HTTP_BAD_REQUEST, "Something went wrong", {
                               "Content-Type": CONTENT_TYPE_TEXT})

    def handle_delete(self, flow: Any):
        """Delete a content object."""
        try:
            content_data = json.loads(flow.get_request().content.decode())
            domain_name = content_data.get('domain_name')
            content_to_delete = content_data.get('content')
            for i, content in enumerate(self.contents):
                if content['domain_name'] == domain_name:
                    if content_to_delete in content['content']:
                        content['content'].remove(content_to_delete)
                        if len(content['content']) == 0:
                            self.db.remove(
                                "contents", "domain_name", domain_name)
                        else:
                            self.db.update(
                                'contents', {'content': content['content']}, 'domain_name', domain_name)
                    result = self.db.fetch_all('contents')
                    self.contents = result if result is not None else []
                    print("delete:")
                    print(self.contents)
                    print("\n\n\n")
                    flow.make_response(HTTP_OK, "Content deleted successfully", {
                                       "Content-Type": CONTENT_TYPE_TEXT})
                    return
            flow.make_response(HTTP_BAD_REQUEST, "Content not found", {
                               "Content-Type": CONTENT_TYPE_TEXT})
        except:
            flow.make_response(HTTP_BAD_REQUEST, "Invalid format", {
                               "Content-Type": CONTENT_TYPE_TEXT})

    def onRequest(self, flow: IFlow) -> bool:
        host = flow.get_host()
        normalized_host = host[len("www."):] if host.startswith(
            "www.") else host

        if normalized_host == "settings.it":
            req = flow.get_request()
            if req.path.endswith("/api/contents"):
                self.handle_request(req.method, flow)

            return True

    def onResponse(self, flow: IFlow) -> bool:
        host = flow.get_host()
        normalized_host = host[len("www."):] if host.startswith(
            "www.") else host

        for content_entry in self.contents:
            if content_entry['domain_name'] in normalized_host:
                response_headers = flow.get_response().headers
                content_type_header = response_headers.get('Content-Type', '')

                if content_type_header:
                    content_type = ContentType.parse(content_type_header)

                    if content_type.type not in content_entry['content']:
                        flow.kill()
                        return False

                    break
        return True
