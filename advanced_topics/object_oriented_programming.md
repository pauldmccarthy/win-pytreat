# Object-oriented programming


By now you might have realised that __everything__ in Python is an
object. Strings are objects, numbers are objects, functions are objects,
modules are objects - __everything__ is an object!


But this does not mean that you have to use Python in an object-oriented
fashion. You can stick with functions and statements, and get quite a lot
done. But some problems are just easier to solve, and to reason about, when
you use an object-oriented approach.


## Objects versus classes


If you are versed in C++, Java, C#, or some other object-oriented language,
then this should all hopefully sound familiar, and you can skip to the next
section.


If you have not done any object-oriented programming before, your first step
is to understand the difference between _objects_ (also known as _instances_)
and _classes_ (also known as _types_).


If you have some experience in C, then you can start off by thinking of a
class as like a `struct` definition - it is a specification for the layout of
a chunk of memory. For example, here is a typical struct definition:

> ```
> /**
>  * Struct representing a stack.
>  */
> typedef struct __stack {
>   uint8_t capacity; /**< the maximum capacity of this stack */
>   uint8_t size;     /**< the current size of this stack     */
>   void  **top;      /**< pointer to the top of this stack   */
> } stack_t;
> ```


Now, an _object_ is not a definition, but rather a thing which resides in
memory. An object can have _attributes_ (pieces of information), and _methods_
(functions associated with the object). You can pass objects around your code,
manipulate their attributes, and call their methods.


Returning to our C metaphor, you can think of an object as like an
instantiation of a struct:


> ```
> stack_t stack;
> stack.capacity = 10;
> ```


The fundamental difference between a `struct` in C, and a `class` in Python
and other object oriented languages, is that you can't (easily) add functions
to a `struct` - it is just a chunk of memory. Whereas in Python, you can add
functions to your class definition, which will then be added as methods when
you create an object from that class.


Of course there are many more differences between C structs and classes (most
notably [inheritance](todo), and [protection](todo)). But if you can
understand the difference between a _definition_ of a C struct, and an
_instantiation_ of that struct, then you are most of the way towards
understanding the difference between a Python _class_, and a Python _object_.


> But just to confuse you, remember that in Python, __everything__ is an
> object - even classes!


## Defining a class


Defining a class in Python is simple. Let's take on a small project, by
developing a class which can be used in place of the `fslmaths` shell command.


```
class FSLMaths(object):
    pass
```


In this statement, we defined a new class called `FSLMaths`, which inherits
from the built-in `object` base-class (see [below](todo) for more details on
inheritance).


Now that we have defined our class, we can create objects - instances of that
class - by calling the class itself, as if it were a function:


```
fm1 = FSLMaths()
fm2 = FSLMaths()
print(fm1)
print(fm2)
```


Although these objects are not of much use at this stage. Let's do some more
work.


## Object creation - the `__init__` method


The first thing that our `fslmaths` replacement will need is an input image.
It makes sense to pass this in when we create an `FSLMaths` object:


```
class FSLMaths(object):
    def __init__(self, inimg):
        self.input = inimg
```


Here we have added a _method_ called `__init__` to our class (remember that a
_method_ is just a function which is associated with a specific object).  This
method expects two arguments - `self`, and `inimg`. So now, when we create an
instance of the `FSLMaths` class, we will need to provide an input image:


```
import nibabel as nib
import os.path as op

input = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
inimg = nib.load(input)
fm    = FSLMaths(inimg)
```


There are a couple of things to note here:


__Our method is called__ `__init__`__, but we didn't actually call the__
`__init__` __method!__ `__init__` is a special method in Python - it is called
when an instance of a class is created. And recall that we can create an
instance of a class by calling the class in the same way that we call a
function.


__We didn't specify the `self` argument - what gives?!?__ The `self` argument
is a special argument that is specific to methods in Python. If you are coming
from C++, Java, C# or similar, `self` in Python is equivalent to `this` in
those languages.


### The `self` argument


In a method, the `self` argument is a reference to the object that the method
was called on. So in this line of code:


```
fm = FSLMaths(inimg)
```


the `self` argument in `__init__` will be a reference to the `FSLMaths` object
that has been created (and is then assigned to the `fm` variable, after the
`__init__` method has finished).


But note that we do not need to provide the `self` argument - this is a quirk
specific to methods in Python - when you call a method on an object (or a
class, to create a new object), the Python runtime will take care of passing
the instance as the `self` argument to to the method.


But when you are writing a class, you _do_ need to explicitly list `self` as
the first argument to all of the methods of the class.


## Attributes


In Python, the term _attribute_ is used to refer to a piece of information
that is associated with an object. An attribute is generally a reference to
another object (which might be a string, a number, or a list, or some other
more complicated object).


Remember that we modified our `FSLMaths` class so that it is passed an input
image on creation:


```
class FSLMaths(object):
    def __init__(self, inimg):
        self.input = inimg

input = op.expanduser('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
fm = FSLMaths(nib.load(input))
```


Take a look at what is going on in the `__init__` method - we take the `inimg`
argument, and create a reference to it called `self.input`. We have added an
_attribute_ to the `FSLMaths` instance, called `input`, and we can access that
attribute like so:


```
print('Input for our FSLMaths instance: {}'.format(fm.input))
```


And that concludes the section on adding attributes to Python objects.


Just kidding. But it really is that simple. This is one aspect of Python which
might be quite jarring to you if you are coming from a language with more
rigid semantics, such as C++ or Java. In those languages, you must pre-specify
all of the attributes and methods that are a part of a class. But Python works
a bit differently - you add attributes to an object affer it has been created.
In fact, you can even do this outside of the class definition<sup>1</sup>:


```
fm = FSLMaths(inimg)
fm.another_attribute = 'Haha'
print(fm.another_attribute)
```


> <sup>1</sup>This not possible with many of the built-in types, such as
> `list` and `dict` objects, nor with types that are defined in Python
> extensions (Python modules that are written in C).


__But...__ while attributes can be added to a Python object at any time, it is
good practice (and makes for more readable and maintainable code) to add all
of an object's attributes within the `__init__` method.


## Methods


We've been dilly-dallying on this little `FSLMaths` project for a while now,
but our class still can't actually do anything. Let's start adding some
functionality:


```
class FSLMaths(object):
    """This class is the Python version of the fslmaths shell command. """

    def __init__(self, inimg):
        """Create an FSLMaths object, which will work on the specified input
        image.
        """
        self.input      = inimg
        self.operations = []

    def add(self, value):
        """Add the specified value to the current image. """
        self.operations.append(('add', value))

    def mul(self, value):
        """Multiply the current image by the specified value. """
        self.operations.append(('mul', value))

    def div(self, value):
        """Divide the current image by the specified value. """
        self.operations.append(('div', value))
```


Woah woah, [slow down egg-head, you're going a mile a
minute!](https://www.youtube.com/watch?v=yz-TemWooa4).  We've modified
`__init__` so that a second attribute called `operations` is added to our
object - this `operations` attribute is simply a list.


Then, we added a handful of methods - `add`, `mul`, and `div` - which each
append a tuple to that `operations` list.


> Note that, just like in the `__init__` method, the first argument that will
> be passed to the `add` method is `self` - a reference to the object that the
> method has been called on.


The idea behind this design is that our `FSLMaths` class will not actually do
anything when we call the `add`, `mul` or `div` methods. Instead, it will
"stage" each operation, and then perform them all in one go. So let's add
another method, `run`, which actually does the work:


```
import nibabel as nib


class FSLMaths(object):
    """This class is the Python version of the fslmaths shell command. """


    def __init__(self, inimg):
        """Create an FSLMaths object, which will work on the specified input
        image.
        """
        self.input      = inimg
        self.operations = []


    def add(self, value):
        """Add the specified value to the current image. """
        self.operations.append(('add', value))


    def mul(self, value):
        """Multiply the current image by the specified value. """
        self.operations.append(('mul', value))


    def div(self, value):
        """Divide the current image by the specified value. """
        self.operations.append(('div', value))


    def run(self, output=None):
        """Apply all staged operations, and return the final result, or
        save it to the specified output file.
        """

        data = self.input.get_data()

        for operation, value in self.operations:

            # if value is a string, we assume that
            # it is a path to an image. Otherwise,
            # we assume that it is a scalar value.
            if isinstance(image, str):
                image = nib.load(value)
                value = image.get_data()

            if operation == 'add':
                data = data + value
            elif operation == 'mul':
                data = data * value
            elif operation == 'div':
                data = data / value

        # turn final output into a nifti,
        # and save it to disk if an
        # 'output' has been specified.
        outimg = nib.nifti1.Nifti1Image(data, inimg.affine)

        if output is not None:
            nib.save(outimg, output)

        return outimg
```


We now have a useable (but not very useful) `FSLMaths` class!


```
input = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
inimg = nib.load(input)
fm = FSLMaths(inimg)
fm.mul(op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm_brain_mask.nii.gz')
fm.run()
```


## Appendix: The `object` base-class

In older code bases, you might see class definitions that look like this,
without explicitly inheriting from the `object` base class:

> ```
> class MyClass:
>     ...
> ```

This syntax is a [throwback to older versions of
Python](https://docs.python.org/2/reference/datamodel.html#new-style-and-classic-classes)
- in Python 3 there is actually no difference between defining a class in this
way, and defining a class in the way we have shown in this tutorial.

But if you are writing code which needs to run on both Python 2 and 3, you
_must_ define your classes to explicitly inherit from the `object` base class.


## Appendix: `__init__` versus `__new__`


In Python, object creation is actually a two-stage process - _creation_, and
then _initialisation_. The `__init__` method gets called during the
_initialisation_ stage - its job is to initialise the state of the object. But
note that, by the time `__init__` gets called, the object has already been
created.


You can also define a method called `__new__` if you need to control the
creation stage, although this is very rarely needed. A brief explanation on
the difference between `__new__` and `__init__` can be found
[here](https://www.reddit.com/r/learnpython/comments/2s3pms/what_is_the_difference_between_init_and_new/cnm186z/),
and you may also wish to take a look at the [official Python
docs](https://docs.python.org/3.5/reference/datamodel.html#basic-customization).
