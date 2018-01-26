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
d = [10,20,30]
e = {'a' : 10, 'b': 20}
```

Any variable can be printed using the function `print()`:
```
print(d)
print(e)
```

> _*Python 3 versus python 2*_:
>
>   Print - for the print statement the brackets are compulsory for *python 3*, but are optional in python 2.  So you will see plenty of code without the brackets but you should get into the habit of using them.
>
>   Division - in python 3 all  division is floating point (like in MATLAB), even if the values are integers, but in python 2 integer division works like it does in C.

---

## Strings

Strings can be specified using single quotes *or* double quotes - as long as they are matched.
Strings can be dereferenced like lists (see later).

For example:
```
s1="test string"
s2='another test string'
```

You can also use triple quotes to capture multi-line strings.  For example:
```
s3='''This is
a string over
multiple lines
'''
print(s3)
```

---

## Tuples and Lists

A tuple is like a list or a vector, but with less flexibility than a full list, however anything can be stored in either a list or tuple, without any consistency being required.  For example:
```
xtuple=(3, 7.6, 'str')
xlist=[1,'mj',-5.4]
```

They can also be nested:
```
x2=(xtuple,xlist)
x3=[xtuple,xlist]
print(x2)
print(x3)
```

### Adding to a list

This is easy:
```
a = [10,20,30]
a = a + [70]
a += [80]
print(a)
```

### Dereferencing

Square brackets are used to dereference tuples, lists, dictionaries, etc.  For example:
```
d = [10,20,30]
print(d[1])
```

> _*Pitfall:*_
>  Python uses zero-based indexing, unlike MATLAB

```
a=[10,20,30,40,50,60]
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

Nested lists can have nested dereferences:
```
b=[[10,20,30],[40,50,60]]
print(b[0][1])
print(b[1][0])
```
but *not* a dereference like b[0,1].

> Note that `len` will only give the length of the top level.
> In general arrays should be preferred to nested lists when the contents are numerical.

### Slicing

A range of values for the indices can be specified to extract values from a list.  For example:
```
print(a[0:3])
```

> _*Pitfall:*_
>
>  Slicing syntax is different from MATLAB in that second number is one plus final index - this is in addition to the zero index difference.

```
a=[10,20,30,40,50,60]
print(a[0:3])    # same as a(1:3) in MATLAB
print(a[1:3])    # same as a(2:3) in MATLAB
```

> _*Pitfall:*_
>
>  Unlike in MATLAB, you cannot use a list as indices instead of an integer or a slice

```
b=[3,4]
print(a[b])
```

### List operations

Multiplication can be used with lists, where multiplication implements replication.

```
d=[10,20,30]
print(d*4)
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
d=[10,20,30]
for x in d:
    print(x)
```

> Note that the indentation within the loop is _*crucial*_.  All python control blocks are delineated purely by indentation.

### Getting help

The function `dir()` can be used to get information about any variable/object/function in python.  It lists the possible operations.

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

The keys and values can take on any type, even dictionaries! Python is nothing if not flexible.  However, each key must be unique.

### Adding to a dictionary

This is very easy:
```
e['c']=555   # just like in Biobank!  ;)
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
for k,v in e.items():
   print((k,v))
```

The print statement here constructs a tuple, which is often used in python.

Another option is:
```
for k in e:
    print((k,e[k]))
```

> Note that in both cases the order is arbitrary. The `sorted` function can be used if you want keys in a sorted order; e.g. `for k in sorted(e):` ...

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
b = a*2
a[0] = 8888
print(b)
```

If an explicit copy is necessary then this can be made using the `copy()` function:
```
a = [7]
b = a.copy()
a[0] = 8888
print(b)
```

> When writing functions this is something to be particularly careful about.

```
def foo1(x):
   x.append(10)
def foo2(x):
   x = x + [10]
def foo3(x):
   return x + [10]

a=[5]
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

 - boolean operators
 - if/else/for
 - a if condition else b
 - introduce range/enumerate

