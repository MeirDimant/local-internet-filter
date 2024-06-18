import json
from core.iflow import IFlow
from core.plugin_base import PluginBase
from dal_db import DalDB

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT = "text/plain"


# This plugin manages the approved domains list
# also, this plugin responsible for blocking unapproved domains
class WhiteListPlugin(PluginBase):
    def __init__(self) -> None:
        """
        Initialize the WhiteListPlugin with a database connection
        and fetch the list of approved domains.
        """
        self.db = DalDB()
        domains_list = self.db.fetch_all('approved_domains')
        self.approved_domains = [item['domain'] for item in domains_list]

    def title(self) -> str:
        return "White List"

    def handle_request(self, method: str, flow: IFlow):
        """Handle HTTP requests based on the method type."""
        if method == "GET":
            self.handle_get(flow)
        elif method == "POST":
            self.handle_post(flow)
        elif method == "DELETE":
            self.handle_delete(flow)

    def handle_get(self, flow):
        """Handles GET requests. Pass to the user the approved domain list"""
        response_content = json.dumps(self.approved_domains)
        flow.make_response(HTTP_OK, response_content, {
                           "Content-Type": CONTENT_TYPE_JSON})

    def handle_post(self, flow):
        """
        Handles POST requests.
        Adding a new approved domain to the list
        """
        new_domain = json.loads(
            flow.get_request().content.decode()).get('domain')

        if new_domain is None:
            flow.make_response(HTTP_BAD_REQUEST, "Bad Request: Missing domain", {
                               "Content-Type": CONTENT_TYPE_TEXT})
            return

        if new_domain in self.approved_domains:
            flow.make_response(HTTP_BAD_REQUEST, "Domain already exists", {
                               "Content-Type": CONTENT_TYPE_TEXT})
            return

        self.db.insert('approved_domains', {'domain': new_domain})
        domains_list = self.db.fetch_all('approved_domains')
        self.approved_domains = [item['domain'] for item in domains_list]
        flow.make_response(HTTP_OK, "Domain added successfully", {
                           "Content-Type": CONTENT_TYPE_TEXT})

    def handle_delete(self, flow):
        """
        Handles DELETE requests.
        Deletes from the list the approved domain sent by the user 
        """
        domain_to_remove = json.loads(
            flow.get_request().content.decode()).get('domain')

        if domain_to_remove in self.approved_domains:
            self.db.remove('approved_domains', 'domain', domain_to_remove)
            domains_list = self.db.fetch_all('approved_domains')
            self.approved_domains = [item['domain'] for item in domains_list]

        response_content = json.dumps(self.approved_domains)
        flow.make_response(HTTP_OK, response_content, {
                           "Content-Type": CONTENT_TYPE_JSON})

    def on_request(self, flow: IFlow) -> bool:
        """Handle incoming requests and manage access based on approved domains."""
        host = flow.get_host()
        normalized_host = host[len("www."):] if host.startswith(
            "www.") else host

        # Redirect requests to "settings.it/api/approved-domains" to the CRUD operations for the approved domains list
        if normalized_host == "settings.it":
            req = flow.get_request()
            if req.path.endswith("/api/approved-domains"):
                self.handle_request(req.method, flow)

            return True

        # Check if the host is in the approved domains list
        if not any(approved_domain in normalized_host for approved_domain in self.approved_domains):
            flow.kill()  # Kill the flow if the host is not approved
            return False
