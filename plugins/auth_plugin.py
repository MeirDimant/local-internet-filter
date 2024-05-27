import json
from core.iflow import IFlow
from core.plugin_base import PluginBase
import random
import string
import hashlib

from dal_db import DalDB


def random_string(length: int):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


session = random_string(20)


class AuthPlugin(PluginBase):
    def __init__(self) -> None:
        self.db = DalDB()

    def title(self):
        return 'Auth'

    def user_exist(self, flow: IFlow) -> None:
        users = self.db.fetch_all('users')
        print(users)
        print("\n\n\n")
        if users:
            flow.make_response(200, json.dumps({"user_exist": True}), {
                               "Content-Type": "application/json"})
        else:
            flow.make_response(403, json.dumps({"user_exist": False}), {
                               "Content-Type": "application/json"})

    def is_logged_in(self, flow: IFlow):
        result = flow.get_cookie('session') == session
        return result

    def register(self, flow: IFlow, un: str, pw: str):
        hashed_pw = hashlib.sha256(pw.encode()).hexdigest()
        password_in_db = self.db.search('users', 'password', hashed_pw)

        if password_in_db is not None:
            response_content = json.dumps({'message': 'Try another password'})
            flow.make_response(
                403, response_content, {"Content-Type": "application/json"})

        self.db.insert('users', {'user-name': un, 'password': hashed_pw})
        response_content = json.dumps({'message': 'You have registerd.'})
        flow.make_response(
            200, response_content, {"Content-Type": "application/json"})

    def log_in(self, flow: IFlow, un: str, pw: str):
        user = self.db.search('users', 'user-name', un)
        if user is None:
            response_content = json.dumps({'message': 'Invalid cridentials'})
            flow.make_response(
                403, response_content, {"Content-Type": "application/json"})

        stored_hashed_password = user[0]['password']
        hashed_input_password = hashlib.sha256(pw.encode()).hexdigest()
        
        if hashed_input_password == stored_hashed_password:
            response_content = json.dumps({'message': 'You are logged in.'})
            flow.make_response_with_cookie(
                200, response_content, {"Content-Type": "application/json"}, 'session', session)
        else:
            esponse_content = json.dumps({'message': 'Invalid cridentials.'})
            flow.make_response(
                403, esponse_content, {"Content-Type": "application/json"})

    def onRequest(self, flow: IFlow) -> bool:
        host = flow.get_host()
        if host == "settings.it":
            req = flow.get_request()
            if req.path.endswith("api/auth/check"):
                if self.is_logged_in(flow):
                    response_content = json.dumps(
                        {'authenticated': True, 'message': 'user is authenticated'})
                    flow.make_response(200, response_content, {
                                       "Content-Type": "application/json"})
                else:
                    response_content = json.dumps(
                        {'authenticated': False, 'message': 'user is Not authenticated'})
                    flow.make_response(403, response_content, {
                                       "Content-Type": "application/json"})
            elif req.path.endswith("api/auth/login"):
                un = json.loads(req.content.decode()).get('username')
                pw = json.loads(req.content.decode()).get('password')
                self.log_in(flow, un, pw)
            elif req.path.endswith("api/auth/register"):
                un = json.loads(req.content.decode()).get('username')
                pw = json.loads(req.content.decode()).get('password')
                self.register(flow, un, pw)
            elif req.path.endswith("api/auth/any"):
                self.user_exist(flow)

        return True
