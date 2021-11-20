import subprocess
from timeTaken import Command

class CurlGet(Command):
    def __init__(self,url:str, headers:bool):
        self.url = url
        self.headers = headers
    
    def execute(self):
        process = None
        if self.headers:
            process = subprocess.run(['curl','--request', 'GET', '-L', '-I', self.url], capture_output=True, text=True,check=True)#this will raise an exception on a error
        else: 
            process = subprocess.run(['curl','--request', 'GET', '-L', self.url], capture_output=True, text=True,check=True)
        self.result = process.stdout
    
    def getResult(self) ->str:
        return self.result 