
# Table of Contents

1.  [Introduction](#org3ca8cfb)
2.  [Projects that use the BbPyP package](#orgee8ef5b)
    1.  [Lexicomb](#org01ea965)
3.  [Configuration](#orgcdab8e9)
    1.  [Logging](#org5825b58)
    2.  [Message Bus](#orga3da92f)
4.  [How to contribute](#orgca220f1)
    1.  [How to setup a developer environment](#orgd08eb69)
    2.  [Where to do your work](#org4b8cb70)
    3.  [Don't forget unit tests](#orgf9ce6f2)
    4.  [Making commits](#org48a162d)
    5.  [Making a pull request](#orgaf302d7)
5.  [Packaging](#org9b1477e)
6.  [License](#orgca5bb48)



<a id="org3ca8cfb"></a>

# Introduction

BbPyP (Blogger Bust Python Project) is a collection of python packages that I intend to use to help develop other more interesting python projects.


<a id="orgee8ef5b"></a>

# Projects that use the BbPyP package


<a id="org01ea965"></a>

## [Lexicomb](https://github.com/BloggerBust/lexicomb)

Lexicomb is a keyword-driven interpreted programming language. The word *Lexicomb* is the contraction of the word *lexical*, meaning content word, and *combinator*, meaning that which combines. The Lexicomb interpreter is composed of a lexical analyzer and a parser combinator.


<a id="orgcdab8e9"></a>

# Configuration

Each bbpyp namespace has a [Dependency Injector IoC container](http://python-dependency-injector.ets-labs.org/containers/index.html) that accepts a python dictionary named *config*.


<a id="org5825b58"></a>

## Logging

**config Key:** logger
**Is Optional:** True

The `logger` configuration key may be set to any valid [logging dictionary configuration](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig). This parameter is entirely optional.

There are four named loggers that can be configured:

1.  `bbpyp.common`

2.  `bbpyp.message_bus`

3.  `bbpyp.lexical_state_machine`

4.  `bbpyp.interpreter_state_machine`


<a id="orga3da92f"></a>

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


<a id="orgca220f1"></a>

# How to contribute

I am happy to accept pull requests. If you need to get a hold of me you can [create an issue](https://github.com/BloggerBust/bbpyp/issues) or [email me directly](https://bloggerbust.ca/about/).


<a id="orgd08eb69"></a>

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


<a id="org4b8cb70"></a>

## Where to do your work

Keep your mainline up to date with upstream.

    git fetch origin --prune
    git checkout master
    git --ff-only origin/master

Make your changes in a feature branch.

    git checkout -b branch_name


<a id="orgf9ce6f2"></a>

## Don't forget unit tests

Unit tests are written using python's [unittest framework](https://docs.python.org/3/library/unittest.html) and [mock library](https://docs.python.org/3/library/unittest.mock.html). Please do write unit tests to accommodate your contribution.


<a id="org48a162d"></a>

## Making commits

Read Chris Beams excellent [article on writing commit messages](https://chris.beams.io/posts/git-commit/) and do your best to follow his advice.


<a id="orgaf302d7"></a>

## Making a pull request

If you feel that your changes would be appreciated upstream, then it is time to create a pull request. Please [write unit tests](#orgf9ce6f2) and run all the tests again before making a pull request to defend against inadvertently braking something.

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

Determine the first commit of the feature branch which will be needed during interactive rebasing.

    git log master..branch_name | grep -iE '^commit' | tail -n 1

    commit f723dcc2c154662b3d6c366fb5ad923865687796

Then, create a squash branch as a spin-off of the feature branch and begin the interactive rebase following [this guidance](https://blog.carbonfive.com/2017/08/28/always-squash-and-rebase-your-git-commits/).

    git checkout -b branch_name_squash
    git rebase -i f723dcc^

Now, if you make a mistake during the rebase, but don't notice until after you have already committed, all of your precious commit history remains in the feature branch. Simply reset the squash branch back to the feature branch and start again. Once you are happy with your rebase, push the squash branch to remote and [create a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).


<a id="org9b1477e"></a>

# Packaging

For convenience distribution requirements, including pep517 package, are defined in [dist-requirements.txt](dist-requirements.txt).

    pip install -q -r dist-requirements.txt
    python -m pep517.build .

By default the wheel and sdist are placed in a directory named dist.

    ls dist

    bbpyp-0.0.2-py3-none-any.whl
    bbpyp-0.0.2.tar.gz


<a id="orgca5bb48"></a>

# License

[Apache License v2.0](LICENSE-2.0.txt)

