# NIfTI images and python

The [`nibabel`](http://nipy.org/nibabel/) module is used to read and write NIfTI
images and also some other medical imaging formats (e.g., ANALYZE, GIFTI,
MINC, MGH).  `nibabel` is included within the FSL python environment.


Building upon `nibabel`, the
[`fslpy`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/) library
contains a number of FSL-specific classes and functions which you may find
useful. But let's start with `nibabel` - `fslpy` is introduced in a different
practical (`advanced_topics/08_fslpy.ipynb`).


## Contents

* [Reading images](#reading-images)
* [Header info](#header-info)
 * [Voxel sizes](#voxel-sizes)
 * [Coordinate orientations and mappings](#orientation-info)
* [Writing images](#writing-images)
* [Exercise](#exercise)

---

<a class="anchor" id="reading-images"></a>
## Reading images

It is easy to read an image:

```
import numpy as np
import nibabel as nib
import os.path as op
filename =  op.expandvars('${FSLDIR}/data/standard/MNI152_T1_1mm.nii.gz')
imobj = nib.load(filename, mmap=False)

# display header object
imhdr = imobj.header

# extract data (as a numpy array)
imdat = imobj.get_fdata()
print(imdat.shape)
```

> Make sure you use the full filename, including the `.nii.gz` extension.
> `fslpy` provides FSL-like automatic file suffix detection though.

> We use the `expandvars()` function above to insert the FSLDIR
> environmental variable into our string. This function is
> discussed more fully in the file management practical.

Reading the data off the disk is not done until `get_fdata()` is called.

> Pitfall:
>
> The option `mmap=False` disables memory mapping, which would otherwise be
> invoked for uncompressed NIfTI files but not for compressed files. Since
> some functionality behaves differently on memory mapped objects, it is
> advisable to turn this off unless you specifically want it.

Once the data is read into a numpy array then it is easily manipulated.

> The `get_fdata` method will return floating point data, regardless of the
> underlying image data type. If you want the image data in the type that it
> is stored (e.g. integer ROI labels), then use
> `imdat = np.asanyarray(imobj.dataobj)` instead.

---

<a class="anchor" id="header-info"></a>
## Header info

There are many methods available on the header object - for example, look at
`dir(imhdr)` or `help(imhdr)` or the [nibabel webpage about NIfTI
images](http://nipy.org/nibabel/nifti_images.html)

<a class="anchor" id="voxel-sizes"></a>
### Voxel sizes

Dimensions of the voxels, in mm, can be found from:

```
voxsize = imhdr.get_zooms()
print(voxsize)
```

<a class="anchor" id="orientation-info"></a>
### Coordinate orientations and mappings

Information about the NIfTI qform and sform matrices can be extracted like this:

```
sform = imhdr.get_sform()
sformcode = imhdr['sform_code']
qform = imhdr.get_qform()
qformcode = imhdr['qform_code']
print(qformcode)
print(qform)
```

You can also get both code and matrix together like this:
```
affine, code = imhdr.get_qform(coded=True)
print(affine, code)
```


---

<a class="anchor" id="writing-images"></a>
## Writing images


If you have created a modified image by making or modifying a numpy array then
you need to put this into a NIfTI image object in order to save it to a file.
The easiest way to do this is to copy all the header info from an existing
image like this:

```
newdata = imdat * imdat
newhdr = imhdr.copy()
newobj = nib.nifti1.Nifti1Image(newdata, None, header=newhdr)
nib.save(newobj, "mynewname.nii.gz")
```

where `newdata` is the numpy array (the above is a random example only) and
`imhdr` is the existing image header (as above).

> It is possible to also just pass in an affine matrix rather than a
> copied header, but we *strongly* recommend against this if you are
> processing an existing image as otherwise you run the risk of
> swapping the left-right orientation.  Those that have used
> `save_avw` in matlab may well have been bitten in this way in the
> past.  Therefore, copy a header from one of the input images
> whenever possible, and just use the affine matrix option if you are
> creating an entirely separate image, like a simulation.

If the voxel size of the image is different, then extra modifications will be
required.  Take a look at the `fslpy` practical for some extra image
manipulation options, including cropping and resampling
(`advanced_topics/08_fslpy.ipynb`).

---


<a class="anchor" id="exercises"></a>
## Exercise


Write some code to read in a 4D fMRI image (you can find one
[here](http://www.fmrib.ox.ac.uk/~mark/files/av.nii.gz) if you don't have one
handy), calculate the tSNR and then save the 3D result.

> The tSNR of a time series signal is simply its mean divided by its standard
> deviation.

```
# Calculate tSNR
```
