#!/usr/bin/env python3
"""
Setup script for armasmgen - AArch64 (Arm v8-A) assembly generator DSL.
"""

from setuptools import setup, find_packages

setup(
    name="armasmgen",
    version="0.1.0",
    description="AArch64 (Arm v8-A) assembly generator DSL",
    long_description="A powerful Python Domain Specific Language for generating AArch64 (ARM v8-A) assembly code with comprehensive instruction support, advanced addressing modes, and mathematical verification capabilities.",
    long_description_content_type="text/plain",
    author="Cheng-Wei Huang",
    author_email="cesarehuang@icloud.com",
    url="https://github.com/cheng-wei-huang0612/ArmAsmGen",
    license="MIT",
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
