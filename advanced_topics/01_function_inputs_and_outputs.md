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

You can think of the star operator as _unpacking_ the contents of the
sequence.


## Keyword arguments


Using keyword arguments allows us to pass arguments to a function in any order
we like.  We could just as easily call our `myfunc` function like so, and get
the same result that we did earlier when using positional arguments:


```
myfunc(c=3, b=2, a=1)
```


Python has another operator - the double-star (`**`), which will unpack
keyword arguments from a `dict`. For example:

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
def myfunc(a=1, b=2, c=3):
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


__WARNING:__ _Never_ define a function with a mutable default value, such as a
`list`, `dict` or other non-primitive type. Let's see what happens when we do:


```
def badfunc(a=[]):
    a.append('end of sequence')
    output = ', '.join([str(elem) for elem in a])
    print(output)
```


With this function, all is well and good if we pass in our own value for `a`:


```
badfunc([1, 2, 3, 4])
badfunc([2, 4, 6])
```


But what happens when we let `badfunc` use the default value for `a`?


```
badfunc()
badfunc()
badfunc()
```


This happens because default argument values are created when the function is
defined, and will persist for the duration of your program. So in this
example, the default value for `a`, a Python `list`, gets created when
`badfunc` is defined, and hangs around for the lifetime of the `badfunc`
function!


## Variable numbers of arguments - `args` and `kwargs`


The `*` and `**` operators can also be used in function definitions - this
indicates that a function may accept a variable number of arguments.


Let's redefine `myfunc` to accept any number of positional arguments - here,
all positional arguments will be passed into `myfunc` as a tuple called
`args`:


```
def myfunc(*args):
    print('myfunc({})'.format(args))
    print('  Number of arguments: {}'.format(len(args)))
    for i, arg in enumerate(args):
        print('  Argument {:2d}: {}'.format(i, arg))

myfunc()
myfunc(1)
myfunc(1, 2, 3)
myfunc(1, 'a', [3, 4])
```


Similarly, we can define a function to accept any number of keyword
arguments. In this case, the keyword arguments will be packed into a `dict`
called `kwargs`:


```
def myfunc(**kwargs):
    print('myfunc({})'.format(kwargs))
    for k, v in kwargs.items():
        print('  Argument {} = {}'.format(k, v))

myfunc()
myfunc(a=1, b=2)
myfunc(a='abc', foo=123)
```


This is a useful technique in many circumstances. For example, if you are
writing a function which calls another function that takes many arguments, you
can use ``**kwargs`` to pass-through arguments to the second function.  As an
example, let's say we have functions `flirt` and `fnirt`, which respectively
perform linear and non-linear registration:


```
def flirt(infile,
          ref,
          outfile=None,
          init=None,
          omat=None,
          dof=12):
    # TODO get MJ to fill this bit in
    pass

def fnirt(infile,
          ref,
          outfile=None,
          aff=None,
          interp='nn',
          refmask=None,
          minmet='lg',
          subsamp=4):
    # TODO get Jesper to fill this bit in
    pass
```


We want to write our own registration function which uses the `flirt` and
`fnirt` functions, while also allowing the `fnirt` parameters to be
customised. We can use `**kwargs` to do this:


```
def do_nonlinear_reg(infile, ref, outfile, **kwargs):
    """Aligns infile to ref using non-linear registration. All keyword
    arguments are passed through to the fnirt function.
    """

    affmat = '/tmp/aff.mat'

    # calculate a rough initial linear alignemnt
    flirt(infile, ref, omat=affmat)

    fnirt(infile, ref, outfile, aff=affmat, **kwargs)
```
