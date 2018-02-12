# Jupyter notebook and IPython
Our main interaction with python so far has been through the [Jupyter notebook](http://jupyter.org/).
These notebooks are extremely popular these days within the python scientific community, however they support many more languages, such as R and octave (and even matlab with the right [plugin](https://github.com/Calysto/matlab_kernel)).
They allow for interactive analysis of your data interspersed by explanatory notes (including LaTeX) with inline plotting.
However, they can not be called as scripts on the command line or be imported from other python code, which makes them rather stand-alone.
This makes them more useful for analysis that needs to be reproducible, but does not need to be replicated on different datasets (e.g., making a plot for a paper).

For more ad-hoc analysis it can be useful to just use the command line (i.e., a REPL).
We strongly recommend to use the IPython (available as `ipython` or `fslipython`) rather than default python REPL (available through `python` or `fslpython`)

Both Ipython and the jupyter notebook offer a whole range of magic commands, which all start with a `%` sign.
* A magic command starting with a single `%` sign will only affect the single line.
* A magic command starting with two '%' signs will affect the whole block of code.

Note that the normal python interpreter will not understand these magic commands, so you will have to take them out when writing a python script or library.

Here we will discuss some of the many features available to you in Ipython and the Jupyter notebook

---

## Getting help
To get the documentation for any object or method simply append a question mark
```
import string
string.capwords?
```

Alternatively you can put two questions marks to get the complete code for the method or object class
```
import string
string.capwords??
```

Both Ipython and Jupyter also come with autocomplete, which is available at any time by pressing the tab key

---

## Running shell commands
Commands starting with a `!` will be sent to the shell rather than the python interpreter.
```
!fslstats ${FSLDIR}/data/standard/FMRIB58_FA_1mm.nii.gz -r
```

You can even capture the output from the shell command in a variable:
```
r = !fslstats ${FSLDIR}/data/standard/FMRIB58_FA_1mm.nii.gz -r
r_lower, r_upper = [float(element) for element in r[0].split()]
print('Bounds are ({:.0f}, {:.0f})'.format(r_lower, r_upper))
```

---

## Running other programming languages
In the notebook you can include a whole code block using another language by using `%%<language>` (for many languages you will have to install a toolkit first, just google your favorite language besides python)
```
%%bash
for filename in `ls *.md` ; do
    head -n 1 ${filename}
done
```

---

## Timing code
We can time a line of code with `%time` or a whole code block using `%%time`.
To get the time needed to calculate the sine of a million random numbers:
```
import numpy as np
numbers = np.random.rand(int(1e6))
%time np.sin(numbers)
```

For very fast evaluation, you might need to run it multiple times to get an accurate estimate. The `%timeit` (or `%%timeit` for a code block) takes care of this for you.
```
import numpy as np
numbers = np.random.rand(10)
%timeit np.sin(numbers)  # this will take a few seconds to run
```

---

## Debugging
Despite your best efforts in many cases some error will crop up
```
import numpy as np
def total(a_list):
    """Calculate the total of a list.

    This is a very naive (not recommended) and bugged implementation
    """
    # create local copy befor changing the input
    local_list = list(a_list)
    total = 0.
    while len(local_list) > 0:
        total += local_list.pop(1)  # returns element at index=1 and removes it
    return total

print(total([2, 3, 4]))
```

You can always open a debugger at the location of the last error by using the `%debug` magic command. You can find a list of commands available in the debugger [here](http://www.georgejhunt.com/olpc/pydebug/pydebug/ipdb.html)
```
%debug
```
Try to check the value of `a_list` and `local_list` from within the debugger.

> WARNING: you need to quit the debugger before any further commands will run (type `q` into the prompt)!

If you always want to enter the debugger when an error is raised you can call `%pdb on` at any time (call `%pdf off` to rever this)

---

## Enabling plotting
By far the most popular scientific plotting library is [matplotlib](https://matplotlib.org/).
You can enable plotting in Ipython or the jupyter notebook using `%matplotlib <backend>`, where [backend](https://matplotlib.org/faq/usage_faq.html#what-is-a-backend) is the system that will be used to display the plots.
When failing to provide a backend it will simply use the default (which is usually fine).
* In the jupyter notebook use the `nbagg` backend for interactive plots or the `inline` backend for non-interactive plots
* Otherwise on Mac OSx use the `macosx` backend
```
%matplotlib nbagg
```
> Keep in mind that as soon as you have started plotting you can no longer change your backend without restarting python.

To do the equivalent in a python script would look like
> ```
> import matplotlib as mpl
> mpl.use(<backend>)
> ```

For interactive use it can be handy to have all the `numpy` numeric functions and `matplotlib` plotting functions directly available without importing them explicitly.
This can be achieved using the `%pylab <backend>` magic command.
```
%pylab nbagg
```

This is equivalent in python code to:
> ```
> import matplotlib as mpl
> mpl.use(<backend>)
> from matplotlib.pylab import *
> ```

I start most of my notebooks or terminals with the `%pylab` command, because afterwards I can just do stuff like:
```
x = linspace(0, pi, 301)
y = sin(x)
plot(x, y, 'r-')
```

---

## Exporting code from the Jupyter notebook
If you have a code cell in the jupyter notebook, that you want to convert into a script, you can use the %%writefile

```
%%writefile script_from_notebook.py
# a bunch of imports
import numpy as np
from datetime import datetime

```

Any additional code cells need to contain the `-a` flag to stop jupyter from overwriting the original code
```
%%writefile -a script_from_notebook.py

print('today is ', datetime.now())
print('sin(3) is ', np.sin(3))
```

We can now run this script
```
!python script_from_notebook.py
```

---

## Exporting code from the Ipython terminal
You can access the full history of your session using `%history`.
To save the history to a file use `%history -f <filename>`.
You will probably have to clean a lot of erroneous commands you typed from that file before you are able to run it as a script.

