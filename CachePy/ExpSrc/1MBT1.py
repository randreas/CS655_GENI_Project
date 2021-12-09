from wget import WGet
import os

from timeTaken import *

import statistics

from ExperimentObserver import SampleStatistics

def runExperiment(fetchOrder,rerunOrig,ExpName:str):
    

    server ="10.10.4.2/"
    proxy = "10.10.5.1"


    
    if rerunOrig:
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

        
        with open(ExpName+'ORIGIN.txt', 'w') as f:
            f.write("Stat,min,avg,max,std_dev\n")
            f.write("Latency,%s,%s,%s,%s\n"%(latency_stats.min,latency_stats.getMean(),latency_stats.max,latency_stats.std_dev))
            f.write("Throughput,%s,%s,%s,%s\n"%(tput_stats.min,tput_stats.getMean(),tput_stats.max,tput_stats.std_dev))
    
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
    with open(ExpName+'PROXY.txt', 'w') as f:
        f.write("Stat,min,avg,max,std_dev\n")
        f.write("Latency,%s,%s,%s,%s\n"%(latency_stats.min,latency_stats.getMean(),latency_stats.max,latency_stats.std_dev))
        f.write("Throughput,%s,%s,%s,%s\n"%(tput_stats.min,tput_stats.getMean(),tput_stats.max,tput_stats.std_dev))

if __name__ =="__main__":

    Exps= [("1MB0.txt","1MB1.txt","1MB2.txt","1MB3.txt","1MB4.txt","1MB5.txt","1MB6.txt","1MB7.txt","1MB8.txt")]
    
    for i in range(len(Exps)):
        print("exp:",Exps[i])
        runExperiment(Exps[i],True,"1MB_EXP1_")

