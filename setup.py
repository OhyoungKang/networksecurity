"""
The setup.py file is an essential part of packaging and
distributing Python projects. It is used by setuptools
(or distutils in older Python versions) to define the configuration
of your project, such as its metadata, dependencies, and more
"""

from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    Reads requirements from requirements.txt file and returns them as a list of strings.
    """
    requirement_lst: List[str] = []
    try:
        with open("requirements.txt", "r") as f:
            # Read lines from the file
            lines = f.readlines()
            # Process each line and remove whitespace characters
            for line in lines:
                requirement = line.strip()
                # Ignore empty lines and -e .
                if requirement and requirement != "-e .":
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Ohyoung Kang",
    author_email="oykang64@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
