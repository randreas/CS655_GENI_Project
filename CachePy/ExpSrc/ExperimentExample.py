
from wget import WGet
import os

from timeTaken import *

import statistics

from ExperimentObserver import SampleStatistics


if __name__ =="__main__":

    fetchOrder = ("index.html","index.html","index.html")

    server ="10.10.4.2/"
    proxy = "10.10.5.1"



    latency_stats = SampleStatistics()
    tput_stats = SampleStatistics()
    for f in fetchOrder:#WITHOUT PROXY
        if os.path.exists(f): #wget download files so just make sure
                os.remove(f)      #we dont already have a copy

        wget = WGet(server+f)
        latency=timeTaken(wget) #timeTaken calls execute on the wget classes,
                                    # and track how long it takes to return in seconds
        latency_stats.add(latency) #add latency sample to our stats tracker

        fileSize = os.stat(f).st_size #get index.html size in bytes
        tput_stats.add((fileSize*8)/latency) #add throughput sample in bits/second
    print("ORIGIN_SERVER")
    print("Stat,min,avg,max,std_dev")
    print("Latency,%s,%s,%s,%s"%(latency_stats.min,latency_stats.getMean(),latency_stats.max,latency_stats.std_dev))
    print("Throughput,%s,%s,%s,%s"%(tput_stats.min,tput_stats.getMean(),tput_stats.max,tput_stats.std_dev))
    
    latency_stats = SampleStatistics()
    tput_stats = SampleStatistics()
    
    for f in fetchOrder:
        if os.path.exists(f): #wget download files so just make sure
                os.remove(f)      #we dont already have a copy

        wget = WGet(server+f,proxy)
        latency=timeTaken(wget) #timeTaken calls execute on the wget classes,
                                    # and track how long it takes to return in seconds
        latency_stats.add(latency) #add latency sample to our stats tracker

        fileSize = os.stat(f).st_size #get index.html size in bytes
        tput_stats.add((fileSize*8)/latency) #add throughput sample in bits/second
    print("PROXY_SERVER")
    print("Latency min/avg/max/std_dev: %s/%s/%s/%s"%(latency_stats.min,latency_stats.getMean(),latency_stats.max,latency_stats.std_dev))
    print("Throughput min/avg/max/std_dev: %s/%s/%s/%s"%(tput_stats.min,tput_stats.getMean(),tput_stats.max,tput_stats.std_dev))

    
        


