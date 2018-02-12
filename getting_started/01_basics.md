# Basic python

This tutorial is aimed at briefly introducing you to the main language
features of python, with emphasis on some of the common difficulties
and pitfalls that are commonly encountered when moving to python.

When going through this make sure that you _run_ each code block
and look at the output, as these are crucial for understanding the
explanations. You can run each block by using _shift + enter_ (including the text blocks, so you can just move down the document with shift + enter).

---

# Basic types

Python has many different types and variables are dynamic and can change types (like MATLAB).  Some of the most commonly used in-built types are:
* integer and floating point scalars
* strings
* tuples
* lists
* dictionary

N-dimensional arrays and other types are supported through common modules (e.g., numpy, scipy, scikit-learn).  These will be covered in a subsequent exercise.

```
a = 4
b = 3.6
c = 'abc'
d = [10, 20, 30]
e = {'a' : 10, 'b': 20}
print(a)
```

Any variable or combination of variables can be printed using the function `print()`:
```
print(d)
print(e)
print(a, b, c)
```

> _*Python 3 versus python 2*_:
>
>   Print - for the print statement the brackets are compulsory for *python 3*, but are optional in python 2.  So you will see plenty of code without the brackets but you should never use `print` without brackets, as this is incompatible with Python 3.
>
>   Division - in python 3 all  division is floating point (like in MATLAB), even if the values are integers, but in python 2 integer division works like it does in C.

---

## Strings

Strings can be specified using single quotes *or* double quotes - as long as they are matched.
Strings can be indexed like lists (see later).

For example:
```
s1 = "test string"
s2 = 'another test string'
print(s1, ' :: ', s2)
```

You can also use triple quotes to capture multi-line strings.  For example:
```
s3 = '''This is
a string over
multiple lines
'''
print(s3)
```

### Format

More interesting strings can be created using the `format` statement, which is very useful in print statements:
```
x = 1
y = 'PyTreat'
s = 'The numerical value is {} and a name is {}'.format(x, y)
print(s)
print('A name is {} and a number is {}'.format(y, x))
```

There are also other options along these lines, but this is the more modern version, although you will see plenty of the other alternatives in old code (i.e., code written before last week). 

### String manipulation

The methods `lower()` and `upper()` are useful for strings.  For example:
```
s = 'This is a Test String'
print(s.upper())
print(s.lower())
```

Another useful method is:
```
s = 'This is a Test String'
s2 = s.replace('Test', 'Better')
print(s2)
```

If you like regular expressions then you're in luck as these are well supported in python using the `re` module.  To use this (like many other "extensions" - called _modules_ in Python - you need to `import` it).  For example:
```
import re
s = 'This is a test of a Test String'
s1 = re.sub(r'a [Tt]est', "an example", s)
print(s1)
```
where the `r` before the quote is used to force the regular expression specification to be a `raw string`.

For more information on matching and substitutions, look up the regular expression module on the web.


You can also split, or tokenize, a string (to turn it into a list) like this:
```
print(s.split())
```

> Note that strings in python 3 are _unicode_ so can represent Chinese characters, etc, and is therefore very flexible.  However, in general you can just be blissfully ignorant of this fact.

---

## Tuples and Lists

Both tuples and lists are builtin python types and are like vectors, 
but for numerical vectors and arrays it is much better to use _numpy_
arrays (or matrices), which are covered in a later tutorial.

A tuple is like a list or a vector, but with less flexibility than a full list, however anything can be stored in either a list or tuple, without any consistency being required.  For example:
```
xtuple = (3, 7.6, 'str')
xlist = [1, 'mj', -5.4]
print(xtuple)
print(xlist)
```

They can also be nested:
```
x2 = (xtuple, xlist)
x3 = [xtuple, xlist]
print('x2 is: ', x2)
print('x3 is: ', x3)
```

### Adding to a list

This is easy:
```
a = [10, 20, 30]
a = a + [70]
a +=  [80]
print(a)
```

### Indexing

Square brackets are used to index tuples, lists, dictionaries, etc.  For example:
```
d = [10, 20, 30]
print(d[1])
```

> _*Pitfall:*_
>  Python uses zero-based indexing, unlike MATLAB

```
a = [10, 20, 30, 40, 50, 60]
print(a[0])
print(a[2])
```

Indices naturally run from 0 to N-1, _but_ negative numbers can be used to reference from the end (circular wrap-around). 
```
print(a[-1])
print(a[-6])
```

However, this is only true for -1 to -N.  Outside of -N to N-1 will generate an `index out of range` error.
```
print(a[-7])
```
```
print(a[6])
```

Length of a tuple or list is given by the `len()` function:
```
print(len(a))
```

Nested lists can have nested indexing:
```
b = [[10, 20, 30], [40, 50, 60]]
print(b[0][1])
print(b[1][0])
```
but *not* an index like b[0, 1].

> Note that `len` will only give the length of the top level.
> In general, numpy arrays should be preferred to nested lists when the contents are numerical.

### Slicing

A range of values for the indices can be specified to extract values from a list.  For example:
```
print(a[0:3])
```

> _*Pitfall:*_
>
>  Slicing syntax is different from MATLAB in that second number is
>  exclusive (i.e., one plus final index) - this is in addition to the zero index difference.

```
a = [10, 20, 30, 40, 50, 60]
print(a[0:3])    # same as a(1:3) in MATLAB
print(a[1:3])    # same as a(2:3) in MATLAB
```

> _*Pitfall:*_
>
>  Unlike in MATLAB, you cannot use a list as indices instead of an
>  integer or a slice (although these can be done in _numpy_).

```
b = [3, 4]
print(a[b])
```

### List operations

Multiplication can be used with lists, where multiplication implements replication.

```
d = [10, 20, 30]
print(d * 4)
```

There are also other operations such as:
```
d.append(40)
print(d)
d.remove(20)
print(d)
d.pop(0)
print(d)
```

### Looping over elements in a list (or tuple)

```
d = [10, 20, 30]
for x in d:
    print(x)
```

> Note that the indentation within the loop is _*crucial*_.  All python control blocks are delineated purely by indentation.

### Getting help

The function `help()` can be used to get information about any variable/object/function in python.   It lists the possible operations. In `ipython` you can also just type `?<blah>` or `<blah>?` instead:

```
help(d)
```


There is also a `dir()` function that gives a basic listing of the operations:

```
dir(d)
```


> Note that google is often more helpful!

---

## Dictionaries

These store key-value pairs.  For example:
```
e = {'a' : 10, 'b': 20}
print(len(e))
print(e.keys())
print(e.values())
print(e['a'])
```

The keys and values can take on almost any type, even dictionaries!
Python is nothing if not flexible.  However, each key must be unique
and the dictionary must be "hashable".

### Adding to a dictionary

This is very easy:
```
e['c'] = 555   # just like in Biobank!  ;)
print(e)
```


### Removing elements from a dictionary

There are two main approaches - `pop` and `del`:
```
e.pop('b')
print(e)
del e['c']
print(e)
```

### Looping over everything in a dictionary

Several variables can jointly work as loop variables in python, which is very convenient.  For example:
```
e = {'a' : 10, 'b': 20, 'c':555}
for k, v in e.items():
   print((k, v))
```

The print statement here constructs a tuple, which is often used in python.

Another option is:
```
for k in e:
    print((k, e[k]))
```

> Note that in both cases the order is arbitrary. The `sorted` function can be used if you want keys in a sorted order; e.g. `for k in sorted(e):` ...
>
> There are also other options if you want a dictionary with ordering.

---

## Copying and references 

In python there are immutable types (e.g. numbers) and mutable types (e.g. lists). The main thing to know is that assignment can sometimes create separate copies and sometimes create references (as in C++). In general, the more complicated types are assigned via references. For example:
```
a = 7
b = a
a = 2348
print(b)
```

As opposed to:
```
a = [7]
b = a
a[0] = 8888
print(b)
```

But if an operation is performed then a copy might be made:
```
a = [7]
b = a * 2
a[0] = 8888
print(b)
```

If an explicit copy is necessary then this can be made using the `list()` constructor:
```
a = [7]
b = list(a)
a[0] = 8888
print(b)
```

There is a constructor for each type and this con be useful for converting between types:
```
xt = (2, 5, 7)
xl = list(xt)
print(xt)
print(xl)
```

> _*Pitfall:*_
>
> When writing functions you need to be particularly careful about references and copies.

```
def foo1(x):
   x.append(10)
def foo2(x):
   x = x + [10]
def foo3(x):
   return x + [10]

a = [5]
print(a)
foo1(a)
print(a)
foo2(a)
print(a)
foo3(a)
print(a)
```

---

## Control flow

### Boolean operators

There is a boolean type in python that can be `True` or `False` (note the capitals). Other values can also be used for True or False (e.g., 1 for True; 0 or None or [] or {} or "") although they are not considered 'equal' in the sense that the operator `==` would consider them the same.

Relevant boolean and comparison operators include: `not`, `and`, `or`, `==` and `!=`

For example:
```
a = True
print('Not a is:', not a)
print('Not 1 is:', not 1)
print('Not 0 is:', not 0)
print('Not {} is:', not {})
print('{}==0 is:', {}==0)
```

There is also the `in` test for strings, lists, etc:
```
print('the' in 'a number of words')
print('of' in 'a number of words')
print(3 in [1, 2, 3, 4])
```


### If statements

The basic syntax of `if` statements is fairly standard, though don't forget that you _*must*_ indent the statements within the conditional/loop block as this is the way of delineating blocks of code in python.  For example:
```
import random
a = random.uniform(-1, 1)
print(a)
if a>0:
   print('Positive')
elif a<0:
   print('Negative')
else:
   print('Zero')
```

Or more generally:
```
a = []    # just one of many examples
if not a:
   print('Variable is true, or at least not empty')
```
This can be useful for functions where a variety of possible input types are being dealt with. 

---

### For loops

The `for` loop works like in bash:
```
for x in [2, 'is', 'more', 'than', 1]:
   print(x)
```
where a list or any other sequence (e.g. tuple) can be used.

If you want a numerical range then use:
```
for x in range(2, 9):
  print(x)
```
Note that, like slicing, the maximum value is one less than the value specified.  Also, `range` actually returns an object that can be iterated over but is not just a list of numbers. If you want a list of numbers then `list(range(2, 9))` will give you this.

A very nice feature of python is that multiple variables can be assigned from a tuple or list:
```
x, y = [4, 7]
print(x)
print(y)
```

and this can be combined with a function called `zip` to make very convenient dual variable loops:
```
alist = ['Some', 'set', 'of', 'items']
blist = list(range(len(alist)))
print(list(zip(alist, blist)))
for x, y in zip(alist, blist):
   print(y, x)
```

This type of loop can be used with any two lists (or similar) to iterate over them jointly.

### While loops

The syntax for this is pretty standard:
```
import random
n = 0
x = 0
while n<100:
   x += random.uniform(0, 1)**2   # where ** is a power operation
   if x>50:
      break
   n += 1
print(x)
```

You can also use `continue` as in other languages.

---

### A quick intro to conditional expressions and list comprehensions

These are more advanced bits of python but are really useful and common, so worth having a little familiarity with at this stage.

#### Conditional expressions

A general expression that can be used in python is: A `if` condition `else` B

For example:
```
import random
x = random.uniform(0, 1)
y = x**2 if x<0.5 else (1 - x)**2
print(x, y)
```


#### List comprehensions

This is a shorthand syntax for building a list like a for loop but doing it in one line, and is very popular in python.  It is quite similar to mathematical set notation.  For example:
```
v1 = [ x**2 for x in range(10) ]
print(v1)
v2 = [ x**2 for x in range(10) if x!=7 ]
print(v2)
```

You'll find that python programmers use this kind of construction _*a lot*_.





