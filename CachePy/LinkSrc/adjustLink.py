import subprocess

def adjustLink(link:str, delay:int, loss:float):
    return subprocess.run('sudo tc qdisc add dev '+ link +' root netem delay '+ str(delay) +'ms loss '+ str(loss),shell=True,check=True)

def delLinkAdj(link:str):
    return subprocess.run('sudo tc qdisc del dev '+ link +' root netem',shell=True,check=True)
