#!/usr/bin/env python3
"""
Setup script for armasmgen - AArch64 (Arm v8-A) assembly generator DSL.
"""

from setuptools import setup, find_packages

setup(
    name="armasmgen",
    version="0.1.0",
    description="AArch64 (Arm v8-A) assembly generator DSL",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
