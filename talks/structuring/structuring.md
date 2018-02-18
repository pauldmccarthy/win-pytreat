# Structuring a Python project


If you are writing code that you are sure will never be seen or used by
anybody else, then you can structure your project however you want, and you
can stop reading now.


However, if you are intending to make your code available for others to use,
you will make their lives easier if you spend a little time organising your
project directory.


A Python project directory should, at the very least, have a structure that
resembles the following:


> ```
>   myproject/
>       mypackage/
>           __init__.py
>           mymodule.py
>       README
>       LICENSE
>       requirements.txt
>       setup.py
> ```


## The `mypackage/` directory


The first thing you should do is make sure that all of your python code is
organised into a sensibly-named
[_package_](https://docs.python.org/3.5/tutorial/modules.html#packages). This
is important, because it greatly reduces the possibility of naming collisions
when people install your library alongside other libraries.  Hands up those of
you who have ever written a file called `utils.[py|m|c|cpp]`!


Check out the `advanced_topics/02_modules_and_packages.ipynb` practical for
more details on packages in Python.


## `README`


Every project should have a README file. This is simply a plain text file
which describes your project and how to use it. It is common and acceptable
for a README file to be written in plain text,
[reStructuredText](http://www.sphinx-doc.org/en/stable/rest.html)
(`README.rst`), or
[markdown](https://guides.github.com/features/mastering-markdown/)
(`README.md`).


## `LICENSE`


Having a LICENSE file makes it easy for people to understand the constraints
under which your code can be used.


## `requirements.txt`


This file is not strictly necessary, but is very common in Python projects.
It contains a list of the Python-based dependencies of your project, in a
standardised syntax.


## Tests



There are no strict rules for where to put your tests (you have tests,
right?). There are two main conventions:


You can store your test files _inside_ your package directory:


> ```
> myproject/
>     mypackage/
>         __init__.py
>         mymodule.py
>         tests/
>             __init__.py
>             test_mymodule.py
> ```



Or, you can store your test files _alongside_ your package directory:


> ```
> myproject/
>     mypackage/
>         __init__.py
>         mymodule.py
>     tests/
>         test_mymodule.py
> ```


If you want your test code to be completely independent of your project's
code, then go with the second option.  However, if you would like your test
code to be distributed as part of your project (so that e.g. end users can run
them), then the first option is probably the best.


But in the end, the standard Python unit testing frameworks
([`pytest`](https://docs.pytest.org/en/latest/) and
[`nose`](http://nose2.readthedocs.io/en/latest/)) are pretty good at finding
your test functions no matter where you've hidden them.


## Versioning


If you are intending to make your project available for public use (e.g. on
[PyPI](https://pypi.python.org/pypi) and/or
[conda](https://anaconda.org/anaconda/repo)), it is __very important__ to
manage the version number of your project. If somebody decides to build their
software on top of your project, they are not going to be very happy with you
if you make substantial, API-breaking changes without changing your version
number in an appropriate manner.


Python has [official standards](https://www.python.org/dev/peps/pep-0440/) on
what constitutes a valid version number. These standards can be quite
complicated but, in the vast majority of cases, a simple three-number
versioning scheme comprising _major_, _minor_, and _patch_ release
numbers should suffice. Such a version number has the form:


>     major.minor.patch


For example, a version number of `1.3.2` has a _major_ release of 1, _minor_
release of 3, and a _patch_ release of 2.


If you follow some simple and rational guidelines for versioning
`your_project`, then people who use your project can, for instance, specify
that they depend on `your_project==1.*`, and be sure that their code will work
for _any_ version of `your_project` with a major release of 1. Following these
simple guidelines greatly improves software interoperability, and makes
everybody (i.e. developers of other projects, and end users) much happier!


Many modern Python projects use some form of [_semantic
versioning_](https://semver.org/). Semantic versioning is simply a set of
guidelines on how to manage your version number:


 - The _major_ release number should be incremented whenever you introduce any
   backwards-incompatible changes. In other words, if you change your code
   such that some other code which uses your code would break, you should
   increment the major release number.

 - The _minor_ release number should be incremented whenever you add any new
   (backwards-compatible) features to your project.

 - The _patch_ release number should be incremented for backwards-compatible
   bug-fixes and other minor changes.


If you like to automate things,
[`bumpversion`](https://github.com/peritus/bumpversion) is a simple tool that
you can use to help manage your version number.


### Deprecate, don't remove!


If you really want to change your API, but can't bring yourself to increment
your major release number, consider _deprecating_ the old API, and postponing
its removal until you are ready for a major release. This will allow you to
change your API, but retain backwards-compatilbiity with the old API until it
can safely be removed at the next major release.


You can use the built-in
[`warnings`](https://docs.python.org/3.5/library/exceptions.html#DeprecationWarning)
module to warn about uses of deprecated items. There are also some
[third-party libraries](https://github.com/briancurtin/deprecation) which make
it easy to mark a function, method or class as being deprecated.


## Cookiecutter


It is worth mentioning
[Cookiecutter](https://github.com/audreyr/cookiecutter), a little utility
program which you can use to generate a skeleton file/directory structure for
a new Python project.


You need to give it a template (there are many available templates, including
for projects in languages other than Python) - a couple of useful templates
are the [minimal Python package
template](https://github.com/kragniz/cookiecutter-pypackage-minimal), and the
[full Python package
template](https://github.com/audreyr/cookiecutter-pypackage) (although the
latter is probably overkill for most).


Here is how to create a skeleton project directory based off the minimal
Python packagetemplate:


```
pip install cookiecutter

# tell cookiecutter to create a directory
# from the pypackage-minimal template
cookiecutter https://github.com/kragniz/cookiecutter-pypackage-minimal.git

# cookiecutter will then prompt you for
# basic information (e.g. projectname,
# author name/email), and then create a
# new directory containing the project
# skeleton.
```
