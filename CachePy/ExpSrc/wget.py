import subprocess
from timeTaken import Command


class WGet(Command):
    def __init__(self,url:str):
        self.url = url
        self.result = None

    def execute(self):
        process = subprocess.run('wget ' + self.url , shell=True,capture_output=True, text=True,check=True)#this will raise an exception on a error
        self.result = process.stdout

    def getResult(self) ->str:
        return self.result 
        

