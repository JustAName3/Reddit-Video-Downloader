import subprocess
import requests

class ServerError(Exception):
    """
    Raise if status_code of HTTPS GET != 200.
    """
    def __init__(self,
                 code: int,
                 url: str,
                 response: requests.Response):

        super().__init__()

        self.code: int = code
        self.url = url
        self.response = response

    def __str__(self):
        return  f"[Error] Server status code: {self.code}"


class FFmpegError(Exception):
    """
    Raise if FFmpeg throws an error.
    """
    def __init__(self,
                 stderr: str,
                 return_code: int,
                 command: str,
                 completed_process: subprocess.CompletedProcess):

        super().__init__()

        self.stderr = stderr
        self.return_code = return_code
        self.command = command
        self.completed_process = completed_process


    def __str__(self):
        return f"[Error] Return code: {self.return_code}, stderr: {self.stderr}"


class Error(Exception):
    """
    Generic Exception class.
    Arguments:
        -description: Description of error
        -caller: Function in which it was raised
    """
    def __init__(self, description, caller):
        super().__init__()

        self.description = description
        self.caller = caller


    def __str__(self):
        return f"[Error] >{self.description}< in function {self.caller}"