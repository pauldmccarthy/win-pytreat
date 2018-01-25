# Basic types

Python has many different types and variables are dynamic and can change types (like MATLAB).  Some of the most commonly used in-built types are:
* integer and floating point scalars
* strings
* tuples
* lists
* dictionary

N-dimensional arrays and other types are supported through common modules (e.g., numpy, scipy, scikit-learn).

```
a = 4
b = 3.6
c = 'abc'
d = [10,20,30]
e = {'a' : 10, 'b': 20}
```

Any variable can be printed using the function:
```
print(...)
```

> Python 3 versus python 2:
>   Print - for the print statement the brackets are compulsory for *python 3*, but are optional in python 2.  So you will see plenty of code without the brackets but you should get into the habit of using them.
>   Division - in python 3 all  division is floating point (like in MATLAB), even if the values are integers, but in python 2 integer division works like it does in C.


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
This is
a string over
multiple lines
```


## Tuples and Lists

Anything can be stored within a list and consistency is not required.  For example:
```
a=[1,'mj',-5.4]
```

### Dereferencing

Square brackets are used to dereference lists, dictionaries, etc.  For example:
```
d = [10,20,30]
d[1]
    20
	```

  ---- use of -1 as an index value

> Pitfall:
>  Python uses zero-based indexing, unlike MATLAB
>    * a=[10,20,30,40,50,60]
>    * a[0]
>        10
>    * a[2]
>        30

### List operations

Addition and multiplication can be used with lists, where multiplication implements replication.

```
d=[10,20,30]
d*2
    [10, 20, 30, 10, 20, 30]
```

There are also other operations such as:
```
d.append(40)

```

USE DIR() TO GET MORE INFO FOR ANY PARTICULAR OBJECT - OR GOOGLE!

## Dictionaries



## Combinations

Can nest these arbitrarily without needing consistency. For example:
```
a=[ [3,5,7] , ['a','e','i','o','u'] , { } ]
```



## Copying and references 
** demonstrate difference between mutable and immutable types

a = 7
b = a
a = 2348
print(b)

a = [7]
b = a
a[0] = 8888
print(b)


> Pitfall:
>  Slicing syntax is also different from MATLAB (second number is one plus final index)
>    * a=[10,20,30,40,50,60]
>    * a[0:3]    # same as a(1:3) in MATLAB
>        [10, 20, 30]
>    * a[1:3]    # same as a(2:3) in MATLAB
>        [20, 30]

> Pitfall:
>  Cannot use a list as indices instead of an integer or a slice
>    * b=[3,4]
>    * a[b]
>        TypeError: list indices must be integers or slices, not list




def foo(x):
   x.append(10)
def foo(x):
   x = x + [10]

def foo(x):
   return x + [10]

def foo(y):
   y = y + 1
def foo(y):
   return y + 1

## Control flow

 - boolean operators
 - if/else/for
 - a if condition else b
 - introduce range/enumerate

