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
        """
        Initialize the agent with its command server location and poll interval.

        Args:
            command_server_ip (str): The IP address of the command server.
            command_server_port (int): The port of the command server.
            poll_interval (int): The time in seconds between polling commands.
        """
        self.id = uuid.uuid4()
        self.poll_interval = poll_interval
        self.timeout = poll_interval
        self.get_url = f"http://{command_server_ip}:{command_server_port}/api/pull"
        self.post_url = f"http://{command_server_ip}:{command_server_port}/api/result"
        self.session = requests.Session()

    def pull_commands(self) -> None:
        """
        Polls the command server for new commands. If new commands are found,
        process them and send the results back to the server.

        If the server does not respond within the poll interval, a timeout
        exception is raised and the agent attempts to poll again. If a
        connection error occurs, a connection error is raised and the agent
        attempts to poll again.
        """
        data = {"agent_id": str(self.id)}
        try:
            r = self.session.get(
                url=self.get_url, data=json.dumps(data), timeout=self.timeout
            )
            cmds = r.json()
            for cmd in cmds:
                print(f"cmd: {cmd}")
                response = self.handle_command(cmd)
                print(f"response: {response}")
                self.send_response(response=response)
        except requests.Timeout:
            print("poll response timed out")
        except requests.ConnectionError:
            print("Can't connect to server")

    def send_response(self, response):
        """
        Send response to CC server.

        This method sends the response, which is a dictionary, to the CC server.
        The response is sent as a POST request to the CC server. If the request
        fails for any reason, the method prints an error message.

        Args:
            response (dict): A dictionary containing the response to the command.
        """
        try:
            requests.post(url=self.post_url, data=json.dumps(response), headers={"Content-Type": "application/json"})
        except:
            print("Pushing result failed")

    def create_response(self, output, error, cmd) -> dict:
        """
        Create a response dictionary.

        Create a dictionary with the output and error of the command, and the
        id of the command that was sent to the agent.

        Args:
            output (str): The output of the command.
            error (str): The error of the command.
            cmd (dict): The command dictionary.

        Returns:
            dict: A dictionary with the response data.
        """
        return {"output": output, "error": error, "cmd_id": cmd["id"]}

    def handle_command(self, cmd) -> dict:
        """
        Processes a command dictionary and returns a response dictionary.

        This method extracts the command type and arguments from the command
        dictionary. It then dispatches the command for execution and creates
        a response based on the output and error from the execution.

        Args:
            cmd (dict): A dictionary containing the command details.

        Returns:
            dict: A dictionary containing the response data.
        """
        # Extract command type and arguments from the command
        cmd_type = cmd["cmd_type"]
        cmd_args = cmd["cmd_args"]
        
        # Dispatch the command and capture the output and error
        (output, error) = self.dispatch_command(cmd_type, cmd_args)
        
        # Create and return the response dictionary
        return self.create_response(output, error, cmd)

    @abstractmethod
    def list_directory_contents(self, path):
        """
        Lists contents of dir specified by the 'path' parameter.
        """
        pass

    def dispatch_command(self, type, args) -> tuple:
        """
        Dispatches a command to the appropriate method.

        This method takes a command type and argument, and calls the appropriate
        method to execute the command. If the command type is not recognized,
        the method returns a tuple with None and an error message.

        Args:
            type (str): The type of command to execute.
            args (str): The arguments for the command.

        Returns:
            tuple: A tuple with the output and error of the command.
        """
        if type == "ls":
            return self.list_directory_contents(json.loads(args)[0])
        else:
            return (None, "Command Not Recognized")

    def run(self) -> None:
        """
        Runs the agent in an infinite loop.

        This method will continuously pull commands from the server and execute
        them, sleeping for the poll interval between each pull.

        Args:
            None

        Returns:
            None
        """
        while True:
            self.pull_commands()
            time.sleep(self.poll_interval)
