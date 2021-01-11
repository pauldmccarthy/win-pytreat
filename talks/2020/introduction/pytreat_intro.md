# Welcome to the WIN PyTreat 2020!


Program: https://docs.google.com/document/d/11LQgxC-LZPG_TXS3MP9tYXNWABAQdTI00iavk-tKttU/edit


__We need to do some setting up, so get your laptop ready!__

__Make sure you have FSL 6.0.3 installed and working!__

__End all sentences with an exclamation mark!__

__Open this page in your web browser!__

https://git.fmrib.ox.ac.uk/fsl/pytreat-practicals-2020/tree/master/talks/introduction/pytreat_intro.md


## Overview


* [Python in a nutshell](#python-in-a-nutshell)
* [`fslpython`](#fslpython)
* [Running Python scripts](#running-python-scripts)
* [Interactive Python: IPython](#interactive-python-ipython)
* [Python editors](#python-editors)
* [Python in your browser: Jupyter Notebook](#python-in-your-browser-jupyter-notebook)
* [Git](#git)
* [The PyTreat practicals](#the-pytreat-practicals)


<a class="anchor" id="python-in-a-nutshell"></a>
## Python in a nutshell


### Pros


* _Flexible_ Feel free to use functions, classes, objects, modules and
  packages. Or don't - it's up to you!

* _Fast_ If you do things right (in other words, if you use `numpy`)

* _Dynamically typed_ No need to declare your variables, or specify their
  types.


```
a = 'Great, I am _so_ sick of writing "char *a;"!'
print(a)

a = 12345
print('a is now an number!', a)
```


* _Intuitive syntax_ How do I run some code for each of the elements in my
  list?


```
a = [1, 2, 3, 4, 5]

for elem in a:
    print(elem)
```


### Cons

* _Dynamically typed_ Easier to make mistakes, harder to catch them

* _No compiler_ See above

* _Slow_ if you don't do things the right way

* _Python 2 is not the same as Python 3_ But there's an easy solution: Forget
  that Python 2 exists.

* _Hard to manage different versions of python_ But we have a solution for
  you: `fslpython`.


<a class="anchor" id="fslpython"></a>
## `fslpython`


FSL 5.0.10 and newer comes with its own version of Python, bundled with nearly
all of the scientific libraries that you are likely to need.


So if you use `fslpython` for all of your development, you can be sure that it
will work in FSL!


> `fslpython` is based on _conda_ and, in FSL 6.0.3, is Python version
> 3.7.3. You can read more about conda [here](https://conda.io/docs/).


<a class="anchor" id="running-python-scripts"></a>
## Running Python scripts


Here's a basic Python script - a _Hello world_ for neuroimaging:


> ```
> #!/usr/bin/env fslpython
>
> # That first line up there ensures that your
> # script will be executed in the fslpython
> # environment. If you are writing a general
> # Python script, you should use this line
> # instead: #!/usr/bin/env python
>
> # In Python, we need to "import" libraries
> # (called modules) before we can use them.
> import sys
> import nibabel as nib
>
> # We can get to our command
> # line arguments via sys.argv
> fpath = sys.argv[1]
>
> # We can use nibabel to load
> # NIFTI images (and other
> # neuroimaging data formats)
> img = nib.load(fpath)
> data = img.get_data()
>
> # Now we're working with a
> # numpy array.
> nzmean = data[data != 0].mean()
>
> print('mean:', nzmean)
> ```


__Exercise__ Save the above code to a file called `script.py`, then run this
in a terminal (replace `/path/to/some/image/on/your/computer.nii.gz` with a
path to some image on your computer):


> ```
> chmod a+x script.py
> ./script.py /path/to/some/image/on/your/computer.nii.gz
> ```


<a class="anchor" id="interactive-python-ipython"></a>
## Interactive Python: IPython


Python is an [_interpreted
language_](https://en.wikipedia.org/wiki/Interpreted_language), like MATLAB.  So
you can either write your code into a file, and then run that file, or you can
type code directly into a Python interpreter.


Python has a standard interpreter built-in - run `fslpython` in a terminal,
and see what happens (use CTRL+D to exit).


__But__ there is another interpreter called [IPython](https://ipython.org/)
which is vastly superior to the standard Python interpreter. Use IPython
instead! It is already installed in `fslpython`, so if you want to do some
interactive work, you can use `fslipython` in a terminal.


__Exercise__ Do it now! Start `fslipython`, then copy/paste this code into the
prompt!


> ```
> # this line is not python - it is
> # specific to ipython/jupyter notebook
> %matplotlib
>
> import numpy as np
>
> x = np.concatenate(([0.25, 0.75], np.arange(0.1, 1.0, 0.1)))
> y = np.concatenate(([0.75, 0.75], -np.sin(np.linspace(np.pi / 4, 3 * np.pi / 4, 9))))
>
> import matplotlib.pyplot as plt
>
> fig = plt.figure()
> ax  = fig.add_subplot(111)
>
> ax.scatter(x, y)
> ```


<a class="anchor" id="python-editors"></a>
## Python editors


> Summary:
>   - Make your tab key insert four spaces. Don't use tab characters in Python
>     code.
>
>   - Use [Spyder](https://pythonhosted.org/spyder/) if you want a MATLAB-like
>     envionment (focus on analysis, rather than coding).
>
>   - Use [PyCharm](https://www.jetbrains.com/pycharm/) if you want an IDE-like
>     environment (focus on coding, rather than analysis).
>
>   - Use [Atom](https://atom.io/) or [VS Code](https://code.visualstudio.com/)
>     if you like using the latest and greatest.
>
>   - If you like your existing editor, use it. But you will be better off if
>     you can integrate it with `fslpython`, [pylint](https://www.pylint.org/)
>     and [pyflakes](https://github.com/PyCQA/pyflakes).


You can use any text editor that you want to edit Python files. But the one
golden rule that you must follow, no matter what editor you use:


__Configure your tab key to insert four spaces. Don't use tab characters in
Python code!__


This is the [standard
convention](https://www.python.org/dev/peps/pep-0008/#indentation) for Python
code. If you deviate from this convention, and somebody else needs to work
with your code, they will be angry at you!


Now, with that out of the way, there are several good Python editors available
to you. If you are getting started with Python, we recommend
[PyCharm](https://www.jetbrains.com/pycharm/) or
[Spyder](https://pythonhosted.org/spyder/).


If you are used to MATLAB, and you do a lot of experimenting or interactive
work, then you might like Spyder. If you spend most of your time writing code
rather than experimenting, then go with PyCharm.


Importantly, both PyCharm and Spyder will correctly indent your Python code!


> If you are going to stick with Emacs for your Python development, then it
> should correctly indent Python code by default.  But if it isn't, add
> the following to your `~/.emacs` file:
>
>     (defun my-python-mode-hook ()
>         (setq indent-tabs-mode     nil)
>         (setq python-indent        4)  ; for versions prior to 24.3
>         (setq python-indent-offset 4)) ; for versions 24.3 or newer
>     (add-hook 'python-mode-hook   'my-python-mode-hook)


### Spyder


Spyder is a MATLAB-like environment for Python. It has a code editor and an
interactive IPython prompt. You can inspect variables that are in your
workspace, plot data, and so on and so forth.


Beyond that, Spyder is fairly simple - it does not have much in the way of
project management tools, or integration with version control (i.e. `git`).


Spyder can be installed directly into `fslpython`:


> If your FSL installation requires administrative privileges to modify, you
> will need to prefix these commands with sudo.
>
> Install Spyder:
>
>     $FSLDIR/fslpython/bin/conda install -n fslpython -y spyder

> Create a link so you can call it easily:
>
>     ln -s $FSLDIR/fslpython/envs/fslpython/bin/spyder $FSLDIR/bin/fslspyder

Now to run Spyder, you can just type:


> ```
> fslspyder &
> ```


Now you need to make sure that Spyder is using the `fslpython` environment to
run your code.


1. Go to _python_ (the menu) > _Preferences_ > Python Interpreter
2. Make sure that _Use the following Python interpreter_ is selected
3. Make sure that the path is `$FSLDIR/fslpython/envs/fslpython/bin/python`
   (for your specific value of `$FSLDIR`).


Type the following into the console to test that everything is working:


```
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
```


### PyCharm


PyCharm is a general-purpose Python development environment. When compared to
Spyder, it is less geared towards interactive analysis, but has better code
editing tools (e.g. autocomplete and refactoring), and better file
management/version control integration.


And it is also easy to install - simply download the Community edition from
the [home page](https://www.jetbrains.com/pycharm/). Then, if you are on a
mac, double-click the `.dmg` file, and drag PyCharm into your `/Applications/`
folder. Then double-click on PyCharm to start it.


Once you have chosen a theme, you will be asked if you would like to create a
_Launcher script_ - do this, because you will then be able to open files from
the terminal by typing `charm [filename]`.


Now you will be presented with a _Welcome to PyCharm_ window. __Before doing
anything else__, click on the _Configure_ button down in the bottom right, and
choose _Preferences_. Then in the _Project Interpreter_ section:


1. Click on the gear button and choose _Add local..._
2. Choose _Existing environment_
3. Click on the _..._ button, and navigate to
   `$FSLDIR/fslpython/envs/fslpython/bin/python`.


### Other options


Emacs is capable of being used as a fully-fledged Python IDE, if you have the
time and patience to configure it.

If you are the fashionable sort, try one of these:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Atom](https://atom.io/)


<a class="anchor" id="python-in-your-browser-jupyter-notebook"></a>
## Python in your browser: Jupyter Notebook


It is possible to do your Python-based development and experimentation inside
your web browser, thanks to the [Jupyter project](https://jupyter.org/).


Jupyter works in the following way:

1. You start a Juptyer web server on your computer. This web server provides
   the environment in which your Python code is executed.

2. You open https://localhost:8888 (or similar) in a web browser - this opens
   a connection to the (locally running) web server.

3. You start a "Notebook" (Jupyter's version of a file), and start typing.
   You can put text, LaTeX, and of course Python code into a notebook.

4. All of the code that you write gets sent to the web server and
   executed. Then the results get sent back to the web browser, and displayed
   in your notebook - magic!


All of the PyTreat practicals are written in a Jupyter notebook. Some of the
talks are too - you're looking at a Jupyter Notebook right now!


<a class="anchor" id="git"></a>
## Git


All the cool kids these days use [git](https://git-scm.com/) to
collaboratively work on their Python code. The PyTreat is a great opportunity
to start learning and using it for your own work!


Git is different from CVS and SVN in that it is _distributed_. In CVS and SVN,
there is only one central repository. You check out a copy of the source from
the repository, make some changes, and then commit those changes back to the
central repository.


In git, there are multiple repositories. There is usually one repository which
acts as the central one, but you will _clone_ (or _fork_) that central
repository to create your own full copy of the repository.


Then, you can make changes and commit them in your own repository. And at any
point, you can push your changes back to the central repository.


### WIN's gitlab server


https://git.fmrib.ox.ac.uk/


If you have a FMRIB account, then you also have a Gitlab account. Gitlab is a
git server that you can use to store your "central" git repository.  Gitlab is
very similar to https://www.github.com, but it is managed by WIN, and your
code is not publicly visible (although it can be if you want).  Gitlab backs
up your code automatically, and has a nice web interface.

You can have up to 10 projects on your gitlab account - talk to the FMRIB IT
people if you need more.


### Using git and gitlab


> We need to go through a couple of intiial configuration steps before
> proceeding. You only need to do this once (for each computer that you use).
>
> First, run these commands to configure git on your system.
>
> ```
> git config --global user.name "Your name"
> git config --global user.email "Your email address"
> ```
>
> Now you need to create a SSH key pair, so your computer can talk to the
> gitlab server without you having to log in. Don't be scared - there are
> detailed instructions on doing this at
> https://git.fmrib.ox.ac.uk/help/ssh/README.md - follow the instructions
> under the section entitled __Generating a new SSH key pair__.


Working with git and gitlab generally involves these steps:

1. Add new files to your local repository, or make changes to existing files.
2. Run `git add` on the new/changed files to _stage_ them.
3. Run `git commit` to commit all staged changes to your local repository.
4. Run `git push` to push those commits to your gitlab repository.


When you start working on a new project (or if you have an existing project
that you want to put into git):


__1. Organise all of your project files into their own folder__


This sounds obvious, but just to be sure.


__2. Create a repository for your project on gitlab__


Log in to gitlab (https://git.fmrib.ox.ac.uk/), then click on the _+_ button
towards the top right, and select _New project_. Give the project a name and
choose its visiblity (note that _Public_ means your project will be visible to
the world).


__3. Turn your project folder into a git repository__


Now, follow the instructions that are listd on your gitlab project home page,
under __Existing folder__ (repeated here):


>     cd existing_folder
>     git init
>     git remote add origin git@git.fmrib.ox.ac.uk:username/project.git
>     git add .
>     git commit -m "Initial commit"
>     git push -u origin master


The `git add .` line will add _all_ of the files in your project directory
into git. If you only want certain files in git, then `git add` them one by
one (or use standard bash file patterns, e.g. `git add *.py`).

You should avoid putting large binary files or data files into git - it works
best with plain text. Talk to the FMRIB IT people if you really need to store
large files in git, as they can help you with this.


__4. Develop your super cool project!__


Now you can get to work! Whenever you make changes to your code that you want
saved,  follow the `git add`, `git commit`, `git push` steps described above.


For example, let's say we have added a new file called `cool_module.py`.  To
get this into git, we would do the following:


```
git add cool_module.py
git commit -m "Added cool module. It's super cool"
git push origin master
```


<a class="anchor" id="the-pytreat-practicals"></a>
## The PyTreat practicals


All of the practicals for PyTreat are hosted in a git repository at:


https://git.fmrib.ox.ac.uk/fsl/pytreat-practicals-2020


So let's go get them!


> ```
> git clone https://git.fmrib.ox.ac.uk/fsl/pytreat-practicals-2020.git
> cd pytreat-practicals-2020
> fslpython -m notebook
> ```
