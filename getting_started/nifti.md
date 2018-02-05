# NIfTI images and python

The [nibabel](http://nipy.org/nibabel/) module is used to read and write NIfTI images and also some other medical imaging formats (e.g., ANALYZE, GIFTI, MINC, MGH).  This module is included within the FSL python environment.

## Reading images

It is easy to read an image:

```
import numpy as np
import nibabel as nib
filename = '/usr/local/fsl/data/standard/MNI152_T1_1mm.nii.gz'
imobj = nib.load(filename, mmap=False)
# display header object
imhdr = imobj.header
# extract data (as an numpy array)
imdat = imobj.get_data().astype(float)
print(imdat.shape)
```

> Make sure you use the full filename, including the .nii.gz extension.

Reading the data off the disk is not done until `get_data()` is called.

> Pitfall:
>
> The option `mmap=False`is necessary as turns off memory mapping, which otherwise would be invoked for uncompressed NIfTI files but not for compressed files. Since some functionality behaves differently on memory mapped objects, it is advisable to turn this off.

Once the data is read into a numpy array then it is easily manipulated.

> We recommend converting it to float at the start to avoid problems with integer arithmetic and overflow, though this is not compulsory.

## Header info

There are many methods available on the header object - for example, look at `dir(imhdr)` or `help(imhdr)` or the [nibabel webpage about NIfTI images](http://nipy.org/nibabel/nifti_images.html)

### Voxel sizes

Dimensions of the voxels, in mm, can be found from:

```
voxsize = imhdr.get_zooms()
print(voxsize)
```

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

## Writing images

If you have created a modified image by making or modifying a numpy array then you need to put this into a NIfTI image object in order to save it to a file.  The easiest way to do this is to copy all the header info from an existing image like this:

```
newdata = imdat * imdat
newhdr = imhdr.copy()
newobj = nib.nifti1.Nifti1Image(newdata, None, header=newhdr)
nib.save(newobj, "mynewname.nii.gz")
```
where `newdata` is the numpy array (the above is a random example only) and `imhdr` is the existing image header (as above).

If the dimensions of the image are different, then extra modifications will be required.  For this, or for making an image from scratch, see the [nibabel documentation](http://nipy.org/nibabel/nifti_images.html) on NIfTI images.



