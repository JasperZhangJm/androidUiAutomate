#content of test_example.py
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import pytest

@pytest.fixture
def error_fixture():
    assert 0

def test_ok():
    print("ok")

def test_fail():
    assert 0

def test_error(error_fixture):
    pass

def test_skip():
    pytest.skip("skip this test")

def test_xfail():
    pytest.xfail("xfailing this test")

@pytest.mark.xfail(reason="always xfail")
def test_xpass():
    pass