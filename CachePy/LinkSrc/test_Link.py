import pytest
import linkTput
import adjustLink
import subprocess

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



