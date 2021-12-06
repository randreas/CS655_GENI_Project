import enum

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

def linkThrougput(soruce:Node,dest:Node):
    #subprocess("iperf -s")
    #subprocess.run('ssh ubuntu@'+Mask+ip+' -i ssh/jpl \'rm /home/ubuntu/d1/Proj/NASA-JPL/raw/*.TIF;rm /home/ubuntu/d1/Proj/NASA-JPL/raw/*.tmp; rmdir /home/ubuntu/d1/Proj/NASA-JPL/raw\'',shell=True)
    pass

