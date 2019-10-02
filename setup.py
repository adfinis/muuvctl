from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="muuvctl",
    version="0.0.1",
    description="Control muuv tables with a command line tool",
    url="https://github.com/adfinis-sygroup/muuvctl",
    author="Cyrill von Wattenwyl, Lucas Bickel, Lukas Grossar",
    license="AGPL-3.0",
    packages=["muuvctl"],
    install_requires=requirements,
    zip_safe=False,
    entry_points={"console_scripts": ["muuvctl=muuvctl.cli:main"]},
)
