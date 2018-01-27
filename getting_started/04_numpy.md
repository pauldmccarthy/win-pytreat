# Numpy


This section introduces you to [`numpy`](http://www.numpy.org/), Python's
numerical computing library.


Numpy is not actually part of the standard Python library. But it is a
fundamental part of the Python ecosystem - it forms the basis for many
important Python libraries, and it (along with its partners
[`scipy`](https://www.scipy.org/), [`matplotlib`](https://matplotlib.org/) and
[`pandas`](https://pandas.pydata.org/)) is what makes Python an attractive
alternative to Matlab as a scientific computing platform.


## Contents


* [The Python list versus the Numpy array](#the-python-list-versus-the-numpy-array)
* [Numpy basics](#numpy-basics)
 * [Creating arrays](#creating-arrays)
 * [Operating on arrays](#operating-on-arrays)
 * [Array properties](#array-properties)
 * [Descriptive statistics](#descriptive-statistics)
 * [Reshaping and rearranging arrays](#reshaping-and-rearranging-arrays)
* [Array indexing](#array-indexing)
 * [Indexing multi-dimensional arrays](#indexing-multi-dimensional-arrays)
 * [Boolean indexing](#boolean-indexing)
 * [Coordinate array indexing](#coordinate-array-indexing)
* [Array operations and broadcasting](#array-operations-and-broadcasting)
* [Generating random numbers](#generating-random-numbers)

* [Appendix: Importing Numpy](#appendix-importing-numpy)
* [Appendix: Vectors in Numpy](#appendix-vectors-in-numpy)



<a class="anchor" id="the-python-list-versus-the-numpy-array"></a>
## The Python list versus the Numpy array


Numpy adds a new data type to the Python language - the `array` (more
specifically, the `ndarray`). A Numpy `array` is a N-dimensional array of
homogeneously-typed numerical data.


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


But __BEWARE!__ A Python list is a terrible data structure for scientific
computing!


This is a major source of confusion for those poor souls who have spent their
lives working in Matlab, but have finally seen the light and switched to
Python. It is _crucial_ to be able to distinguish between a Python list and a
Numpy array.


___Python list == Matlab cell array:___ A list in python is akin to a cell
array in Matlab - they can store anything, but are extremely inefficient, and
unwieldy when you have more than a couple of dimensions.


___Numy array == Matlab matrix:___ These are in contrast to the Numpy array
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
```


If you look carefully at the code above, you will notice that we are still
actually using Python lists. We have declared our data sets in exactly the
same way as we did earlier, by denoting them with square brackets `[` and `]`.


The key difference here is that these lists immediately get converted into
Numpy arrays, by passing them to the `np.array` function.  To clarify this
point, we could rewrite this code in the following equivalent manner:


```
import numpy as np

# Define our data sets as python lists
data       = [10, 8, 12, 14, 7, 6, 11]
xyz_coords = [[-11.4,   1.0,  22.6],
              [ 22.7, -32.8,  19.1],
              [ 62.8, -18.2, -34.5]]

# Convert them to numpy arrays
data       = np.array(data)
xyz_coords = np.array(xyz_coords)
```


Of course, in practice, we would never create a Numpy array in this way - we
will be loading our data from text or binary files directly into a Numpy
array, thus completely bypassing the use of Python lists and the costly
list-to-array conversion.  I'm emphasising this to help you understand the
difference between Python lists and Numpy arrays. Apologies if you've already
got it, forgiveness please.


<a class="anchor" id="numpy-basics"></a>
## Numpy basics


Let's get started.


```
import numpy as np
```


<a class="anchor" id="creating-arrays"></a>
### Creating arrays


Numpy has quite a few functions which behave similarly to their equivalents in
Matlab:


```
print('np.zeros gives us zeros:                       ', np.zeros(5))
print('np.ones gives us ones:                         ', np.ones(5))
print('np.arange gives us a range:                    ', np.arange(5))
print('np.linspace gives us N linearly spaced numbers:', np.linspace(0, 1, 5))
print('np.random.random gives us random numbers:      ', np.random.random(5))
print('np.random.randint gives us random integers:    ', np.random.randint(1, 10, 5))
print('np.eye gives us an identity matrix:')
print(np.eye(4))
print('np.diag gives us a diagonal matrix:')
print(np.diag([1, 2, 3, 4]))
```


> There will be more on random numbers [below](#generating-random-numbers).


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


<a class="anchor" id="operating-on-arrays"></a>
### Operating on arrays


All of the mathematical operators you know and love can be applied to Numpy
arrays:


```
a = np.random.randint(1, 10, (3, 3))
print('a:')
print(a)
print('a + 2:')
print( a + 2)
print('a * 3:')
print( a * 3)
print('a % 2:')
print( a % 2)
```


We'll cover more advanced array operations
[below](#array-operations-and-broadcasting).


<a class="anchor" id="array-properties"></a>
### Array properties


Numpy is a bit different than Matlab in the way that you interact with
arrays. In Matlab, you would typically pass an array to a built-in function,
e.g. `size(M)`, `ndims(M)`, etc. In contrast, a Numpy array is a Python
object which has _attributes_ that contain basic information about the array:


```
z = np.zeros((2, 3, 4))
print(z)
print('Shape:                     ', z.shape)
print('Number of dimensions:      ', z.ndim)
print('Number of elements:        ', z.size)
print('Data type:                 ', z.dtype)
print('Number of bytes:           ', z.nbytes)
print('Length of first dimension: ', len(z))
```


> As depicted above, passing a Numpy array to the built-in `len` function will
> only give you the length of the first dimension, so you will typically want
> to avoid using it - use the `size` attribute instead.


<a class="anchor" id="descriptive-statistics"></a>
### Descriptive statistics


Similarly, a Numpy array has a set of methods<sup>1</sup> which allow you to
calculate basic descriptive statisics on an array:


```
a = np.random.random(10)
print('a: ', a)
print('min:          ', a.min())
print('max:          ', a.max())
print('index of min: ', a.argmin())  # remember that in Python, list indices
print('index of max: ', a.argmax())  # start from zero - Numpy is the same!
print('mean:         ', a.mean())
print('variance:     ', a.var())
print('stddev:       ', a.std())
print('sum:          ', a.sum())
print('prod:         ', a.prod())
```


> <sup>1</sup> Python, being an object-oriented language, distinguishes
> between _functions_ and _methods_. _Method_ is simply the term used to refer
> to a function that is associated with a specific object. Similarly, the term
> _attribute_ is used to refer to some piece of information that is attached
> to an object, such as `z.shape`, or `z.dtype`.


<a class="anchor" id="reshaping-and-rearranging-arrays"></a>
### Reshaping and rearranging arrays


A numpy array can be reshaped very easily, using the `reshape` method.

```
a = np.random.randint(1, 10, (4, 4))
b = a.reshape((2, 8))
print('a:')
print(a)
print('b:')
print(b)
```


Note that this does not modify the underlying data in any way - the `reshape`
method returns a _view_ of the same array, just indexed differently:


```
a[3, 3] = 12345
b[0, 7] = 54321
print('a:')
print(a)
print('b:')
print(b)
```


If you need to create a reshaped copy of an array, use the `np.array`
function:


```
a = np.random.randint(1, 10, (4, 4))
b = np.array(a.reshape(2, 8))
a[3, 3] = 12345
b[0, 7] = 54321
print('a:')
print(a)
print('b:')
print(b)
```


The `T` attribute is a shortcut to obtain the transpose of an array.


```
a = np.random.randint(1, 10, (4, 4))
print(a)
print(a.T)
```


The `transpose` method allows you to obtain more complicated rearrangements
of an array's axes:


```
a = np.random.randint(1, 10, (2, 3, 4))
b = a.transpose((2, 0, 1))
print('a: ', a.shape)
print(a)
print('b:', b.shape)
print(b)
```


> Note again that the `T` attribute and `transpose` method return _views_ of
> your array.


Numpy has some useful functions which allow you to concatenate or stack
multiple arrays into one. The `concatenate` function does what it says on the
tin:


```
a = np.zeros(3)
b = np.ones(3)

print('1D concatenation:', np.concatenate((a, b)))

a = np.zeros((3, 3))
b = np.ones((3, 3))

print('2D column-wise concatenation:')
print(np.concatenate((a, b), axis=1))

print('2D row-wise concatenation:')

# The axis parameter defaults to 0,
# so it is not strictly necessary here.
print(np.concatenate((a, b), axis=0))
```


The `hstack`, `vstack` and `dstack` functions allow you to concatenate vectors
or arrays along the first, second, or third dimension respectively:

```
a = np.zeros(3)
b = np.ones(3)

print('a: ', a)
print('b: ', b)

hstacked = np.hstack((a, b))
vstacked = np.vstack((a, b))
dstacked = np.dstack((a, b))

print('hstacked: (shape {}):'.format(hstacked.shape))
print( hstacked)
print('vstacked: (shape {}):'.format(vstacked.shape))
print( vstacked)
print('dstacked: (shape {}):'.format(dstacked.shape))
print( dstacked)
```


<a class="anchor" id="array-indexing"></a>
## Array indexing


Just like in Matlab, slicing up your arrays is a breeze in Numpy.  If you are
after some light reading, you might want to check out the [comprehensive Numpy
Indexing
reference](https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html).


> As with indexing regular Python lists, array indices start from 0, and end
> indices (if specified) are exclusive.


Let's whet our appetites with some basic 1D array slicing:


```
a = np.random.randint(1, 10, 10)

print('a:                              ', a)
print('first element:                  ', a[0])
print('first two elements:             ', a[:2])
print('last element:                   ', a[a.shape[0] - 1])
print('last element again:             ', a[-1])
print('last two elements:              ', a[-2:])
print('middle four elements:           ', a[3:7])
print('Every second element:           ', a[::2])
print('Every second element, reversed: ', a[1::-2])
```


Note that slicing an array in this way returns a _view_, not a copy, into that
array:


```
a = np.random.randint(1, 10, 10)
print('a:', a)
every2nd = a[::2]
print('every 2nd:', every2nd)
every2nd += 10
print('a':, a)
```


<a class="anchor" id="indexing-multi-dimensional-arrays"></a>
### Indexing multi-dimensional arrays


Multi-dimensional array indexing works in much the same way as one-dimensional
indexing but with, well, more dimensions:


```
a = np.random.randint(1, 10, (5, 5))
print('a:')
print(a)
print(' First row:     ', a[  0, :])
print(' Last row:      ', a[ -1, :])
print(' second column: ', a[  :, 1])
print(' Centre:')
print(a[1:4, 1:4])
```


For arrays with more than two dimensions, the ellipsis (`...`) is a handy
feature - it allows you to specify a slice comprising all elements along
more than one dimension:


```
a = np.random.randint(1, 10, (3, 3, 3))
print('a:')
print(a)
print('All elements at x=0:')
print(a[0, ...])
print('All elements at z=2:')
print(a[..., 2])
print('All elements at x=0, z=2:')
print(a[0, ..., 2])
```


<a class="anchor" id="boolean-indexing"></a>
### Boolean indexing


A numpy array can be indexed with a boolean array of the same shape. For
example:


```
a = np.random.randint(1, 10, 10)

print('a:                          ', a)
print('a > 5:                      ', a > 4)
print('elements in a that are > 5: ', a[a > 5])
```


Logical operators `~` (not), `&` (and) and `|` (or) can be used to manipulate
and combine boolean Numpy arrays:

```
a    = np.random.randint(1, 10, 10)
gt5  = a > 5
even = a % 2 == 0

print('a:                                    ', a)
print('elements in a which are > 5:          ', a[gt5])
print('elements in a which are <= 5:         ', a[~gt5])
print('elements in a which are even:         ', a[even])
print('elements in a which are odd:          ', a[~even])
print('elements in a which are > 5 and even: ', a[gt5 &  even])
print('elements in a which are > 5 or odd:   ', a[gt5 | ~even])
```


<a class="anchor" id="coordinate-array-indexing"></a>
### Coordinate array indexing


```

```


<a class="anchor" id="array-operations-and-broadcasting"></a>
## Array operations and broadcasting



<a class="anchor" id="generating-random-numbers"></a>
## Generating random numbers


<a class="anchor" id="appendix-importing-numpy"></a>
## Appendix: Importing Numpy


For interactive exploration/experimentation, you might want to import
Numpy like this:


```
from numpy import *
```


This makes your Python session very similar to Matlab - you can call all
of the Numpy functions directly:


```
e = array([1, 2, 3, 4, 5])
z = zeros((100, 100))
d = diag([2, 3, 4, 5])

print(e)
print(z)
print(d)
```


But if you are writing a script or application using Numpy, I implore you to
Numpy like this instead:


```
import numpy as np
```


The downside to this is that you will have to prefix all Numpy functions with
`np.`, like so:


```
e = np.array([1, 2, 3, 4, 5])
z = np.zeros((100, 100))
d = np.diag([2, 3, 4, 5])

print(e)
print(z)
print(d)
```


There is a big upside, however, in that other people who have to read/use your
code will like you a lot more. This is because it will be easier for them to
figure out what the hell your code is doing. Namespaces are your friend - use
them!


<a class="anchor" id="appendix-vectors-in-numpy"></a>
## Appendix: Vectors in Numpy


One aspect of Numpy which might trip you up, and which can be quite
frustrating at times, is that Numpy has no understanding of row or column
vectors.  __An array with only one dimension is neither a row, nor a column
vector - it is just a 1D array__.  If you have a 1D array, and you want to use
it as a row vector, you need to reshape it to a shape of `(1, N)`. Similarly,
to use a 1D array as a column vector, you must reshape it to have shape
`(N, 1)`.


In general, when you are mixing 1D arrays with 2- or N-dimensional arrays, you
need to make sure that your arrays have the correct shape. For example:


```
r = np.random.randint(1, 10, 3)

print('r is a row:                                  ', r)
print('r.T should be a column:                      ', r.T, ' ... huh?')
print('Ok, make n a 2D array with one row:          ', r.reshape(1, -1))
print('We could also use the np.atleast_2d function:', np.atleast_2d(r))
print('Now we can transpose r to get a column:')
print(np.atleast_2d(r).T)
```


> Here we used a handy feature of the `reshape` method - if you pass `-1` for
> the size of one dimension, it will automatically determine the size to use
> for that dimension.
