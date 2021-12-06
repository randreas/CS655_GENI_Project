import subprocess

def adjustLink(link:str, delay:int, loss:float):
    subprocess.run('sudo tc qdisc add dev '+ link +' root netem delay '+ str(delay) +'ms loss '+ str(loss),shell=True,check=True)

def delLinkAdj(link:str):
    subprocess.run('sudo tc qdisc del dev '+ link +' root netem',shell=True,check=True)

def showLinkAdj(link:str):
    p =subprocess.run('sudo tc qdisc show | grep '+link,shell=True,capture_output=True,check=True,text=True)

    out = p.stdout
    delay = out.split(" ")[11]
    loss = out.split(" ")[13].split("\n")[0]
    return delay,loss
    

