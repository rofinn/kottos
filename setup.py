#!/usr/bin/env python
# 192.168.1.90,91,92 502
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

DEPS = ["paho-mqtt", "pyserial", "uModbus"]
TEST_DEPS = ["coverage", "pytest>=3.6", "pytest-cov"]
CHECK_DEPS = ["flake8", "flake8-quotes", "pep8-naming"]
DOCS_DEPS = [
    "sphinx",
    "sphinx-rtd-theme",
    "sphinxcontrib-runcmd",
    "recommonmark",
    "sphinx-autoapi",
]

EXTRAS = {
    "test": TEST_DEPS,
    "docs": DOCS_DEPS,
    "check": CHECK_DEPS,
    "dev": TEST_DEPS + DOCS_DEPS + CHECK_DEPS,
}

setup(
    name="kottos",
    version="0.1.0",
    description="Python package for combining & aggregating IoT sensor data with AWS",
    author="Rory Finnegan",
    author_email="rory.finnegan@gmail.com",
    url="https://github.com/rofinn/kottos",
    packages=["kottos", "kottos.modbus", "kottos.mqtt"],
    install_requires=DEPS,
    tests_require=TEST_DEPS,
    extras_require=EXTRAS,
)
