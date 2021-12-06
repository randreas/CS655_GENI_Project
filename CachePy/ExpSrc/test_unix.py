import pytest
from wget import WGet
import os
from curl import CurlGet
from timeTaken import *


def test_wget():
    try:
        url = "www.github.com"
        if os.path.exists("index.html"):
            os.remove("index.html")

        wget = WGet(url)
        wget.execute()

        assert os.path.exists("index.html")

        fileSize = os.stat("index.html").st_size


        assert fileSize == 277577
    finally:
        if os.path.exists("index.html"):
            os.remove("index.html")

def test_curlGet():
    url = "www.github.com"

    curl = CurlGet(url,False)
    curl.execute()

    fileSize = len(curl.getResult().encode('utf-8'))

    assert  fileSize == 277577 

def test_timeTaken():
    try:
        url = "www.github.com"

        wget = WGet(url)
        curlGet = CurlGet(url,False)
    
    
        wgetLatency = timeTaken(wget)
        curlGetLatency = timeTaken(curlGet)

        print("WGet: %s seconds \n CurlGet: %s" % (wgetLatency,curlGetLatency))

        assert 1 ==1 # I just want to make sure that these calls dont throw an error
    finally:
        if os.path.exists("index.html"):
            os.remove("index.html")

import statistics

from ExperimentObserver import SampleStatistics

def test_sampleStatistics():
    test_list = [4.1,5.1,8.1,9.1,10.1]

    std = statistics.pstdev(test_list)

    stats = SampleStatistics()

    total = 0.0

    for sample in test_list:
        stats.add(sample)
        total = total + sample
    
    avg  = total / len(test_list)

    error_band = 1.0 / (10 ** 3) 
    
    std_band = std * error_band

    avg_band = avg * error_band

    assert (std - std_band) < stats.std_dev
    assert (std + std_band) > stats.std_dev

    assert stats.max == 10.1
    assert stats.min == 4.1

    assert (avg - avg_band) < stats.getMean()
    assert (avg + avg_band) > stats.getMean()


def test_HowToUse():
    try:
        url = "www.github.com" #sample website

        latency_stats = SampleStatistics()
        tput_stats = SampleStatistics()
        for i in range(4):
            if os.path.exists("index.html"): #wget download files so just make sure
                os.remove("index.html")      #we dont already have a copy
            wget = WGet(url)
            latency=timeTaken(wget) #timeTaken calls execute on the wget classes,
                                    # and track how long it takes to return in seconds
            latency_stats.add(latency) #add latency sample to our stats tracker

            fileSize = os.stat("index.html").st_size #get index.html size in bytes
            tput_stats.add((fileSize*8)/latency) #add throughput sample in bits/second
        print("Latency min/avg/max/std_dev: %s/%s/%s/%s"%(latency_stats.min,latency_stats.getMean(),latency_stats.max,latency_stats.std_dev))
        print("Throughput min/avg/max/std_dev: %s/%s/%s/%s"%(tput_stats.min,tput_stats.getMean(),tput_stats.max,tput_stats.std_dev))
        
    finally:
        if os.path.exists("index.html"):
            os.remove("index.html")

    



