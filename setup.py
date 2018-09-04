#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='kottos',
    version='0.1.0',
    description='Python package for combining & aggregating IoT sensor data with AWS',
    author='Rory Finnegan',
    author_email='rory.finnegan@gmail.com',
    url='https://github.com/rofinn/kottos',
    packages=['kottos'],
    install_requires=[
        'paho-mqtt',
        'pyserial',
        'uModbus'
    ],
    test_requires=[
        'pytest'
    ],
)