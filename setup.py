#!/usr/bin/env python

from setuptools import setup, find_packages


install_requires = []

setup(
    name="role-identification",
    version="0.2.0",
    author="Jason Maldonis",
    author_email="jason@merakianalytics.com",
    url="https://github.com/meraki-analytics/role-identification",
    description="Identifies roles for teams in League of Legends",
    keywords=["LoL", "League of Legends", "Role Identification", "Role ID", "RoleID"],
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
