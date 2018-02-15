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


### Compress all uncompressed images


Write a function which recursively scans a directory, and replaces all `.nii`
files with `.nii.gz` files, using the built-in
[`gzip`](https://docs.python.org/3.5/library/gzip.html) library to perform
the compression.


### Write your own `os.path.splitext`


Write an implementation of `os.path.splitext` which works with compressed or
uncompressed NIFTI images.


> Hint: you know what suffixes to expect!


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
