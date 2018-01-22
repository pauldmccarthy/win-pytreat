# File management


In this section we will introduce you to file management - how do we find and
manage files, directories and paths in Python?


Most of Python's built-in functionality for managing files and paths is spread
across the following modules:


 - [`os`](https://docs.python.org/3.5/library/os.html)
 - [`shutil`](https://docs.python.org/3.5/library/shutil.html)
 - [`os.path`](https://docs.python.org/3.5/library/os.path.html)
 - [`glob`](https://docs.python.org/3.5/library/glob.html)
 - [`fnmatch`](https://docs.python.org/3.5/library/fnmatch.html)


The `os` and `shutil` modules have functions allowing you to manage _files and
directories_. The `os.path`, `glob` and `fnmatch` modules have functions for
managing file and directory _paths_.


> Another standard library -
> [`pathlib`](https://docs.python.org/3.5/library/pathlib.html) - was added in
> Python 3.4, and provides an object-oriented interface to path management. We
> aren't going to cover `pathlib` here, but feel free to take a look at it if
> you are into that sort of thing.


## Contents


If you are impatient, feel free to dive straight in to the exercises, and use the
other sections as a reference. You might miss out on some neat tricks though.


* [Managing files and directories](#managing-files-and-directories)
 * [Querying and changing the current directory](#querying-and-changing-the-current-directory)
 * [Directory listings](#directory-listings)
 * [Creating and removing directories](#creating-and-removing-directories)
 * [Moving and removing files](#moving-and-removing-files)
 * [Walking a directory tree](#walking-a-directory-tree)
 * [Copying, moving, and removing directory trees](#copying-moving-and-removing-directory-trees)
* [Managing file paths](#managing-file-paths)
 * [File and directory tests](#file-and-directory-tests)
 * [Deconstructing paths](#deconstructing-paths)
 * [Absolute and relative paths](#absolute-and-relative-paths)
 * [Wildcard matching a.k.a. globbing](#wildcard-matching-aka-globbing)
 * [Expanding the home directory and environment variables](#expanding-the-home-directory-and-environment-variables)
 * [Cross-platform compatibility](#cross-platform-compatbility)
* [Exercises](#exercises)
 * [Re-name subject directories](#re-name-subject-directories)
 * [Re-organise a data set](#re-organise-a-data-set)
 * [Re-name subject files](#re-name-subject-files)
 * [Compress all uncompressed images](#compress-all-uncompressed-images)
 * [Write your own `os.path.splitext`](#write-your-own-os-path-splitext)
 * [Write a function to return a specific image file](#write-a-function-to-return-a-specific-image-file)
 * [Solutions](#solutions)


<a class="anchor" id="managing-files-and-directories"></a>
## Managing files and directories


The `os` module contains functions for querying and changing the current
working directory, moving and removing individual files, and for listing,
creating, removing, and traversing directories.


```
import os
import os.path as op
```


> If you are using a library with a long name, you can create an alias for it
> using the `as` keyword, as we have done here for the `os.path` module.


<a class="anchor" id="querying-and-changing-the-current-directory"></a>
### Querying and changing the current directory


You can query and change the current directory with the `os.getcwd` and
`os.chdir` functions.


> Here we're also going to use the `expanduser` function from the `os.path`
> module, which allows us to expand the tilde character to the user's home
> directory This is [covered in more detail
> below](#expanding-the-home-directory-and-environment-variables).


```
cwd = os.getcwd()
print('Current directory: {}'.format(cwd))

os.chdir(op.expanduser('~'))
print('Changed to: {}'.format(os.getcwd()))

os.chdir(cwd)
print('Changed back to: {}'.format(cwd))
```


For the rest of this practical, we're going to use a little data set that has
been pre-generated, and is located in a sub-directory called
`file_management`.


```
os.chdir('file_management')
```


<a class="anchor" id="directory-listings"></a>
### Directory listings


Use the `os.listdir` function to get a directory listing (a.k.a. the Unix `ls`
command):


```
cwd = os.getcwd()
listing = os.listdir(cwd)
print('Directory listing: {}'.format(cwd))
print('\n'.join([p for p in listing]))
print()

datadir = 'raw_mri_data'
listing = os.listdir(datadir)
print('Directory listing: {}'.format(datadir))
print('\n'.join([p for p in listing]))
```


> Check out the `os.scandir` function as an alternative to `os.listdir`, if
> you have performance problems on large data sets.


> In the code above, we used the string `join` method to print each path in
> our directory listing on a new line. If you have a list of strings, the
> `join` method is a handy way to insert a delimiting character or string
> (e.g. newline, space, tab, comma - any string you want), between each string
> in the list.


<a class="anchor" id="creating-and-removing-directories"></a>
### Creating and removing directories


You can, not surprisingly, use the `os.mkdir` function to make a
directory. The `os.makedirs` function is also handy - it is equivalent to
`mkdir -p` in Unix:


```
print(os.listdir('.'))
os.mkdir('onedir')
os.makedirs('a/big/tree/of/directories')
print(os.listdir('.'))
```


The `os.rmdir` and `os.removedirs` functions perform the reverse
operations. The `os.removedirs` function will only remove empty directories,
and you must pass it the _leaf_ directory, just like `rmdir -p` in Unix:


```
os.rmdir('onedir')
os.removedirs('a/big/tree/of/directories')
print(os.listdir('.'))
```


<a class="anchor" id="moving-and-removing-files"></a>
### Moving and removing files


The `os.remove` and `os.rename` functions perform the equivalent of the Unix
`rm` and `mv` commands for files. Just like in Unix, if the destination file
you pass to `os.rename` already exists, it will be silently overwritten!


```
with open('file.txt', 'wt') as f:
    f.write('This file contains nothing of interest')

print(os.listdir())
os.rename('file.txt', 'file2.txt')
print(os.listdir())
os.remove('file2.txt')
print(os.listdir())
```


The `os.rename` function will also work on directories, but the `shutil.move`
function (covered below) is more flexible.


<a class="anchor" id="walking-a-directory-tree"></a>
### Walking a directory tree


The `os.walk` function is a useful one to know about. It is a bit fiddly to
use, but it is the best option if you need to traverse a directory tree.  It
will recursively iterate over all of the files in a directory tree - by
default it will traverse the tree in a breadth-first manner.


```
# On each iteration of the loop, we get:
#   - root:  the current directory
#   - dirs:  a list of all sub-directories in the root
#   - files: a list of all files in the root
for root, dirs, files in os.walk('raw_mri_data'):
    print('Current directory: {}'.format(root))
    print('  Sub-directories:')
    print('\n'.join(['    {}'.format(d) for d in dirs]))
    print('  Files:')
    print('\n'.join(['    {}'.format(f) for f in files]))
```


> Note that `os.walk` does not guarantee a specific ordering in the lists of
> files and sub-directories that it returns. However, you can force an
> ordering quite easily - see its
> [documentation](https://docs.python.org/3.5/library/os.html#os.walk) for
> more details.


If you need to traverse the directory depth-first, you can use the `topdown`
parameter:


```
for root, dirs, files in os.walk('raw_mri_data', topdown=False):
    print('Current directory: {}'.format(root))
    print('  Sub-directories:')
    print('\n'.join(['    {}'.format(d) for d in dirs]))
    print('  Files:')
    print('\n'.join(['    {}'.format(f) for f in files]))
```


> Here we have explicitly named the `topdown` argument when passing it to the
> `os.walk` function. This is referred to as a a _keyword argument_ - unnamed
> arguments aqe referred to as _positional arguments_. We'll give some more
> examples of positional and keyword arguments below.


<a class="anchor" id="copying-moving-and-removing-directory-trees"></a>
### Copying, moving, and removing directory trees


The `shutil` module contains some higher level functions for copying and
moving files and directories.


```
import shutil
```


The `shutil.copy` and `shutil.move` functions work just like the Unix `cp` and
`mv` commands:


```
# copy the source file to a destination file
src = 'raw_mri_data/subj_1/t1.nii'
shutil.copy(src, 'subj_1_t1.nii')

print(os.listdir('.'))

# copy the source file to a destination directory
os.mkdir('data_backup')
shutil.copy('subj_1_t1.nii', 'data_backup')

print(os.listdir('.'))
print(os.listdir('data_backup'))

# Move the file copy into that destination directory
shutil.move('subj_1_t1.nii', 'data_backup/subj_1_t1_backup.nii')

print(os.listdir('.'))
print(os.listdir('data_backup'))

# Move that destination directory into another directory
os.mkdir('data_backup_backup')
shutil.move('data_backup', 'data_backup_backup')

print(os.listdir('.'))
print(os.listdir('data_backup_backup'))
```


The `shutil.copytree` function allows you to copy entire directory trees - it
is the equivalent of the Unix `cp -r` command. The reverse operation is provided
by the `shutil.rmtree` function:


```
shutil.copytree('raw_mri_data', 'raw_mri_data_backup')
print(os.listdir('.'))
shutil.rmtree('raw_mri_data_backup')
shutil.rmtree('data_backup_backup')
print(os.listdir('.'))
```


<a class="anchor" id="managing-file-paths"></a>
## Managing file paths


The `os.path` module contains functions for creating and manipulating file and
directory paths, such as stripping directory prefixes and suffixes, and
joining directory paths in a cross-platform manner. In this code, we are using
`op` to refer to `os.path` - remember that we [created an alias
earlier](#managing-files-and-directories).


> Note that many of the functions in the `os.path` module do not care if your
> path actually refers to a real file or directory - they are just
> manipulating the path string, and will happily generate invalid or
> non-existent paths for you.


<a class="anchor" id="file-and-directory-tests"></a>
### File and directory tests


If you want to know whether a given path is a file, or a directory, or whether
it exists at all, then the `os.path` module has got your back with its
`isfile`, `isdir`, and `exists` functions. Let's define a silly function which
will tell us what a path is:

```
# This function takes an optional keyword
# argument "existonly", which controls
# whether the path is only tested for
# existence. We can call it either with
# or without this argument.
def whatisit(path, existonly=False):

    print('Does {} exist? {}'.format(path, op.exists(path)))

    if not existonly:
        print('Is {} a file? {}'     .format(path, op.isfile(path)))
        print('Is {} a directory? {}'.format(path, op.isdir( path)))
```


Now let's use that function to test some paths.


> Here we are using the `op.join` function to construct paths - it is [covered
> below](#cross-platform-compatbility).


```
dirname  = op.join('raw_mri_data')
filename = op.join('raw_mri_data', 'subj_1', 't1.nii')
nonexist = op.join('very', 'unlikely', 'to', 'exist')

whatisit(dirname)
whatisit(filename)
whatisit(nonexist)
whatisit(nonexist, existonly=True)
```


<a class="anchor" id="deconstructing-paths"></a>
### Deconstructing paths


If you are only interested in the directory or file component of a path then
the `os.path` module has the `dirname`, `basename`, and `split` functions.


```
path = '/path/to/my/image.nii'

print('Directory name:           {}'.format(op.dirname( path)))
print('Base name:                {}'.format(op.basename(path)))
print('Directory and base names: {}'.format(op.split(   path)))
```


> Note here that `op.split` returns both the directory and base names - it is
> super easy to define a Python function that returns multiple values, simply by
> having it return a tuple. For example, the implementation of `op.split` might
> look something like this:
>
>
> ```
> def mysplit(path):
>     dirname  = op.dirname(path)
>     basename = op.basename(path)
>
>     # It is not necessary to use round brackets here
>     # to denote the tuple - the return values will
>     # be implicitly grouped into a tuple for us.
>     return dirname, basename
> ```
>
>
> When calling a function which returns multiple values, you can _unpack_ those
> values in a single statement like so:
>
>
> ```
> dirname, basename = mysplit(path)
>
> print('Directory name: {}'.format(dirname))
> print('Base name:      {}'.format(basename))
> ```


If you want to extract the prefix or suffix of a file, you can use `splitext`:


```
prefix, suffix = op.splitext('image.nii')

print('Prefix: {}'.format(prefix))
print('Suffix: {}'.format(suffix))
```


> Double-barrelled file suffixes (e.g. `.nii.gz`) are the work of the devil.
> Correct handling of them is an open problem in Computer Science, and is
> considered by many to be unsolvable.  For `imglob`, `imcp`, and `immv`-like
> functionality, check out the `fsl.utils.path` and `fsl.utils.imcp` modules,
> part of the [`fslpy` project](https://pypi.python.org/pypi/fslpy).


<a class="anchor" id="absolute-and-relative-paths"></a>
### Absolute and relative paths


The `os.path` module has three useful functions for converting between
absolute and relative paths. The `op.abspath` and `op.relpath` functions will
respectively turn the provided path into an equivalent absolute or relative
path.


```
path = op.abspath('relative/path/to/some/file.txt')

print('Absolutised: {}'.format(path))
print('Relativised: {}'.format(op.relpath(path)))
```


By default, the `op.abspath` and `op.relpath` functions work relative to the
current working directory. The `op.relpath` function allows you to specify a
different directory to work from, and another function - `op.normpath` -
allows you create absolute paths with a different starting
point. `op.normpath` will take care of removing duplicate back-slashes,
and resolving references to `"."` and `".."`:


```
path = 'relative/path/to/some/file.txt'
root = '/vols/Data/'
abspath = op.normpath(op.join(root, path))

print('Absolute path: {}'.format(abspath))
print('Relative path: {}'.format(op.relpath(abspath, root)))
```


<a class="anchor" id="wildcard-matching-aka-globbing"></a>
### Wildcard matching a.k.a. globbing


The `glob` module has a function, also called `glob`, which allows you to find
files, based on unix-style wildcard pattern matching.


```
import glob

root = 'raw_mri_data'

# find all niftis for subject 1
images = glob.glob(op.join(root, 'subj_1', '*.nii*'))

print('Subject #1 images:')
print('\n'.join(['  {}'.format(i) for i in images]))

# find all subject directories
subjdirs = glob.glob(op.join(root, 'subj_*'))

print('Subject directories:')
print('\n'.join(['  {}'.format(d) for d in subjdirs]))
```


As with [`os.walk`](walking-a-directory-tree), the order of the results
returned by `glob.glob` is arbitrary. Unfortunately the undergraduate who
acquired this specific data set did not think to use zero-padded subject IDs
(you'll be pleased to know that this student was immediately kicked out of his
college and banned from ever returning), so we can't simply sort the paths
alphabetically. Instead, let's use some trickery to sort the subject
directories numerically by ID:


Let's define a function which, given a subject directory, returns the numeric
subject ID:


```
def get_subject_id(subjdir):

    # Remove any leading directories (e.g. "raw_mri_data/")
    subjdir = op.basename(subjdir)

    # Split "subj_[id]" into two words
    prefix, sid = subjdir.split('_')

    # return the subject ID as an integer
    return int(sid)
```


This function works like so:


```
print(get_subject_id('raw_mri_data/subj_9'))
```


Now that we have this function, we can sort the directories in one line of
code, via the built-in
[`sorted`](https://docs.python.org/3.5/library/functions.html#sorted)
function.  The directories will be sorted according to the `key` function that
we specify, which provides a mapping from each directory to a sortable
&quot;key&quot;:


```
subjdirs = sorted(subjdirs, key=get_subject_id)
print('Subject directories, sorted by ID:')
print('\n'.join(['  {}'.format(d) for d in subjdirs]))
```

As of Python 3.5, `glob.glob` also supports recursive pattern matching via the
`recursive` flag. Let's say we want a list of all resting-state scans in our
data set:


```
rscans = glob.glob('raw_mri_data/**/rest.nii.gz', recursive=True)

print('Resting state scans:')
print('\n'.join(rscans))
```


Internally, the `glob` module uses the `fnmatch` module, which implements the
pattern matching logic.

* If you are searching your file system for files and directory, use
  `glob.glob`.

* But if you already have a set of paths, you can use the `fnmatch.fnmatch`
  and `fnmatch.filter` functions to identify which paths match your pattern.


For example, let's retrieve all images that are in our data set:

```
allimages = glob.glob(op.join('raw_mri_data', '**', '*.nii*'), recursive=True)
print('All images in experiment:')

# Let's just print the first and last few
print('\n'.join(['  {}'.format(i) for i in allimages[:3]]))
print('  .')
print('  .')
print('  .')
print('\n'.join(['  {}'.format(i) for i in allimages[-3:]]))
```


Now let's reduce that list to only those images which are uncompressed:


```
import fnmatch

# filter a list of images
uncompressed = fnmatch.filter(allimages, '*.nii')
print('All uncompressed images:')
print('\n'.join(['  {}'.format(i) for i in uncompressed]))
```


And further reduce the list by identifying which of these images are T1 scans,
and are from our fictional patient group, made up of subjects 1, 4, 7, 8, and
9:


```
patients = [1, 4, 7, 8, 9]

print('All uncompressed T1 images from patient group:')
for filename in uncompressed:

    fullfile = filename
    dirname, filename = op.split(fullfile)
    subjid = get_subject_id(dirname)

    if subjid in patients and fnmatch.fnmatch(filename, 't1.*'):
        print('  {}'.format(fullfile))
```


<a class="anchor" id="expanding-the-home-directory-and-environment-variables"></a>
### Expanding the home directory and environment variables


You have [already been
introduced](#querying-and-changing-the-current-directory) to the
`op.expanduser` function. Another handy function  is the `op.expandvars` function.
which will expand expand any environment variables in a path:


```
print(op.expanduser('~'))
print(op.expandvars('$HOME'))
```


<a class="anchor" id="cross-platform-compatbility"></a>
### Cross-platform compatibility


If you are the type of person who likes running code on both Windows and Unix
machines, you will be delighted to learn that the `os`  module has a couple
of useful attributes:


 - `os.sep` contains the separator character that is used in file paths on
   your platform (i.e. &#47; on Unix, &#92; on Windows).
 - `os.pathsep` contains the separator character that is used when creating
   path lists (e.g. on your `$PATH`  environment variable - &#58; on Unix,
   and &#58; on Windows).


You will also find the `op.join` function handy. Given a set of directory
and/or file names, it will construct a path suited to the platform that you
are running on:


```
path = op.join('home', 'fsluser', '.bash_profile')

# if you are on Unix, you will get 'home/fsluser/.bash_profile'.
# On windows, you will get 'home\\fsluser\\.bash_profile'
print(path)

# Tn create an absolute path from
# the file system root, use os.sep:
print(op.join(op.sep, 'home', 'fsluser', '.bash_profile'))
```


<a class="anchor" id="exercises"></a>
## Exercises


<a class="anchor" id="re-name-subject-directories"></a>
### Re-name subject directories


Write a function which can rename the subject directories in `raw_mri_data` so
that the subject IDs are padded with zeros, and thus will be able to be sorted
alphabetically. This function:


  - Should accept the path to the parent directory of the data set
    (`raw_mri_data` in this case).
  - Should be able to handle any number of subjects
    > Hint: `numpy.log10`

  - May assume that the subject directory names follow the pattern
    `subj_[id]`, where `[id]` is the integer subject ID.


<a class="anchor" id="re-organise-a-data-set"></a>
### Re-organise a data set


Write a function which can be used to separate the data for each group
(patients: 1, 4, 7, 8, 9, and controls: 2, 3, 5, 6, 10) into sub-directories
`CON` and `PAT`.

This function should work with any number of groups, and should accept three
parameters:

 - The root directory of the data set (e.g. `raw_mri_data`).
 - A list of strings, the labels for each group.
 - A list of lists, with each list containing the subject IDs for one group.


<a class="anchor" id="re-name-subject-files"></a>
### Re-name subject files


Write a function which, given a subject directory, renames all of the image
files for this subject so that they are prefixed with `[group]_subj_[id]`,
where `[group]` is either `CON` or `PAT`, and `[id]` is the (zero-padded)
subject ID.


This function should accept the following parameters:
 - The subject directory
 - The subject group


**Bonus 1** Make your function work with both `.nii` and `.nii.gz` files.

**Bonus 2** If you completed [the previous exercise](#re-organise-a-data-set),
write a second function which accepts the data set directory as a sole
parameter, and then calls the first function for every subject.


<a class="anchor" id="compress-all-uncompressed-images"></a>
### Compress all uncompressed images


Write a function which recursively scans a directory, and replaces all `.nii`
files with `.nii.gz` files, using the built-in
[`gzip`](https://docs.python.org/3.5/library/gzip.html) library to perform
the compression.


<a class="anchor" id="write-your-own-os-path-splitext"></a>
### Write your own `os.path.splitext`


Write an implementation of `os.path.splitext` which works with compressed or
uncompressed NIFTI images.


> Hint: you know what suffixes to expect!


<a class="anchor" id="write-a-function-to-return-a-specific-image-file"></a>
### Write a function to return a specific image file


Assuming that you have completed the previous exercises, and re-organised
`raw_mri_data` so that it has the structure:

  `raw_mri_data/[group]/subj_[id]/[group]_subj_[id]_[modality].nii.gz`

write a function which is given:

 - the data set directory
 - a group label
 - integer ubject ID
 - modality (`'t1'`, `'t2'`, `'task'`, `'rest'`)

and which returns the fully resolved path to the relevant image file.

 > Hint: Python has [regular
   expressions](https://docs.python.org/3.5/library/re.html) - you might want
   to use one to cope with zero-padding.

**Bonus** Modify the function so the group label does not need to be passed in.


<a class="anchor" id="solutions"></a>
### Solutions


Use the `print_solution` function, defined below, to print the solution for a
specific exercise.


```
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import IPython

# Pass the title of the exercise you
# are interested to this function
def print_solution(extitle):
    solfile = ''.join([c.lower() if c.isalnum() else '_' for c in extitle])
    solfile = op.join('.solutions', '{}.py'.format(solfile))

    if not op.exists(solfile):
        print('Can\'t find solution to exercise "{}"'.format(extitle))
        return

    with open(solfile, 'rt') as f:
        code = f.read()

    formatter = HtmlFormatter()
    return IPython.display.HTML('<style type="text/css">{}</style>{}'.format(
        formatter.get_style_defs('.highlight'),
        highlight(code, PythonLexer(), formatter)))
```
