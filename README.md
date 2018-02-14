# 2018 WIN PyTreat


This repository contains Jupyter notebooks and data for the 2018 WIN PyTreat.
It contains two sets of practicals:

- The `getting_started` directory contains a series of practicals intended
  for those of you who are new to the Python programming language, or need
  a refresher.

- The `advanced_topics` directory contains a series of practicals on various
  aspects of the Python programming language - these are intended for those
  of you who are familiar with the basics of Python, and want to learn more
  about the language.


These practicals have been written under the assumption that FSL 5.0.10 is
installed.


## For attendees


To run these notebooks in the `fslpython` environment, you must first install
jupyter:


```
# If your FSL installation requires administrative privileges to modify, then
# you MUST run these commands as root - don't just prefix each individual
# command with sudo, or you will probably install jupyter into the wrong
# location!
#
# One further complication - once you have become root, $FSLDIR may not be set,
# so either set it as we have done below, or make sure that it is set, before
# proceeding.
sudo su
export FSLDIR=/usr/local/fsl
source $FSLDIR/fslpython/bin/activate fslpython
conda install jupyter
source deactivate
ln -s $FSLDIR/fslpython/envs/fslpython/bin/jupyter $FSLDIR/bin/fsljupyter
```


Then, clone this repository on your local machine, and run
`fsljupyter notebook`:


```
git clone git@git.fmrib.ox.ac.uk:fsl/pytreat-2018-practicals.git
cd pytreat-2018-practicals
fsljupyter notebook
```


Have fun!


## For contributors


The upstream repository can be found at:

https://git.fmrib.ox.ac.uk/fsl/pytreat-2018-practicals


To contribute to the practicals:

1. Fork the upstream repository on gitlab

2. Make a local clone of your fork:

    ```
    git clone git@git.fmrib.ox.ac.uk:<username>/pytreat-2018-practicals
    ```

3. Add the upstream repository as a remote:

    ```
    git remote add upstream git@git.fmrib.ox.ac.uk:fsl/pytreat-2018-practicals.git
    ```

4. Make your changes on your local repository

5. Rebase onto the upstream repository, and push your changes to your fork:

    ```
    git fetch --all
    git rebase upstream/master
    git push --force origin master
    ```

6. In gitlab, submit a merge request from your fork back to the upstream
   repository.


When you install `jupyter` above, you may also wish to install
[`notedown`](https://github.com/aaren/notedown):

```
# .
# see instructions above
# .
conda install jupyter
pip install notedown
source deactivate
ln -s $FSLDIR/fslpython/envs/fslpython/bin/jupyter  $FSLDIR/bin/fsljupyter
ln -s $FSLDIR/fslpython/envs/fslpython/bin/notedown $FSLDIR/bin/fslnotedown
```

`notedown` is a handy tool which allows you to convert a markdown (`.md`) file
to a Jupyter notebook (`.ipynb`) file. So you can write your practical in your
text editor of choice, and then convert it into a notebook, instead of writing
the practical in the web browser interface. If you install notedown as
suggested in the code block above, you can run it on a markdown file like so:


```
fslnotedown my_markdown_file.md > my_notebook.ipynb
```
