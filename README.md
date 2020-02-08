
# Table of Contents

1.  [Introduction](#orgbb07392)
2.  [Projects](#org4061666)
    1.  [Lexicomb](#org41bac77)
3.  [How to contribute](#org4c9fbeb)
    1.  [How to setup a developer environment](#org08111cd)
    2.  [Where to do your work](#org80c01b6)
    3.  [Don't forget unit tests](#org296fb67)
    4.  [Making commits](#org44907d6)
4.  [License](#orgc67d713)
    5.  [Test a packaged installation](#orga2dc1de)
    6.  [Making a pull request](#org5334aab)



<a id="orgbb07392"></a>

# Introduction

BbPyP (Blogger Bust Python Projects) is a collection of python packages that I intend to use to help develop other more interesting python projects.


<a id="org4061666"></a>

# Projects


<a id="org41bac77"></a>

## [Lexicomb](https://github.com/BloggerBust/lexicomb)


<a id="org4c9fbeb"></a>

# How to contribute

I am happy to accept pull requests. If you need to get a hold of me you can [create an issue](https://github.com/BloggerBust/bbpyp/issues) or [email me directly](https://bloggerbust.ca/about/).


<a id="org08111cd"></a>

## How to setup a developer environment

First, [fork this repository](https://github.com/login?return_to=%2FBloggerBust%2Fbbpyp) and clone your fork to a local dev environment.

    git clone https://github.com/<your-username>/bbpyp.git

Next, create a venv and install the latest pip and setuptools.

    cd bbpyp
    python -m venv venv
    source venv/bin/activate
    python -m pip install --upgrade pip setuptools

Lastly, install the *dev* extra requirements declared in [setup.py](setup.py) `extras_require` and run the unit tests.

    source venv/bin/activate
    python setup.py develop
    python -m pip install -e .[dev]
    python -m unittest discover


<a id="org80c01b6"></a>

## Where to do your work

Make your changes in a feature branch keeping your mainline up to date with upstream.

    git checkout -b branch_name


<a id="org296fb67"></a>

## Don't forget unit tests

Unit tests are written using python's [unittest framework](https://docs.python.org/3/library/unittest.html) and [mock library](https://docs.python.org/3/library/unittest.mock.html). Please do write unit tests to accommodate your contribution.


<a id="org44907d6"></a>

## Making commits

Read Chris Beams excellent [article on writing commit messages](https://chris.beams.io/posts/git-commit/) and do your best to follow his advice.


<a id="orga2dc1de"></a>

## Test a packaged installation

To test packaging and installation you will need to install the *dist* extra requirements declared in [setup.py](setup.py) `extras_require`

    python setup.py sdist bdist_wheel
    python -m twine check dist/*


<a id="org5334aab"></a>

## Making a pull request

If you feel that your changes would be appreciated upstream then it is time to create a pull request. Please [write unit tests](#org8e82216) and run all the tests again before making a pull request to defend against inadvertently braking something.

    python -m unittest discover

Then create a squash branch and [rebase with a single squashed commit](https://blog.carbonfive.com/2017/08/28/always-squash-and-rebase-your-git-commits/). A squash branch is just a spin-off branch where you can perform the squash and rebase without the fear of corrupting your feature branch. My preference is to perform an interactive rebase. Note, that a squash branch is pointless if you only made a single commit.

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


<a id="orgc67d713"></a>

# License

[Apache License v2.0](LICENSE-2.0.txt)

