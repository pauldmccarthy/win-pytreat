# WIN PyTreat seriesx


This repository contains Jupyter notebooks and data for the WIN PyTreat series.
It contains the following:

- The `talks` directory contains a series of _Topyc_ talks that have been/will
  be given during the PyTreat.

- The `getting_started` directory contains a series of practicals intended
  for those of you who are new to the Python programming language, or need
  a refresher.

- The `advanced_topics` directory contains a series of practicals on various
  aspects of the Python programming language - these are intended for those
  of you who are familiar with the basics of Python, and want to learn more
  about the language.

- The `applications` directory contains a series of practicals which focus
  on using Python to accomplish specific tasks.

The practicals have been written under the assumption that FSL 6.0.3 is
installed.


## For attendees


These notebooks can be run in the `fslpython` environment using:


```
git clone https://git.fmrib.ox.ac.uk/fsl/win-pytreat.git
cd win-pytreat
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


**IMPORTANT** Temporarily hosting at https://github.com/pauldmccarthy/win-pytreat, instead
of https://git.fmrib.ox.ac.uk/fsl/win-pytreat


The main repository can be found at:

https://git.fmrib.ox.ac.uk/fsl/win-pytreat


Updates to the master branch should occur via merge requests. You can choose
to either work on a branch within this repository  (recommended), or on a fork of this
repository (advanced).

### Using a branch within this repository (recommended)

1. Make a local clone of the repository:

    ```
    git clone https://git.fmrib.ox.ac.uk/fsl/win-pytreat.git
    ```

2. Create a branch for your work:

    ```
    git checkout -b my_cool_branch origin/master
    ```

3. Make your changes on this branch.

    ```
    git add <my_new_and_changed_files>
    git commit -m 'super cool updates'
    ```

4. Push your changes to the gitlab repository:

    ```
    git push origin my_cool_branch
    ```

5. In gitlab, submit a merge request from your branch onto the master
   branch.

    https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html


### Using a fork of this repository (advanced)

1. Fork the upstream repository on gitlab

2. Make a local clone of your fork:

    ```
    git clone https://git.fmrib.ox.ac.uk/<your_username>/win-pytreat.git
    ```

3. Add the upstream repository as a remote:

    ```
    git remote add upstream https://git.fmrib.ox.ac.uk/fsl/win-pytreat.git
    ```

4. Make your changes on your local repository

    ```
    git add <my_new_and_changed_files>
    git commit -m 'super cool updates'
    ```

5. Push your changes to your fork:

    ```
    git push origin master
    ```

6. In gitlab, submit a merge request from your fork back to the upstream
   repository.

    https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html


### Updating your local repository

To bring in the changes that other people have contributed to the main
repository into your local repository:

```
git fetch --all

```

Then, do this if you are working on a branch within the main repository:

```
# make sure you are on the correct local branch:
git checkout my_cool_branch
git merge origin/master
```

Or, do this if you are working on a fork of the main repository:
```
git checkout master
git merge upstream/master
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
$FSLDIR/fslpython/bin/conda install -n fslpython -c conda-forge notedown
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
