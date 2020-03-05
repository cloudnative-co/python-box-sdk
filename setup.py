from setuptools import setup, find_packages

setup(
    name="BoxSDK-Cn",
    version="0.0.6a",
    description="Box-SDK-Cn",
    author="sebastian",
    author_email="seba@cloudnative.co.jp",
    packages=find_packages(),
    install_requires=[
        "boxsdk[jwt]",
        "PyYaml",
        "jmespath"
    ],
    entry_points={
        "console_scripts": [
        ]
    },
)
