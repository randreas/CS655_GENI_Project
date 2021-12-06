import pytest
from wget import WGet
import os
from curl import CurlGet
from timeTaken import *

serverip ="10.10.4.2"
c1 = "10.10.1.2"

def test_wget():
    try:
        if os.path.exists("index.html"):
            os.remove("index.html")

        wget = WGet(serverip)
        wget.execute()

        assert os.path.exists("index.html")

        fileSize = os.stat("index.html").st_size


    finally:
        if os.path.exists("index.html"):
            os.remove("index.html")

def test_proxy_wget():
    try:
        if os.path.exists("index.html"):
            os.remove("index.html")

        wget = WGet(serverip,proxy=c1)
        wget.execute()

        assert os.path.exists("index.html")

        fileSize = os.stat("index.html").st_size


    finally:
        if os.path.exists("index.html"):
            os.remove("index.html")


def test_curlGet():

    curl = CurlGet(serverip,False)
    curl.execute()

    fileSize = len(curl.getResult().encode('utf-8'))

    assert  fileSize == len("HelloWorld!\n")

