from distutils.core import setup

from setuptools import find_packages

setup(
    name="expose-text",
    version="0.1.1b",
    url="https://openredact.org/",
    author="Jonas Langhabel, Malte Ostendorff",
    author_email="hello@openredact.org",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    license="MIT",
    description="A Python module that exposes text for modification in multiple file types.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["pdfrw==0.4", "defusedxml==0.6.0", "beautifulsoup4==4.9.1", "wkhtmltopdf==0.2", "pdfkit==0.6.1"],
    python_requires=">=3.7",
)
