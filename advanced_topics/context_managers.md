# Context managers


The recommended way to open a file in Python is via the `with` statement:


```
with open('context_managers.md', 'rt') as f:
    firstlines = f.readlines()[:4]
    firstlines = [l.strip() for l in firstlines]
    print('\n'.join(firstlines))
```


This is because the `with` statement ensures that the file will be closed
automatically, even if an error occurs inside the `with` statement.


The `with` statement is obviously hiding some internal details from us. But
these internals are in fact quite straightforward, and are known as [_context
managers_](https://docs.python.org/3.5/reference/datamodel.html#context-managers).


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


## Functions as context managers


In fact, there is another way to create context managers in Python. The
built-in [`contextlib`
module](https://docs.python.org/3.5/library/contextlib.html#contextlib.contextmanager)
has a decorator called `@contextmanager`, which allows us to turn __any__
function into a context manager.  The only requirement is that the function
must have a `yield` statement<sup>1</sup>. So we could rewrite our `TempDir`
class from above as a function:


```
import os
import shutil
import tempfile
import contextlib

@contextlib.contextmanager
def tempdir():
    testdir = tempfile.mkdtemp()
    prevdir = os.getcwd()
    try:

        os.chdir(testdir)
        yield testdir

    finally:
        os.chdir(prevdir)
        shutil.rmtree(testdir)
```

This new `tempdir` function is used in exactly the same way as our `TempDir`
class:


```
print('In directory:      {}'.format(os.getcwd()))

with tempdir():
    print('Now in directory:  {}'.format(os.getcwd()))

print('Back in directory: {}'.format(os.getcwd()))
```


> <sup>1</sup> The `yield` keyword is used in _generator functions_.
> Functions which are used with the `@contextmanager` decorator must be
> generator functions which yield exactly one value.
> [Generators](https://www.python.org/dev/peps/pep-0289/) and [generator
> functions](https://docs.python.org/3.5/glossary.html#term-generator) are
> beyond the scope of this practical.


Since it is possible to write a function which is a context manager, it is of
course also possible to write a _method_ which is a context manager.


```
TODO suppress notification example
```


## Nesting context managers




## Useful references


* [Context manager classes](https://docs.python.org/3.5/reference/datamodel.html#context-managers)
* The [`contextlib` module](https://docs.python.org/3.5/library/contextlib.html)
