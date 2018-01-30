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
 * [Array properties](#array-properties)
 * [Descriptive statistics](#descriptive-statistics)
 * [Reshaping and rearranging arrays](#reshaping-and-rearranging-arrays)
* [Operating on arrays](#operating-on-arrays)
 * [Scalar operations](#scalar-operations)
 * [Multi-variate operations](#multi-variate-operations)
 * [Matrix multplication](#matrix-multiplication)
 * [Broadcasting](#broadcasting)
 * [Linear algebra](#linear-algebra)
* [Array indexing](#array-indexing)
 * [Indexing multi-dimensional arrays](#indexing-multi-dimensional-arrays)
 * [Boolean indexing](#boolean-indexing)
 * [Coordinate array indexing](#coordinate-array-indexing)

* [Appendix A: Generating random numbers](#appendix-generating-random-numbers)
* [Appendix B: Importing Numpy](#appendix-importing-numpy)
* [Appendix C: Vectors in Numpy](#appendix-vectors-in-numpy)

* [Useful references](#useful-references)


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


This is a major source of confusion for people who are learning Python, and
are trying to write efficient code. It is _crucial_ to be able to distinguish
between a Python list and a Numpy array.


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
print('np.random.random gives us random numbers [0-1]:', np.random.random(5))
print('np.random.randint gives us random integers:    ', np.random.randint(1, 10, 5))
print('np.eye gives us an identity matrix:')
print(np.eye(4))
print('np.diag gives us a diagonal matrix:')
print(np.diag([1, 2, 3, 4]))
```


> See the [appendix](#appendix-generating-random-numbers) for more information
> on generating random numbers in Numpy.


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
a = np.arange(16).reshape(4, 4)
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
a = np.arange(16).reshape((4, 4))
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
a = np.arange(16).reshape((4, 4))
print(a)
print(a.T)
```


The `transpose` method allows you to obtain more complicated rearrangements
of an N-dimensional array's axes:


```
a = np.arange(24).reshape((2, 3, 4))
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


<a class="anchor" id="operating-on-arrays"></a>
## Operating on arrays


If you are coming from Matlab, you should read this section as, while many
Numpy operations behave similarly to Matlab, there are a few important
behaviours which differ from what you might expect.


<a class="anchor" id="scalar-operations"></a>
### Scalar operations


All of the mathematical operators you know and love can be applied to Numpy
arrays:


```
a = np.arange(1, 10).reshape((3, 3))
print('a:')
print(a)
print('a + 2:')
print( a + 2)
print('a * 3:')
print( a * 3)
print('a % 2:')
print( a % 2)
```


<a class="anchor" id="multi-variate-operations"></a>
### Multi-variate operations


Many operations in Numpy operate on an element-wise basis. For example:


```
a = np.ones(5)
b = np.random.randint(1, 10, 5)

print('a:     ', a)
print('b:     ', b)
print('a + b: ', a + b)
print('a * b: ', a * b)
```


This also extends to higher dimensional arrays:


```
a = np.ones((4, 4))
b = np.arange(16).reshape((4, 4))

print('a:')
print(a)
print('b:')
print(b)

print('a + b')
print(a + b)
print('a * b')
print(a * b)
```


Wait ... what's that you say? Oh, I couldn't understand because of all the
froth coming out of your mouth. I guess you're angry that `a * b` didn't give
you the matrix product, like it would have in Matlab.  Well all I can say is
that Numpy is not Matlab. Matlab operations are typically consistent with
linear algebra notation. This is not the case in Numpy. Get over it. Take a
calmative.


<a class="anchor" id="matrix-multiplication"></a>
### Matrix multiplication


When your heart rate has returned to its normal caffeine-induced state, you
can use the `@` operator or the `dot` method, to perform matrix
multiplication:


```
a = np.arange(1, 5).reshape((2, 2))
b = a.T

print('a:')
print(a)
print('b:')
print(b)

print('a @ b')
print(a @ b)

print('a.dot(b)')
print(a.dot(b))

print('b.dot(a)')
print(b.dot(a))
```


> The `@` matrix multiplication operator is a relatively recent addition to
> Python and Numpy, so you might not see it all that often in existing
> code. But it's here to stay, so if you don't need to worry about
> backwards-compatibility, go ahead and use it!


<a class="anchor" id="broadcasting"></a>
### Broadcasting


One of the coolest features of Numpy is _broadcasting_<sup>2</sup>.
Broadcasting allows you to perform element-wise operations on arrays which
have a different shape. For each axis in the two arrays, Numpy will implicitly
expand the shape of the smaller axis to match the shape of the larger one. You
never need to use `repmat` ever again!


> <sup>2</sup>Mathworks have shamelessly stolen Numpy's broadcasting behaviour
> and included it in Matlab versions from 2016b onwards, referring to it as
> _implicit expansion_.


Broadcasting allows you to, for example, add the elements of a 1D vector to
all of the rows or columns of a 2D array:


```
a = np.arange(9).reshape((3, 3))
b = np.arange(1, 4)
print('a:')
print(a)
print('b: ', b)
print('a * b (row-wise broadcasting):')
print(a * b)
print('a * b.T (column-wise broadcasting):')
print(a * b.reshape(-1, 1))
```


> Here we used a handy feature of the `reshape` method - if you pass `-1` for
> the size of one dimension, it will automatically determine the size to use
> for that dimension. Take a look at [the
> appendix](#appendix-vectors-in-numpy) for a discussion on vectors in Numpy.


Here is a more useful example, where we use broadcasting to de-mean the rows
or columns of an array:


```
a = np.arange(9).reshape((3, 3))
print('a:')
print(a)

print('a (cols demeaned):')
print(a - a.mean(axis=0))

print('a (rows demeaned):')
print(a - a.mean(axis=1).reshape(-1, 1))
```


> As demonstrated above, many functions in Numpy accept an `axis` parameter,
> allowing you to apply the function along a specific axis. Omitting the
> `axis` parameter will apply the function to the whole array.


Broadcasting can sometimes be confusing, but the rules which Numpy follows to
align arrays of different sizes, and hence determine how the broadcasting
should be applied, are pretty straightforward. If something is not working,
and you can't figure out why refer to the [official
documentation](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html).


<a class="anchor" id="linear-algebra"></a>
### Linear algebra


Numpy is first and foremost a library for general-purpose numerical computing.
But it does have a range of linear algebra functionality, hidden away in the
[`numpy.linalg`](https://docs.scipy.org/doc/numpy/reference/routines.linalg.html)
module. Here are a couple of quick examples:


```
import numpy.linalg as npla

a = np.array([[1, 2, 3,  4],
              [0, 5, 6,  7],
              [0, 0, 8,  9],
              [0, 0, 0, 10]])

print('a:')
print(a)

print('inv(a)')
print(npla.inv(a))

eigvals, eigvecs = npla.eig(a)

print('eigenvalues and vectors of a:')
for val, vec in zip(eigvals, eigvecs):
    print('{:2.0f} - {}'.format(val, vec))
```


<a class="anchor" id="array-indexing"></a>
## Array indexing


Just like in Matlab, slicing up your arrays is a breeze in Numpy.  If you are
after some light reading, you might want to check out the [comprehensive Numpy
Indexing
reference](https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html).


> As with indexing regular Python lists, array indices start from 0, and end
> indices (if specified) are exclusive.


Let's whet our appetites with some basic 1D array slicing. Numpy supports the
standard Python
[__slice__](https://www.pythoncentral.io/how-to-slice-listsarrays-and-tuples-in-python/)
notation for indexing, where you can specify the start and end indices, and
the step size, via the `start:stop:step` syntax:


```
a = np.arange(10)

print('a:                              ', a)
print('first element:                  ', a[0])
print('first two elements:             ', a[:2])
print('last element:                   ', a[a.shape[0] - 1])
print('last element again:             ', a[-1])
print('last two elements:              ', a[-2:])
print('middle four elements:           ', a[3:7])
print('Every second element:           ', a[1::2])
print('Every second element, reversed: ', a[-1::-2])
```


Note that slicing an array in this way returns a _view_, not a copy, into that
array:


```
a = np.arange(10)
print('a:', a)
every2nd = a[::2]
print('every 2nd:', every2nd)
every2nd += 10
print('a:', a)
```


<a class="anchor" id="indexing-multi-dimensional-arrays"></a>
### Indexing multi-dimensional arrays


Multi-dimensional array indexing works in much the same way as one-dimensional
indexing but with, well, more dimensions:


```
a = np.arange(25).reshape((5, 5))
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
a = np.arange(27).reshape((3, 3, 3))
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
a = np.arange(10)

print('a:                          ', a)
print('a > 5:                      ', a > 4)
print('elements in a that are > 5: ', a[a > 5])
```


In contrast to the simple indexing we have already seen, boolean indexing will
return a _copy_ of the indexed data, __not__ a view. For example:


```
a = np.arange(10)
b = a[a > 5]
print('a: ', a)
print('b: ', b)
print('Setting b[0] to 999')
b[0] = 999
print('a: ', a)
print('b: ', b)
```


> In general, any 'simple' indexing operation on a Numpy array, where the
> indexing object comprises integers, slices (using the standard Python
> `start:stop:step` notation), colons (`:`) and/or ellipses (`...`), will
> result in a __view__ into the indexed array. Any 'advanced' indexing
> operation, where the indexing object contains anything else (e.g. boolean or
> integer arrays, or even python lists), will result in a __copy__ of the
> data.


Logical operators `~` (not), `&` (and) and `|` (or) can be used to manipulate
and combine boolean Numpy arrays:


```
a    = np.arange(10)
gt5  = a > 5
even = a % 2 == 0

print('a:                                    ', a)
print('elements in a which are > 5:          ', a[ gt5])
print('elements in a which are <= 5:         ', a[~gt5])
print('elements in a which are even:         ', a[ even])
print('elements in a which are odd:          ', a[~even])
print('elements in a which are > 5 and even: ', a[gt5 &  even])
print('elements in a which are > 5 or odd:   ', a[gt5 | ~even])
```


Numpy also has two handy functions, `all` and `any`, which respectively allow
you to perform boolean `and` and `or` operations along the axes of an array:


```
a = np.arange(9).reshape((3, 3))

print('a:')
print(a)
print('rows with any element divisible by 3: ', np.any(a % 3 == 0, axis=1))
print('cols with any element divisible by 3: ', np.any(a % 3 == 0, axis=0))
print('rows with all elements divisible by 3:', np.all(a % 3 == 0, axis=1))
print('cols with all elements divisible by 3:', np.all(a % 3 == 0, axis=0))
```




<a class="anchor" id="coordinate-array-indexing"></a>
### Coordinate array indexing


You can index a numpy array using another array containing coordinates into
the first array.  As with boolean indexing, this will result in a copy of the
data.  Generally, you will need to have a separate array, or list, of
coordinates for each axis of the array you wish to index:


```
a = np.arange(16).reshape((4, 4))
print('a:')
print(a)

rows    = [0, 2, 3]
cols    = [1, 0, 2]
indexed = a[rows, cols]

for r, c, v in zip(rows, cols, indexed):
    print('a[{}, {}] = {}'.format(r, c, v))
```


The `numpy.where` function can be combined with boolean arrays to easily
generate of coordinate arrays for values which meet some condition:


```
a = np.arange(16).reshape((4, 4))
print('a:')
print(a)

evenx, eveny = np.where(a % 2 == 0)

print('even X coordinates:', evenx)
print('even Y coordinates:', eveny)

print(a[evenx, eveny])
```


<a class="anchor" id="appendix-generating-random-numbers"></a>
## Appendix A: Generating random numbers


<a class="anchor" id="appendix-importing-numpy"></a>
## Appendix B: Importing Numpy


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
Numpy (and its commonly used sub-modules) like this instead:


```
import numpy        as np
import numpy.random as npr
import numpy.linalg as npla
```


The downside to this is that you will have to prefix all Numpy functions with
`np.`, like so:


```
e = np.array([1, 2, 3, 4, 5])
z = np.zeros((100, 100))
d = np.diag([2, 3, 4, 5])
r = npr.random(5)

print(e)
print(z)
print(d)
print(r)
```


There is a big upside, however, in that other people who have to read/use your
code will like you a lot more. This is because it will be easier for them to
figure out what the hell your code is doing. Namespaces are your friend - use
them!


<a class="anchor" id="appendix-vectors-in-numpy"></a>
## Appendix C: Vectors in Numpy


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


<a class="anchor" id="useful-references"></a>
## Useful references


* [The Numpy manual](https://docs.scipy.org/doc/numpy/)
* [Linear algebra with `numpy.linalg`](https://docs.scipy.org/doc/numpy/reference/routines.linalg.html)
* [Numpy broadcasting](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)
* [Numpy indexing](https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html)
* [Python slicing](https://www.pythoncentral.io/how-to-slice-listsarrays-and-tuples-in-python/)