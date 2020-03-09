# Modules and packages


Python gives you a lot of flexibility in how you organise your code. If you
want, you can write a Python program just as you would write a Bash script.
You don't _have_ to use functions, classes, modules or packages if you don't
want to, or if the script task does not require them.


But when your code starts to grow beyond what can reasonably be defined in a
single file, you will (hopefully) want to start arranging it in a more
understandable manner.


For this practical we have prepared a handful of example files - you can find
them alongside this notebook file, in a directory called
`02_modules_and_packages/`.


## Contents

* [What is a module?](#what-is-a-module)
* [Importing modules](#importing-modules)
 * [Importing specific items from a module](#importing-specific-items-from-a-module)
 * [Importing everything from a module](#importing-everything-from-a-module)
 * [Module aliases](#module-aliases)
 * [What happens when I import a module?](#what-happens-when-i-import-a-module)
 * [How can I make my own modules importable?](#how-can-i-make-my-own-modules-importable)
* [Modules versus scripts](#modules-versus-scripts)
* [What is a package?](#what-is-a-package)
 * [`__init__.py`](#init-py)
* [Useful references](#useful-references)

```
import os
os.chdir('02_modules_and_packages')
```

<a class="anchor" id="what-is-a-module"></a>
## What is a module?


Any file ending with `.py` is considered to be a module in Python. Take a look
at `02_modules_and_packages/numfuncs.py` - either open it in your editor, or
run this code block:


```
with open('numfuncs.py', 'rt') as f:
    for line in f:
        print(line.rstrip())
```


This is a perfectly valid Python module, although not a particularly useful
one. It contains an attribute called `PI`, and a function `add`.


<a class="anchor" id="importing-modules"></a>
## Importing modules


Before we can use our module, we must `import` it. Importing a module in
Python will make its contents available in the local scope.  We can import the
contents of `numfuncs` like so:


```
import numfuncs
```


This imports `numfuncs` into the local scope - everything defined in the
`numfuncs` module can be accessed by prefixing it with `numfuncs.`:


```
print('PI:', numfuncs.PI)
print(numfuncs.add(1, 50))
```


There are a couple of other ways to import items from a module...


<a class="anchor" id="importing-specific-items-from-a-module"></a>
### Importing specific items from a module


If you only want to use one, or a few items from a module, you can import just
those items - a reference to just those items will be created in the local
scope:


```
from numfuncs import add
print(add(1, 3))
```


<a class="anchor" id="importing-everything-from-a-module"></a>
### Importing everything from a module


It is possible to import _everything_ that is defined in a module like so:


```
from numfuncs import *
print('PI: ', PI)
print(add(1, 5))
```


__PLEASE DON'T DO THIS!__ Because every time you do, somewhere in the world, a
software developer will spontaneously stub his/her toe, and start crying.
Using this approach can make more complicated programs very difficult to read,
because it is not possible to determine the origin of the functions and
attributes that are being used.


And naming collisions are inevitable when importing multiple modules in this
way, making it very difficult for somebody else to figure out what your code
is doing:


```
from numfuncs import *
from strfuncs import *

print(add(1, 5))
```


Instead, it is better to give modules a name when you import them.  While this
requires you to type more code, the benefits of doing this far outweigh the
hassle of typing a few extra characters - it becomes much easier to read and
trace through code when the functions you use are accessed through a namespace
for each module:


```
import numfuncs
import strfuncs
print('number add: ', numfuncs.add(1, 2))
print('string add: ', strfuncs.add(1, 2))
```

<a class="anchor" id="module-aliases"></a>
### Module aliases


And Python allows you to define an _alias_ for a module when you import it,
so you don't necessarily need to type out the full module name each time
you want to access something inside:


```
import numfuncs as nf
import strfuncs as sf
print('number add: ', nf.add(1, 2))
print('string add: ', sf.add(1, 2))
```


You have already seen this in the earlier practicals - here are a few
aliases which have become a de-facto standard for commonly used Python
modules:


```
import os.path           as op
import numpy             as np
import nibabel           as nib
import matplotlib        as mpl
import matplotlib.pyplot as plt
```

<a class="anchor" id="what-happens-when-i-import-a-module"></a>
### What happens when I import a module?


When you `import` a module, the contents of the module file are literally
executed by the Python runtime, exactly the same as if you had typed its
contents into `ipython`. Any attributes, functions, or classes which are
defined in the module will be bundled up into an object that represents the
module, and through which you can access the module's contents.


When we typed `import numfuncs` in the examples above, the following events
occurred:


1. Python created a `module` object to represent the module.

2. The `numfuncs.py` file was read and executed, and all of the items defined
   inside `numfuncs.py` (i.e. the `PI` attribute and the `add` function) were
   added to the `module` object.

3. A local variable called `numfuncs`, pointing to the `module` object,
   was added to the local scope.


Because module files are literally executed on import, any statements in the
module file which are not encapsulated inside a class or function will be
executed.  As an example, take a look at the file `sideeffects.py`. Let's
import it and see what happens:


```
import sideeffects
```


Ok, hopefully that wasn't too much of a surprise. Something which may be less
intuitive, however, is that a module's contents will only be executed on the
_first_ time that it is imported. After the first import, Python caches the
module's contents (all loaded modules are accessible through
[`sys.modules`](https://docs.python.org/3.5/library/sys.html#sys.modules)). On
subsequent imports, the cached version of the module is returned:


```
import sideeffects
```

<a class="anchor" id="how-can-i-make-my-own-modules-importable"></a>
### How can I make my own modules importable?


When you `import` a module, Python searches for it in the following locations,
in the following order:


1. Built-in modules (e.g. `os`, `sys`, etc.).
2. In the current directory or, if a script has been executed, in the directory
   containing that script.
3. In directories listed in the `$PYTHONPATH` environment variable.
4. In installed third-party libraries (e.g. `numpy`).


If you are experimenting or developing your program, the quickest and easiest
way to make your module(s) importable is to add their containing directory to
the `PYTHONPATH`. But if you are developing a larger piece of software, you
should probably organise your modules into *packages*, which are [described
below](#what-is-a-package).


<a class="anchor" id="modules-versus-scripts"></a>
## Modules versus scripts


You now know that Python treats all files ending in `.py` as importable
modules. But all files ending in `.py` can also be treated as scripts. In
fact, there no difference between a _module_ and a _script_ - any `.py` file
can be executed as a script, or imported as a module, or both.


Have a look at the file `02_modules_and_packages/module_and_script.py`:


```
with open('module_and_script.py', 'rt') as f:
    for line in f:
        print(line.rstrip())
```


This file contains two functions `mul` and `main`.  The
`if __name__ == '__main__':` clause at the bottom is a standard trick in Python
that allows you to add code to a file that is _only executed when the module is
called as a script_. Try it in a terminal now:


> `python 02_modules_and_packages/module_and_script.py`


But if we `import` this module from another file, or from an interactive
session, the code within the `if __name__ == '__main__':` clause will not be
executed, and we can access its functions just like any other module that we
import.


```
import module_and_script as mas

a = 1.5
b = 3

print('mul({}, {}): {}'.format(a, b, mas.mul(a, b)))
print('calling main...')
mas.main([str(a), str(b)])
```


<a class="anchor" id="what-is-a-package"></a>
## What is a package?


You now know how to split your Python code up into separate files
(a.k.a. *modules*). When your code grows beyond a handful of files, you may
wish for more fine-grained control over the namespaces in which your modules
live. Python has another feature which allows you to organise your modules
into *packages*.


A package in Python is simply a directory which:


* Contains a special file called `__init__.py`
* May contain one or more module files (any other files ending in `*.py`)
* May contain other package directories.


For example, the [FSLeyes](https://git.fmrib.ox.ac.uk/fsl/fsleyes/fsleyes)
code is organised into packages and sub-packages as follows (abridged):


> ```
> fsleyes/
>     __init__.py
>     main.py
>     frame.py
>     views/
>         __init__.py
>         orthopanel.py
>         lightboxpanel.py
>     controls/
>         __init__.py
>         locationpanel.py
>         overlaylistpanel.py
> ```


Within a package structure, we will typically still import modules directly,
via their full path within the package:


```
import fsleyes.main as fmain
fmain.fsleyes_main()
```

<a class="anchor" id="init-py"></a>
### `__init__.py`


Every Python package must have an `__init__.py` file. In many cases, this will
actually be an empty file, and you don't need to worry about it any more, apart
from knowing that it is needed. But you can use `__init__.py` to perform some
package-specific initialisation, and/or to customise the package's namespace.


As an example, take a look the `02_modules_and_packages/fsleyes/__init__.py`
file in our mock FSLeyes package. We have imported the `fsleyes_main` function
from the `fsleyes.main` module, making it available at the package level. So
instead of importing the `fsleyes.main` module, we could instead just import
the `fsleyes` package:


```
import fsleyes
fsleyes.fsleyes_main()
```


<a class="anchor" id="useful-references"></a>
## Useful references

* [Modules and packages in Python](https://docs.python.org/3/tutorial/modules.html)
* [Using `__init__.py`](http://mikegrouchy.com/blog/2012/05/be-pythonic-__init__py.html)
