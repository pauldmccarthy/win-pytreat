# Welcome to the WIN Virtual Mini PyTreat 2020!


This notebook is available at:


https://git.fmrib.ox.ac.uk/fsl/pytreat-practicals-2020/-/tree/master/talks%2Fvirtual_intro/intro.ipynb


If you have FSL installed and you'd like to follow along *interactively*,
follow the instructions for attendees in the `README.md` file of the above
repository, and then open the `talks/virtual_intro/intro.ipynb` notebook.


# Contents


* [Introduction](#introduction)
  * [Python in a nutshell](#python-in-a-nutshell)
  * [Different ways of running Python](#different-ways-of-running-python)
* [Variables and basic types](#variables-and-basic-types)
  * [Integer and floating point scalars](#integer-and-floating-point-scalars)
  * [Strings](#strings)
  * [Lists and tuples](#lists-and-tuples)
  * [Dictionaries](#dictionaries)
  * [A note on mutablility](#a-note-on-mutablility)
* [Flow control](#flow-control)
  * [List comprehensions](#list-comprehensions)
* [Reading and writing text files](#reading-and-writing-text-files)
  * [Example: processing lesion counts](#example-processing-lesion-counts)
* [Functions](#functions)
* [Working with `numpy`](#working-with-numpy)
  * [The Python list versus the `numpy` array](#the-python-list-versus-the-numpy-array)
  * [Creating arrays](#creating-arrays)
  * [Example: reading arrays from text files](#example-reading-arrays-from-text-files)


<a class="anchor" id="introduction"></a>
# Introduction


This talk is an attempt to give a whirlwind overview of the Python programming
language.  It is assumed that you have experience with another programming
language (e.g. MATLAB).


This talk is presented as an interactive [Jupyter
Notebook](https://jupyter.org/) - you can run all of the code on your own
machine - click on a code block, and press **SHIFT+ENTER**. You can also "run"
the text sections, so you can just move down the document by pressing
**SHIFT+ENTER**.


It is also possible to *change* the contents of each code block (these pages
are completely interactive) so do experiment with the code you see and try
some variations!


You can get help on any Python object, function, or method by putting a `?`
before or after the thing you want help on:


```
a = 'hello!'
?a.upper
```


And you can explore the available methods on a Python object by using the
**TAB** key:


```
# Put the cursor after the dot, and press the TAB key...
a.
```


<a class="anchor" id="python-in-a-nutshell"></a>
## Python in a nutshell


**Pros**


* _Flexible_ Feel free to use functions, classes, objects, modules and
  packages. Or don't - it's up to you!

* _Fast_ If you do things right (in other words, if you use `numpy`)

* _Dynamically typed_ No need to declare your variables, or specify their
  types.

* _Intuitive syntax_ How do I run some code for each of the elements in my
  list?


```
a = [1, 2, 3, 4, 5]

for elem in a:
    print(elem)
```


**Cons**


* _Dynamically typed_ Easier to make mistakes, harder to catch them

* _No compiler_ See above

* _Slow_ if you don't do things the right way

* _Python 2 is not the same as Python 3_ But there's an easy solution: Forget
  that Python 2 exists.

* _Hard to manage different versions of python_ But we have a solution for
  you: `fslpython`.


Python is a widely used language, so you can get lots of help through google
and [stackoverflow](https://stackoverflow.com). But make sure that the
information you find is for **Python 3**, and **not** for **Python 2**!
Python 2 is obsolete, but is still used by many organisations, so you will
inevitably come across many Python 2 resources.


The differences between Python 2 and 3 are small, but important. The most
visible difference is in the `print` function: in Python 3, we write
`print('hello!')`, but in Python 2, we would write `print 'hello!'`.


FSL 5.0.10 and newer comes with its own version of Python, bundled with nearly
all of the scientific libraries that you are likely to need.


So if you use `fslpython` for all of your development, you can be sure that it
will work in FSL!


<a class="anchor" id="different-ways-of-running-python"></a>
## Different ways of running Python


Many of the Pytreat talks and practicals are presented as *Jupyter notebooks*,
which is a way of running python code in a web browser.


Jupyter notebooks are good for presentations and practicals, and some people
find them very useful for exploratory data analysis. But they're not the only
way of running Python code.


**Run Python from a file**


This works just like it does in MATLAB:


1. Put your code in a `.py` file (e.g. `mycode.py`).
2. Run `fslpython mycode.py` in a terminal.
3. ??
4. Profit.


**Run python in an interpreter**


Python is an [*interpreted
language*](https://en.wikipedia.org/wiki/Interpreted_language), like MATLAB.
So you can either write your code into a file, and then run that file, or you
can type code directly into a Python interpreter.


Python has a standard interpreter built-in - run `fslpython` in a terminal,
and see what happens (use CTRL+D to exit).


**But** there is another interpreter called [IPython](https://ipython.org/)
which is vastly superior to the standard Python interpreter. Use IPython
instead! It is already installed in `fslpython`, so if you want to do some
interactive work, you can use `fslipython` in a terminal.


<a class="anchor" id="variables-and-basic-types"></a>
# Variables and basic types


There are many different types of values in Python. Python *variables* do not
have a type though - a variable can refer to values of any type, and a
variable can be updated to refer to different values (of different
types). This is just like how things work in MATLAB.


<a class="anchor" id="integer-and-floating-point-scalars"></a>
## Integer and floating point scalars

```
a = 7
b = 1 / 3
c = a + b
print('a:    ', a)
print('b:    ', b)
print('c:    ', c)
print('b:     {:0.4f}'.format(b))
print('a + b:', a + b)
```


<a class="anchor" id="strings)"></a>
## Strings


```
a = 'Hello'
b = "Kitty"
c = '''
Magic
multi-line
strings!
'''

print(a, b)
print(a + b)
print('{}, {}!'.format(a, b))
print(c)
```


String objects have a number of useful methods:


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


Two common and convenient string methods are `strip()` and `split()`.  The
first will remove any whitespace at the beginning and end of a string:


```
s2 = '   A very    spacy   string       '
print('*' + s2 + '*')
print('*' + s2.strip() + '*')
```


With `split()` we can tokenize a string (to turn it into a list of strings)
like this:


```
print(s.split())
print(s2.split())
```


We can also use the `join` method to re-construct a new string. Imagine that
we need to reformat some data from being comma-separated to being
space-separated:


```
data = ' 1,2,3,4,5,6,7  '
```


`strip`, `split` and `join` makes this job trivial:


```
print('Original:               {}'.format(data))
print('Strip, split, and join: {}'.format(' '.join(data.strip().split(','))))
```


<a class="anchor" id="lists-and-tuples"></a>
## Lists and tuples


Both tuples and lists are built-in Python types and are like cell-arrays in
MATLAB. For numerical vectors and arrays it is much better to use *numpy*
arrays, which are covered later.


Tuples are defined using round brackets and lists are defined using square
brackets. For example:


```
t = (3, 7.6, 'str')
l = [1, 'mj', -5.4]
print(t)
print(l)

t2 = (t, l)
l2 = [t, l]
print('t2 is: ', t2)
print('l3 is: ', l2)
```


The key difference between lists and tuples is that tuples are *immutable*
(once created, they cannot be changed), whereas lists are *mutable*:


```
a = [10, 20, 30]
a = a + [70]
a += [80]
print(a)
```


Square brackets are used to index tuples, lists, strings, dictionaries, etc.
For example:


```
d = [10, 20, 30]
print(d[1])
```


> **MATLAB pitfall:** Python uses zero-based indexing, unlike MATLAB, where
> indices start from 1.


```
a = [10, 20, 30, 40, 50, 60]
print(a[0])
print(a[2])
```


A range of values for the indices can be specified to extract values from a
list or tuple using the `:` character.  For example:


```
print(a[0:3])
```



> **MATLAB pitfall:** Note that Python's slicing syntax is different from
> MATLAB in that the second number is *exclusive*, i.e. `a[0:3]` gives us the
> elements of `a` at positions `0`, `1` and `2` , but *not* at position `3`.


When slicing a list or tuple, you can leave the start and end values out -
when you do this, Python will assume that you want to start slicing from the
beginning or the end of the list.  For example:


```
print(a[:3])
print(a[1:])
print(a[:])
print(a[:-1])
```


You can also change the step size, which is specified by the third value (not
the second one, as in MATLAB).  For example:


```
print(a[0:4:2])
print(a[::2])
print(a[::-1])
```


Some methods are available on `list` objects for adding and removing items:


```
print(d)
d.append(40)
print(d)
d.extend([50, 60])
print(d)
d = d + [70, 80]
print(d)
d.remove(20)
print(d)
d.pop(0)
print(d)
```


What will `d.append([50,60])` do, and how is it different from
`d.extend([50,60])`?


```
d.append([50, 60])
print(d)
```


<a class="anchor" id="dictionaries"></a>
## Dictionaries


Dictionaries (or *dicts*) can be used to store key-value pairs. Almost
anything can used as a key, and anything can be stored as a value; it is
common to use strings as keys:


```
e = {'a' : 10, 'b': 20}
print(len(e))
print(e.keys())
print(e.values())
print(e['a'])
```


Like lists (and unlike tuples), dicts are mutable, and have a number of
methods for manipulating them:


```
e['c'] = 30
e.pop('a')
e.update({'a' : 100, 'd' : 400})
print(e)
e.clear()
print(e)
```


<a class="anchor" id="a-note-on-mutability"></a>
## A note on mutablility


Python variables can refer to values which are either mutable, or
immutable. Examples of immutable values are strings, tuples, and integer and
floating point scalars. Examples of mutable values are lists, dicts, and most
user-defined types.


When you pass an immutable value around (e.g. into a function, or to another
variable), it works the same as if you were to copy the value and pass in the
copy - the original value is not changed:


```
a = 'abcde'
b = a
b = b.upper()
print('a:', a)
print('b:', b)
```


In contrast, when you pass a mutable value around, you are passing a
*reference* to that value - there is only ever one value in existence, but
multiple variables refer to it. You can manipulate the value through any of
the variables that refer to it:


```
a = [1, 2, 3, 4, 5]
b = a

a[3] = 999
b.append(6)

print('a', a)
print('b', b)
```


<a class="anchor" id="flow-control"></a>
# Flow control


Python also has a boolean type which can be either `True` or `False`. Most
Python types can be implicitly converted into booleans when used in a
conditional expression.


Relevant boolean and comparison operators include: `not`, `and`, `or`, `==`
and `!=`


For example:
```
a = True
b = False
print('Not a is:', not a)
print('a or b is:', a or b)
print('a and b is:', a and b)
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


We can use boolean values in `if`-`else` conditional expressions:


```
a = [1, 2, 3, 4]
val = 3
if val in a:
    print('Found {}!'.format(val))
else:
    print('{} not found :('.format(val))
```


Note that the indentation in the `if`-`else` statement is **crucial**.
**All** python control blocks are delineated purely by indentation. We
recommend using **four spaces** and no tabs, as this is a standard practice
and will help a lot when collaborating with others.


You can use the `for` statement to loop over elements in a list:


```
d = [10, 20, 30]
for x in d:
    print(x)
```


You can also loop over the key-value pairs in a dict:


```
a = {'a' : 10, 'b' : 20, 'c' : 30}
print('a.items()')
for key, val in a.items():
    print(key, val)
print('a.keys()')
for key in a.keys():
    print(key, a[key])
print('a.values()')
for val in a.values():
    print(val)
```


> In older versions of Python 3, there was no guarantee of ordering when using dictionaries.
> However, a of Python 3.7, dictionaries will remember the order in which items are inserted,
> and the `keys()`, `values()`, and `items()` methods will return elements in that order.
>

> If you want a dictionary with ordering, *and* you want your code to work with
> Python versions older than 3.7, you can use the
> [`OrderedDict`](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
> class.


There are some handy built-in functions that you can use with `for` loops:


```
d = [10, 20, 30]
print('Using the range function')
for i in range(len(d)):
    print('element at position {}: {}'.format(i, d[i]))

print('Using the enumerate function')
for i, elem in enumerate(d):
    print('element at position {}: {}'.format(i, elem))
```


<a class="anchor" id=" list-comprehensions"></a>
## List comprehensions


Python has a really neat way to create lists (and dicts), called
*comprehensions*. Let's say we have some strings, and we want to count the
number of characters in each of them:


```
strings = ['hello', 'howdy', 'hi', 'hey']
nchars = [len(s) for s in strings]
for s, c in zip(strings, nchars):
    print('{}: {}'.format(s, c))
```


> The `zip` function "zips" two or more sequences, so you can loop over them
> together.


Or we could store the character counts in a dict:


```
nchars = { s : len(s) for s in strings }

for s, c in nchars.items():
    print('{}: {}'.format(s, c))
```


<a class="anchor" id=" reading-and-writing-text-files"></a>
# Reading and writing text files


The syntax to open a file in python is
`with open(<filename>, <mode>) as <file_object>: <block of code>`, where


* `filename` is a string with the name of the file
* `mode` is one of 'r' (for read-only access), 'w' (for writing a file, this
  wipes out any existing content), 'a' (for appending to an existing file).
* `file_object` is a variable name which will be used within the `block of
  code` to access the opened file.


For example the following will read all the text in `data/file.txt` and print
it:


```
with open('data/file.txt', 'r') as f:
    print(f.read())
```


A very similar syntax is used to write files:


```
with open('new_file.txt', 'w') as f:
    f.write('This is my first line\n')
    f.writelines(['Second line\n', 'and the third\n'])
```


<a class="anchor" id="example-processing-lesion-counts"></a>
## Example: processing lesion counts


Imagine that we have written an amazing algorithm in Python which
automatically counts the number of lesions in an individual's structural MRI
image.


```
subject_ids   = ['01', '07', '21', '32']
lesion_counts = [  4,    9,   13,    2]
```


We may wish to process this data in another application (e.g. Excel or SPSS).
Let's save the results out to a CSV (comma-separated value) file:


```
with open('lesion_counts.csv', 'w') as f:
    f.write('Subject ID, Lesion count\n')
    for subj_id, count in zip(subject_ids, lesion_counts):
        f.write('{}, {}\n'.format(subj_id, count))
```


We can now load the `lesion_counts.csv` file into our analysis software of
choice. Or we could load it back into another Python session, and store
the data in a dict:


```
lesion_counts = {}

with open('lesion_counts.csv', 'r') as f:
    # skip the header
    f.readline()
    for line in f.readlines():
        subj_id, count = line.split(',')
        lesion_counts[subj_id] = int(count)

print('Loaded lesion counts:')
for subj, count in lesion_counts.items():
    print('{}: {}'.format(subj, count))
```


<a class="anchor" id="functions"></a>
## Functions


You will find functions pretty familiar in python to start with, although they
have a few options which are really handy and different from C++ or matlab (to
be covered in a later practical).  To start with we'll look at a simple
function but note a few key points:


* you *must* indent everything inside the function (it is a code block and
 indentation is the only way of determining this - just like for the guts of a
 loop)
* you can return *whatever you want* from a python function, but only a single
 object - it is usual to package up multiple things in a tuple or list, which
 is easily unpacked by the calling invocation: e.g., `a, b, c = myfunc(x)`
* parameters are passed by *reference* (more on this below)


```
def myfunc(x, y, z=0):
    r2 = x*x + y*y + z*z
    r = r2**0.5
    return r,  r2

rad = myfunc(10, 20)
print(rad)
rad, dummy = myfunc(10, 20, 30)
print(rad)
rad, _ = myfunc(10,20,30)
print(rad)
```


> Note that the `_` is used as shorthand here for a dummy variable
> that you want to throw away.
>
> The return statement implicitly creates a tuple to return and is equivalent
> to `return (r, r2)`


One nice feature of python functions is that you can name the arguments when
you call them, rather than only doing it by position.  For example:


```
def myfunc(x, y, z=0, flag=''):
    if flag=='L1':
        r = abs(x) + abs(y) + abs(z)
    else:
        r = (x*x + y*y + z*z)**0.5
    return r

rA = myfunc(10, 20)
rB = myfunc(10, 20, flag='L1')
rC = myfunc(10, 20, flag='L1', z=30)
print(rA, rB, rC)
```


You will often see python functions called with these named arguments. In
fact, for functions with more than 2 or 3 variables this naming of arguments
is recommended, because it clarifies what each of the arguments does for
anyone reading the code.


Arguments passed into a python function are *passed by reference* - this is
where the difference between *mutable* and *immutable* types becomes
important - if you pass a mutable object into a function, the function
might change it!


```
def changeList(l):
   l[0] = 'mwahahaha!'

mylist = [1,2,3,4,5]

print('before:', mylist)
changelist(mylist)
print('after:', mylist)
```


<a class="anchor" id="working-with-numpy"></a>
# Working with `numpy`


This section introduces you to [`numpy`](http://www.numpy.org/), Python's
numerical computing library. Numpy adds a new data type to the Python
language - the `array` (more specifically, the `ndarray`). A Numpy `array`
is a N-dimensional array of homogeneously-typed numerical data.


Pretty much every scientific computing library in Python is built on top of
Numpy - whenever you want to access some data, you will be accessing it in the
form of a Numpy array. So it is worth getting to know the basics.


<a class="anchor" id="the-python-list-versus-the-numpy-array"></a>
## The Python list versus the `numpy` array


You have already been introduced to the Python `list`, which you can easily
use to store a handful of numbers (or anything else):


```
data = [10, 8, 12, 14, 7, 6, 11]
```


You could also emulate a 2D or ND matrix by using lists of lists, for example:


```
xyz_coords = [[-11.4,   1.0,  22.6],
              [ 22.7, -32.8,  19.1],
              [ 62.8, -18.2, -34.5]]
```


For simple tasks, you could stick with processing your data using python
lists, and the built-in
[`math`](https://docs.python.org/3.5/library/math.html) library. And this
might be tempting, because it does look quite a lot like what you might type
into Matlab.


But **BEWARE!** A Python list is a terrible data structure for scientific
computing!


This is a major source of confusion for people who are learning Python, and
are trying to write efficient code. It is _crucial_ to be able to distinguish
between a Python list and a Numpy array.


**Python list == Matlab cell array:** A list in Python is akin to a cell
array in Matlab - they can store anything, but are extremely inefficient, and
unwieldy when you have more than a couple of dimensions.


**Numpy array == Matlab matrix:** These are in contrast to the Numpy array
and Matlab matrix, which are both thin wrappers around a contiguous chunk of
memory, and which provide blazing-fast performance (because behind the scenes
in both Numpy and Matlab, it's C, C++ and FORTRAN all the way down).


So you should strongly consider turning those lists into Numpy arrays:


```
import numpy as np

data = np.array([10, 8, 12, 14, 7, 6, 11])

xyz_coords = np.array([[-11.4,   1.0,  22.6],
                       [ 22.7, -32.8,  19.1],
                       [ 62.8, -18.2, -34.5]])
print('data:', data)
print('xyz_coords:', xyz_coords)
```


> Numpy is not a "built-in" library, so we have to import it. The statement
> `import numpy as np` tells Python to *Import the `numpy` library, and make
> it available as a variable called `np`.*


<a class="anchor" id="creating-arrays"></a>
## Creating arrays


Numpy has quite a few functions which behave similarly to their equivalents in
Matlab:


```
print('np.zeros gives us zeros:                       ', np.zeros(5))
print('np.ones gives us ones:                         ', np.ones(5))
print('np.arange gives us a range:                    ', np.arange(5))
print('np.linspace gives us N linearly spaced numbers:', np.linspace(0, 1, 5))
print('np.random.random gives us random numbers [0-1]:', np.random.random(5))
print('np.random.randint gives us random integers:    ', np.random.randint(1, 10, 5))
print('np.eye gives us an identity matrix:')
print(np.eye(4))
print('np.diag gives us a diagonal matrix:')
print(np.diag([1, 2, 3, 4]))
```


The `zeros` and `ones` functions can also be used to generate N-dimensional
arrays:


```
z = np.zeros((3, 4))
o = np.ones((2, 10))
print(z)
print(o)
```


> Note that, in a 2D Numpy array, the first axis corresponds to rows, and the
> second to columns - just like in Matlab.



> **MATLAB pitfall:** Arithmetic operations on arrays in Numpy work on an
> *elementwise* basis. In particular, if you multiply two arrays together,
> you will get the elementwise product. You **won't** get the dot product,
> like you would in MATLAB. You can, however, use the `@` operator to perform
> matrix multiplication on numpy arrays.


<a class="anchor" id="example-reading-arrays-from-text-files"></a>
## Example: reading arrays from text files


The `numpy.loadtxt` function is capable of loading numerical data from
plain-text files. By default it expects space-separated data:


```
data = np.loadtxt('data/space_separated.txt')
print('data in data/space_separated.txt:')
print(data)
```


But you can also specify the delimiter to expect<sup>1</sup>:


```
data = np.loadtxt('data/comma_separated.txt', delimiter=',')
print('data in data/comma_separated.txt:')
print(data)
```


> <sup>1</sup> And many other things such as file headers, footers, comments,
> and newline characters - see the
> [docs](https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html)
> for more information.


Of course you can also save data out to a text file just as easily, with
[`numpy.savetxt`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html):


```
data = np.random.randint(1, 10, (10, 10))
np.savetxt('mydata.txt', data, delimiter=',', fmt='%i')
```


Jupyter notebooks have a special feature - if you start a line with a `!`
character, you can run a `bash` command. Let's look at the file we just
generated:


```
!cat mydata.txt
```


> The `!` feature won't work in regular Python scripts.


Here's how we can load a 2D array fom a file, and calculate the mean of each
column:


```
data     = np.loadtxt('data/2d_array.txt', comments='%')
colmeans = data.mean(axis=0)

print('Column means')
print('\n'.join(['{}: {:0.2f}'.format(i, m) for i, m in enumerate(colmeans)]))
```
