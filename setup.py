from setuptools import setup
import os

version = '1.0'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="SMPOST",
    version="1.0",
    author="Shubham Tripathi",
    author_email="stripathi1770@gmail.com",
    description=("Social Media POS Tagger"),
    license="",
    keywords="POS Tagger Social Media",
    url="",
    packages=["SMPOST"],
    long_description=read('README.md'),
    include_package_data=True,
)