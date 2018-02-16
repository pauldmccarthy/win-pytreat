# Main scientific python libraries
See https://scipy.org/

Most of these packages have or are in thr progress of dropping support for python2.
So use python3!

## [Numpy](http://www.numpy.org/): arrays
This is the main library underlying (nearly) all of the scientific python ecosystem.
See the tutorial in the beginner session or [the official numpy tutorial](https://docs.scipy.org/doc/numpy-dev/user/quickstart.html) for usage details.

The usual nickname of numpy is np:
```
import numpy as np
```

Numpy includes support for:
- N-dimensional arrays with various datatypes
- basic functions (e.g., polynomials)
- basic linear algebra
- random number generation

## [Scipy](https://scipy.org/scipylib/index.html): most general scientific tools
At the top level this module includes all of the basic functionality from numpy.
You could import this as, but you might as well import numpy directly.
```
import scipy as sp
```

The main strength in scipy lies in its sub-packages:
```
from scipy import optimize
def costfunc(params):
    return params[0] ** 2 * (params[1] - 3) ** 2 + (params[0] - 2) ** 2
optimize.minimize(costfunc, x0=[0, 0], method='l-bfgs-b')
```

Tutorials for all sub-packages can be found [here](https://docs.scipy.org/doc/scipy-1.0.0/reference/).

## [Matplotlib](https://matplotlib.org/): Main plotting library
```
import matplotlib as mpl
mpl.use('nbagg')
import matplotlib.pyplot as plt
```
The matplotlib tutorials are [here](https://matplotlib.org/tutorials/index.html)

```
x = np.linspace(0, 2, 100)

plt.plot(x, x, label='linear')
plt.plot(x, x**2, label='quadratic')
plt.plot(x, x**3, label='cubic')

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()

plt.show()
```

Alternatives:
- [Mayavi](http://docs.enthought.com/mayavi/mayavi/): 3D plotting (hard to install)
- [Bokeh](https://bokeh.pydata.org/en/latest/) among many others: interactive plots in the browser (i.e., in javascript)

## [Ipython](http://ipython.org/)/[Jupyter](https://jupyter.org/) notebook: interactive python environments
There are many [useful extensions available](https://github.com/ipython-contrib/jupyter_contrib_nbextensions).

## [Pandas](https://pandas.pydata.org/): Analyzing "clean" data
Once your data is in tabular form (e.g. Biobank IDP's), you want to use pandas dataframes to analyze them.
This brings most of the functionality of R into python.
Pandas has excellent support for:
- fast IO to many tabular formats
- accurate handling of missing data
- Many, many routines to handle data
  - group by categorical data (i.e., male/female, or age groups)
  - joining/merging data
  - time series support
- statistical models through [statsmodels](http://www.statsmodels.org/stable/index.html)
- plotting though seaborn [seaborn](https://seaborn.pydata.org/)
- Use [dask](https://dask.pydata.org/en/latest/) if your data is too big for memory (or if you want to run in parallel)

You should also install `numexpr` and `bottleneck` for optimal performance.

For the documentation check [here](http://pandas.pydata.org/pandas-docs/stable/index.html)

### Adjusted example from statsmodels tutorial
```
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
```

```
df = sm.datasets.get_rdataset("Guerry", "HistData").data
df
```

```
df.describe()
```

```
df.groupby('Region').mean()
```

```
results = smf.ols('Lottery ~ Literacy + np.log(Pop1831)', data=df).fit()
results.summary()
```

```
df['log_pop'] = np.log(df.Pop1831)
df
```

```
results = smf.ols('Lottery ~ Literacy + log_pop', data=df).fit()
results.summary()
```

```
results = smf.ols('Lottery ~ Literacy + np.log(Pop1831) + Region', data=df).fit()
results.summary()
```

```
results = smf.ols('Lottery ~ Literacy + np.log(Pop1831) + Region + Region * Literacy', data=df).fit()
results.summary()
```

```
%matplotlib nbagg
import seaborn as sns
sns.pairplot(df, hue="Region", vars=('Lottery', 'Literacy', 'log_pop'))
```

## [Sympy](http://www.sympy.org/en/index.html): Symbolic programming
```
import sympy as sym  # no standard nickname
```

```
x, a, b, c = sym.symbols('x, a, b, c')
sym.solve(a * x ** 2 + b * x + c, x)
```

```
sym.integrate(x/(x**2+a*x+2), x)
```

```
f = sym.utilities.lambdify((x, a), sym.integrate((x**2+a*x+2), x))
f(np.random.rand(10), np.random.rand(10))
```

# Other topics
## [Argparse](https://docs.python.org/3.6/howto/argparse.html): Command line arguments
```
%%writefile test_argparse.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("x", type=int, help="the base")
    parser.add_argument("y", type=int, help="the exponent")
    args = parser.parse_args()
    answer = args.x**args.y

    if args.verbose:
        print("{} to the power {} equals {}".format(args.x, args.y, answer))
    else:
        print("{}^{} == {}".format(args.x, args.y, answer))

if __name__ == '__main__':
    main()
```

```
%run test_argparse.py 3 8 -v
```

```
%run test_argparse.py -h
```

```
%run test_argparse.py 3 8.5 -q
```

### [Gooey](https://github.com/chriskiehl/Gooey): GUI from command line tool
```
%%writefile test_gooey.py
import argparse
from gooey import Gooey

@Gooey
def main():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("x", type=int, help="the base")
    parser.add_argument("y", type=int, help="the exponent")
    args = parser.parse_args()
    answer = args.x**args.y

    if args.verbose:
        print("{} to the power {} equals {}".format(args.x, args.y, answer))
    else:
        print("{}^{} == {}".format(args.x, args.y, answer))

if __name__ == '__main__':
    main()
```

```
%run test_gooey.py
```

```
!gcoord_gui
```

## [Jinja2](http://jinja.pocoo.org/docs/2.10/): HTML generation
```
%%writefile image_list.jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    {% block head %}
    <title>{{ title }}</title>
    {% endblock %}
</head>
<body>
    <div id="content">
        {% block content %}
            {% for description, filenames in images %}
                <p>
                    {{ description }}
                </p>
                {% for filename in filenames %}
                    <a href="{{ filename }}">
                        <img src="{{ filename }}">
                    </a>
                {% endfor %}
            {% endfor %}
        {% endblock %}
    </div>
    <footer>
        Created on {{ time }}
    </footer>
</body>
</html>
```

```
def plot_sine(amplitude, frequency):
    x = np.linspace(0, 2 * np.pi, 100)
    y = amplitude * np.sin(frequency * x)
    plt.plot(x, y)
    plt.xticks([0, np.pi, 2 * np.pi], ['0', '$\pi$', '$2 \pi$'])
    plt.ylim(-1.1, 1.1)
    filename = 'plots/A{:.2f}_F{:.2f}.png'.format(amplitude, frequency)
    plt.title('A={:.2f}, F={:.2f}'.format(amplitude, frequency))
    plt.savefig(filename)
    plt.close(plt.gcf())
    return filename

!mkdir plots
amplitudes = [plot_sine(A, 1.) for A in [0.1, 0.3, 0.7, 1.0]]
frequencies = [plot_sine(1., F) for F in [1, 2, 3, 4, 5, 6]]
```

```
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
loader = FileSystemLoader('.')
env = Environment(loader=loader)
template = env.get_template('image_list.jinja2')

images = [
    ('Varying the amplitude', amplitudes),
    ('Varying the frequency', frequencies),
]

with open('image_list.html', 'w') as f:
    f.write(template.render(title='Lots of sines',
                            images=images, time=datetime.now()))
```

```
!open image_list.html
```

## Neuroimage packages
The [nipy](http://nipy.org/) ecosystem covers most of these.

### [CIFTI](https://github.com/MichielCottaar/cifti): easy creation/manipulation
```
import nibabel
thickness = nibabel.load('100307/fsaverage_LR32k/100307.L.thickness.32k_fs_LR.shape.gii').darrays[0].data
thickness
```

```
import cifti
ctx = thickness != 0
arr = np.random.rand(ctx.sum())

bm_ctx = cifti.BrainModel.from_mask(ctx, name='CortexLeft')
sc = cifti.Scalar.from_names(['random'])
cifti.write('random_ctx.dscalar.nii', arr[None, :], (sc, bm_ctx))
```

```
!wb_view 100307/fsaverage_LR32k/100307.*.32k_fs_LR.surf.gii random_ctx.dscalar.nii
```

```
img = nibabel.load('100307/aparc+aseg.nii.gz')
cerebellum = img.get_data() == 8

bm = bm_ctx + cifti.BrainModel.from_mask(cerebellum, name='CerebellumLeft', affine=img.affine)
sc = cifti.Scalar.from_names(['random'])
arr = np.random.rand(len(bm))
cifti.write('random_ctx_cerebellum.dscalar.nii', arr[None, :], (sc, bm))
```

```
!wb_view 100307/fsaverage_LR32k/100307.*.32k_fs_LR.surf.gii 100307/aparc+aseg.nii.gz random_ctx_cerebellum.dscalar.nii
```

```
arr = abs(thickness[ctx, None] - thickness[None, ctx])
cifti.write('diff_thickness.dconn.nii', arr, (bm_ctx, bm_ctx))
```

```
!wb_view 100307/fsaverage_LR32k/100307.*.32k_fs_LR.surf.gii diff_thickness.dconn.nii
```

## [networkx](https://networkx.github.io/): graph theory

## GUI
- [tkinter](https://docs.python.org/3.6/library/tkinter.html): thin wrapper around Tcl/Tk; included in python
- [wxpython](https://www.wxpython.org/): Wrapper around the C++ wxWidgets library
```
%%writefile wx_hello_world.py
#!/usr/bin/env python
"""
Hello World, but with more meat.
"""

import wx

class HelloFrame(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self)

        # and put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="Hello World!", pos=(25,25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = HelloFrame(None, title='Hello World 2')
    frm.Show()
    app.MainLoop()
```

```
%run wx_hello_world.py
```

## Machine learning
- scikit-learn
- theano/tensorflow/pytorch
  - keras

## [Pycuda](https://documen.tician.de/pycuda/): Programming the GPU
```
import pycuda.autoinit
import pycuda.driver as drv

from pycuda.compiler import SourceModule
mod = SourceModule("""
__global__ void multiply_them(double *dest, double *a, double *b)
{
  const int i = threadIdx.x;
  dest[i] = a[i] * b[i];
}
""")

multiply_them = mod.get_function("multiply_them")

a = np.random.randn(400)
b = np.random.randn(400)

dest = np.zeros_like(a)
multiply_them(
        drv.Out(dest), drv.In(a), drv.In(b),
        block=(400,1,1), grid=(1,1))

print(dest-a*b)
```

## Testing
- [unittest](https://docs.python.org/3.6/library/unittest.html): python built-in testing
> ```
> import unittest
>
> class TestStringMethods(unittest.TestCase):
>
>     def test_upper(self):
>         self.assertEqual('foo'.upper(), 'FOO')
>
>     def test_isupper(self):
>         self.assertTrue('FOO'.isupper())
>         self.assertFalse('Foo'.isupper())
>
>     def test_split(self):
>         s = 'hello world'
>         self.assertEqual(s.split(), ['hello', 'world'])
>         # check that s.split fails when the separator is not a string
>         with self.assertRaises(TypeError):
>             s.split(2)
>
> if __name__ == '__main__':
>     unittest.main()
> ```
- [doctest](https://docs.python.org/3.6/library/doctest.html): checks the example usage in the documentation
> ```
> def factorial(n):
>     """Return the factorial of n, an exact integer >= 0.
>
>     >>> [factorial(n) for n in range(6)]
>     [1, 1, 2, 6, 24, 120]
>     >>> factorial(30)
>     265252859812191058636308480000000
>     >>> factorial(-1)
>     Traceback (most recent call last):
>         ...
>     ValueError: n must be >= 0
>
>     Factorials of floats are OK, but the float must be an exact integer:
>     >>> factorial(30.1)
>     Traceback (most recent call last):
>         ...
>     ValueError: n must be exact integer
>     >>> factorial(30.0)
>     265252859812191058636308480000000
>
>     It must also not be ridiculously large:
>     >>> factorial(1e100)
>     Traceback (most recent call last):
>         ...
>     OverflowError: n too large
>     """
>
>     import math
>     if not n >= 0:
>         raise ValueError("n must be >= 0")
>     if math.floor(n) != n:
>         raise ValueError("n must be exact integer")
>     if n+1 == n:  # catch a value like 1e300
>         raise OverflowError("n too large")
>     result = 1
>     factor = 2
>     while factor <= n:
>         result *= factor
>         factor += 1
>     return result
>
>
> if __name__ == "__main__":
>     import doctest
>     doctest.testmod()
> ```
Two external packages provide more convenient unit tests:
- [py.test](https://docs.pytest.org/en/latest/)
- [nose2](http://nose2.readthedocs.io/en/latest/usage.html)
> ```
> # content of test_sample.py
> def inc(x):
>     return x + 1
>
> def test_answer():
>     assert inc(3) == 5
> ```

- [coverage](https://coverage.readthedocs.io/en/coverage-4.5.1/): measures which part of the code is covered by the tests

## Linters
Linters check the code for any syntax errors, [style errors](https://www.python.org/dev/peps/pep-0008/), unused variables, unreachable code, etc.
- [pylint](https://pypi.python.org/pypi/pylint): most extensive linter
- [pyflake](https://pypi.python.org/pypi/pyflakes): if you think pylint is too strict
- [pep8](https://pypi.python.org/pypi/pep8): just checks for style errors
- [mypy](http://mypy-lang.org/): adding explicit typing to python