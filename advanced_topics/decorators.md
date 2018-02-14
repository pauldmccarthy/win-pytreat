# Decorators


Remember that in Python, everything is an object, including functions. This
means that we can do things like:


- Pass a function as an argument to another function.
- Create/define a function inside another function.
- Write a function which returns another function.


These abilities mean that we can do some neat things with functions in Python.


* [Overview](#overview)
* [Decorators on methods](#decorators-on-methods)
* [Example - memoization](#example-memoization)
* [Decorators with arguments](#decorators-with-arguments)
* [Chaining decorators](#chaining-decorators)
* [Decorator classes](#decorator-classes)
* [Appendix: Functions are not special](#appendix-functions-are-not-special)
* [Appendix: Closures](#appendix-closures)
* [Appendix: Decorators without arguments versus decorators with arguments](#appendix-decorators-without-arguments-versus-decorators-with-arguments)
* [Appendix: Per-instance decorators](#appendix-per-instance-decorators)
* [Appendix: Preserving function metadata](#appendix-preserving-function-metadata)
* [Appendix: Class decorators](#appendix-class-decorators)
* [Useful references](#useful-references)


<a class="anchor" id="overview"></a>
## Overview


Let's say that we want a way to calculate the execution time of any function
(this example might feel familiar to you if you have gone through the
practical on operator overloading).


Our first attempt at writing such a function might look like this:


```
import time
def timeFunc(func, *args, **kwargs):

    start  = time.time()
    retval = func(*args, **kwargs)
    end    = time.time()

    print('Ran {} in {:0.2f} seconds'.format(func.__name__, end - start))

    return retval
```


The `timeFunc` function accepts another function, `func`, as its first
argument. It calls `func`, passing it all of the other arguments, and then
prints the time taken for `func` to complete:


```
import numpy        as np
import numpy.linalg as npla

def inverse(a):
    return npla.inv(a)

data    = np.random.random((2000, 2000))
invdata = timeFunc(inverse, data)
```


But this means that whenever we want to time something, we have to call the
`timeFunc` function directly. Let's take advantage of the fact that we can
define a function inside another funciton. Look at the next block of code
carefully, and make sure you understand what our new `timeFunc` implementation
is doing.


```
import time
def timeFunc(func):

    def wrapperFunc(*args, **kwargs):

        start  = time.time()
        retval = func(*args, **kwargs)
        end    = time.time()

        print('Ran {} in {:0.2f} seconds'.format(func.__name__, end - start))

        return retval

    return wrapperFunc
```


This new `timeFunc` function is again passed a function `func`, but this time
as its sole argument. It then creates and returns a new function,
`wrapperFunc`. This `wrapperFunc` function calls and times the function that
was passed to `timeFunc`.  But note that when `timeFunc` is called,
`wrapperFunc` is _not_ called - it is only created and returned.


Let's use our new `timeFunc` implementation:


```
import numpy        as np
import numpy.linalg as npla

def inverse(a):
    return npla.inv(a)

data    = np.random.random((2000, 2000))
inverse = timeFunc(inverse)
invdata = inverse(data)
```


Here, we did the following:


1. We defined a function called `inverse`:

  > ```
  > def inverse(a):
  >     return npla.inv(a)
  > ```

2. We passed the `inverse` function to the `timeFunc` function, and
   re-assigned the return value of `timeFunc` back to `inverse`:

  > ```
  > inverse = timeFunc(inverse)
  > ```

3. We called the new `inverse` function:

  > ```
  > invdata = inverse(data)
  > ```


So now the `inverse` variable refers to an instantiation of `wrapperFunc`,
which holds a reference to the original definition of `inverse`.


> If this is not clear, take a break now and read through the appendix on how
> [functions are not special](#appendix-functions-are-not-special).


Guess what? We have just created a __decorator__. A decorator is simply a
function which accepts a function as its input, and returns another function
as its output. In the example above, we have _decorated_ the `inverse`
function with the `timeFunc` decorator.


Python provides an alternative syntax for decorating one function with
another, using the `@` character. The approach that we used to decorate
`inverse` above:


```
def inverse(a):
    return npla.inv(a)

inverse = timeFunc(inverse)
invdata = inverse(data)
```


is semantically equivalent to this:


```
@timeFunc
def inverse(a):
    return npla.inv(a)

invdata = inverse(data)
```


<a class="anchor" id="decorators-on-methods"></a>
## Decorators on methods


Applying a decorator to the methods of a class works in the same way:


```
import numpy.linalg as npla

class MiscMaths(object):

    @timeFunc
    def inverse(self, a):
        return npla.inv(a)
```


Now, the `inverse` method of all `MiscMaths` instances will be timed:


```
mm1 = MiscMaths()
mm2 = MiscMaths()

i1 = mm1.inverse(np.random.random((1000, 1000)))
i2 = mm2.inverse(np.random.random((1500, 1500)))
```


Note that only one `timeFunc` decorator was created here - the `timeFunc`
function was only called once - when the `MiscMaths` class was defined.  This
might be clearer if we re-write the above code in the following (equivalent)
manner:


```
class MiscMaths(object):
    def inverse(self, a):
        return npla.inv(a)

MiscMaths.inverse = timeFunc(MiscMaths.inverse)
```


So only one `wrapperFunc` function exists, and this function is _shared_ by
all instances of the `MiscMaths` class - (such as the `mm1` and `mm2`
instances in the example above). In many cases this is not a problem, but
there can be situations where you need each instance of your class to have its
own unique decorator.


> If you are interested in solutions to this problem, take a look at the
> appendix on [per-instance decorators](#appendix-per-instance-decorators).


<a class="anchor" id="example-memoization"></a>
## Example - memoization


Let's move onto another example.
[Meowmoization](https://en.wikipedia.org/wiki/Memoization) is a common
performance optimisation technique used in cats. I mean software. Essentially,
memoization refers to the process of maintaining a cache for a function which
performs some expensive calculation. When the function is executed with a set
of inputs, the calculation is performed, and then a copy of the inputs and the
result are cached. If the function is called again with the same inputs, the
cached result can be returned.


This is a perfect problem to tackle with decorators:


```
def memoize(func):

    cache = {}

    def wrapper(*args):

        # is there a value in the cache
        # for this set of inputs?
        cached = cache.get(args, None)

        # If not, call the function,
        # and cache the result.
        if cached is None:
            cached      = func(*args)
            cache[args] = cached
        else:
            print('Cached {}({}): {}'.format(func.__name__, args, cached))

        return cached

    return wrapper
```


We can now use our `memoize` decorator to add a memoization cache to any
function.  Let's memoize a function which generates the $n^{th}$ number in the
[Fibonacci series](https://en.wikipedia.org/wiki/Fibonacci_number):


```
@memoize
def fib(n):

    if n in (0, 1):
        print('fib({}) = {}'.format(n, n))
        return 1

    twoback = 1
    oneback = 1
    val     = 0

    for _ in range(2, n):

        val     = oneback + twoback
        twoback = oneback
        oneback = val

    print('fib({}) = {}'.format(n, val))

    return val
```


For a given input, when `fib` is called the first time, it will calculate the
$n^{th}$ Fibonacci number:


```
for i in range(10):
    fib(i)
```


However, on repeated calls with the same input, the calculation is skipped,
and instead the result is retrieved from the memoization cache:


```
for i in range(10):
    fib(i)
```


> If you are wondering how the `wrapper` function is able to access the
> `cache` variable, refer to the [appendix on closures](#appendix-closures).


<a class="anchor" id="decorators-with-arguments"></a>
## Decorators with arguments


Continuing with our memoization example, let's say that we want to place a
limit on the maximum size that our cache can grow to. For example, the output
of our function might have large memory requirements, so we can only afford to
store a handful of pre-calculated results. It would be nice to be able to
specify the maximum cache size when we define our function to be memoized,
like so:


> ```
> # cache at most 10 results
> @limitedMemoize(10):
> def fib(n):
>     ...
> ```


In order to support this, our `memoize` decorator function needs to be
modified - it is currently written to accept a function as its sole argument,
but we need it to accept a cache size limit.


```
from collections import OrderedDict

def limitedMemoize(maxSize):

    cache = OrderedDict()

    def decorator(func):
        def wrapper(*args):

            # is there a value in the cache
            # for this set of inputs?
            cached = cache.get(args, None)

            # If not, call the function,
            # and cache the result.
            if cached is None:

                cached = func(*args)

                # If the cache has grown too big,
                # remove the oldest item. In practice
                # it would make more sense to remove
                # the item with the oldest access
                # time, but this is good enough for
                # an introduction!
                if len(cache) >= maxSize:
                    cache.popitem(last=False)

                cache[args] = cached
            else:
                print('Cached {}({}): {}'.format(func.__name__, args, cached))

            return cached
        return wrapper
    return decorator
```

> We used the handy
> [`collections.OrderedDict`](https://docs.python.org/3.5/library/collections.html#collections.OrderedDict)
> class here which preserves the insertion order of key-value pairs.


This is starting to look a little complicated - we now have _three_ layers of
functions. This is necessary when you wish to write a decorator which accepts
arguments (refer to the
[appendix](#appendix-decorators-without-arguments-versus-decorators-with-arguments)
for more details).


But this `limitedMemoize` decorator is used in essentially the same way as our
earlier `memoize` decorator:


```
@limitedMemoize(5)
def fib(n):

    if n in (1, 2):
        print('fib({}) = 1'.format(n))
        return 1

    twoback = 1
    oneback = 1
    val     = 0

    for _ in range(2, n):

        val     = oneback + twoback
        twoback = oneback
        oneback = val

    print('fib({}) = {}'.format(n, val))

    return val
```


Except that now, the `fib` function will only cache up to 5 values.


```
fib(10)
fib(11)
fib(12)
fib(13)
fib(14)
print('The result for 10 should come from the cache')
fib(10)
fib(15)
print('The result for 10 should no longer be cached')
fib(10)
```


<a class="anchor" id="chaining-decorators"></a>
## Chaining decorators


Decorators can easily be chained, or nested:


```
import time

@timeFunc
@memoize
def expensiveFunc(n):
    time.sleep(n)
    return n
```


> Remember that this is semantically equivalent to the following:
>
> ```
> def expensiveFunc(n):
>     time.sleep(n)
>     return n
>
> expensiveFunc = timeFunc(memoize(expensiveFunc))
> ```


Now we can see the effect of our memoization layer on performance:


```
expensiveFunc(0.5)
expensiveFunc(1)
expensiveFunc(1)
```


<a class="anchor" id="decorator-classes"></a>
## Decorator classes


By now, you will have gained the impression that a decorator is a function
which _decorates_ another function. But if you went through the practical on
operator overloading, you might remember the special `__call__` method, that
allows an object to be called as if it were a function.


This feature allows us to write our decorators as classes, instead of
functions. This can be handy if you are writing a decorator that has
complicated behaviour, and/or needs to maintain some sort of state which
cannot be easily or elegantly written using nested functions.


As an example, let's say we are writing a framework for unit testing. We want
to be able to "mark" our test functions like so, so they can be easily
identified and executed:


> ```
> @unitTest
> def testblerk():
>     """tests the blerk algorithm."""
>     ...
> ```


With a decorator like this, we wouldn't need to worry about where our tests
are located - they will all be detected because we have marked them as test
functions. What does this `unitTest` decorator look like?


```
class TestRegistry(object):

    def __init__(self):
        self.testFuncs = []

    def __call__(self, func):
        self.testFuncs.append(func)

    def listTests(self):
        print('All registered tests:')
        for test in self.testFuncs:
            print(' ', test.__name__)

    def runTests(self):
        for test in self.testFuncs:
            print('Running test {:10s} ... '.format(test.__name__), end='')
            try:
                test()
                print('passed!')
            except Exception as e:
                print('failed!')

# Create our test registry
registry = TestRegistry()

# Alias our registry to "unitTest"
# so that we can register tests
# with a "@unitTest" decorator.
unitTest = registry
```

So we've defined a class, `TestRegistry`, and created an instance of it,
`registry`, which will manage all of our unit tests. Now, in order to "mark"
any function as being a unit test, we just need to use the `unitTest`
decorator (which is simply a reference to our `TestRegistry` instance):


```
@unitTest
def testFoo():
    assert 'a' in 'bcde'

@unitTest
def testBar():
    assert 1 > 0

@unitTest
def testBlerk():
    assert 9 % 2 == 0
```


Now that these functions have been registered with our `TestRegistry`
instance, we can run them all:

```
registry.listTests()
registry.runTests()
```


> Unit testing is something which you must do! This is __especially__
> important in an interpreted language such as Python, where there is no
> compiler to catch all of your mistakes.
>
> Python has a built-in
> [`unittest`](https://docs.python.org/3.5/library/unittest.html) module,
> however the third-party [`pytest`](https://docs.pytest.org/en/latest/) and
> [`nose`](http://nose2.readthedocs.io/en/latest/) are popular.  It is also
> wise to combine your unit tests with
> [`coverage`](https://coverage.readthedocs.io/en/coverage-4.5.1/), which
> tells you how much of your code was executed, or _covered_ when your
> tests were run.


<a class="anchor" id="appendix-functions-are-not-special"></a>
## Appendix: Functions are not special


When we write a statement like this:


```
a = [1, 2, 3]
```


the variable `a` is a reference to a `list`. We can create a new reference to
the same list, and delete `a`:


```
b = a
del a
```


Deleting `a` doesn't affect the list at all - the list still exists, and is
now referred to by a variable called `b`.


```
print('b: ', b)
```

`a` has, however, been deleted:


```
print('a: ', a)
```


The variables `a` and `b` are just references to a list that is sitting in
memory somewhere - renaming or removing a reference does not have any effect
upon the list<sup>2</sup>.


If you are familiar with C or C++, you can think of a variable in Python as
like a `void *` pointer - it is just a pointer of an unspecified type, which
is pointing to some item in memory (which does have a specific type). Deleting
the pointer does not have any effect upon the item to which it was pointing.


> <sup>2</sup> Until no more references to the list exist, at which point it
> will be
> [garbage-collected](https://www.quora.com/How-does-garbage-collection-in-Python-work-What-are-the-pros-and-cons).


Now, functions in Python work in _exactly_ the same way as variables.  When we
define a function like this:


```
def inverse(a):
    return npla.inv(a)

print(inverse)
```


there is nothing special about the name `inverse` - `inverse` is just a
reference to a function that resides somewhere in memory. We can create a new
reference to this function:


```
inv2 = inverse
```


And delete the old reference:


```
del inverse
```


But the function still exists, and is still callable, via our second
reference:


```
print(inv2)
data    = np.random.random((10, 10))
invdata = inv2(data)
```


So there is nothing special about functions in Python - they are just items
that reside somewhere in memory, and to which we can create as many references
as we like.


> If it bothers you that `print(inv2)` resulted in
> `<function inverse at ...>`, and not `<function inv2 at ...>`, then refer to
> the appendix on
> [preserving function metdata](#appendix-preserving-function-metadata).


<a class="anchor" id="appendix-closures"></a>
## Appendix: Closures


Whenever we define or use a decorator, we are taking advantage of a concept
called a [_closure_][wiki-closure]. Take a second to re-familiarise yourself
with our `memoize` decorator function from earlier - when `memoize` is called,
it creates and returns a function called `wrapper`:


[wiki-closure]: https://en.wikipedia.org/wiki/Closure_(computer_programming)


```
def memoize(func):

    cache = {}

    def wrapper(*args):

        # is there a value in the cache
        # for this set of inputs?
        cached = cache.get(args, None)

        # If not, call the function,
        # and cache the result.
        if cached is None:
            cached      = func(*args)
            cache[args] = cached
        else:
            print('Cached {}({}): {}'.format(func.__name__, args, cached))

        return cached

    return wrapper
```


Then `wrapper` is executed at some arbitrary point in the future. But how does
it have access to `cache`, defined within the scope of the `memoize` function,
after the execution of `memoize` has ended?


```
def nby2(n):
    return n * 2

# wrapper function is created here (and
# assigned back to the nby2 reference)
nby2 = memoize(nby2)

# wrapper function is executed here
print('nby2(2): ', nby2(2))
print('nby2(2): ', nby2(2))
```


The trick is that whenever a nested function is defined in Python, the scope
in which it is defined is preserved for that function's lifetime. So `wrapper`
has access to all of the variables within the `memoize` function's scope, that
were defined at the time that `wrapper` was created (which was when we called
`memoize`).  This is why `wrapper` is able to access `cache`, even though at
the time that `wrapper` is called, the execution of `memoize` has long since
finished.


This is what is known as a
[_closure_](https://www.geeksforgeeks.org/python-closures/). Closures are a
fundamental, and extremely powerful, aspect of Python and other high level
languages. So there's your answer,
[fishbulb](https://www.youtube.com/watch?v=CiAaEPcnlOg).


<a class="anchor" id="appendix-decorators-without-arguments-versus-decorators-with-arguments"></a>
## Appendix: Decorators without arguments versus decorators with arguments


There are three ways to invoke a decorator with the `@` notation:


1. Naming it, e.g. `@mydecorator`
2. Calling it, e.g. `@mydecorator()`
3. Calling it, and passing it arguments, e.g. `@mydecorator(1, 2, 3)`


Python expects a decorator function to behave differently in the second and
third scenarios, when compared to the first:

```
def decorator(*args):
    print('  decorator({})'.format(args))
    def wrapper(*args):
        print('    wrapper({})'.format(args))
    return wrapper

print('Scenario #1: @decorator')
@decorator
def noop():
    pass

print('\nScenario #2: @decorator()')
@decorator()
def noop():
    pass

print('\nScenario #3: @decorator(1, 2, 3)')
@decorator(1, 2, 3)
def noop():
    pass
```


So if a decorator is "named" (scenario 1), only the decorator function
(`decorator` in the example above) is called, and is passed the decorated
function.


But if a decorator function is "called" (scenarios 2 or 3), both the decorator
function (`decorator`), __and its return value__ (`wrapper`) are called - the
decorator function is passed the arguments that were provided, and its return
value is passed the decorated function.


This is why, if you are writing a decorator function which expects arguments,
you must use three layers of functions, like so:


```
def decorator(*args):
    def realDecorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return realDecorator
```


> The author of this practical is angry about this, as he does not understand
> why the Python language designers couldn't allow a decorator function to be
> passed both the decorated function, and any arguments that were passed when
> the decorator was invoked, like so:
>
> ```
> def decorator(func, *args, **kwargs): # args/kwargs here contain
>                                       # whatever is passed to the
>                                       # decorator
>
>     def wrapper(*args, **kwargs):     # args/kwargs here contain
>                                       # whatever is passed to the
>                                       # decorated function
>          return func(*args, **kwargs)
>
>     return wrapper
> ```


<a class="anchor" id="appendix-per-instance-decorators"></a>
## Appendix: Per-instance decorators


In the section on [decorating methods](#decorators-on-methods), you saw
that when a decorator is applied to a method of a class,  that decorator
is invoked just once, and shared by all instances of the class. Consider this
example:


```
def decorator(func):
    print('Decorating {} function'.format(func.__name__))
    def wrapper(*args, **kwargs):
        print('Calling decorated function {}'.format(func.__name__))
        return func(*args, **kwargs)
    return wrapper

class MiscMaths(object):

    @decorator
    def add(self, a, b):
        return a + b
```


Note that `decorator` was called at the time that the `MiscMaths` class was
defined. Now, all `MiscMaths` instances share the same `wrapper` function:


```
mm1 = MiscMaths()
mm2 = MiscMaths()

print('1 + 2 =', mm1.add(1, 2))
print('3 + 4 =', mm2.add(3, 4))
```


This is not an issue in many cases, but it can be problematic in some. Imagine
if we have a decorator called `ensureNumeric`, which makes sure that arguments
passed to a function are numbers:


```
def ensureNumeric(func):
    def wrapper(*args):
        args = tuple([float(a) for a in args])
        return func(*args)
    return wrapper
```


This all looks well and good - we can use it to decorate a numeric function,
allowing strings to be passed in as well:


```
@ensureNumeric
def mul(a, b):
    return a * b

print(mul( 2,   3))
print(mul('5', '10'))
```


But what will happen when we try to decorate a method of a class?


```
class MiscMaths(object):

    @ensureNumeric
    def add(self, a, b):
        return a + b

mm = MiscMaths()
print(mm.add('5', 10))
```


What happened here?? Remember that the first argument passed to any instance
method is the instance itself (the `self` argument). Well, the `MiscMaths`
instance was passed to the `wrapper` function, which then tried to convert it
into a `float`.  So we can't actually apply the `ensureNumeric` function as a
decorator on a method in this way.


There are a few potential solutions here. We could modify the `ensureNumeric`
function, so that the `wrapper` ignores the first argument. But this would
mean that we couldn't use `ensureNumeric` with standalone functions.


But we _can_ manually apply the `ensureNumeric` decorator to `MiscMaths`
instances when they are initialised.  We can't use the nice `@ensureNumeric`
syntax to apply our decorators, but this is a viable approach:


```
class MiscMaths(object):

    def __init__(self):
        self.add = ensureNumeric(self.add)

    def add(self, a, b):
        return a + b

mm = MiscMaths()
print(mm.add('5', 10))
```


Another approach is to use a second decorator, which dynamically creates the
real decorator when it is accessed on an instance. This requires the use of an
advanced Python technique called
[_descriptors_](https://docs.python.org/3.5/howto/descriptor.html), which is
beyond the scope of this practical. But if you are interested, you can see an
implementation of this approach
[here](https://git.fmrib.ox.ac.uk/fsl/fslpy/blob/1.6.8/fsl/utils/memoize.py#L249).


<a class="anchor" id="appendix-preserving-function-metadata"></a>
## Appendix: Preserving function metadata


You may have noticed that when we decorate a function, some of its properties
are lost. Consider this function:


```
def add2(a, b):
    """Adds two numbers together."""
    return a + b
```


The `add2` function is an object which has some attributes, e.g.:


```
print('Name: ', add2.__name__)
print('Help: ', add2.__doc__)
```


However, when we apply a decorator to `add2`:


```
def decorator(func):
    def wrapper(*args, **kwargs):
        """Internal wrapper function for decorator."""
        print('Calling decorated function {}'.format(func.__name__))
        return func(*args, **kwargs)
    return wrapper


@decorator
def add2(a, b):
    """Adds two numbers together."""
    return a + b
```


Those attributes are lost, and instead we get the attributes of the `wrapper`
function:


```
print('Name: ', add2.__name__)
print('Help: ', add2.__doc__)
```


While this may be inconsequential in most situations, it can be quite annoying
in some, such as when we are automatically [generating
documentation](http://www.sphinx-doc.org/) for our code.


Fortunately, there is a workaround, available in the built-in
[`functools`](https://docs.python.org/3.5/library/functools.html#functools.wraps)
module:


```
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Internal wrapper function for decorator."""
        print('Calling decorated function {}'.format(func.__name__))
        return func(*args, **kwargs)
    return wrapper

@decorator
def add2(a, b):
    """Adds two numbers together."""
    return a + b
```


We have applied the `@functools.wraps` decorator to our internal `wrapper`
function - this will essentially replace the `wrapper` function metdata with
the metadata from our `func` function. So our `add2` name and documentation is
now preserved:


```
print('Name: ', add2.__name__)
print('Help: ', add2.__doc__)
```


<a class="anchor" id="appendix-class-decorators"></a>
## Appendix: Class decorators


> Not to be confused with [_decorator classes_](#decorator-classes)!


In this practical, we have shown how decorators can be applied to functions
and methods. But decorators can in fact also be applied to _classes_. This is
a fairly niche feature that you are probably not likely to need, so we will
only cover it briefly.


Imagine that we want all objects in our application to have a globally unique
(within the application) identifier. We could use a decorator which contains
the logic for generating unique IDs, and defines the interface that we can
use on an instance to obtain its ID:


```
import random

allIds = set()

def uniqueID(cls):
    class subclass(cls):
        def getUniqueID(self):

            uid = getattr(self, '_uid', None)

            if uid is not None:
                return uid

            while uid is None or uid in set():
                uid = random.randint(1, 100)

            self._uid = uid
            return uid

    return subclass
```


Now we can use the `@uniqueID` decorator on any class that we need to
have a unique ID:

```
@uniqueID
class Foo(object):
    pass

@uniqueID
class Bar(object):
    pass
```


All instances of these classes will have a `getUniqueID` method:


```
f1 = Foo()
f2 = Foo()
b1 = Bar()
b2 = Bar()

print('f1: ', f1.getUniqueID())
print('f2: ', f2.getUniqueID())
print('b1: ', b1.getUniqueID())
print('b2: ', b2.getUniqueID())
```


<a class="anchor" id="useful-references"></a>
## Useful references


* [Understanding decorators in 12 easy steps](http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/)
* [The decorators they won't tell you about](https://github.com/hchasestevens/hchasestevens.github.io/blob/master/notebooks/the-decorators-they-wont-tell-you-about.ipynb)
* [Closures - Wikipedia][wiki-closure]
* [Closures in Python](https://www.geeksforgeeks.org/python-closures/)
* [Garbage collection in Python](https://www.quora.com/How-does-garbage-collection-in-Python-work-What-are-the-pros-and-cons)

[wiki-closure]: https://en.wikipedia.org/wiki/Closure_(computer_programming)
