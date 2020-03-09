# Threading and parallel processing


The Python language has built-in support for multi-threading in the
[`threading`](https://docs.python.org/3/library/threading.html) module, and
true parallelism in the
[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html)
module.  If you want to be impressed, skip straight to the section on
[`multiprocessing`](todo).


> *Note*: If you are familiar with a "real" programming language such as C++
> or Java, you might be disappointed with the native support for parallelism in
> Python. Python threads do not run in parallel because of the Global
> Interpreter Lock, and if you use `multiprocessing`, be prepared to either
> bear the performance hit of copying data between processes, or jump through
> hoops order to share data between processes.
>
> This limitation *might* be solved in a future Python release by way of
> [*sub-interpreters*](https://www.python.org/dev/peps/pep-0554/), but the
> author of this practical is not holding his breath.


## Threading


The [`threading`](https://docs.python.org/3/library/threading.html) module
provides a traditional multi-threading API that should be familiar to you if
you have worked with threads in other languages.


Running a task in a separate thread in Python is easy - simply create a
`Thread` object, and pass it the function or method that you want it to
run. Then call its `start` method:


```
import time
import threading

def longRunningTask(niters):
    for i in range(niters):
        if i % 2 == 0: print('Tick')
        else:          print('Tock')
        time.sleep(0.5)

t = threading.Thread(target=longRunningTask, args=(8,))

t.start()

while t.is_alive():
    time.sleep(0.4)
    print('Waiting for thread to finish...')
print('Finished!')
```


You can also `join` a thread, which will block execution in the current thread
until the thread that has been `join`ed has finished:


```
t = threading.Thread(target=longRunningTask, args=(6, ))
t.start()

print('Joining thread ...')
t.join()
print('Finished!')
```


### Subclassing `Thread`


It is also possible to sub-class the `Thread` class, and override its `run`
method:


```
class LongRunningThread(threading.Thread):
    def __init__(self, niters, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.niters = niters

    def run(self):
        for i in range(self.niters):
            if i % 2 == 0: print('Tick')
            else:          print('Tock')
            time.sleep(0.5)

t = LongRunningThread(6)
t.start()
t.join()
print('Done')
```


### Daemon threads


By default, a Python application will not exit until _all_ active threads have
finished execution.  If you want to run a task in the background for the
duration of your application, you can mark it as a `daemon` thread - when all
non-daemon threads in a Python application have finished, all daemon threads
will be halted, and the application will exit.


You can mark a thread as being a daemon by setting an attribute on it after
creation:


```
t = threading.Thread(target=longRunningTask)
t.daemon = True
```


See the [`Thread`
documentation](https://docs.python.org/3/library/threading.html#thread-objects)
for more details.


### Thread synchronisation


The `threading` module provides some useful thread-synchronisation primitives
- the `Lock`, `RLock` (re-entrant `Lock`), and `Event` classes.  The
`threading` module also provides `Condition` and `Semaphore` classes - refer
to the [documentation](https://docs.python.org/3/library/threading.html) for
more details.


#### `Lock`


The [`Lock`](https://docs.python.org/3/library/threading.html#lock-objects)
class (and its re-entrant version, the
[`RLock`](https://docs.python.org/3/library/threading.html#rlock-objects))
prevents a block of code from being accessed by more than one thread at a
time. For example, if we have multiple threads running this `task` function,
their [outputs](https://www.youtube.com/watch?v=F5fUFnfPpYU) will inevitably
become intertwined:


```
def task():
    for i in range(5):
        print('{} Woozle '.format(i), end='')
        time.sleep(0.1)
        print('Wuzzle')

threads = [threading.Thread(target=task) for i in range(5)]
for t in threads:
    t.start()
```


But if we protect the critical section with a `Lock` object, the output will
look more sensible:


```
lock = threading.Lock()

def task():

    for i in range(5):
        with lock:
            print('{} Woozle '.format(i), end='')
            time.sleep(0.1)
            print('Wuzzle')

threads = [threading.Thread(target=task) for i in range(5)]
for t in threads:
    t.start()
```


> Instead of using a `Lock` object in a `with` statement, it is also possible
> to manually call its `acquire` and `release` methods:
>
>     def task():
>         for i in range(5):
>             lock.acquire()
>             print('{} Woozle '.format(i), end='')
>             time.sleep(0.1)
>             print('Wuzzle')
>             lock.release()


Python does not have any built-in constructs to implement `Lock`-based mutual
exclusion across several functions or methods - each function/method must
explicitly acquire/release a shared `Lock` instance. However, it is relatively
straightforward to implement a decorator which does this for you:


```
def mutex(func, lock):
    def wrapper(*args):
        with lock:
            func(*args)
    return wrapper

class MyClass(object):

    def __init__(self):
        lock = threading.Lock()
        self.safeFunc1 = mutex(self.safeFunc1, lock)
        self.safeFunc2 = mutex(self.safeFunc2, lock)

    def safeFunc1(self):
        time.sleep(0.1)
        print('safeFunc1 start')
        time.sleep(0.2)
        print('safeFunc1 end')

    def safeFunc2(self):
        time.sleep(0.1)
        print('safeFunc2 start')
        time.sleep(0.2)
        print('safeFunc2 end')

mc = MyClass()

f1threads = [threading.Thread(target=mc.safeFunc1) for i in range(4)]
f2threads = [threading.Thread(target=mc.safeFunc2) for i in range(4)]

for t in f1threads + f2threads:
    t.start()
```


Try removing the `mutex` lock from the two methods in the above code, and see
what it does to the output.


#### `Event`


The
[`Event`](https://docs.python.org/3/library/threading.html#event-objects)
class is essentially a boolean [semaphore][semaphore-wiki]. It can be used to
signal events between threads. Threads can `wait` on the event, and be awoken
when the event is `set` by another thread:


[semaphore-wiki]: https://en.wikipedia.org/wiki/Semaphore_(programming)


```
import numpy as np

processingFinished = threading.Event()

def processData(data):
    print('Processing data ...')
    time.sleep(2)
    print('Result: {}'.format(data.mean()))
    processingFinished.set()

data = np.random.randint(1, 100, 100)

t = threading.Thread(target=processData, args=(data,))
t.start()

processingFinished.wait()
print('Processing finished!')
```

### The Global Interpreter Lock (GIL)


The [*Global Interpreter
Lock*](https://docs.python.org/3/c-api/init.html#thread-state-and-the-global-interpreter-lock)
is an implementation detail of [CPython](https://github.com/python/cpython)
(the official Python interpreter).  The GIL means that a multi-threaded
program written in pure Python is not able to take advantage of multiple
cores - this essentially means that only one thread may be executing at any
point in time.


The `threading` module does still have its uses though, as this GIL problem
does not affect tasks which involve calls to system or natively compiled
libraries (e.g. file and network I/O, Numpy operations, etc.). So you can,
for example, perform some expensive processing on a Numpy array in a thread
running on one core, whilst having another thread (e.g. user interaction)
running on another core.


## Multiprocessing


For true parallelism, you should check out the
[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html)
module.


The `multiprocessing` module spawns sub-processes, rather than threads, and so
is not subject to the GIL constraints that the `threading` module suffers
from. It provides two APIs - a "traditional" equivalent to that provided by
the `threading` module, and a powerful higher-level API.


> Python also provides the
> [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html)
> module, which offers a simpler alternative API to `multiprocessing`. It
> offers no functionality over `multiprocessing`, so is not covered here.

### `threading`-equivalent API


The
[`Process`](https://docs.python.org/3/library/multiprocessing.html#the-process-class)
class is the `multiprocessing` equivalent of the
[`threading.Thread`](https://docs.python.org/3/library/threading.html#thread-objects)
class.  `multprocessing` also has equivalents of the [`Lock` and `Event`
classes](https://docs.python.org/3/library/multiprocessing.html#synchronization-between-processes),
and the other synchronisation primitives provided by `threading`.


So you can simply replace `threading.Thread` with `multiprocessing.Process`,
and you will have true parallelism.


Because your "threads" are now independent processes, you need to be a little
careful about how to share information across them. If you only need to share
small amounts of data, you can use the [`Queue` and `Pipe`
classes](https://docs.python.org/3/library/multiprocessing.html#exchanging-objects-between-processes),
in the `multiprocessing` module. If you are working with large amounts of data
where copying between processes is not feasible, things become more
complicated, but read on...


### Higher-level API - the `multiprocessing.Pool`


The real advantages of `multiprocessing` lie in its higher level API, centered
around the [`Pool`
class](https://docs.python.org/3/library/multiprocessing.html#using-a-pool-of-workers).


Essentially, you create a `Pool` of worker processes - you specify the number
of processes when you create the pool. Once you have created a `Pool`, you can
use its methods to automatically parallelise tasks. The most useful are the
`map`, `starmap` and `apply_async` methods.



The `Pool` class is a context manager, so can be used in a `with` statement,
e.g.:

> ```
> with mp.Pool(processes=16) as pool:
>     # do stuff with the pool
> ```

It is possible to create a `Pool` outside of a `with` statement, but in this
case you must ensure that you call its `close` mmethod when you are finished.
Using a `Pool` in a `with` statement is therefore recommended, because you know
that it will be shut down correctly, even in the event of an error.


> The best number of processes to use for a `Pool` will depend on the system
> you are running on (number of cores), and the tasks you are running (e.g.
> I/O bound or CPU bound).


#### `Pool.map`


The
[`Pool.map`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.map)
method is the multiprocessing equivalent of the built-in
[`map`](https://docs.python.org/3/library/functions.html#map) function - it
is given a function, and a sequence, and it applies the function to each
element in the sequence.


```
import                    time
import multiprocessing as mp
import numpy           as np

def crunchImage(imgfile):

    # Load a nifti image, do stuff
    # to it. Use your imagination
    # to fill in this function.
    time.sleep(2)

    # numpy's random number generator
    # will be initialised in the same
    # way in each process, so let's
    # re-seed it.
    np.random.seed()
    result = np.random.randint(1, 100, 1)

    print(imgfile, ':', result)

    return result

imgfiles = ['{:02d}.nii.gz'.format(i) for i in range(20)]

print('Crunching images...')

start = time.time()

with mp.Pool(processes=16) as p:
     results = p.map(crunchImage, imgfiles)

end = time.time()

print('Total execution time: {:0.2f} seconds'.format(end - start))
```


The `Pool.map` method only works with functions that accept one argument, such
as our `crunchImage` function above. If you have a function which accepts
multiple arguments, use the
[`Pool.starmap`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.starmap)
method instead:


```
def crunchImage(imgfile, modality):
    time.sleep(2)

    np.random.seed()

    if modality == 't1':
        result = np.random.randint(1, 100, 1)
    elif modality == 't2':
        result = np.random.randint(100, 200, 1)

    print(imgfile, ': ', result)

    return result

imgfiles   = ['t1_{:02d}.nii.gz'.format(i) for i in range(10)] + \
             ['t2_{:02d}.nii.gz'.format(i) for i in range(10)]
modalities = ['t1'] * 10 + ['t2'] * 10

args = [(f, m) for f, m in zip(imgfiles, modalities)]

print('Crunching images...')

start = time.time()

with mp.Pool(processes=16) as pool:
     results = pool.starmap(crunchImage, args)

end = time.time()

print('Total execution time: {:0.2f} seconds'.format(end - start))
```


The `map` and `starmap` methods also have asynchronous equivalents `map_async`
and `starmap_async`, which return immediately. Refer to the
[`Pool`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing.pool)
documentation for more details.


#### `Pool.apply_async`


The
[`Pool.apply`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.apply)
method will execute a function on one of the processes, and block until it has
finished.  The
[`Pool.apply_async`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.apply_async)
method returns immediately, and is thus more suited to asynchronously
scheduling multiple jobs to run in parallel.


`apply_async` returns an object of type
[`AsyncResult`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.AsyncResult).
An `AsyncResult` object has `wait` and `get` methods which will block until
the job has completed.


```
import                    time
import multiprocessing as mp
import numpy           as np


def linear_registration(src, ref):
    time.sleep(1)

    return np.eye(4)

def nonlinear_registration(src, ref, affine):

    time.sleep(3)

    # this number represents a non-linear warp
    # field - use your imagination people!
    np.random.seed()
    return np.random.randint(1, 100, 1)

t1s = ['{:02d}_t1.nii.gz'.format(i) for i in range(20)]
std = 'MNI152_T1_2mm.nii.gz'

print('Running structural-to-standard registration '
      'on {} subjects...'.format(len(t1s)))

# Run linear registration on all the T1s.
start = time.time()
with mp.Pool(processes=16) as pool:

    # We build a list of AsyncResult objects
    linresults = [pool.apply_async(linear_registration, (t1, std))
                  for t1 in t1s]

    # Then we wait for each job to finish,
    # and replace its AsyncResult object
    # with the actual result - an affine
    # transformation matrix.
    for i, r in enumerate(linresults):
        linresults[i] = r.get()

end = time.time()

print('Linear registrations completed in '
      '{:0.2f} seconds'.format(end - start))

# Run non-linear registration on all the T1s,
# using the linear registrations to initialise.
start = time.time()
with mp.Pool(processes=16) as pool:
    nlinresults = [pool.apply_async(nonlinear_registration, (t1, std, aff))
                   for (t1, aff) in zip(t1s, linresults)]

    # Wait for each non-linear reg to finish,
    # and store the resulting warp field.
    for i, r in enumerate(nlinresults):
        nlinresults[i] = r.get()

end = time.time()

print('Non-linear registrations completed in '
      '{:0.2f} seconds'.format(end - start))

print('Non linear registrations:')
for t1, result in zip(t1s, nlinresults):
    print(t1, ':', result)
```


## Sharing data between processes


When you use the `Pool.map` method (or any of the other methods we have shown)
to run a function on a sequence of items, those items must be copied into the
memory of each of the child processes. When the child processes are finished,
the data that they return then has to be copied back to the parent process.


Any items which you wish to pass to a function that is executed by a `Pool`
must be *pickleable*<sup>1</sup> - the built-in
[`pickle`](https://docs.python.org/3/library/pickle.html) module is used by
`multiprocessing` to serialise and de-serialise the data passed to and
returned from a child process. The majority of standard Python types (`list`,
`dict`, `str` etc), and Numpy arrays can be pickled and unpickled, so you only
need to worry about this detail if you are passing objects of a custom type
(e.g. instances of classes that you have written, or that are defined in some
third-party library).


> <sup>1</sup>*Pickleable* is the term used in the Python world to refer to
> something that is *serialisable* - basically, the process of converting an
> in-memory object into a binary form that can be stored and/or transmitted.


There is obviously some overhead in copying data back and forth between the
main process and the worker processes; this may or may not be a problem.  For
most computationally intensive tasks, this communication overhead is not
important - the performance bottleneck is typically going to be the
computation time, rather than I/O between the parent and child processes.


However, if you are working with a large dataset, you have determined that
copying data between processes is having a substantial impact on your
performance, and instead wish to *share* a single copy of the data between
the processes, you will need to:

 1. Structure your code so that the data you want to share is accessible at
    the *module level*.
 2. Define/create/load the data *before* creating the `Pool`.


This is because, when you create a `Pool`, what actually happens is that the
process your Pythonn script is running in will [**fork**](wiki-fork) itself -
the child processes that are created are used as the worker processes by the
`Pool`. And if you create/load your data in your main process *before* this
fork occurs, all of the child processes will inherit the memory space of the
main process, and will therefore have (read-only) access to the data, without
any copying required.


[wiki-fork]: https://en.wikipedia.org/wiki/Fork_(system_call)


### Read-only sharing


Let's see this in action with a simple example. We'll start by defining a
little helper function which allows us to track the total memory usage, using
the unix `free` command:


```
# todo mac version
import subprocess as sp
def memusage(msg):
    stdout = sp.run(['free', '--mega'], capture_output=True).stdout.decode()
    stdout = stdout.split('\n')[1].split()
    total  = stdout[1]
    used   = stdout[2]
    print('Memory usage {}: {} / {} MB'.format(msg, used, total))
```


Now our task is simply to calculate the sum of a large array of numbers. We're
going to create a big chunk of data, and process it in chunks, keeping track
of memory usage as the task progresses:


```
import                    time
import multiprocessing as mp
import numpy           as np

memusage('before creating data')

# allocate 500MB of data
data = np.random.random(500 * (1048576 // 8))

# Assign nelems values to each worker
# process (hard-coded so we need 12
# jobs to complete the task)
nelems =  len(data) // 12

memusage('after creating data')

# Each job process nelems values,
# starting from the specified offset
def process_chunk(offset):
    time.sleep(1)
    return data[offset:offset + nelems].sum()

# Generate an offset into the data for each job -
# we will call process_chunk for each offset
offsets = range(0, len(data), nelems)

# Create our worker process pool
with mp.Pool(4) as pool:

    results = pool.map_async(process_chunk, offsets)

    # Wait for all of the jobs to finish
    elapsed = 0
    while not results.ready():
        memusage('after {} seconds'.format(elapsed))
        time.sleep(1)
        elapsed += 1

    results = results.get()

print('Total sum:   ', sum(results))
print('Sanity check:', data.sum())
```


You should be able to see that only one copy of `data` is created, and is
shared by all of the worker processes without any copying taking place.

So things are reasonably straightforward if you only need read-only acess to
your data. But what if your worker processes need to be able to modify the
data? Go back to the code block above and:

1. Modify the `process_chunk` function so that it modifies every element of
   its assigned portion of the data before calculating and returning the sum.
   For example:

   > ```
   > data[offset:offset + nelems] += 1
   > ```

2. Restart the Jupyter notebook kernel (*Kernel -> Restart*) - this example is
   somewhat dependent on the behaviour of the Python garbage collector, so it
   helps to start afresh


2. Re-run the two code blocks, and watch what happens to the memory usage.


What happened? Well, you are seeing [copy-on-write](wiki-copy-on-write) in
action. When the `process_chunk` is invoked, it is given a reference to the
original data array in the memory space of the parent process. But as soon as
an attempt is made to modify it, a copy of the data, in the memory space of
the child process, is created. The modifications are then applied to this
child process, and not to the original copy. So the total memory usage has
blown out to twice as much as before, and the changes made by each child
process are being lost!


[wiki-copy-on-write]: https://en.wikipedia.org/wiki/Copy-on-write


### Read/write sharing


> If you have worked with a real programming language with true parallelism
> and shared memory via within-process multi-threading, feel free to take a
> break at this point. Breathe. Relax. Go punch a hole in a wall. I've been
> coding in Python for years, and this still makes me angry. Sometimes
> ... don't tell anyone I said this ... I even find myself wishing I were
> coding in *Java* instead of Python. Ugh. I need to take a shower.


In order to truly share memory between multiple processes, the
`multiprocessing` module provides the [`Value`, `Array`, and `RawArray`
classes](https://docs.python.org/3/library/multiprocessing.html#shared-ctypes-objects),
which allow you to share individual values, or arrays of values, respectively.


The `Array` and `RawArray` classes essentially wrap a typed pointer (from the
built-in [`ctypes`](https://docs.python.org/3/library/ctypes.html) module) to
a block of memory. We can use the `Array` or `RawArray` class to share a Numpy
array between our worker processes. The difference between an `Array` and a
`RawArray` is that the former offers low-level synchronised
(i.e. process-safe) access to the shared memory. This is necessary if your
child processes will be modifying the same parts of your data.


> If you need fine-grained control over synchronising access to shared data by
> multiple processes, all of the [synchronisation
> primitives](https://docs.python.org/3/library/multiprocessing.html#synchronization-between-processes)
> from the `multiprocessing` module are at your disposal.


The requirements for sharing memory between processes still apply here - we
need to make our data accessible at the *module level*, and we need to create
our data before creating the `Pool`. And to achieve read and write capability,
we also need to make sure that our input and output arrays are located in
shared memory - we can do this via the `Array` or `RawArray`.


As an example, let's say we want to parallelise processing of an image by
having each worker process perform calculations on a chunk of the image.
First, let's define a function which does the calculation on a specified set
of image coordinates:


```
import multiprocessing as mp
import ctypes
import numpy as np
np.set_printoptions(suppress=True)


def process_chunk(shape, idxs):

    # Get references to our
    # input/output data, and
    # create Numpy array views
    # into them.
    sindata  = process_chunk.input_data
    soutdata = process_chunk.output_data
    indata   = np.ctypeslib.as_array(sindata) .reshape(shape)
    outdata  = np.ctypeslib.as_array(soutdata).reshape(shape)

    # Do the calculation on
    # the specified voxels
    outdata[idxs] = indata[idxs] ** 2
```


Rather than passing the input and output data arrays in as arguments to the
`process_chunk` function, we set them as attributes of the `process_chunk`
function. This makes the input/output data accessible at the module level,
which is required in order to share the data between the main process and the
child processes.


Now let's define a second function which process an entire image. It does the
following:


1. Initialises shared memory areas to store the input and output data.
2. Copies the input data into shared memory.
3. Sets the input and output data as attributes of the `process_chunk` function.
4. Creates sets of indices into the input data which, for each worker process,
   specifies the portion of the data that it is responsible for.
5. Creates a worker pool, and runs the `process_chunk` function for each set
   of indices.


```
def process_dataset(data):

    nprocs   = 8
    origData = data

    # Create arrays to store the
    # input and output data
    sindata  = mp.RawArray(ctypes.c_double, data.size)
    soutdata = mp.RawArray(ctypes.c_double, data.size)
    data     = np.ctypeslib.as_array(sindata).reshape(data.shape)
    outdata  = np.ctypeslib.as_array(soutdata).reshape(data.shape)

    # Copy the input data
    # into shared memory
    data[:]  = origData

    # Make the input/output data
    # accessible to the process_chunk
    # function. This must be done
    # *before* the worker pool is
    # created - even though we are
    # doing things differently to the
    # read-only example, we are still
    # making the data arrays accessible
    # at the *module* level, so the
    # memory they are stored in can be
    # shared with the child processes.
    process_chunk.input_data  = sindata
    process_chunk.output_data = soutdata

    # number of voxels to be computed
    # by each worker process.
    nvox = int(data.size / nprocs)

    # Generate coordinates for
    # every voxel in the image
    xlen, ylen, zlen = data.shape
    xs, ys, zs = np.meshgrid(np.arange(xlen),
                             np.arange(ylen),
                             np.arange(zlen))

    xs = xs.flatten()
    ys = ys.flatten()
    zs = zs.flatten()

    # We're going to pass each worker
    # process a list of indices, which
    # specify the data items which that
    # worker process needs to compute.
    xs = [xs[nvox * i:nvox * i + nvox] for i in range(nprocs)] + [xs[nvox * nprocs:]]
    ys = [ys[nvox * i:nvox * i + nvox] for i in range(nprocs)] + [ys[nvox * nprocs:]]
    zs = [zs[nvox * i:nvox * i + nvox] for i in range(nprocs)] + [zs[nvox * nprocs:]]

    # Build the argument lists for
    # each worker process.
    args = [(data.shape, (x, y, z)) for x, y, z in zip(xs, ys, zs)]

    # Create a pool of worker
    # processes and run the jobs.
    with mp.Pool(processes=nprocs) as pool:
        pool.starmap(process_chunk, args)

    return outdata
```


Now we can call our `process_data` function just like any other function:


```
indata  = np.array(np.arange(64).reshape((4, 4, 4)), dtype=np.float64)
outdata = process_dataset(data)

print('Input')
print(data)

print('Output')
print(outdata)
```
