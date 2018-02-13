# Decorators


Remember that in Python, everything is an object, including functions. This
means that we can do things like:


- Pass a function as an argument to another function.
- Create/define a function inside another function.
- Write a function which returns another function.


These abilities mean that we can do some neat things with functions in Python.


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


Ok, this looks like it might do the trick:


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


The `timeFunc` function is given a function as its sole argument. It then
creates and returns a new function, `wrapperFunc`. This `wrapperFunc` function
calls and times the function that was passed to `timeFunc`<sup>1</sup>.  But
note that when `timeFunc` is called, `wrapperFunc` is _not_ called - it is
only created and returned.


> <sup>1</sup> If you are wondering how the `wrapperFunc` is able to access
> the `func` argument, refer to the [appendix on
> closures](#appendix-closures).


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

1. We defined a function called `inverse`,
2. We passed the `inverse` function to the `timeFunc` function
3. We re-assigned the return value of `timeFunc` back to `inverse`.


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
[appendix](appendix-decorators-without-arguments-versus-decorators-with-arguments)
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
expensiveFunc(1)
expensiveFunc(2)
expensiveFunc(2)
```


## Decorator classes

> not to be confused with _class decorators_ - see the
> [appendix](#appendix-class-decorators)






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
like a `void *` pointer - it is just a pointer of an undefined type, which is
pointing to some item in memory (which does have a specific type). Deleting
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
> `<function inverse at ...>`, and not `<function inv2 at ...>`, then keep
> going straight through to the
> [next appendix](#appendix-preserving-function-metadata).


## Appendix: Preserving function metadata


TODO `functools.wraps`


## Appendix: Closures



Whenever we define or use a decorator, we are taking advantage of a concept
called a [_closure_](https://www.geeksforgeeks.org/python-closures/). Take a
second to re-familiarise yourself with our `timeFunc` decorator function from
earlier - when `timeFunc` is called, it creates and returns `wrapperFunc`:


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


Then `wrapperFunc` is executed at some arbitrary point in the future. But how
does it have access to `func`, defined within the scope of the `timeFunc`
function, after the execution of `timeFunc` has ended?


```
def pause(secs):
    print('Pausing for {} seconds ...'.format(secs))
    time.sleep(secs)
    print('Finished pausing')

# wrapperFunc is created here
pause = timeFunc(pause)

# wrapperFunc is executed here
pause(2)
```


The trick is that whenever a nested function is defined in Python, the scope
in which it is defined is preserved for that function's lifetime. So
`wrapperFunc` has access to all of the variables within the `timeFunc`
function's scope, that were defined at the time that `wrapperFunc` was created
(which was when we called `timeFunc`).  This is why `wrapperFunc` is able to
access `func`, even though at the time that `wrapperFunc` is called, the
execution of `timeFunc` has long since finished.


This is what is known as a _closure_. Closures are a fundamental, and
extremely powerful, aspect of Python and other high level languages such as
Javascript. So there's your answer,
[fishbulb](https://www.youtube.com/watch?v=CiAaEPcnlOg).


## Appendix: Decorators without arguments versus decorators with arguments


There are three ways to invoke a decorator with the `@` notation:


1. Naming it (e.g. `@mydecorator`)
2. Calling it (e.g. `@mydecorator()`)
3. Calling it, and passing it arguments (e.g. `@mydecorator(1, 2, 3)`)


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


## Appendix: class decorators


TODO


## Useful references


* [Decorator tutorial](http://blog.thedigitalcatonline.com/blog/2015/04/23/python-decorators-metaprogramming-with-style/)
* [Another decorator tutorial](https://realpython.com/blog/python/primer-on-python-decorators/)
* [Closures in Python](https://www.geeksforgeeks.org/python-closures/)
* [Garbage collection in Python](https://www.quora.com/How-does-garbage-collection-in-Python-work-What-are-the-pros-and-cons)
