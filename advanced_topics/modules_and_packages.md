# Modules and packages


Python gives you a lot of flexibility in how you organise your code. If you
want, you can write a Python program just as you would write a Bash script.
You don't _have_ to use functions, classes, modules or packages if you don't
want to, or if the script's task does not require them.


But when your code starts to grow beyond what can reasonably be defined in a
single file, you will (hopefully) want to start arranging it in a more
understandable manner.


For this practical we have prepared a handful of example files - you can find
them alongside this notebook file, in a directory called
`modules_and_packages/`.


```
import os
os.chdir('modules_and_packages')
```


## What is a module?


Any file ending with `.py` is considered to be a module in Python. Take a look
at `modules_and_packages/numfuncs.py` - either open it in your editor, or run
this code block:


```
with open('numfuncs.py', 'rt') as f:
    for line in f:
        print(line.rstrip())
```


This is a perfectly valid Python module, although not a particularly useful
one. It contains an attribute called `PI`, and a function `add`.


## Importing modules


Before we can use our module, we must `import` it. Importing a module in
Python will make its contents available to the local scope.  We can import the
contents of `mymodule` like so:


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


### Importing specific items from a module


If you only want to use one, or a few items from a module, you can import just
those items - a reference to just those items will be created in the local
scope:


```
from numfuncs import add
print(add(1, 3))
```


### Importing everything from a module


It is possible to import _everything_ that is defined in a module like so:


```
from numfuncs import *
print('PI: ', PI)
print(add(1, 5))
```


__PLEASE DON'T DO THIS!__ Because every time you do, somewhere in the world, a
software developer will will spontaneously stub his/her toe, and start crying.
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
requires you to type more code, the benefits of doing this far outweighs the
hassle of typing a few extra characters - it becomes much easier to read and
trace through code when the functions you use are accessed through a namespace
for each module:


```
import numfuncs
import strfuncs
print('number add: ', numfuncs.add(1, 2))
print('string add: ', strfuncs.add(1, 2))
```


And Python allows you to define an _alias_ for a module when you import it,
so you don't necessarily need to type out the full module name each time
you want to access something inside:


```
import numfuncs as nf
import strfuncs as sf
print('number add: ', nf.add(1, 2))
print('string add: ', sf.add(1, 2))
```


## What happens when I import a module?


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


## What is a package?




# Useful references

* [Modules in Python](https://docs.python.org/3.5/tutorial/modules.html)