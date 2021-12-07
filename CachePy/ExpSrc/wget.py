import subprocess
from timeTaken import Command


class WGet(Command):
    def __init__(self,url:str,proxy:str=None):
        self.url = url
        self.proxy = proxy
        self.result = None

    def execute(self):
        if self.proxy == None:
            process = subprocess.run('wget ' + self.url , shell=True,capture_output=True, text=True,check=True)#this will raise an exception on a error
        else:
            cmd = 'wget '+ self.url +' -e http_proxy='+self.proxy+':8080'
            process = subprocess.run(cmd,shell=True,capture_output=True, text=True)
            self.result = process.stdout
         

    def getResult(self) ->str:
        return self.result 
        

