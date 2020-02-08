from setuptools import setup, find_namespace_packages

setup(
    name="bbpyp",
    version="0.0.1",
    author="Trevor Wilson",
    author_email="trevor.wilson@bloggerbust.ca",
    description=("BloggerBust Python Projects common packages"),
    license="Apache License v2.0",
    keywords="Blogger Bust, state machine, combinator, lexical, interpreter, message bus",
    url="https://github.com/BloggerBust/bbpyp",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Software Development",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License"
    ],
    namespace_packages=["bbpyp"],
    packages=find_namespace_packages(include=["bbpyp.*"]),
    python_requires=">=3.6, <3.8", # I have only tested with 3.69 and 3.75
    install_requires=[
        "dependency-injector==3.14.5",
        "trio==0.13.0"
    ],
    extras_require={
        "dev": [
            "mock==3.0.5",
            "autopep8== 1.3.2"
        ],
        "dist": [
            "twine==3.1.1",
            "wheel==0.34.2"
        ]
    },
    zip_safe=False
)
