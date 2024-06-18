from plugins.white_list_plugin import WhiteListPlugin
import json
import unittest
from unittest.mock import Mock, patch
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
CONTENT_TYPE_TEXT = "text/plain"
CONTENT_TYPE_JSON = "application/json"


class TestWhiteListPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = WhiteListPlugin()
        self.mock_flow = Mock()
        self.plugin.db = Mock()
        self.plugin.approved_domains = ["example.com", "test.com"]

    ### tests onRequest function ###
    def test_on_request_with_approved_host_and_specific_path(self):
        self.mock_flow.get_host.return_value = "www.settings.it"
        self.mock_flow.get_request.return_value.path = "/api/approved-domains"

        # Mocking handle_request to chek if called
        self.plugin.handle_request = Mock()

        result = self.plugin.on_request(self.mock_flow)

        self.plugin.handle_request.assert_called_once()
        self.assertTrue(
            result, "onRequest should return True when host and path are correct")

    def test_on_request_with_unapproved_host_name(self):
        self.mock_flow.get_host.return_value = "www.settings.it"
        self.mock_flow.get_request.return_value.path = "/not/interesting/path"

        self.plugin.handle_request = Mock()

        result = self.plugin.on_request(self.mock_flow)

        self.plugin.handle_request.assert_not_called()
        self.assertTrue(
            result, "onRequest should still return True for handled host regardless of path")

    def test_on_request_with_unapproved_domain(self):
        self.mock_flow.get_host.return_value = "unapproved.domain.com"
        self.plugin.approved_domains = ["this.is.approved.domain"]

        result = self.plugin.on_request(self.mock_flow)

        self.mock_flow.kill.assert_called_once()
        self.assertFalse(
            result, "onRequest should return False and kill the flow for unapproved domains")

    ### test for handle_get method ###
    def test_handle_get(self):
        self.plugin.handle_get(self.mock_flow)
        response_content = json.dumps(self.plugin.approved_domains)

        self.mock_flow.make_response.assert_called_once_with(
            HTTP_OK, response_content, {"Content-Type": CONTENT_TYPE_JSON}
        )

    ### tests for handle_post method ###
    def test_handle_post_with_missing_domain(self):
        self.mock_flow.get_request.return_value.content.decode.return_value = json.dumps({
        })

        self.plugin.handle_post(self.mock_flow)

        self.mock_flow.make_response.assert_called_once_with(
            HTTP_BAD_REQUEST, "Bad Request: Missing domain", {
                "Content-Type": CONTENT_TYPE_TEXT}
        )

    def test_handle_post_with_existing_domain(self):
        self.mock_flow.get_request.return_value.content.decode.return_value = json.dumps({
                                                                                         "domain": "example.com"})

        self.plugin.handle_post(self.mock_flow)

        self.mock_flow.make_response.assert_called_once_with(
            HTTP_BAD_REQUEST, "Domain already exists", {
                "Content-Type": CONTENT_TYPE_TEXT}
        )

    def test_handle_post_with_new_domain(self):
        new_domain = "newdomain.com"
        self.mock_flow.get_request.return_value.content.decode.return_value = json.dumps({
                                                                                         "domain": new_domain})
        self.plugin.db.fetch_all.return_value = [
            {"domain": d} for d in self.plugin.approved_domains + [new_domain]]

        self.plugin.handle_post(self.mock_flow)

        self.plugin.db.insert.assert_called_once_with(
            'approved_domains', {'domain': new_domain})
        self.mock_flow.make_response.assert_called_once_with(
            HTTP_OK, "Domain added successfully", {
                "Content-Type": CONTENT_TYPE_TEXT}
        )
        self.assertIn(new_domain, self.plugin.approved_domains)

    ### tests for handle_delete method ###
    def test_handle_delete_with_existing_domain(self):
        domain_to_remove = "example.com"
        self.mock_flow.get_request.return_value.content.decode.return_value = json.dumps(
            {"domain": domain_to_remove})
        self.plugin.db.fetch_all.return_value = [
            {"domain": d} for d in ["test.com"]]

        self.plugin.handle_delete(self.mock_flow)

        self.plugin.db.remove.assert_called_once_with(
            'approved_domains', 'domain', domain_to_remove)
        self.mock_flow.make_response.assert_called_once_with(
            HTTP_OK, json.dumps(["test.com"]), {
                "Content-Type": CONTENT_TYPE_JSON}
        )
        self.assertNotIn(domain_to_remove, self.plugin.approved_domains)
        self.assertIn("test.com", self.plugin.approved_domains)

    def test_handle_delete_with_non_existing_domain(self):
        domain_to_remove = "nonexistent.com"
        self.mock_flow.get_request.return_value.content.decode.return_value = json.dumps(
            {"domain": domain_to_remove})

        self.plugin.handle_delete(self.mock_flow)

        self.plugin.db.remove.assert_not_called()
        self.mock_flow.make_response.assert_called_once_with(
            HTTP_OK, json.dumps(self.plugin.approved_domains), {
                "Content-Type": CONTENT_TYPE_JSON}
        )


if __name__ == '__main__':
    unittest.main()
