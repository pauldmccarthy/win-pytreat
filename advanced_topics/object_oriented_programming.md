# Object-oriented programming in Python


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
class as like a `struct` definition - a `struct` is a specification for the
layout of a chunk of memory. For example, here is a typical struct definition:

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


One of the major differences between a `struct` in C, and a `class` in Python
and other object oriented languages, is that you can't (easily) add functions
to a `struct` - it is just a chunk of memory. Whereas in Python, you can add
functions to your class definition, which will then be added as methods when
you create an object from that class.


Of course there are many more differences between C structs and classes (most
notably [inheritance](todo), [polymorphism](todo), and [access
protection](todo)). But if you can understand the difference between a
_definition_ of a C struct, and an _instantiation_ of that struct, then you
are most of the way towards understanding the difference between a _class_,
and an _object_.


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
_method_ is just a function which is defined in a cliass, and which can be
called on instances of that class).  This method expects two arguments -
`self`, and `inimg`. So now, when we create an instance of the `FSLMaths`
class, we will need to provide an input image:


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
is a special argument for methods in Python. If you are coming from C++, Java,
C# or similar, `self` in Python is equivalent to `this` in those languages.


### The `self` argument


In a method, the `self` argument is a reference to the object that the method
was called on. So in this line of code:


```
fm = FSLMaths(inimg)
```


the `self` argument in `__init__` will be a reference to the `FSLMaths` object
that has been created (and is then assigned to the `fm` variable, after the
`__init__` method has finished).


But note that we do not need to explicitly provide the `self` argument - when
you call a method on an object, or when you create a new object, the Python
runtime will take care of passing the instance as the `self` argument to the
method.


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

input = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
fm    = FSLMaths(nib.load(input))
```


Take a look at what is going on in the `__init__` method - we take the `inimg`
argument, and create a reference to it called `self.input`. We have added an
_attribute_ to the `FSLMaths` instance, called `input`, and we can access that
attribute like so:


```
print('Input for our FSLMaths instance: {}'.format(fm.input.get_filename()))
```


And that concludes the section on adding attributes to Python objects.


Just kidding. But it really is that simple. This is one aspect of Python which
might be quite jarring to you if you are coming from a language with more
rigid semantics, such as C++ or Java. In those languages, you must pre-specify
all of the attributes and methods that are a part of a class. But Python is
more flexible - you simply add attributes to an object affer it has been
created.  In fact, you can even do this outside of the class
definition<sup>1</sup>:


```
fm = FSLMaths(inimg)
fm.another_attribute = 'Haha'
print(fm.another_attribute)
```


__But...__ while attributes can be added to a Python object at any time, it is
good practice (and makes for more readable and maintainable code) to add all
of an object's attributes within the `__init__` method.


> <sup>1</sup>This not possible with many of the built-in types, such as
> `list` and `dict` objects, nor with types that are defined in Python
> extensions (Python modules that are written in C).


## Methods


We've been dilly-dallying on this little `FSLMaths` project for a while now,
but our class still can't actually do anything. Let's start adding some
functionality:


```
class FSLMaths(object):

    def __init__(self, inimg):
        self.input      = inimg
        self.operations = []

    def add(self, value):
        self.operations.append(('add', value))

    def mul(self, value):
        self.operations.append(('mul', value))

    def div(self, value):
        self.operations.append(('div', value))
```


Woah woah, [slow down egg-head, you're going a mile a
minute!](https://www.youtube.com/watch?v=yz-TemWooa4)  We've modified
`__init__` so that a second attribute called `operations` is added to our
object - this `operations` attribute is simply a list.


Then, we added a handful of methods - `add`, `mul`, and `div` - which each
append a tuple to that `operations` list.


> Note that, just like in the `__init__` method, the first argument that will
> be passed to these methods is `self` - a reference to the object that the
> method has been called on.


The idea behind this design is that our `FSLMaths` class will not actually do
anything when we call the `add`, `mul` or `div` methods. Instead, it will
"stage" each operation, and then perform them all in one go. So let's add
another method, `run`, which actually does the work:


```
import numpy   as np
import nibabel as nib

class FSLMaths(object):

    def __init__(self, inimg):
        self.input      = inimg
        self.operations = []

    def add(self, value):
        self.operations.append(('add', value))

    def mul(self, value):
        self.operations.append(('mul', value))

    def div(self, value):
        self.operations.append(('div', value))

    def run(self, output=None):

        data = np.array(self.input.get_data())

        for oper, value in self.operations:

            # Values could be an image that
            # has already been loaded.
            elif isinstance(value, nib.nifti1.Nifti1Image):
                value = value.get_data()

            # Otherwise we assume that
            # values are scalars.

            if oper == 'add':
                data = data + value
            elif oper == 'mul':
                data = data * value
            elif oper == 'div':
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
mask  = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm_brain_mask.nii.gz')
input = nib.load(input)
mask  = nib.load(mask)
fm    = FSLMaths(input)

fm.mul(mask)
fm.add(-10)

outimg = fm.run()

norigvox = (inimg .get_data() > 0).sum()
nmaskvox = (outimg.get_data() > 0).sum()

print('Number of voxels >0 in original image: {}'.format(norigvox))
print('Number of voxels >0 in masked image:   {}'.format(nmaskvox))
```


## Protecting attribute access


In our `FSLMaths` class, the input image was added as an attribute called
`input` to `FSLMaths` objects. We saw that it is easy to read the attributes
of an object - if we have a `FSLMaths` instance called `fm`, we can read its
input image via `fm.input`.


But it is just as easy to write the attributes of an object. What's to stop
some sloppy research assistant from overwriting our `input` attribute?


```
inimg = nib.load(op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz'))
fm = FSLMaths(inimg)
fm.input = None
fm.run()
```


Well, the scary answer is ... there is __nothing__ stopping you from doing
whatever you want to a Python object. You can add, remove, and modify
attributes at will. You can even replace the methods of an existing object if
you like:


```
fm = FSLMaths(inimg)

def myadd(value):
    print('Oh no, I\'m not going to add {} to '
          'your image. Go away!'.format(value))

fm.add = myadd
fm.add(123)

fm.mul = None
fm.mul(123)
```


But you really shouldn't get into the habit of doing devious things like
this - take a look at the appendix for a [brief discussion on this topic](todo).


Python tends to assume that programmers are "responsible adults", and hence
doesn't do much in the way of restricting access to the attributes or methods
of an object. This is in contrast to languages like C++ and Java, where the
notion of a private attribute or method is strictly enforced by the language.


However, there are a couple of conventions in Python that are [universally
adhered
to](https://docs.python.org/3.5/tutorial/classes.html#private-variables):

* Class-level attributes and methods, and module-level attributes, functions,
  and classes, which begin with a single underscore (`_`), should be
  considered _protected_ - they are intended for internal use only, and should
  not be considered part of the public API of a class or module.  This is not
  enforced by the language in any way<sup>2</sup> - remember, we are all
  responsible adults here!

* Class-level attributes and methods which begin with a double-underscore
  (`__`) should be considered _private_. Python provides a weak form of
  enforcement for this rule - any attribute or method with such a name will
  actually be _renamed_ (in a standardised manner) at runtime, so that it is
  not accessible through its original name. It is still accessible via its
  [mangled
  name](https://docs.python.org/3.5/tutorial/classes.html#private-variables)
  though.


> <sup>2</sup> With the exception that module-level fields which begin with a
> single underscore will not be imported into the local scope via the
> `from [module] import *` techinque.


So with all of this in mind, we can adjust our `FSLMaths` class to discourage
our sloppy research assistant from overwriting the `input` attribute:


```
# remainder of definition omitted for brevity
class FSLMaths(object):
    def __init__(self, inimg):
        self.__input      = inimg
        self.__operations = []
```

But now we have lost the ability to read our `__input` attribute:


```
inimg = nib.load(op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz'))
fm = FSLMaths(inimg)
print(fm.__input)
```


### A better way - properties


Python has a feature called
[`properties`](https://docs.python.org/3.5/library/functions.html#property),
which is a nice means of controlling access to the attributes of an object. We
can use properties by defining a "getter" method which can be used to access
our attributes, and "decorating" them with the `@property` decorator (we will
cover decorators in a later practical).


```
class FSLMaths(object):
    def __init__(self, inimg):
        self.__input      = inimg
        self.__operations = []

    @property
    def input(self):
        return self.__input
```


So we are still storing our input image as a private attribute, but now
we have made it available in a read-only manner via the `input` property:


```
input = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
inimg = nib.load(input)
fm    = FSLMaths(inimg)

print(fm.input.get_filename())
```


Note that, even though we have defined `input` as a method, we can access it
like an attribute - this is due to the magic behind the `@property` decorator.


We can also define "setter" methods for a property. For example, we might wish
to add the ability for a user of our `FSLMaths` class to change the input
image after creation.


```
class FSLMaths(object):
    def __init__(self, inimg):
        self.__input      = None
        self.__operations = []
        self.input        = inimg

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, value):
        if not isinstance(value, nib.nifti1.Nifti1Image):
            raise ValueError('value must be a NIFTI image!')
        self.__input = value
```


Property setters are a nice way to add validation logic when an attribute is
assigned a value. We are doing this in the above example, by making sure that
the new input is a NIFTI image:


```
input = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
inimg = nib.load(input)
fm    = FSLMaths(inimg)

print('Input:     ', fm.input.get_filename())

# let's change the input
# to a different image
input2   = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm_brain.nii.gz')
inimg2   = nib.load(input2)
fm.input = inimg2

print('New input: ', fm.input.get_filename())

# this is going to explode
fm.input = 'abcde'
```

> Note also that we used the `input` setter method within `__init__` to
> validate the initial `inimg` that was passed in during creation.


## Inheritance


One of the major advantages of an object-oriented programming approach is
_inheritance_ - the ability to define hierarchical relationships between
classes and instances.


### The basics


For example, a veterinary surgery might be running some Python code which
looks like the following. Perhaps it is used to assist the nurses in
identifying an animal when it arrives at the surgery:


```
class Animal(object):
    def noiseMade(self):
        raise NotImplementedError('This method is implemented by sub-classes')

class Dog(Animal):
    def noiseMade(self):
        return 'Woof'

class Cat(Animal):
    def noiseMade(self):
        return 'Meow'

class Labrador(Dog):
    pass

class Chihuahua(Dog):
    def noiseMade(self):
        return 'Yap yap yap'
```


Hopefully this example doesn't need much in the way of explanation - this
collection of classes captures a hierarchical relationship which exists in the
real world (and also captures the inherently annoying nature of
chihuahuas). For example, in the real world, all dogs are animals, but not all
animals are dogs.  Therefore in our model, the `Dog` class has specified
`Animal` as its base class. We say that the `Dog` class _extends_, _derives
from_, or _inherits from_, the `Animal` class, and that all `Dog` instances
are also `Animal` instances (but not vice-versa).


What does that `noiseMade` method do?  There is a `noiseMade` method defined
on the `Animal` class, but it has been re-implemented, or _overridden_ in the
`Dog`, `Cat`, and `Chihuahua` classes (but not on the `Labrador` class).  We
can call the `noiseMade` method on any `Animal` instance, but the specific
behaviour that we get is dependent on the specific type of animal.


```
d  = Dog()
l  = Labrador()
c  = Cat()
ch = Chihuahua()

print('Noise made by dogs:       {}'.format(d .noiseMade()))
print('Noise made by labradors:  {}'.format(l .noiseMade()))
print('Noise made by cats:       {}'.format(c .noiseMade()))
print('Noise made by chihuahuas: {}'.format(ch.noiseMade()))
```


### Code re-use and problem decomposition


Inheritance allows us to split a problem into smaller problems, and to re-use
code.  Let's demonstrate this with a more involved example.  Imagine that a
former colleague had written a class called `Operator`:


> I know this is a little abstract (and quite contrived), but bear with me
> here.


```
class Operator(object):

    def __init__(self):
        self.__operations = []
        self.__opFuncs    = {}

    @property
    def operations(self):
        return list(self.__operations)

    @property
    def functions(self):
        return dict(self.__opFuncs)

    def addFunction(self, name, func):
        self.__opFuncs[name] = func

    def do(self, name, *values):
        self.__operations.append((name, values))

    def preprocess(self, value):
        return value

    def run(self, input):
        data = self.preprocess(input)
        for oper, vals in self.__operations:
            func = self.__opFuncs[oper]
            vals = [self.preprocess(v) for v in vals]
            data = func(data, *vals)
        return data
```


This `Operator` class provides an interface and logic to execute a chain of
operations - an operation is some function which accepts one or more inputs,
and produce one output.


But it stops short of defining any operations. Instead, we can create another
class - a sub-class - which derives from the `Operator` class. This sub-class
will define the operations that will ultimately be executed by the `Operator`
class. All that the `Operator` class does is:

- Allow functions to be registered with the `addFunction` method - all
  registered functions can be used via the `do` method.

- Stage an operation (using a registered function) via the `do` method. Note
  that `do` allows any number of values to be passed to it, as we used the `*`
  operator when specifying the `values` argument.

- Run all staged operations via the `run` method - it passes an input through
  all of the operations that have been staged, and then returns the final
  result.


Let's define a sub-class:


```
class NumberOperator(Operator):

    def __init__(self):
        super().__init__()
        self.addFunction('add',    self.add)
        self.addFunction('mul',    self.mul)
        self.addFunction('negate', self.negate)

    def preprocess(self, value):
        return float(value)

    def add(self, a, b):
        return a + b

    def mul(self, a, b):
        return a * b

    def negate(self, a):
        return -a
```


The `NumberOperator` is a sub-class of `Operator`, which we can use for basic
numerical calculations. It provides a handful of simple numerical methods, but
the most interesting stuff is inside `__init__`:


> ```
> super().__init__()
> ```


This line invokes `Operator.__init__` - the initialisation method for the
`Operator` base-class. In Python, we can use the [built-in `super`
method](https://docs.python.org/3.5/library/functions.html#super) to take care
of correctly calling methods that are defined in an object's base-class (or
classes, in the case of [multiple inheritance](todo)).


> ```
> self.addFunction('add',    self.add)
> self.addFunction('mul',    self.mul)
> self.addFunction('negate', self.negate)
> ```


Here we are registering all of the functionality that is provided by the
`NumberOperator` class, via the `Opoerator.addFunction` method.


The `NumberOperator` class has also overridden the `preprocess` method, to
ensure that all values handled by the `Operator` are numbers. This method gets
called within the `run` method - for a `NumberOperator` instance, the
`NumberOperator.preprocess` method will get called<sup>1</sup>.

> <sup>1</sup> We can still [access overridden base-class methods](todo link)
> via the `super()` function, or by explicitly calling the base-class
> implementation.



Now let's see what our `NumberOperator` class does:


```
no = NumberOperator()
no.do('add', 10)
no.do('mul', 2)
no.do('negate')

print('Operations on {}: {}'.format(10,  no.run(10)))
print('Operations on {}: {}'.format(2.5, no.run(5)))
```


It works! While this is a contrived example, hopefully you can see how
inheritance can be used to break a problem down into sub-problems:

- The `Operator` class provides all of the logic needed to manage and execute
  operations, without caring about what those operations are actually doing.

- This leaves the `NumberOperator` class free to concentrate on implementing
  the functions that are specific to its task, and not having to worry about
  how they are executed.


We could also easily implement other `Operator` sub-classes to work on
different data types, such as arrays, images, or even non-numeric data such as
strings:


```
class StringOperator(Operator):
    def __init__(self):
        super().__init__()
        self.addFunction('capitalise', self.capitalise)
        self.addFunction('concat',     self.concat)

    def preprocess(self, value):
        return str(value)

    def capitalise(self, s):
        return ' '.join([w[0].upper() + w[1:] for w in s.split()])

    def concat(self, s1, s2):
        return s1 + s2

so = StringOperator()
so.do('capitalise')
so.do('concat', '!')

print(so.run('python is an ok language'))
```


### Polymorphism


Inheritance also allows us to take advantage of _polymorphism_, which refers
to idea that, in an object-oriented language, we should be able to use an
object without having complete knowledge about the class, or type, of that
object. For example, we should be able to write a function which expects an
`Operator` instance, but which should work on an instance of any `Operator`
sub-classs. For example, we can write a function which prints a summary
of an `Operator` instance:


```
def operatorSummary(o):
    print(type(o).__name__)
    print('  All functions: ')
    for fname in o.functions.keys():
        print('    {}'.format(fname))
    print('  Staged operations: ')
    for i, (fname, vals) in enumerate(o.operations):
        vals = ', '.join([str(v) for v in vals])
        print('    {}: {}({})'.format(i + 1, fname, vals))
```


Because the `operatorSummary` function only uses methods that are defined
in the `Operator` base-class, we can use it on _any_ `Operator` instance,
regardless of its type:


```
operatorSummary(no)
operatorSummary(so)
```


### Multiple inheritance


Mention the MRO





## Class attributes and methods


Up to this point we have been covering how to add attributes and methods to an
_object_. But it is also possible to add methods and attributes to a _class_
(`static` methods and fields, for those of you familiar with C++ or Java).


Class attributes and methods can be accessed without having to create an
instance of the class - they are not associated with individual objects, but
rather to the class itself.


Class methods and attributes can be useful in several scenarios - as a
hypothetical, not very useful example, let's say that we want to gain usage
statistics for how many times each type of operation is used on instances of
our `FSLMaths` class. We might, for example, use this information in a grant
application to show evidence that more research is needed to optimise the
performance of the `add` operation.


### Class attributes


Let's add a `dict` as a class attribute to the `FSLMaths` class - this `dict`

called on a `FSLMaths` object, that object will increment the class-level
counters for each operation that is applied:


```
import numpy   as np
import nibabel as nib

class FSLMaths(object):

    # It's this easy to add a class-level
    # attribute. This dict is associated
    # with the FSLMaths *class*, not with
    # any individual FSLMaths instance.
    opCounters = {}

    def __init__(self, inimg):
        self.input      = inimg
        self.operations = []

    def add(self, value):
        self.operations.append(('add', value))

    def mul(self, value):
        self.operations.append(('mul', value))

    def div(self, value):
        self.operations.append(('div', value))

    def run(self, output=None):

        data = np.array(self.input.get_data())

        for oper, value in self.operations:

            # Code omitted for brevity

            # Increment the usage counter
            # for this operation.
            FSLMaths.opCounters[oper] = self.opCounters.get(oper, 0) + 1
```


So let's see it in action:


```
input = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
mask  = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm_brain_mask.nii.gz')
inimg = nib.load(input)

fm1 = FSLMaths(inimg)
fm2 = FSLMaths(inimg)

fm1.mul(mask)
fm1.add(15)

fm2.add(25)
fm1.div(1.5)

fm1.run()
fm2.run()

print('FSLMaths usage statistics')
for oper in ('add', 'div', 'mul'):
    print('  {} : {}'.format(oper, FSLMaths.opCounters.get(oper, 0)))
```


### Class methods


It is just as easy to add a method to a class - let's take our reporting code
from above, and add it as a method to the `FSLMaths` class:


```
class FSLMaths(object):

    opCounters = {}

    # We use the @classmethod decorator to denote a class
    # method. Also note that, where a regular method which
    # is called on an instance will be passed the instance
    # as its first argument ('self'), a class method will
    # be passed the class itself as the first argument -
    # the standard convention is to call this argument 'cls'.
    @classmethod
    def usage(cls):
        print('FSLMaths usage statistics')
        for oper in ('add', 'div', 'mul'):
            print('  {} : {}'.format(oper, FSLMaths.opCounters.get(oper, 0)))

    def __init__(self, inimg):
        self.input      = inimg
        self.operations = []

    def add(self, value):
        self.operations.append(('add', value))

    def mul(self, value):
        self.operations.append(('mul', value))

    def div(self, value):
        self.operations.append(('div', value))

    def run(self, output=None):

        data = np.array(self.input.get_data())

        for oper, value in self.operations:

            # Code omitted for brevity

            # Increment the usage counter
            # for this operation.
            FSLMaths.opCounters[oper] = self.opCounters.get(oper, 0) + 1
```


alling a class method is the same as accessing a class attribute:


```
input = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
mask  = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm_brain_mask.nii.gz')
inimg = nib.load(input)

fm1 = FSLMaths(inimg)
fm2 = FSLMaths(inimg)

fm1.mul(mask)
fm1.add(15)

fm2.add(25)
fm1.div(1.5)

fm1.run()
fm2.run()

FSLMaths.usage()
```

Note that it is also possible to access class attributes and methods through
instances:


```
print(fm1.opCounters)
print(fm1.usage())
```


## Appendix: The `object` base-class


When you are defining a class, you need to specify the base-class from which
your class inherits. If your class does not inherit from a particular class,
then it should inherit from the built-in `object` class:

> ```
> class MyClass(object):
>     ...
> ```


However, in older code bases, you might see class definitions that look like
this, without explicitly inheriting from the `object` base class:

> ```
> class MyClass:
>     ...
> ```

This syntax is a [throwback to older versions of
Python](https://docs.python.org/2/reference/datamodel.html#new-style-and-classic-classes).
In Python 3 there is actually no difference between in whether you define your
class in the way we have shown in this tutorial, or the old-style way.


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


## Appendix: Monkey-patching


The act of run-time modification of objects or class definitions is referred
to as [_monkey-patching_](https://en.wikipedia.org/wiki/Monkey_patch) and,
while it is allowed by the Python programming language, it is generally
considered quite rude practice.


Just because you _can_ do something doesn't mean that you _should_. Python
gives you the flexibility to write your software in whatever manner you deem
suitable.  __But__ if you want to write software that will be used, adopted,
and maintained by other people, you should be polite, write your code in a
clear, readable fashion, and avoid the use of devious tactics such as
monkey-patching.


__However__, while monkey-patching may seem like a horrific programming
practice to those of you coming from the realms of C++, Java, and the like,
(and it is horrific in many cases), it can be _extremely_ useful in certain
circumstances.  For instance, monkey-patching makes unit testing [a
breeze](https://docs.python.org/3.5/library/unittest.mock.html) in Python.


As another example, consider the scenario where you are dependent on a third
party library which has bugs in it. No problem - while you are waiting for the
library author to release a new version of the library, you can write your own
working implementation and [monkey-patch it
in](https://git.fmrib.ox.ac.uk/fsl/fsleyes/fsleyes/blob/0.21.0/fsleyes/views/viewpanel.py#L726)!


## Appendix: Method overloading


Method overloading (defining multiple methods on a class, each accepting
different arguments) is one of the only object-oriented features that is not
present in Python. Becuase Python does not perform any runtime checks on the
types of arguments that are passed to a method, or the compatibility of the
method to accept the arguments, it would not be possible to determine which
implementation of a method is to be called.


However, because a Python method can be written to accept any number or type
of arguments, it is very easy to to build your own overloading logic by
writing a "dispatch" method. Here is YACE (Yet Another Contrived Example):


```
class Adder(object):

    def add(self, *args):
        if   len(args) == 2: return self.__add2(*args)
        elif len(args) == 3: return self.__add3(*args)
        elif len(args) == 4: return self.__add4(*args)

    def __add2(self, a, b):
        return a + b

    def __add3(self, a, b, c):
        return a + b + c

    def __add4(self, a, b, c, d):
        return a + b + c + d

a = Adder()

print('Add two:   {}'.format(a.add(1, 2)))
print('Add three: {}'.format(a.add(1, 2, 3)))
print('Add four:  {}'.format(a.add(1, 2, 3, 4)))
```

## Useful references


https://docs.python.org/3.5/library/unittest.mock.html
https://docs.python.org/3.5/tutorial/classes.html
https://docs.python.org/3.5/library/functions.html
https://docs.python.org/2/reference/datamodel.html
https://www.reddit.com/r/learnpython/comments/2s3pms/what_is_the_difference_between_init_and_new/cnm186z/
https://docs.python.org/3.5/reference/datamodel.html
http://www.jesshamrick.com/2011/05/18/an-introduction-to-classes-and-inheritance-in-python/
https://www.digitalocean.com/community/tutorials/understanding-class-inheritance-in-python-3

https://docs.python.org/3.5/library/functions.html#super