# Operator overloading


> This practical assumes you are familiar with the basics of object-oriented
> programming in Python.


Operator overloading, in an object-oriented programming language, is the
process of customising the behaviour of _operators_ (e.g. `+`, `*`, `/` and
`-`) on user-defined types. This practical aims to show you that operator
overloading is __very__ easy to do in Python.


## Overview


In Python, when you add two numbers together:


```
a = 5
b = 10
r = a + b
print(r)
```


What actually goes on behind the scenes is this:


```
r = a.__add__(b)
print(r)
```


In other words, whenever you use the `+` operator on two variables (the
operands to the `+` operator), the Python interpreter calls the `__add__`
method of the first operand (`a`), and passes the second operand (`b`) as an
argument.


So it is very easy to use the `+` operator with our own classes - all we have
to do is implement a method called `__add__`.


## Arithmetic operators


Let's play with an example - a class which represents a 2D vector:


```
class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Vector({}, {})'.format(self.x, self.y)
```


> Note that we have implemented the special `__str__` method, which allows our
> `Vector` instances to be converted into strings.


If we try to use the `+` operator on this class, we are bound to get an error:


```
v1 = Vector(2, 3)
v2 = Vector(4, 5)
print(v1 + v2)
```


But all we need to do to support the `+` operator is to implement a method
called `__add__`:


```
class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Vector({}, {})'.format(self.x, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x,
                      self.y + other.y)
```


And now we can use `+` on `Vector` objects - it's that easy:


```
v1 = Vector(2, 3)
v2 = Vector(4, 5)
print('{} + {} = {}'.format(v1, v2, v1 + v2))
```


Our `__add__` method creates and returns a new `Vector` which contains the sum
of the `x` and `y` components of the `Vector` on which it is called, and the
`Vector` which is passed in.  We could also make the `__add__` method work
with scalars, by extending its definition a bit:


```
class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x,
                          self.y + other.y)
        else:
            return Vector(self.x + other, self.y + other)

    def __str__(self):
        return 'Vector({}, {})'.format(self.x, self.y)
```


So now we can add both `Vectors` and scalars numbers together:


```
v1 = Vector(2, 3)
v2 = Vector(4, 5)
n  = 6

print('{} + {} = {}'.format(v1, v2, v1 + v2))
print('{} + {} = {}'.format(v1, n,  v1 + n))
```


Other nuemric and logical operators can be supported by implementing the
appropriate method, for example:

- Multiplication (`*`): `__mul__`
- Division (`/`): `__div__`
- Negation (`-`): `__neg__`
- In-place addition (`+=`): `__iadd__`
- Exclusive or (`^`): `__xor__`


Take a look at the [official
documentation](https://docs.python.org/3.5/reference/datamodel.html#emulating-numeric-types)
for a full list of the arithmetic and logical operators that your classes can
support.


## Equality and comparison operators


Adding support for equality (`==`, `!=`) and comparison (e.g. `>=`) operators
is just as easy. Imagine that we have a class called `Label`, which represents
a label in a lookup table. Our `Label` has an integer label, a name, and an
RGB colour:


```
class Label(object):
    def __init__(self, label, name, colour):
        self.label  = label
        self.name   = name
        self.colour = colour
```


In order to ensure that a list of `Label` objects is ordered by their label
values, we can implement a set of functions, so that `Label` classes can be
compared using the standard comparison operators:


```
import functools

@functools.total_ordering
class Label(object):
    def __init__(self, label, name, colour):
        self.label  = label
        self.name   = name
        self.colour = colour

    def __str__(self):
        rgb = ''.join(['{:02x}'.format(c) for c in self.colour])
        return 'Label({}, {}, #{})'.format(self.label, self.name, rgb)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.label == other.label

    def __lt__(self, other):
        return self.label < other.label
```

> We also added `__str__` and `__repr__` methods to the `Label` class so that
> `Label` instances will be printed nicely.


Now we can compare and sort our `Label` instances:


```
l1 = Label(1, 'Parietal',  (255,   0,   0))
l2 = Label(2, 'Occipital', (  0, 255,   0))
l3 = Label(3, 'Temporal',  (  0,   0, 255))

print('{} >  {}: {}'.format(l1, l2, l1  > l2))
print('{} <  {}: {}'.format(l1, l3, l1  < l3))
print('{} != {}: {}'.format(l2, l3, l2 != l3))
print(sorted((l3, l1, l2)))
```


The `@functools.total_ordering` is a convenience decorator which, given a
class that implements equality and a single comparison function (`__lt__` in
the above code), will "fill in" the remainder of the comparison operators.  If
you need very specific or complicated behaviour, then you can provide methods
for _all_ of the comparison operators, e.g. `__gt__` for `>`, `__ge__` for
`>=`, etc.).


But if you just want the operators to work in the conventional manner, you can
just use the `@functools.total_ordering` decorator, and provide `__eq__`, and
just one of `__lt__`, `__le__`, `__gt__` or `__ge__`.


Refer to the [official
documentation](https://docs.python.org/3.5/reference/datamodel.html#object.__lt__)
for all of the details on supporting comparison operators.


> You may see the `__cmp__` method in older code bases - this provides a
> C-style comparison function which returns `<0`, `0`, or `>0` based on
> comparing two items. This has been superseded by the rich
> comparison operators and is no longer used in Python 3.


## The indexing operator `[]`


The indexing operator (`[]`) is generally used by "container" types, such as
the built-in `list` and `dict` classes.


At its essence, there are only three types of behaviours that are possible
with the `[]` operator. All that is needed to support them are to implement
three special methods in your class, regardless of whether your class will be
indexed by sequential integers (like a `list`) or by hashable values (like a
`dict`):


- __Retrieval__ is performed by the `__getitem__` method
- __Assignment__ is performed by the `__setitem__` method
- __Deletion__ is performed by the `__delitem__` method


Note that, if you implement these methods in your own class, there is no
requirement for them to actually provide any form. However if you don't, you
will probably confuse users of your code - make sure you explain it all in
your comprehensive documentation!


The following contrived example demonstrates all three behaviours:


```
class TwoTimes(object):

    def __init__(self):
        self.__deleted  = set()
        self.__assigned = {}

    def __getitem__(self, key):
        if key in self.__deleted:
            raise KeyError('{} has been deleted!')
        elif key in self.__assigned:
            return self.__assigned[key]
        else:
            return key * 2

    def __setitem__(self, key, value):
        self.__assigned[key] = value

    def __delitem__(self, key):
        self.__deleted.add(key)
```


Guess what happens whenever we index a `TwoTimes` object:


```
tt = TwoTimes()
print('TwoTimes[{}] = {}'.format(2,     tt[2]))
print('TwoTimes[{}] = {}'.format(6,     tt[6]))
print('TwoTimes[{}] = {}'.format('abc', tt['abc']))
```


For some unknown reason, the `TwoTimes` class allows us to override the value
for a specific key:


```
print(tt[4])
tt[4] = 'this is not 4 * 4'
print(tt[4])
```


And we can also "delete" keys:


```
print(tt['12345'])
del tt['12345']

# this is going to raise an error
print(tt['12345'])
```


If you wish to support the Python `start:stop:step` [slice
notation](https://www.pythoncentral.io/how-to-slice-listsarrays-and-tuples-in-python/),
you simply need to write your `__getitem__` and `__setitem__` methods so that they
can detect `slice` objects:


```
class TwoTimes(object):

    def __init__(self, max):
        self.__max = max

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start or 0
            stop  = key.stop  or self.__max
            step  = key.step  or 1
        else:
            start = key
            stop  = key + 1
            step  = 1

        return [i * 2 for i in range(start, stop, step)]
```

```
tt = TwoTimes(10)

print(tt[5])
print(tt[3:7])
print(tt[::2])
```




> It is possible to sub-class the built-in `list` and `dict` classes if you
> wish to extend their functionality in some way. However, if you are writing
> a class that should mimic the one of the `list` or `dict` classes, but work
> in a different way internally (e.g. a `dict`-like object which uses a
> different hashing algorithm), the `Sequence` and `MutableMapping` classes
> are [a better choice](https://stackoverflow.com/a/7148602) - you can find
> them in the
> [`collections.abc`](https://docs.python.org/3.5/library/collections.abc.html)
> module.


## The call operator `()`


Remember how everything in Python is an object, even functions? When you call
a function, a method called `__call__` is called on the function object. We can
implement the `__call__` method on our own class, which will allow us to "call"
objects as if they are functions.


For example, the `TimedFunction` class allows us to calculate the execution
time of any function:


## The dot operator `.`


Python allows us to override the `.` (dot) operator which is used to access
the attributes and methods of an object.  attributes and methods of an
object. This is a fairly niche feature, and you need to be careful that you
don't unintentionally introduce recursive attribute lookups into your code.





```
class Vector(object):
    def __init__(self, xyz):
        self.__xyz = list(xyz)

    def __str__(self):
        return 'Vector({})'.format(', '.join(self.__xyz))

    def __getattr__(self, key):
        key = ['xyz'.index(c) for c in key]
        return [self.__xyz[c] for c in key]

    def __setattr__(self, key, value):
        pass        # key = ['xyz'.index(c) for c in key]
```


```
v = Vector((4, 5, 6))

print('xyz: ', v.xyz)
print('yz:  ', v.yz)
print('zxy: ', v.xzy)
print('y:   ', v.y)
```


## Other special methods
