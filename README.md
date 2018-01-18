# 2018 WIN PyTreat


This repository contains Jupyter notebooks and data for the 2018 WIN PyTreat.


The master repository can be found at:

https://git.fmrib.ox.ac.uk/fsl/pytreat-2018-practicals


To contribute to the practicals:

1. Fork the master repository on gitlab

2. Make your changes on your fork

3. Submit a merge request back to the master repository



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
> you to convert a markdownd (`.md`) file to a Jupyter notebook (`.ipynb`)
> file. So you can write your practical in your text editor of choice, and
> then convert it into a notebook, instead of writing the practical in the web
> browser interface.


Now you can start the notebook server from the repository root:

```
fsljupyter notebook
```
