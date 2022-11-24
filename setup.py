import setuptools

from startctfutil import __version__, __author__, __license__

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="startctf",
    version=__version__,
    author=__author__,
    scripts=["startctf"],
    license=__license__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stautonico/startctf",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ]
)
