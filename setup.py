import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nexia_thermostat",
    version="0.0.1",
    author="JDare",
    author_email="jez433@gmail.com",
    description="A package for interacting with Nexia Thermostats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JDare/NexiaThermostat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)