from base_agent import BaseAgent
import os


class LinuxAgent(BaseAgent):
    """
    Extends BaseAgent for Linux-specific functionality.
    """

    def list_directory_contents(self, path: str) -> tuple:
        error = None
        output = None

        if not path.endswith("/"):
            path += "/"

        if not os.path.exists(path):
            error = f"The path: {path} does not exist"
            return (output, error)

        contents = os.listdir(path=path)
        output = []
        for item in contents:
            if os.path.isdir(path + item):
                output.append(item + "/")
            else:
                output.append(item)

        return (output, error)


def main():
    linux_agent = LinuxAgent()
    linux_agent.run()


if __name__ == "__main__":
    main()
