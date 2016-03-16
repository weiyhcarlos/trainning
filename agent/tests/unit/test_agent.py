#!/usr/bin/env python

import pytest
from code import __main__
import subprocess

modules_all = "-m cpu disk net average_load"

module_single = "-m cpu"


@pytest.fixture(scope = "function")
def instance(request):
    def func():
        child=subprocess.Popen("service agent stop", shell=True)
        child.wait()
    request.addfinalizer(func)
    child = subprocess.Popen("service agent start", shell=True)
    child.wait()

@pytest.fixture(scope = "function")
def clean(request):
    def func():
        child=subprocess.Popen("service agent stop", shell=True)
        child.wait()
    request.addfinalizer(func)

def test_options_v(clean):
    child = subprocess.Popen("python agent.py -v", shell=True)
    child.wait()

def test_options_h(clean):
    child = subprocess.Popen("python agent.py -h", shell=True)
    child.wait()

def test_options_t(clean):
    child = subprocess.Popen("python agent.py -t 10", shell=True)
    child.wait()


def test_options_m_all(clean):
    child = subprocess.Popen("python agent.py -m all", shell=True)
    child.wait()

def test_options_m_single(clean):
    child = subprocess.Popen("python agent.py -m cpu", shell=True)
    child.wait()

def test_options_m_update(instance):
    child = subprocess.Popen("python agent.py -m cpu", shell=True)
    child.wait()
