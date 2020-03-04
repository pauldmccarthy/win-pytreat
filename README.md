# 2020 WIN PyTreat


This repository contains Jupyter notebooks and data for the 2020 WIN PyTreat.
It contains the following:

- The `talks` directory contains some (but not all) of the _Topyc_ talks that
  will be given throughout the week.

- The `getting_started` directory contains a series of practicals intended
  for those of you who are new to the Python programming language, or need
  a refresher.

- The `advanced_topics` directory contains a series of practicals on various
  aspects of the Python programming language - these are intended for those
  of you who are familiar with the basics of Python, and want to learn more
  about the language.


The practicals have been written under the assumption that FSL 6.0.3 is
installed.


## For attendees


These notebooks can be run in the `fslpython` environment using:


```
git clone https://git.fmrib.ox.ac.uk/fsl/pytreat-practicals-2020.git
cd pytreat-practicals-2020
fslpython -m notebook
```

A page should open in your web browser - to access the practicals, navigate
into one of the `getting_started` or `advanced_topics` directories, and click
on the `.ipynb` file you are interested in. Some of the talks are also
presented in notebook form - navigate to the talk you are interested in
(within the `talks` directory), and click on the `.ipynb` file to follow
along.


Throughout the week we might make changes to this repository. When this
happens, we will ask you to update your local clone of the repository with the
following command:


```
git stash save
git pull origin master
git stash pop
```


Have fun!


## For contributors


The main repository can be found at:

https://git.fmrib.ox.ac.uk/fsl/pytreat-practicals-2020


Updates to the master branch should occur via merge requests. You can choose
to either work on a branch within this repository, or on a fork of this
repository.

### Using a branch within this repository

1. Make a local clone of the repository:

    ```
    git clone https://git.fmrib.ox.ac.uk/fsl/pytreat-practicals-2020.git
    ```

2. Create a branch for your work:

    ```
    git checkout -b my_cool_branch origin/master
    ```

3. Make your changes on this branch.

4. Push your changes to the gitlab repository:

    ```
    git push origin my_cool_branch
    ```

5. In gitlab, submit a merge request from your branch onto the master
   branch.


### Using a fork of this repository

1. Fork the upstream repository on gitlab

2. Make a local clone of your fork:

    ```
    git clone https://git.fmrib.ox.ac.uk/<your_username>/pytreat-practicals-2020.git
    ```

3. Add the upstream repository as a remote:

    ```
    git remote add upstream https://git.fmrib.ox.ac.uk/fsl/pytreat-practicals-2020.git
    ```

4. Make your changes on your local repository

5. Push your changes to your fork:

    ```
    git push origin master
    ```

6. In gitlab, submit a merge request from your fork back to the upstream
   repository.


### Updating your local repository

To bring in the changes that other people have contributed to the main
repository into your local repository:


```
git fetch --all

# make sure you are on the correct local branch - if you followed the
# instructions above and are working on a fork of the main repository:
git checkout master

# Or if you are working on a branch within the main repository:
git checkout my_cool_branch

# Do this if you are working on a fork of the main repository
git merge upstream/master

# Or do this if you are working on a branch within the main repository
git merge origin/master
```


> Or, if you are comfortable with git, `rebase` is so much cooler:
>
> ```
> git fetch --all
>
> # replace <branch_name> with your local branch name
> git checkout <remote_name>/master
>
> # replace <remote_name> with the main repository name
> git rebase <remote_name>/master
> ```


### Writing your talk as a Jupyter notebook

You may wish to install [`notedown`](https://github.com/aaren/notedown):

```
source $FSLDIR/fslpython/bin/activate fslpython
pip install notedown
source deactivate
fslpython -m notedown
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
