from wget import WGet
import os
from curl import CurlGet
from timeTaken import *

def delIndex():
    if os.path.exists("index.html"):
        os.remove("index.html")  


if __name__ == "__main__":
    url = "http://172.17.4.6"
    delIndex()
    
    wget = WGet(url)

    latency = timeTaken(wget)

    delIndex()

      
