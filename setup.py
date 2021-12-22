import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent


README = "Automate scraping data with single functions call"

setup(
    name="scrape-easy",
    version="1.0.0",
    description="Automate scraping data with single functions call",
    long_description=README,
    long_descrption_content_type="text/markdown",
    url="https://github.com/king-tomi/easy-scrape",
    author="Ayodabo Tomisin",
    author_email="ayodabooluwatomisin@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("test",)),
    include_package_data=True,
    install_requires=["bs4", "requests", "pytest"],
)