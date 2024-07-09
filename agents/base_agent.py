"""
Class to define basic agent functionality
"""

import requests
import uuid
import time



class BaseAgent():

    def __init__(self, command_server_ip = "127.0.0.1", command_server_port = 8000, poll_interval = 5) -> None:
        self.id = uuid.uuid4()
        self.command_server_ip = command_server_ip
        self.command_server_port = command_server_port
        self.poll_interval = poll_interval

    def pull_commands(self) -> None:
        url = f"http://{self.command_server_ip}:{self.command_server_port}/command/pull"
        params = {"agent_id": self.id}
        try:
            response = requests.get(url=url, params=params)
        except:
            pass

    def run(self) -> None:
        
        while True:
            self.pull_commands()
            time.sleep(self.poll_interval)


def main():
    base_agent = BaseAgent()
    base_agent.run()

if __name__ == "__main__":
    main()

    

