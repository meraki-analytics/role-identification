#!/usr/bin/env python

import sys

from setuptools import setup, find_packages


install_requires = [
    "cassiopeia"
]

# Require python 3.6
if sys.version_info.major != 3 and sys.version_info.minor != 6:
    sys.exit("Cassiopeia requires Python 3.6.")

setup(
    name="role-identification",
    version="0.0.1",
    author="Jason Maldonis",
    author_email="jason@merakianalytics.com",
    url="https://github.com/meraki-analytics/role-identification",
    description="Identifies roles for teams in League of Legends",
    keywords=["LoL", "League of Legends", "Cassiopeia"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
    packages=find_packages(),
    zip_safe=True,
    install_requires=install_requires,
    include_package_data=True
)
