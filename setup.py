from setuptools import find_packages, setup

setup(
    name="Code Review Agent",
    version="0.0.1",
    author="Aathi",
    author_email="aathi8924@gmail.com",
    packages=find_packages(),
    install_requires=["autogen-agentchat", "autogen-core", "autogen-ext", "asyncio"]
)