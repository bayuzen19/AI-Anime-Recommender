from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="anime-recommender",
    author="Bayuzen Ahmad",
    gmail="bayuzen19@gmail.com",
    version="0.0.1",
    packages=find_packages(),
    install_requires = requirements
)