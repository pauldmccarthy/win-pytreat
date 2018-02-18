# Threading and parallel processing


The Python language has built-in support for multi-threading in the
[`threading`](https://docs.python.org/3.5/library/threading.html) module, and
true parallelism in the
[`multiprocessing`](https://docs.python.org/3.5/library/multiprocessing.html)
module.  If you want to be impressed, skip straight to the section on
[`multiprocessing`](todo).





## Threading


The [`threading`](https://docs.python.org/3.5/library/threading.html) module
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
documentation](https://docs.python.org/3.5/library/threading.html#thread-objects)
for more details.


### Thread synchronisation


The `threading` module provides some useful thread-synchronisation primitives
- the `Lock`, `RLock` (re-entrant `Lock`), and `Event` classes.  The
`threading` module also provides `Condition` and `Semaphore` classes - refer
to the [documentation](https://docs.python.org/3.5/library/threading.html) for
more details.


#### `Lock`


The [`Lock`](https://docs.python.org/3.5/library/threading.html#lock-objects)
class (and its re-entrant version, the
[`RLock`](https://docs.python.org/3.5/library/threading.html#rlock-objects))
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
[`Event`](https://docs.python.org/3.5/library/threading.html#event-objects)
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


The [_Global Interpreter
Lock_](https://docs.python.org/3/c-api/init.html#thread-state-and-the-global-interpreter-lock)
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
[`multiprocessing`](https://docs.python.org/3.5/library/multiprocessing.html)
module.


The `multiprocessing` module spawns sub-processes, rather than threads, and so
is not subject to the GIL constraints that the `threading` module suffers
from. It provides two APIs - a "traditional" equivalent to that provided by
the `threading` module, and a powerful higher-level API.


### `threading`-equivalent API


The
[`Process`](https://docs.python.org/3.5/library/multiprocessing.html#the-process-class)
class is the `multiprocessing` equivalent of the
[`threading.Thread`](https://docs.python.org/3.5/library/threading.html#thread-objects)
class.  `multprocessing` also has equivalents of the [`Lock` and `Event`
classes](https://docs.python.org/3.5/library/multiprocessing.html#synchronization-between-processes),
and the other synchronisation primitives provided by `threading`.


So you can simply replace `threading.Thread` with `multiprocessing.Process`,
and you will have true parallelism.


Because your "threads" are now independent processes, you need to be a little
careful about how to share information across them. Fortunately, the
`multiprocessing` module provides [`Queue` and `Pipe`
classes](https://docs.python.org/3.5/library/multiprocessing.html#exchanging-objects-between-processes)
which make it easy to share data across processes.


### Higher-level API - the `multiprocessing.Pool`


The real advantages of `multiprocessing` lie in its higher level API, centered
around the [`Pool`
class](https://docs.python.org/3.5/library/multiprocessing.html#using-a-pool-of-workers).


Essentially, you create a `Pool` of worker processes - you specify the number
of processes when you create the pool.


> The best number of processes to use for a `Pool` will depend on the system
> you are running on (number of cores), and the tasks you are running (e.g.
> I/O bound or CPU bound).


Once you have created a `Pool`, you can use its methods to automatically
parallelise tasks. The most useful are the `map`, `starmap` and
`apply_async` methods.


#### `Pool.map`


The
[`Pool.map`](https://docs.python.org/3.5/library/multiprocessing.html#multiprocessing.pool.Pool.map)
method is the multiprocessing equivalent of the built-in
[`map`](https://docs.python.org/3.5/library/functions.html#map) function - it
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

p = mp.Pool(processes=16)

print('Crunching images...')

start   = time.time()
results = p.map(crunchImage, imgfiles)
end     = time.time()

print('Total execution time: {:0.2f} seconds'.format(end - start))
```


The `Pool.map` method only works with functions that accept one argument, such
as our `crunchImage` function above. If you have a function which accepts
multiple arguments, use the
[`Pool.starmap`](https://docs.python.org/3.5/library/multiprocessing.html#multiprocessing.pool.Pool.starmap)
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

pool = mp.Pool(processes=16)

args = [(f, m) for f, m in zip(imgfiles, modalities)]

print('Crunching images...')

start   = time.time()
results = pool.starmap(crunchImage, args)
end     = time.time()

print('Total execution time: {:0.2f} seconds'.format(end - start))
```


The `map` and `starmap` methods also have asynchronous equivalents `map_async`
and `starmap_async`, which return immediately. Refer to the
[`Pool`](https://docs.python.org/3.5/library/multiprocessing.html#module-multiprocessing.pool)
documentation for more details.


#### `Pool.apply_async`


The
[`Pool.apply`](https://docs.python.org/3.5/library/multiprocessing.html#multiprocessing.pool.Pool.apply)
method will execute a function on one of the processes, and block until it has
finished.  The
[`Pool.apply_async`](https://docs.python.org/3.5/library/multiprocessing.html#multiprocessing.pool.Pool.apply_async)
method returns immediately, and is thus more suited to asynchronously
scheduling multiple jobs to run in parallel.


`apply_async` returns an object of type
[`AsyncResult`](https://docs.python.org/3.5/library/multiprocessing.html#multiprocessing.pool.AsyncResult).
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

pool = mp.Pool(processes=16)

print('Running structural-to-standard registration '
      'on {} subjects...'.format(len(t1s)))

# Run linear registration on all the T1s.
#
# We build a list of AsyncResult objects
linresults = [pool.apply_async(linear_registration, (t1, std))
              for t1 in t1s]

# Then we wait for each job to finish,
# and replace its AsyncResult object
# with the actual result - an affine
# transformation matrix.
start = time.time()
for i, r in enumerate(linresults):
    linresults[i] = r.get()
end = time.time()

print('Linear registrations completed in '
      '{:0.2f} seconds'.format(end - start))

# Run non-linear registration on all the T1s,
# using the linear registrations to initialise.
nlinresults = [pool.apply_async(nonlinear_registration, (t1, std, aff))
               for (t1, aff) in zip(t1s, linresults)]

# Wait for each non-linear reg to finish,
# and store the resulting warp field.
start = time.time()
for i, r in enumerate(nlinresults):
    nlinresults[i] = r.get()
end = time.time()

print('Non-linear registrations completed in '
      '{:0.2f} seconds'.format(end - start))

print('Non linear registrations:')
for t1, result in zip(t1s, nlinresults):
    print(t1, ':', result)
```
