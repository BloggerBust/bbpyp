
# Table of Contents

1.  [Introduction](#orgf6af6c8)
2.  [Projects that use the BbPyP package](#org93b6086)
    1.  [Lexicomb](#orgdbabb60)
3.  [Configuration](#org4082526)
    1.  [Logging](#org67537e2)
    2.  [Message Bus](#orgadcd1c2)
4.  [How to contribute](#org2083291)
    1.  [How to setup a developer environment](#orge28ae61)
    2.  [Where to do your work](#org9c758d9)
    3.  [Don't forget unit tests](#org19bf540)
    4.  [Making commits](#orgd4ba094)
    5.  [Making a pull request](#orga20d302)
5.  [Packaging](#org964a6c8)
6.  [License](#org45ffc14)



<a id="orgf6af6c8"></a>

# Introduction

BbPyP (Blogger Bust Python Project) is a collection of python packages that I intend to use to help develop other more interesting python projects.


<a id="org93b6086"></a>

# Projects that use the BbPyP package


<a id="orgdbabb60"></a>

## [Lexicomb](https://github.com/BloggerBust/lexicomb)

Lexicomb is a keyword-driven interpreted programming language. The word *Lexicomb* is the contraction of the word *lexical*, meaning content word, and *combinator*, meaning that which combines. The Lexicomb interpreter is composed of a lexical analyzer and a parser combinator.


<a id="org4082526"></a>

# Configuration

Each bbpyp namespace has a [Dependency Injector IoC container](http://python-dependency-injector.ets-labs.org/containers/index.html) that accepts a python dictionary named *config*.


<a id="org67537e2"></a>

## Logging

**config Key:** logger
**Is Optional:** True

The `logger` configuration key may be set to any valid [logging dictionary configuration](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig). This parameter is entirely optional.

There are four named loggers that can be configured:

1.  `bbpyp.common`

2.  `bbpyp.message_bus`

3.  `bbpyp.lexical_state_machine`

4.  `bbpyp.interpreter_state_machine`


<a id="orgadcd1c2"></a>

## Message Bus

**config Key:** `memory_channel_topic`
**Is Optional:** True

    "memory_channel_topic": {
        "topic_name_1": {
            "publish_concurrency": 1,
            "subscribe_concurrency": 1
        },
        "topic_name_2": {
            "publish_concurrency": 1,
            "subscribe_concurrency": 1,
        },
        "topic_name_3": {
            "publish_concurrency": 1,
            "subscribe_concurrency": 1,
            "queue_type": QueueType.SEQUENCE
        }
    },

Memory channels allow the passing of objects between tasks owned by a single process. The `bbpyp.message_bus` package uses the [Trio library's memory channel](https://trio.readthedocs.io/en/stable/reference-core.html#trio.open_memory_channel) to facilitate `Pub/Sub`.  The `memory_channel_topic` config attribute tells the message bus how many concurrent memory connections should be created for each topic with respect to publishing and subscribing. Cross channel communication is currently made possible using queues. The `queue_type` attribute may be set to `QueueType.SEQUENCE` or `QueueType.FIFO` with `QueueType.FIFO` being the default.

**config Key:** `memory_channel_topic_default`
**Is Optional:** True

    "memory_channel_topic_default": {
        "publish_concurrency": 1,
        "subscribe_concurrency": 1,      
        "queue_type": QueueType.FIFO      
    },

Provides default settings for any topic that is not configured in `memory_channel_topic`. If `memory_channel_topic_default` is not set, then it defaults to the values shown above.

**config Key:** `memory_channel_max_buffer_size`
**Is Optional:** True

    "memory_channel_max_buffer_size": 5

The number of objects that can be temporarily stored in a memory channel prior to being processed. The default is 5.


<a id="org2083291"></a>

# How to contribute

I am happy to accept pull requests. If you need to get a hold of me you can [create an issue](https://github.com/BloggerBust/bbpyp/issues) or [email me directly](https://bloggerbust.ca/about/).


<a id="orge28ae61"></a>

## How to setup a developer environment

First, [fork this repository](https://github.com/login?return_to=%2FBloggerBust%2Fbbpyp) and clone your fork to a local dev environment.

    git clone https://github.com/<your-username>/bbpyp.git

Next, create a venv and install the latest pip and setuptools.

    cd bbpyp
    python -m venv venv
    source venv/bin/activate
    pip install -q --upgrade pip setuptools

Lastly, install the *dev* requirements declared in [dev-requirements.txt](dev-requirements.txt) and run the unit tests.

    pip install -q -r dev-requirements.txt
    python -m unittest discover

    ...............................................................................................................................................
    ----------------------------------------------------------------------
    Ran 143 tests in 0.554s
    
    OK


<a id="org9c758d9"></a>

## Where to do your work

Keep your mainline up to date with upstream.

    git fetch origin --prune
    git checkout master
    git --ff-only origin/master

Make your changes in a feature branch.

    git checkout -b branch_name


<a id="org19bf540"></a>

## Don't forget unit tests

Unit tests are written using python's [unittest framework](https://docs.python.org/3/library/unittest.html) and [mock library](https://docs.python.org/3/library/unittest.mock.html). Please do write unit tests to accommodate your contribution.


<a id="orgd4ba094"></a>

## Making commits

Read Chris Beams excellent [article on writing commit messages](https://chris.beams.io/posts/git-commit/) and do your best to follow his advice.


<a id="orga20d302"></a>

## Making a pull request

If you feel that your changes would be appreciated upstream then it is time to create a pull request. Please [write unit tests](#org19bf540) and run all the tests again before making a pull request to defend against inadvertently braking something.

    python -m unittest discover

If you have made many intermittent commits in your feature branch, then please make a squash branch and [rebase with a single squashed commit](https://blog.carbonfive.com/2017/08/28/always-squash-and-rebase-your-git-commits/). A squash branch is just a spin-off branch where you can perform the squash and rebase without the fear of corrupting your feature branch. My preference is to perform an interactive rebase. Note, that a squash branch is pointless if you only made a single commit.

First switch to master and fast forward to HEAD. This will reduce the risk of having a merge conflict later.

    git checkout master
    git fetch origin --prune
    git merge --ff-only origin/master

Next, switch back to your feature branch and pull any changes fetched to master. If there are conflicts, then resolve them. Be sure to run all the tests once more if you had to merge with changes from upstream.

    git checkout branch_name
    git pull origin/master
    python -m unittest discover

Then, create your squash branch and begin the interactive rebase following [this guidance](https://blog.carbonfive.com/2017/08/28/always-squash-and-rebase-your-git-commits/).

    git checkout -b branch_name_squash
    git rebase -i branch_name_squash

Finally, push the squash branch to remote and [create a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).


<a id="org964a6c8"></a>

# Packaging

For convenience distribution requirements, including pep517 package, are defined in [dist-requirements.txt](dist-requirements.txt).

    pip install -q -r dist-requirements.txt
    python -m pep517.build .

By default the wheel and sdist are placed in a directory named dist.

    ls dist

    bbpyp-0.0.2-py3-none-any.whl
    bbpyp-0.0.2.tar.gz


<a id="org45ffc14"></a>

# License

[Apache License v2.0](LICENSE-2.0.txt)

