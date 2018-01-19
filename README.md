# 2018 WIN PyTreat


This repository contains Jupyter notebooks and data for the 2018 WIN PyTreat.


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


To run these notebooks in the `fslpython` environment, you must first install
jupyter:


```
source $FSLDIR/fslpython/bin/activate fslpython
conda install jupyter
pip install notedown
source deactivate
ln -s $FSLDIR/fslpython/envs/fslpython/bin/jupyter $FSLDIR/bin/fsljupyter
ln -s $FSLDIR/fslpython/envs/fslpython/bin/notedown $FSLDIR/bin/fslnotedown
```


> [`notedown`](https://github.com/aaren/notedown) is a handy tool which allows
> you to convert a markdown (`.md`) file to a Jupyter notebook (`.ipynb`)
> file. So you can write your practical in your text editor of choice, and
> then convert it into a notebook, instead of writing the practical in the web
> browser interface. If you install notedown as suggested in the code block
> above, you can run it on a markdown file like so:
>
> ```
> fslnotedown my_markdown_file.md > my_notebook.ipynb
> ```


Now you can start the notebook server from the repository root:

```
fsljupyter notebook
```
