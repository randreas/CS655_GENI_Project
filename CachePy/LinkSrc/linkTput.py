import subprocess
import enum
import os
import re
class Node(enum.Enum):
    Client = 'client'
    Router = 'router'
    Server = 'server'
    Cache1 = 'cache1'
    Cache2 = 'cache2'



def buildLinkMaps():
    clientMap={ Node.Router:"10.10.3.2",
                Node.Cache1:"10.10.1.2",
                Node.Cache2:"10.10.2.1"}
    
    
    routerMap={ Node.Client:"10.10.3.1",
                Node.Server:"10.10.4.2",
                Node.Cache1:"10.10.5.1",
                Node.Cache2:"10.10.6.1"}
    
    serverMap={ Node.Router:"10.10.4.1"}

    cache1Map={ Node.Client:"10.10.1.1",
                Node.Router:"10.10.5.2"}
    
    cache2Map={ Node.Client:"10.10.2.2",
                Node.Router:"10.10.6.2"}

    return {Node.Client:clientMap,
            Node.Router:routerMap,
            Node.Server:serverMap,
            Node.Cache1:cache1Map,
            Node.Cache2:cache2Map}

def linkThrougput(dest:Node):

    print("Iperf server daemon must be running at dest!")

    p = subprocess.run("iperf -s",shell=True,capture_output=True,text=True, check=True)

    #subprocess.run('ssh ubuntu@'+Mask+ip+' -i ssh/jpl \'rm /home/ubuntu/d1/Proj/NASA-JPL/raw/*.TIF;rm /home/ubuntu/d1/Proj/NASA-JPL/raw/*.tmp; rmdir /home/ubuntu/d1/Proj/NASA-JPL/raw\'',shell=True)
    pass

def activateIperfServer():
    
    p = subprocess.run('iperf -s -D',shell=True,capture_output=True,text=True,check=True)

    output = p.stderr
    iD=re.search(r"\d+",output)
    iD = iD.group()

    f = open('LinkSrc/IperfId.txt','w')
    f.write(iD)
    f.close()

    pass

def deactiveIperServer():
    pid = readIperfServerStatus()

    if pid == -1:
        print("No Server currently Activated")
    else:
        p = subprocess.run('kill -9 '+ str(pid),shell=True,capture_output=True,text=True,check=True)
        os.remove('LinkSrc/IperfId.txt')
    






def readIperfServerStatus():
    if os.path.exists("LinkSrc/IperfId.txt"):
        with open('LinkSrc/IperfId.txt') as f:
            line = f.readline()
            return int(line)
    else:
        return -1

