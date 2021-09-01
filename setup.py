# -*- coding: utf-8 -*-
"""
setup.py

installation script

"""

from setuptools import setup, find_packages

PACKAGE_NAME = "nflschedule"


def run():
    setup(
        name=PACKAGE_NAME,
        version="0.2",
        description="python library for standardizing NFL schedule information",
        author="Eric Truett",
        author_email="eric@erictruett.com",
        license="MIT",
        packages=find_packages(),
        package_data={PACKAGE_NAME: ["data/*.*"]},
        zip_safe=False,
        install_requires=["python-dateutil>=2.4", "pandas>=1.0"],
    )


if __name__ == "__main__":
    run()
