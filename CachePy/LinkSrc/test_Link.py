import pytest
import linkTput
import adjustLink
import subprocess
import os 

def test_buildLinkMap():
    m = linkTput.buildLinkMaps()
    assert m[linkTput.Node.Client][linkTput.Node.Router] == "10.10.3.2"

def test_adjustLink():
    try:
        adjustLink.adjustLink("eth0",1,0.01)
        delay,loss = adjustLink.showLinkAdj("eth0")
        assert delay == '1.0ms' 
        assert loss == '0.01%'
    finally:
       adjustLink.delLinkAdj("eth0")


def test_Activate_IperfServer():
    assert os.path.exists("LinkSrc/IperfId.txt") == False #Make sure that this is the case, AKA no IperfServer is running 
                                                            #DO NOT JUST DELETE THE FILE TO MAKE THIS PASS
    try:
        linkTput.activateIperfServer()
        assert os.path.exists("LinkSrc/IperfId.txt") == True
        pass
    finally:
        linkTput.deactiveIperServer()
    pass


def test_readingIperfStatus():
    assert os.path.exists("LinkSrc/IperfId.txt") == False #Make sure that this is the case, AKA no IperfServer is running 
                                                            #DO NOT JUST DELETE THE FILE TO MAKE THIS PASS

    f = open('LinkSrc/IperfId.txt','w')
    f.write('9769')
    f.close()
    try:
        assert os.path.exists("LinkSrc/IperfId.txt") == True
        assert linkTput.readIperfServerStatus() == 9769     
    finally:
        os.remove('LinkSrc/IperfId.txt')
    



