# Numpy


This section introduces you to [`numpy`](http://www.numpy.org/), Python's
numerical computing library.


Numpy is not actually part of the standard Python library. But it is a
fundamental part of the Python ecosystem - it forms the basis for many
important Python libraries, and it (along with its partners
[`scipy`](https://www.scipy.org/) and [`matplotlib`](https://matplotlib.org/))
is what makes Python a viable alternative to Matlab as a scientific computing
platform.


## Contents


* [The Python list versus the Numpy array](#the-python-list-versus-the-numpy-array)
* [Importing Numpy](#importing-numpy)
* [Numpy basics](#numpy-basics)
* [Indexing](#indexing)


<a class="anchor" id="the-python-list-versus-the-numpy-array"></a>
## The Python list versus the Numpy array


Numpy adds a new data type to the Python language - the `array` (more
specifically, the `ndarray`). You have already been introduced to the Python
`list`, which you can easily use to store a handful of numbers (or anything
else):


```
data = [10, 8, 12, 14, 7, 6, 11]
```


You could also emulate a 2D or ND matrix by using lists of lists, for example:


```
xyz_coords = [[-11.4, 1.0, 22.6], [22.7, -32.8, 19.1], [62.8, -18.2, -34.5]]
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
Python. It is very important to be able to distinguish between a Python list,
and a Numpy array.


A list in python is akin to a cell array in Matlab - they can store anything,
but are extremely inefficient, and unwieldy when you have more than a couple
of dimensions.


These are in contrast to the Numpy array and Matlab matrix, which are both
thin wrappers around a contiguous chunk of memory, and which provide
blazing-fast performance (because behind the scenes in both Numpy and Matlab,
it's C, C++ and FORTRAN all the way down).


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
same way that we did earlier, by denoting them with square brackets `[` and
`]`.


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


I'm emphasising this to help you understand the difference between Python
lists and Numpy arrays. Apologies if you've already got it.


<a class="anchor" id="importing-numpy"></a>
## Importing numpy


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


<a class="anchor" id="numpy-basics"></a>
## Numpy basics


Let's get started.


```
import numpy as np
```


<a class="anchor" id="indexing"></a>
## Indexing
