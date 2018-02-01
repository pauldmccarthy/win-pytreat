# Function inputs and outputs


In Python, arguments to a function can be specified in two different ways - by
using _positional_ arguments, or by using _keyword_ arguments.


## Positional arguments


Let's say we have a function that looks like this


```
def myfunc(a, b, c):
   print('First argument: ', a)
   print('Second argument:', b)
   print('Third argument: ', c)
```


If we call this function like so:


```
myfunc(1, 2, 3)
```


The values `1`, `2` and `3` get assigned to arguments `a`, `b`, and `c`
respectively, based on the position in which they are passed.


Python allows us to pass positional arguments into a function from a sequence,
using the star (`*`) operator. So we could store our arguments in a list or
tuple, and then pass the list straight in:

```
args = [3, 4, 5]
myfunc(*args)
```

You can think of the star operator as 'unpacking' the contents of the
sequence.


## Keyword arguments


Using keyword arguments allows us to pass arguments to a function in any order
we like.  We could just as easily call our `myfunc` function like so, and get
the same result that we did earlier when using positional arguments:


```
myfunc(c=3, b=2, a=1)
```


Python has another operator - the double-star (`**`), which will unpack
keyword arguments from `dict`. For example:

```
kwargs = {'a' : 4, 'b' : 5, 'c' : 6}
myfunc(**kwargs)
```


## Combining positional and keyword arguments


In fact, we can use both of these techniques at once, like so:

```
args   = (100, 200)
kwargs = {'c' : 300}

myfunc(*args, **kwargs)
```


## Default argument values


Function arguments can be given default values, like so:


```
myfunc(a=1, b=2, c=3):
    print('First argument: ', a)
    print('Second argument:', b)
    print('Third argument: ', c)
```


Now we can call `myfunc`, only passing the arguments that we need to. The
arguments which are unspecified in the function call will be assigned their
default value:


```
myfunc()
myfunc(10)
myfunc(10, b=30)
myfunc(c=300)
```


> Pitfall: mutable argument values


You can see here that
