from distutils.core import setup

from setuptools import find_packages

setup(
    name="expose-text",
    version="0.1.0a",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    license="MIT",
    description="A Python module that exposes text for modification in multiple file types.",
    long_description=open("README.md").read(),
    install_requires=["pdfrw==0.4", "defusedxml==0.6.0", "beautifulsoup4==4.9.1"],
)
