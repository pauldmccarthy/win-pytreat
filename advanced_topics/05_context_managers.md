# Context managers


The recommended way to open a file in Python is via the `with` statement:


```
with open('05_context_managers.md', 'rt') as f:
    firstlines = f.readlines()[:4]
    firstlines = [l.strip() for l in firstlines]
    print('\n'.join(firstlines))
```


This is because the `with` statement ensures that the file will be closed
automatically, even if an error occurs inside the `with` statement.


The `with` statement is obviously hiding some internal details from us. But
these internals are in fact quite straightforward, and are known as [_context
managers_](https://docs.python.org/3.5/reference/datamodel.html#context-managers).


* [Anatomy of a context manager](#anatomy-of-a-context-manager)
 * [Why not just use `try ... finally`?](#why-not-just-use-try-finally)
* [Uses for context managers](#uses-for-context-managers)
 * [Handling errors in `__exit__`](#handling-errors-in-exit)
 * [Suppressing errors with `__exit__`](#suppressing-errors-with-exit)
* [Nesting context managers](#nesting-context-managers)
* [Functions as context managers](#functions-as-context-managers)
* [Methods as context managers](#methods-as-context-managers)
* [Useful references](#useful-references)


<a class="anchor" id="anatomy-of-a-context-manager"></a>
## Anatomy of a context manager


A _context manager_ is simply an object which has two specially named methods
`__enter__` and `__exit__`. Any object which has these methods can be used in
a `with` statement.


Let's define a context manager class that we can play with:


```
class MyContextManager(object):
    def __enter__(self):
        print('In enter')
    def __exit__(self, *args):
        print('In exit')
```


Now, what happens when we use `MyContextManager` in a `with` statement?


```
with MyContextManager():
    print('In with block')
```


So the `__enter__` method is called before the statements in the `with` block,
and the `__exit__` method is called afterwards.


Context managers are that simple. What makes them really useful though, is
that the `__exit__` method will be called even if the code in the `with` block
raises an error. The error will be held, and only raised after the `__exit__`
method has finished:


```
with MyContextManager():
    print('In with block')
    assert 1 == 0
```


This means that we can use context managers to perform any sort of clean up or
finalisation logic that we always want to have executed.


<a class="anchor" id="why-not-just-use-try-finally"></a>
### Why not just use `try ... finally`?


Context managers do not provide anything that cannot be accomplished in other
ways.  For example, we could accomplish very similar behaviour using
[`try` - `finally` logic](https://docs.python.org/3.5/tutorial/errors.html#handling-exceptions) -
the statements in the `finally` clause will *always* be executed, whether an
error is raised or not:


```
print('Before try block')
try:
    print('In try block')
    assert 1 == 0
finally:
    print('In finally block')
```


But context managers have the advantage that you can implement your clean-up
logic in one place, and re-use it as many times as you want.


<a class="anchor" id="uses-for-context-managers"></a>
## Uses for context managers


We have already talked about how context managers can be used to perform any
task which requires some initialistion and/or clean-up logic. As an example,
here is a context manager which creates a temporary directory, and then makes
sure that it is deleted afterwards.


```
import os
import shutil
import tempfile

class TempDir(object):

    def __enter__(self):

        self.tempDir = tempfile.mkdtemp()
        self.prevDir = os.getcwd()

        print('Changing to temp dir: {}'.format(self.tempDir))
        print('Previous directory:   {}'.format(self.prevDir))

        os.chdir(self.tempDir)

    def __exit__(self, *args):

        print('Changing back to:  {}'.format(self.prevDir))
        print('Removing temp dir: {}'.format(self.tempDir))

        os    .chdir( self.prevDir)
        shutil.rmtree(self.tempDir)
```


Now imagine that we have a function which loads data from a file, and performs
some calculation on it:


```
import numpy as np

def complexAlgorithm(infile):
    data = np.loadtxt(infile)
    return data.mean()
```


We could use the `TempDir` context manager to write a test case for this
function,  and not have to worry about cleaning up the test data:


```
with TempDir():
    print('Testing complex algorithm')

    data = np.random.random((100, 100))
    np.savetxt('data.txt', data)

    result = complexAlgorithm('data.txt')

    assert result > 0.1 and result < 0.9
    print('Test passed (result: {})'.format(result))
```


<a class="anchor" id="handling-errors-in-exit"></a>
### Handling errors in `__exit__`


By now you must be [panicking](https://youtu.be/cSU_5MgtDc8?t=9) about why I
haven't mentioned those conspicuous `*args` that get passed to the`__exit__`
method.  It turns out that a context manager's [`__exit__`
method](https://docs.python.org/3.5/reference/datamodel.html#object.__exit__)
is always passed three arguments.


Let's adjust our `MyContextManager` class a little so we can see what these
arguments are for:


```
class MyContextManager(object):
    def __enter__(self):
        print('In enter')

    def __exit__(self, arg1, arg2, arg3):
        print('In exit')
        print('  arg1: ', arg1)
        print('  arg2: ', arg2)
        print('  arg3: ', arg3)
```


If the code inside the `with` statement does not raise an error, these three
arguments will all be `None`.


```
with MyContextManager():
    print('In with block')
```


However, if the code inside the `with` statement raises an error, things look
a little different:


```
with MyContextManager():
    print('In with block')
    raise ValueError('Oh no!')
```


So when an error occurs, the `__exit__` method is passed the following:

- The [`Exception`](https://docs.python.org/3.5/tutorial/errors.html)
  type that was raised.
- The `Exception` instance that was raised.
- A [`traceback`](https://docs.python.org/3.5/library/traceback.html) object
  which can be used to get more information about the exception (e.g. line
  number).


<a class="anchor" id="suppressing-errors-with-exit"></a>
### Suppressing errors with `__exit__`


The `__exit__` method is also capable of suppressing errors - if it returns a
value of `True`, then any error that was raised will be ignored. For example,
we could write a context manager which ignores any assertion errors, but
allows other errors to halt execution as normal:


```
class MyContextManager(object):
    def __enter__(self):
        print('In enter')

    def __exit__(self, arg1, arg2, arg3):
        print('In exit')
        if issubclass(arg1, AssertionError):
            return True
        print('  arg1: ', arg1)
        print('  arg2: ', arg2)
        print('  arg3: ', arg3)
```

> Note that if a function or method does not explicitly return a value, its
> return value is `None` (which would evaluate to `False` when converted to a
> `bool`).  Also note that we are using the built-in
> [`issubclass`](https://docs.python.org/3.5/library/functions.html#issubclass)
> function, which allows us to test the type of a class.


Now, when we use `MyContextManager`, any assertion errors are suppressed,
whereas other errors will be raised as normal:


```
with MyContextManager():
    assert 1 == 0

print('Continuing execution!')

with MyContextManager():
    raise ValueError('Oh no!')
```


<a class="anchor" id="nesting-context-managers"></a>
## Nesting context managers


It is possible to nest `with` statements:

```
with open('05_context_managers.md', 'rt') as inf:
    with TempDir():
        with open('05_context_managers.md.copy', 'wt') as outf:
            outf.write(inf.read())
```


You can also use multiple context managers in a single `with` statement:


```
with open('05_context_managers.md', 'rt') as inf, \
     TempDir(), \
     open('05_context_managers.md.copy', 'wt') as outf:
    outf.write(inf.read())
```


<a class="anchor" id="functions-as-context-managers"></a>
## Functions as context managers


In fact, there is another way to create context managers in Python. The
built-in [`contextlib`
module](https://docs.python.org/3.5/library/contextlib.html#contextlib.contextmanager)
has a decorator called `@contextmanager`, which allows us to turn __any
function__ into a context manager.  The only requirement is that the function
must have a `yield` statement<sup>1</sup>. So we could rewrite our `TempDir`
class from above as a function:


```
import os
import shutil
import tempfile
import contextlib

@contextlib.contextmanager
def tempdir():
    tdir    = tempfile.mkdtemp()
    prevdir = os.getcwd()
    try:

        os.chdir(tdir)
        yield tdir

    finally:
        os.chdir(prevdir)
        shutil.rmtree(tdir)
```


This new `tempdir` function is used in exactly the same way as our `TempDir`
class:


```
print('In directory:      {}'.format(os.getcwd()))

with tempdir() as tmp:
    print('Now in directory:  {}'.format(os.getcwd()))

print('Back in directory: {}'.format(os.getcwd()))
```


The `yield tdir` statement in our `tempdir` function causes the `tdir` value
to be passed to the `with` statement, so in the line `with tempdir() as tmp`,
the variable `tmp` will be given the value `tdir`.


> <sup>1</sup> The `yield` keyword is used in _generator functions_.
> Functions which are used with the `@contextmanager` decorator must be
> generator functions which yield exactly one value.
> [Generators](https://www.python.org/dev/peps/pep-0289/) and [generator
> functions](https://docs.python.org/3.5/glossary.html#term-generator) are
> beyond the scope of this practical.


<a class="anchor" id="methods-as-context-managers"></a>
## Methods as context managers


Since it is possible to write a function which is a context manager, it is of
course also possible to write a _method_ which is a context manager. Let's
play with another example. We have a `Notifier` class which can be used to
notify interested listeners when an event occurs. Listeners can be registered
for notification via the `register` method:


```
from collections import OrderedDict

class Notifier(object):
    def __init__(self):
        super().__init__()
        self.listeners = OrderedDict()

    def register(self, name, func):
        self.listeners[name] = func

    def notify(self):
        for listener in self.listeners.values():
            listener()
```


Now, let's build a little plotting application. First of all, we have a `Line`
class, which represents a line plot. The `Line` class is a sub-class of
`Notifier`, so whenever its display properties (`colour`, `width`, or `name`)
change, it emits a notification, and whatever is drawing it can refresh the
display:


```
import numpy as np

class Line(Notifier):

    def __init__(self, data):
        super().__init__()
        self.__data   = data
        self.__colour = '#000000'
        self.__width  = 1
        self.__name   = 'line'

    @property
    def xdata(self):
        return np.arange(len(self.__data))

    @property
    def ydata(self):
        return np.copy(self.__data)

    @property
    def colour(self):
        return self.__colour

    @colour.setter
    def colour(self, newColour):
        self.__colour = newColour
        print('Line: colour changed: {}'.format(newColour))
        self.notify()

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, newWidth):
        self.__width = newWidth
        print('Line: width changed: {}'.format(newWidth))
        self.notify()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, newName):
        self.__name = newName
        print('Line: name changed: {}'.format(newName))
        self.notify()
```


Now let's write a `Plotter` class, which can plot one or more `Line`
instances:


```
import matplotlib.pyplot as plt

class Plotter(object):
    def __init__(self, axis):
        self.__axis   = axis
        self.__lines  = []

    def addData(self, data):
        line = Line(data)
        self.__lines.append(line)
        line.register('plot', self.lineChanged)
        self.draw()
        return line

    def lineChanged(self):
        self.draw()

    def draw(self):
        print('Plotter: redrawing plot')

        ax = self.__axis
        ax.clear()
        for line in self.__lines:
            ax.plot(line.xdata,
                    line.ydata,
                    color=line.colour,
                    linewidth=line.width,
                    label=line.name)
        ax.legend()
```


Let's create a `Plotter` object, and add a couple of lines to it (note that
the `matplotlib` plot will open in a separate window):


```
# this line is only necessary when
# working in jupyer notebook/ipython
%matplotlib

fig     = plt.figure()
ax      = fig.add_subplot(111)
plotter = Plotter(ax)
l1      = plotter.addData(np.sin(np.linspace(0, 6 * np.pi, 50)))
l2      = plotter.addData(np.cos(np.linspace(0, 6 * np.pi, 50)))

fig.show()
```


Now, when we change the properties of our `Line` instances, the plot will be
automatically updated:


```
l1.colour = '#ff0000'
l2.colour = '#00ff00'
l1.width  = 2
l2.width  = 2
l1.name   = 'sine'
l2.name   = 'cosine'
```


Pretty cool! However, this seems very inefficient - every time we change the
properties of a `Line`, the `Plotter` will refresh the plot. If we were
plotting large amounts of data, this would be unacceptable, as plotting would
simply take too long.


Wouldn't it be nice if we were able to perform batch-updates of `Line`
properties, and only refresh the plot when we are done? Let's add an extra
method to the `Plotter` class:


```
import contextlib

class Plotter(object):
    def __init__(self, axis):
        self.__axis        = axis
        self.__lines       = []
        self.__holdUpdates = False

    def addData(self, data):
        line = Line(data)
        self.__lines.append(line)
        line.register('plot', self.lineChanged)

        if not self.__holdUpdates:
            self.draw()
        return line

    def lineChanged(self):
        if not self.__holdUpdates:
            self.draw()

    def draw(self):
        print('Plotter: redrawing plot')

        ax = self.__axis
        ax.clear()
        for line in self.__lines:
            ax.plot(line.xdata,
                    line.ydata,
                    color=line.colour,
                    linewidth=line.width,
                    label=line.name)
        ax.legend()

    @contextlib.contextmanager
    def holdUpdates(self):
        self.__holdUpdates = True
        try:
            yield
            self.draw()
        finally:
            self.__holdUpdates = False
```


This new `holdUpdates` method allows us to temporarily suppress notifications
from all `Line` instances. So now, we can update many `Line` properties
without performing any redundant redraws:


```
fig     = plt.figure()
ax      = fig.add_subplot(111)
plotter = Plotter(ax)

plt.show()

with plotter.holdUpdates():
    l1        = plotter.addData(np.sin(np.linspace(0, 6 * np.pi, 50)))
    l2        = plotter.addData(np.cos(np.linspace(0, 6 * np.pi, 50)))
    l1.colour = '#0000ff'
    l2.colour = '#ffff00'
    l1.width  = 1
    l2.width  = 1
    l1.name   = '$sin(x)$'
    l2.name   = '$cos(x)$'
```


<a class="anchor" id="useful-references"></a>
## Useful references


* [Context manager classes](https://docs.python.org/3.5/reference/datamodel.html#context-managers)
* The [`contextlib` module](https://docs.python.org/3.5/library/contextlib.html)
