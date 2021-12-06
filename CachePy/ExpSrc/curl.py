import subprocess
from timeTaken import Command

class CurlGet(Command):
    def __init__(self,url:str, headers:bool, proxy:str=None):
        self.url = url
        self.headers = headers
        self.proxy=proxy
    
    def execute(self):
        process = None
        if self.proxy == None:
            if self.headers:
                process = subprocess.run(['curl','--request', 'GET', '-L', '-I', self.url], capture_output=True, text=True,check=True)#this will raise an exception on a error
            else: 
                process = subprocess.run(['curl','--request', 'GET', '-L', self.url], capture_output=True, text=True,check=True)
        else:
            if self.headers:
                cmd = 'curl -x http://'+ self.proxy':8080 --request GET -L -I '+ self.url
                process = subprocess.run(, capture_output=True, text=True,check=True)#this will raise an exception on a error
        self.result = process.stdout
    
    def getResult(self) ->str:
        return self.result 