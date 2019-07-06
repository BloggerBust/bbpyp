import os
from setuptools import setup, find_namespace_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="bbp",
    version="0.0.1",
    author="Trevor Wilson",
    author_email="trevor.wilson@bloggerbust.ca",
    description=("BloggerBust Projects"),
    license="Apache License v2.0",
    keywords="BloggerBust projects: Message Bus, State machine, Lexical State Machine",
    url="https://bloggerbust.ca",
    # read('README.md'),
    long_description="Blogger Bust Projects",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Software Development",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License"
    ],
    namespace_packages=["bbp"],
    packages=find_namespace_packages(include=["bbp.*"]),
    python_requires=">=3.5",
    install_requires=[
        "dependency-injector==3.14.5",
        "trio==0.13.0"
    ],
    extras_require={
        "dev": [
            "mock==3.0.5",
            "autopep8== 1.3.2"
        ]
    },
    zip_safe=False,  # sorry, no eggs

    test_suite='test'
)
