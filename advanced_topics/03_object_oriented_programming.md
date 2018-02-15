# Object-oriented programming in Python


By now you might have realised that __everything__ in Python is an
object. Strings are objects, numbers are objects, functions are objects,
modules are objects - __everything__ is an object!


But this does not mean that you have to use Python in an object-oriented
fashion. You can stick with functions and statements, and get quite a lot
done. But some problems are just easier to solve, and to reason about, when
you use an object-oriented approach.


* [Objects versus classes](#objects-versus-classes)
* [Defining a class](#defining-a-class)
* [Object creation - the `__init__` method](#object-creation-the-init-method)
 * [Our method is called `__init__`, but we didn't actually call the `__init__` method!](#our-method-is-called-init)
 * [We didn't specify the `self` argument - what gives?!?](#we-didnt-specify-the-self-argument)
* [Attributes](#attributes)
* [Methods](#methods)
* [Protecting attribute access](#protecting-attribute-access)
 * [A better way - properties](#a-better-way-properties])
* [Inheritance](#inheritance)
 * [The basics](#the-basics)
 * [Code re-use and problem decomposition](#code-re-use-and-problem-decomposition)
 * [Polymorphism](#polymorphism)
 * [Multiple inheritance](#multiple-inheritance)
* [Class attributes and methods](#class-attributes-and-methods)
 * [Class attributes](#class-attributes)
 * [Class methods](#class-methods)
* [Appendix: The `object` base-class](#appendix-the-object-base-class)
* [Appendix: `__init__` versus `__new__`](#appendix-init-versus-new)
* [Appendix: Monkey-patching](#appendix-monkey-patching)
* [Appendix: Method overloading](#appendix-method-overloading)
* [Useful references](#useful-references)


<a class="anchor" id="objects-versus-classes"></a>
## Objects versus classes


If you are versed in C++, Java, C#, or some other object-oriented language,
then this should all hopefully sound familiar, and you can skip to the next
section.


If you have not done any object-oriented programming before, your first step
is to understand the difference between _objects_ (also known as
_instances_) and _classes_ (also known as _types_).


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


<a class="anchor" id="defining-a-class"></a>
## Defining a class


Defining a class in Python is simple. Let's take on a small project, by
developing a class which can be used in place of the `fslmaths` shell command.


```
class FSLMaths(object):
    pass
```


In this statement, we defined a new class called `FSLMaths`, which inherits
from the built-in `object` base-class (see [below](inheritance) for more
details on inheritance).


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


<a class="anchor" id="object-creation-the-init-method"></a>
## Object creation - the `__init__` method


The first thing that our `fslmaths` replacement will need is an input image.
It makes sense to pass this in when we create an `FSLMaths` object:


```
class FSLMaths(object):
    def __init__(self, inimg):
        self.img = inimg
```


Here we have added a _method_ called `__init__` to our class (remember that a
_method_ is just a function which is defined in a class, and which can be
called on instances of that class).  This method expects two arguments -
`self`, and `inimg`. So now, when we create an instance of the `FSLMaths`
class, we will need to provide an input image:


```
import nibabel as nib
import os.path as op

fpath = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
inimg = nib.load(fpath)
fm    = FSLMaths(inimg)
```


There are a couple of things to note here...


<a class="anchor" id="our-method-is-called-init"></a>
### Our method is called `__init__`, but we didn't actually call the `__init__` method!


`__init__` is a special method in Python - it is called when an instance of a
class is created. And recall that we can create an instance of a class by
calling the class in the same way that we call a function.


There are a number of "special" methods that you can add to a class in Python
to customise various aspects of how instances of the class behave.  One of the
first ones you may come across is the `__str__` method, which defines how an
object should be printed (more specifically, how an object gets converted into
a string). For example, we could add a `__str__` method to our `FSLMaths`
class like so:


```
class FSLMaths(object):

    def __init__(self, inimg):
        self.img = inimg

    def __str__(self):
        return 'FSLMaths({})'.format(self.img.get_filename())

fpath = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
inimg = nib.load(fpath)
fm    = FSLMaths(inimg)

print(fm)
```


Refer to the [official
docs](https://docs.python.org/3.5/reference/datamodel.html#special-method-names)
for details on all of the special methods that can be defined in a class. And
take a look at the appendix for some more details on [how Python objects get
created](appendix-init-versus-new).


<a class="anchor" id="we-didnt-specify-the-self-argument"></a>
### We didn't specify the `self` argument - what gives?!?


The `self` argument is a special argument for methods in Python. If you are
coming from C++, Java, C# or similar, `self` in Python is equivalent to `this`
in those languages.


In a method, the `self` argument is a reference to the object that the method
was called on. So in this line of code:


```
fm = FSLMaths(inimg)
```


the `self` argument in `__init__` will be a reference to the `FSLMaths` object
that has been created (and is then assigned to the `fm` variable, after the
`__init__` method has finished).


But note that you __do not__ need to explicitly provide the `self` argument
when you call a method on an object, or when you create a new object. The
Python runtime will take care of passing the instance to its method, as the
first argument to the method.


But when you are writing a class, you __do__ need to explicitly list `self` as
the first argument to all of the methods of the class.


<a class="anchor" id="attributes"></a>
## Attributes


In Python, the term __attribute__ is used to refer to a piece of information
that is associated with an object. An attribute is generally a reference to
another object (which might be a string, a number, or a list, or some other
more complicated object).


Remember that we modified our `FSLMaths` class so that it is passed an input
image on creation:


```
class FSLMaths(object):
    def __init__(self, inimg):
        self.img = inimg

fpath = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
fm    = FSLMaths(nib.load(fpath))
```


Take a look at what is going on in the `__init__` method - we take the `inimg`
argument, and create a reference to it called `self.img`. We have added an
_attribute_ to the `FSLMaths` instance, called `img`, and we can access that
attribute like so:


```
print('Input for our FSLMaths instance: {}'.format(fm.img.get_filename()))
```


And that concludes the section on adding attributes to Python objects.


Just kidding. But it really is that simple. This is one aspect of Python which
might be quite jarring to you if you are coming from a language with more
rigid semantics, such as C++ or Java. In those languages, you must pre-specify
all of the attributes and methods that are a part of a class. But Python is
much more flexible - you can simply add attributes to an object after it has
been created.  In fact, you can even do this outside of the class
definition<sup>1</sup>:


```
fm = FSLMaths(inimg)
fm.another_attribute = 'Haha'
print(fm.another_attribute)
```


__But ...__ while attributes can be added to a Python object at any time, it is
good practice (and makes for more readable and maintainable code) to add all
of an object's attributes within the `__init__` method.


> <sup>1</sup>This not possible with many of the built-in types, such as
> `list` and `dict` objects, nor with types that are defined in Python
> extensions (Python modules that are written in C).


<a class="anchor" id="methods"></a>
## Methods


We've been dilly-dallying on this little `FSLMaths` project for a while now,
but our class still can't actually do anything. Let's start adding some
functionality:


```
class FSLMaths(object):

    def __init__(self, inimg):
        self.img        = inimg
        self.operations = []

    def add(self, value):
        self.operations.append(('add', value))

    def mul(self, value):
        self.operations.append(('mul', value))

    def div(self, value):
        self.operations.append(('div', value))
```


Woah woah, [slow down egg-head!](https://www.youtube.com/watch?v=yz-TemWooa4)
We've modified `__init__` so that a second attribute called `operations` is
added to our object - this `operations` attribute is simply a list.


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
        self.img        = inimg
        self.operations = []

    def add(self, value):
        self.operations.append(('add', value))

    def mul(self, value):
        self.operations.append(('mul', value))

    def div(self, value):
        self.operations.append(('div', value))

    def run(self, output=None):

        data = np.array(self.img.get_data())

        for oper, value in self.operations:

            # Value could be an image.
            # If not, we assume that
            # it is a scalar/numpy array.
            if isinstance(value, nib.nifti1.Nifti1Image):
                value = value.get_data()


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
fpath = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
fmask = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm_brain_mask.nii.gz')
inimg = nib.load(fpath)
mask  = nib.load(fmask)
fm    = FSLMaths(inimg)

fm.mul(mask)
fm.add(-10)

outimg = fm.run()

norigvox = (inimg .get_data() > 0).sum()
nmaskvox = (outimg.get_data() > 0).sum()

print('Number of voxels >0 in original image: {}'.format(norigvox))
print('Number of voxels >0 in masked image:   {}'.format(nmaskvox))
```


<a class="anchor" id="protecting-attribute-access"></a>
## Protecting attribute access


In our `FSLMaths` class, the input image was added as an attribute called
`img` to `FSLMaths` objects. We saw that it is easy to read the attributes
of an object - if we have a `FSLMaths` instance called `fm`, we can read its
input image via `fm.img`.


But it is just as easy to write the attributes of an object. What's to stop
some sloppy research assistant from overwriting our `img` attribute?


```
inimg = nib.load(op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz'))
fm = FSLMaths(inimg)
fm.img = None
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
this. Think of the poor souls who inherit your code years after you have left
the lab - if you go around overwriting all of the methods and attributes of
your objects, they are not going to have a hope in hell of understanding what
your code is actually doing, and they are not going to like you very
much. Take a look at the appendix for a [brief discussion on this
topic](appendix-monkey-patching).


Python tends to assume that programmers are "responsible adults", and hence
doesn't do much in the way of restricting access to the attributes or methods
of an object. This is in contrast to languages like C++ and Java, where the
notion of a private attribute or method is strictly enforced by the language.


However, there are a couple of conventions in Python that are [universally
adhered
to](https://docs.python.org/3.5/tutorial/classes.html#private-variables):

* Class-level attributes and methods, and module-level attributes, functions,
  and classes, which begin with a single underscore (`_`), should be
  considered __protected__ - they are intended for internal use only, and
  should not be considered part of the public API of a class or module.  This
  is not enforced by the language in any way<sup>2</sup> - remember, we are
  all responsible adults here!

* Class-level attributes and methods which begin with a double-underscore
  (`__`) should be considered __private__. Python provides a weak form of
  enforcement for this rule - any attribute or method with such a name will
  actually be _renamed_ (in a standardised manner) at runtime, so that it is
  not accessible through its original name (it is still accessible via its
  [mangled
  name](https://docs.python.org/3.5/tutorial/classes.html#private-variables)
  though).


> <sup>2</sup> With the exception that module-level fields which begin with a
> single underscore will not be imported into the local scope via the
> `from [module] import *` techinque.


So with all of this in mind, we can adjust our `FSLMaths` class to discourage
our sloppy research assistant from overwriting the `img` attribute:


```
# remainder of definition omitted for brevity
class FSLMaths(object):
    def __init__(self, inimg):
        self.__img        = inimg
        self.__operations = []
```

But now we have lost the ability to read our `__img` attribute:


```
inimg = nib.load(op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz'))
fm = FSLMaths(inimg)
print(fm.__img)
```


<a class="anchor" id="a-better-way-properties"></a>
### A better way - properties


Python has a feature called
[`properties`](https://docs.python.org/3.5/library/functions.html#property),
which is a nice way of controlling access to the attributes of an object. We
can use properties by defining a "getter" method which can be used to access
our attributes, and "decorating" them with the `@property` decorator (we will
cover decorators in a later practical).


```
class FSLMaths(object):
    def __init__(self, inimg):
        self.__img        = inimg
        self.__operations = []

    @property
    def img(self):
        return self.__img
```


So we are still storing our input image as a private attribute, but now we
have made it available in a read-only manner via the public `img` property:


```
fpath = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
inimg = nib.load(fpath)
fm    = FSLMaths(inimg)

print(fm.img.get_filename())
```


Note that, even though we have defined `img` as a method, we can access it
like an attribute - this is due to the magic behind the `@property` decorator.


We can also define "setter" methods for a property. For example, we might wish
to add the ability for a user of our `FSLMaths` class to change the input
image after creation.


```
class FSLMaths(object):
    def __init__(self, inimg):
        self.__img        = None
        self.__operations = []
        self.img          = inimg

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, value):
        if not isinstance(value, nib.nifti1.Nifti1Image):
            raise ValueError('value must be a NIFTI image!')
        self.__img = value
```


> Note that we used the `img` setter method within `__init__` to validate the
> initial `inimg` that was passed in during creation.


Property setters are a nice way to add validation logic for when an attribute
is assigned a value. In this example, an error will be raised if the new input
is not a NIFTI image.


```
fpath = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
inimg = nib.load(fpath)
fm    = FSLMaths(inimg)

print('Input:     ', fm.img.get_filename())

# let's change the input
# to a different image
fpath2 = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm_brain.nii.gz')
inimg2 = nib.load(fpath2)
fm.img = inimg2

print('New input: ', fm.img.get_filename())

print('This is going to explode')
fm.img = 'abcde'
```


<a class="anchor" id="inheritance"></a>
## Inheritance


One of the major advantages of an object-oriented programming approach is
_inheritance_ - the ability to define hierarchical relationships between
classes and instances.


<a class="anchor" id="the-basics"></a>
### The basics


My local veterinary surgery runs some Python code which looks like the
following, to assist the nurses in identifying an animal when it arrives at
the surgery:


```
class Animal(object):
    def noiseMade(self):
        raise NotImplementedError('This method must be '
                                  'implemented by sub-classes')

class Dog(Animal):
    def noiseMade(self):
        return 'Woof'

class TalkingDog(Dog):
    def noiseMade(self):
        return 'Hi Homer, find your soulmate!'

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
`Dog`,
[`TalkingDog`](https://twitter.com/simpsonsqotd/status/427941665836630016?lang=en),
`Cat`, and `Chihuahua` classes (but not on the `Labrador` class).  We can call
the `noiseMade` method on any `Animal` instance, but the specific behaviour
that we get is dependent on the specific type of animal.


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


Note that calling the `noiseMade` method on a `Labrador` instance resulted in
the `Dog.noiseMade` implementation being called.


<a class="anchor" id="code-re-use-and-problem-decomposition"></a>
### Code re-use and problem decomposition


Inheritance allows us to split a problem into smaller problems, and to re-use
code.  Let's demonstrate this with a more involved (and even more contrived)
example.  Imagine that a former colleague had written a class called
`Operator`:


```
class Operator(object):

    def __init__(self):
        super().__init__() # this line will be explained later
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
the most interesting stuff is inside `__init__`.


> ```
> super().__init__()
> ```


This line invokes `Operator.__init__` - the initialisation method for the
`Operator` base-class.


In Python, we can use the [built-in `super`
method](https://docs.python.org/3.5/library/functions.html#super) to take care
of correctly calling methods that are defined in an object's base-class (or
classes, in the case of [multiple inheritance](multiple-inheritance)).


> The `super` function is one thing which changed between Python 2 and 3 -
> in Python 2, it was necessary to pass both the type and the instance
> to `super`. So it is common to see code that looks like this:
>
> ```
> def __init__(self):
>     super(NumberOperator, self).__init__()
> ```
>
> Fortunately things are a lot cleaner in Python 3.


Let's move on to the next few lines in `__init__`:


> ```
> self.addFunction('add',    self.add)
> self.addFunction('mul',    self.mul)
> self.addFunction('negate', self.negate)
> ```


Here we are registering all of the functionality that is provided by the
`NumberOperator` class, via the `Operator.addFunction` method.


The `NumberOperator` class has also overridden the `preprocess` method, to
ensure that all values handled by the `Operator` are numbers. This method gets
called within the `Operator.run` method - for a `NumberOperator` instance, the
`NumberOperator.preprocess` method will get called<sup>3</sup>.


> <sup>3</sup> When a sub-class overrides a base-class method, it is still
> possible to access the base-class implementation [via the `super()`
> function](https://stackoverflow.com/a/4747427) (the preferred method), or by
> [explicitly calling the base-class
> implementation](https://stackoverflow.com/a/2421325).


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

<a class="anchor" id="polymorphism"></a>
### Polymorphism


Inheritance also allows us to take advantage of _polymorphism_, which refers
to idea that, in an object-oriented language, we should be able to use an
object without having complete knowledge about the class, or type, of that
object. For example, we should be able to write a function which expects an
`Operator` instance, but which will work on an instance of any `Operator`
sub-classs. As an example, let's write a function which prints a summary of an
`Operator` instance:


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
regardless of its specific type:


```
operatorSummary(no)
operatorSummary(so)
```


<a class="anchor" id="multiple-inheritance"></a>
### Multiple inheritance


Python allows you to define a class which has multiple base classes - this is
known as _multiple inheritance_. For example, we might want to build a
notification mechanisim into our `StringOperator` class, so that listeners can
be notified whenever the `capitalise` method gets called. It so happens that
our old colleague of `Operator` class fame also wrote a `Notifier` class which
allows listeners to register to be notified when an event occurs:


```
class Notifier(object):

    def __init__(self):
        super().__init__()
        self.__listeners = {}

    def register(self, name, func):
        self.__listeners[name] = func

    def notify(self, *args, **kwargs):
        for func in self.__listeners.values():
            func(*args, **kwargs)
```


Let's modify the `StringOperator` class to use the functionality of the
`Notifier ` class:


```
class StringOperator(Operator, Notifier):

    def __init__(self):
        super().__init__()
        self.addFunction('capitalise', self.capitalise)
        self.addFunction('concat',     self.concat)

    def preprocess(self, value):
        return str(value)

    def capitalise(self, s):
        result = ' '.join([w[0].upper() + w[1:] for w in s.split()])
        self.notify(result)
        return result

    def concat(self, s1, s2):
        return s1 + s2
```


Now, anything which is interested in uses of the `capitalise` method can
register as a listener on a `StringOperator` instance:


```
so = StringOperator()

def capitaliseCalled(result):
    print('Capitalise operation called: {}'.format(result))

so.register('mylistener', capitaliseCalled)

so.do('capitalise')
so.do('concat', '?')

print(so.run('did you notice that functions are objects too'))
```


> Simple classes such as the `Notifier` are sometimes referred to as
> [_mixins_](https://en.wikipedia.org/wiki/Mixin).


If you wish to use multiple inheritance in your design, it is important to be
aware of the mechanism that Python uses to determine how base class methods
are called (and which base class method will be called, in the case of naming
conflicts). This is referred to as the Method Resolution Order (MRO) - further
details on the topic can be found
[here](https://www.python.org/download/releases/2.3/mro/), and a more concise
summary
[here](http://python-history.blogspot.co.uk/2010/06/method-resolution-order.html).


Note also that for base class `__init__` methods to be correctly called in a
design which uses multiple inheritance, _all_ classes in the hierarchy must
invoke `super().__init__()`. This can become complicated when some base
classes expect to be passed arguments to their `__init__` method. In scenarios
like this it may be prefereable to manually invoke the base class `__init__`
methods instead of using `super()`. For example:


> ```
> class StringOperator(Operator, Notifier):
>     def __init__(self):
>         Operator.__init__(self)
>         Notifier.__init__(self)
> ```


This approach has the disadvantage that if the base classes change, you will
have to change these invocations. But the advantage is that you know exactly
how the class hierarchy will be initialised. In general though, doing
everything with `super()` will result in more maintainable code.


<a class="anchor" id="class-attributes-and-methods"></a>
## Class attributes and methods


Up to this point we have been covering how to add attributes and methods to an
_object_. But it is also possible to add methods and attributes to a _class_
(`static` methods and fields, for those of you familiar with C++ or Java).


Class attributes and methods can be accessed without having to create an
instance of the class - they are not associated with individual objects, but
rather with the class itself.


Class methods and attributes can be useful in several scenarios - as a
hypothetical, not very useful example, let's say that we want to gain usage
statistics for how many times each type of operation is used on instances of
our `FSLMaths` class. We might, for example, use this information in a grant
application to show evidence that more research is needed to optimise the
performance of the `add` operation.


<a class="anchor" id="class-attributes"></a>
### Class attributes


Let's add a `dict` called `opCounters` as a class attribute to the `FSLMaths`
class - whenever an operation is called on a `FSLMaths` instance, the counter
for that operation will be incremented:


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
        self.img        = inimg
        self.operations = []

    def add(self, value):
        self.operations.append(('add', value))

    def mul(self, value):
        self.operations.append(('mul', value))

    def div(self, value):
        self.operations.append(('div', value))

    def run(self, output=None):

        data = np.array(self.img.get_data())

        for oper, value in self.operations:

            # Code omitted for brevity

            # Increment the usage counter
            # for this operation. We can
            # access class attributes (and
            # methods) through the class
            # itself.
            FSLMaths.opCounters[oper] = self.opCounters.get(oper, 0) + 1
```


So let's see it in action:


```
fpath = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
fmask = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm_brain_mask.nii.gz')
inimg = nib.load(fpath)
mask  = nib.load(fmask)

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


<a class="anchor" id="class-methods"></a>
### Class methods


It is just as easy to add a method to a class - let's take our reporting code
from above, and add it as a method to the `FSLMaths` class.


A class method is denoted by the
[`@classmethod`](https://docs.python.org/3.5/library/functions.html#classmethod)
decorator. Note that, where a regular method which is called on an instance
will be passed the instance as its first argument (`self`), a class method
will be passed the class itself as the first argument - the standard
convention is to call this argument `cls`:


```
class FSLMaths(object):

    opCounters = {}

    @classmethod
    def usage(cls):
        print('FSLMaths usage statistics')
        for oper in ('add', 'div', 'mul'):
            print('  {} : {}'.format(oper, FSLMaths.opCounters.get(oper, 0)))

    def __init__(self, inimg):
        self.img        = inimg
        self.operations = []

    def add(self, value):
        self.operations.append(('add', value))

    def mul(self, value):
        self.operations.append(('mul', value))

    def div(self, value):
        self.operations.append(('div', value))

    def run(self, output=None):

        data = np.array(self.img.get_data())

        for oper, value in self.operations:
            FSLMaths.opCounters[oper] = self.opCounters.get(oper, 0) + 1
```


> There is another decorator -
> [`@staticmethod`](https://docs.python.org/3.5/library/functions.html#staticmethod) -
> which can be used on methods defined within a class. The difference
> between a `@classmethod` and a `@staticmethod` is that the latter will _not_
> be passed the class (`cls`).


calling a class method is the same as accessing a class attribute:


```
fpath = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz')
fmask = op.expandvars('$FSLDIR/data/standard/MNI152_T1_2mm_brain_mask.nii.gz')
inimg = nib.load(fpath)
mask  = nib.load(fmask)

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
fm1.usage()
```


<a class="anchor" id="appendix-the-object-base-class"></a>
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
In Python 3 there is actually no difference in defining classes in the
"new-style" way we have used throughout this tutorial, or the "old-style" way
mentioned in this appendix.


But if you are writing code which needs to run on both Python 2 and 3, you
__must__ define your classes in the new-style convention, i.e. by explicitly
inheriting from the `object` base class. Therefore, the safest approach is to
always use the new-style format.


<a class="anchor" id="appendix-init-versus-new"></a>
## Appendix: `__init__` versus `__new__`


In Python, object creation is actually a two-stage process - _creation_, and
then _initialisation_. The `__init__` method gets called during the
_initialisation_ stage - its job is to initialise the state of the object. But
note that, by the time `__init__` gets called, the object has already been
created.


You can also define a method called `__new__` if you need to control the
creation stage, although this is very rarely needed. One example of where you
might need to implement the `__new__` method is if you wish to create a
[subclass of a
`numpy.array`](https://docs.scipy.org/doc/numpy-1.14.0/user/basics.subclassing.html)
(although you might alternatively want to think about redefining your problem
so that this is not necessary).


A brief explanation on
the difference between `__new__` and `__init__` can be found
[here](https://www.reddit.com/r/learnpython/comments/2s3pms/what_is_the_difference_between_init_and_new/cnm186z/),
and you may also wish to take a look at the [official Python
docs](https://docs.python.org/3.5/reference/datamodel.html#basic-customization).


<a class="anchor" id="appendix-monkey-patching"></a>
## Appendix: Monkey-patching


The act of run-time modification of objects or class definitions is referred
to as [_monkey-patching_](https://en.wikipedia.org/wiki/Monkey_patch) and,
whilst it is allowed by the Python programming language, it is generally
considered quite bad practice.


Just because you _can_ do something doesn't mean that you _should_. Python
gives you the flexibility to write your software in whatever manner you deem
suitable.  __But__ if you want to write software that will be used, adopted,
maintained, and enjoyed by other people, you should be polite, write your code
in a clear, readable fashion, and avoid the use of devious tactics such as
monkey-patching.


__However__, while monkey-patching may seem like a horrific programming
practice to those of you coming from the realms of C++, Java, and the like,
(and it is horrific in many cases), it can be _extremely_ useful in certain
circumstances.  For instance, monkey-patching makes [unit testing a
breeze in Python](https://docs.python.org/3.5/library/unittest.mock.html).


As another example, consider the scenario where you are dependent on a third
party library which has bugs in it. No problem - while you are waiting for the
library author to release a new version of the library, you can write your own
working implementation and [monkey-patch it
in!](https://git.fmrib.ox.ac.uk/fsl/fsleyes/fsleyes/blob/0.21.0/fsleyes/views/viewpanel.py#L726)


<a class="anchor" id="appendix-method-overloading"></a>
## Appendix: Method overloading


Method overloading (defining multiple methods with the same name in a class,
but each accepting different arguments) is one of the only object-oriented
features that is not present in Python. Becuase Python does not perform any
runtime checks on the types of arguments that are passed to a method, or the
compatibility of the method to accept the arguments, it would not be possible
to determine which implementation of a method is to be called. In other words,
in Python only the name of a method is used to identify that method, unlike in
C++ and Java, where the full method signature (name, input types and return
types) is used.


However, because a Python method can be written to accept any number or type
of arguments, it is very easy to to build your own overloading logic by
writing a "dispatch" method<sup>4</sup>. Here is YACE (Yet Another Contrived
Example):


```
class Adder(object):

    def add(self, *args):
        if   len(args) == 2: return self.__add2(*args)
        elif len(args) == 3: return self.__add3(*args)
        elif len(args) == 4: return self.__add4(*args)
        else:
            raise AttributeError('No method available to accept {} '
                                 'arguments'.format(len(args)))

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

> <sup>4</sup>Another option is the [`functools.singledispatch`
> decorator](https://docs.python.org/3.5/library/functools.html#functools.singledispatch),
> which is more complicated, but may allow you to write your dispatch logic in
> a more concise manner.


<a class="anchor" id="useful-references"></a>
## Useful references


The official Python documentation has a wealth of information on the internal
workings of classes and objects, so these pages are worth a read:


* https://docs.python.org/3.5/tutorial/classes.html
* https://docs.python.org/3.5/reference/datamodel.html
