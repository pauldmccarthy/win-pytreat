# `fslpy`

`fslpy` is a Python library which is built into FSL, and contains a range of
functionality for working with neuroimaging data in an FSL context.

This practical highlights some of the most useful features provided by
`fslpy`. You may find `fslpy` useful if you are writing Python code to
perform analyses and image processing in conjunction with FSL.


> **Note**: `fslpy` is distinct from `fslpython` - `fslpython` is the Python
> environment that is baked into FSL. `fslpy` is a Python library which is
> installed into the `fslpython` environment.


* [The `Image` class, and other data types](#the-image-class-and-other-data-types)
* [FSL atlases](#fsl-atlases)
* [The `filetree`](#the-filetree)
* [NIfTI coordinate systems](#nifti-coordinate-systems)
* [Image processing](#image-processing)
* [FSL wrapper functions](#fsl-wrapper-functions)


<a class="anchor" id="the-image-class-and-other-data-types"></a>
## The `Image` class, and other data types


The `fsl.data.image` module provides the `Image` class, which sits on top of
`nibabel` and contains some handy functionality if you need to work with
coordinate transformations, or do some FSL-specific processing. The `Image`
class provides features such as:

- Support for NIFTI1, NIFTI2, and ANALYZE image files
- Access to affine transformations between the voxel, FSL and world coordinate
  systems
- Ability to load metadata from BIDS sidecar files

Some simple image processing routines are also provided - these are covered
[below](#image-processing).


### Creating images

It's easy to create an `Image` - you can create one from a file name:

```
from fsl.data.image import Image
stddir = op.expandvars('${FSLDIR}/data/standard/')

# load a FSL image - the file
# suffix is optional, just like
# in real FSL-land!
img = Image(op.join(stddir, 'MNI152_T1_1mm'))
```

You can crearte an `Image` from an existing `nibabel` image:

```
# load a nibabel image, and
# convert it into an FSL image
nibimg = nib.load(op.join(stddir, 'MNI152_T1_1mm.nii.gz'))
img    = Image(nibimg)
``

Or you can create an `Image` from a `numpy` array:

```
data = np.zeros((100, 100, 100))
img = Image(data, xform=np.eye(4))
```





<a class="anchor" id="fsl-atlases"></a>
## FSL atlases

<a class="anchor" id="the-filetree"></a>
## The `filetree`

<a class="anchor" id="nifti-coordinate-systems"></a>
## NIfTI coordinate systems

<a class="anchor" id="image-processing"></a>
## Image processing

<a class="anchor" id="fsl-wrapper-functions"></a>
## FSL wrapper functions



<a class="anchor" id="nifti-coordinate-systems"></a>
## NIfTI coordinate systems



The `getAffine` method gives you access to affine transformations which can be
used to convert coordinates between the different coordinate systems
associated with an image. Have some MNI coordinates you'd like to convert to
voxels? Easy!

```
mnicoords = np.array([[0,   0,  0],
                      [0, -18, 18]])

world2vox = img.getAffine('world', 'voxel')
vox2world = img.getAffine('voxel', 'world')

# Apply the world->voxel
# affine to the coordinates
voxcoords = (np.dot(world2vox[:3, :3], mnicoords.T)).T + world2vox[:3, 3]

# The code above is a bit fiddly, so
# instead of figuring it out, you can
# just use the transform() function:
from fsl.transform.affine import transform
voxcoords = transform(mnicoords, world2vox)

# just to double check, let's transform
# those voxel coordinates back into world
# coordinates
backtomni = transform(voxcoords, vox2world)

for m, v, b in zip(mnicoords, voxcoords, backtomni):
    print(m, '->', v, '->', b)
```

> The `Image.getAffine` method can give you transformation matrices
> between any of these coordinate systems:
>
>  - `'voxel'`: Image data voxel coordinates
>  - `'world'`: mm coordinates, defined by the sform/qform of an image
>  - `'fsl'`: The FSL coordinate system, used internally by many FSL tools
>    (e.g. FLIRT)



Oh, that example was too easy I hear you say? Try this one on for size. Let's
say we have run FEAT on some task fMRI data, and want to get the MNI
coordinates of the voxel with peak activation.

> This is what people used to use `Featquery` for, back in the un-enlightened
> days.


Let's start by identifying the voxel with the biggest t-statistic:

```
featdir = op.join(op.join('05_nifti', 'fmri.feat'))

# The Image.data attribute returns a
# numpy array containing, well, the
# image data.
tstat1 = Image(op.join(featdir, 'stats', 'tstat1')).data

# Recall from the numpy practical that
# argmax gives us a 1D index into a
# flattened view of the array. We can
# use the unravel_index function to
# convert it into a 3D index.
peakvox = np.abs(tstat1).argmax()
peakvox = np.unravel_index(peakvox, tstat1.shape)
print('Peak voxel coordinates for tstat1:', peakvox, tstat1[peakvox])
```


Now that we've got the voxel coordinates in functional space, we need to
transform them into MNI space. FEAT provides a transformation which goes
directly from functional to standard space, in the `reg` directory:

```
func2std = np.loadtxt(op.join(featdir, 'reg', 'example_func2standard.mat'))
```

But ... wait a minute ... this is a FLIRT matrix! We can't just plug voxel
coordinates into a FLIRT matrix and expect to get sensible results, because
FLIRT works in an internal FSL coordinate system, which is not quite
`'voxel'`, and not quite `'world'`. So we need to do a little more work.
Let's start by loading our functional image, and the MNI152 template (the
source and reference images of our FLIRT matrix):

```
func = Image(op.join(featdir, 'reg', 'example_func'))
std  = Image(op.expandvars(op.join('$FSLDIR', 'data', 'standard', 'MNI152_T1_2mm')))
```


Now we can use them to get affines which convert between all of the different
coordinate systems - we're going to combine them into a single uber-affine,
which transforms our functional-space voxels into MNI world coordinates via:

   1. functional voxels -> FLIRT source space
   2. FLIRT source space -> FLIRT reference space
   3. FLIRT referece space -> MNI world coordinates


```
vox2fsl = func.getAffine('voxel', 'fsl')
fsl2mni = std .getAffine('fsl',   'world')
```

Combining two affines into one is just a simple dot-product. There is a
`concat()` function which does this for us, for any number of affines:

```
from fsl.transform.affine import concat

# To combine affines together, we
# have to list them in reverse -
# linear algebra is *weird*.
funcvox2mni = concat(fsl2mni, func2std, vox2fsl)
```

So we've now got some voxel coordinates from our functional data, and an affine
to transform into MNI world coordinates. The rest is easy:

```
mnicoords = transform(peakvox, funcvox2mni)
print('Peak activation (MNI coordinates):', mnicoords)
```


> Note that in the above example we are only applying a linear transformation
> into MNI space - in reality you would also want to apply your non-linear
> structural-to-standard transformation too. But this is left as an exercise
> for the reader ;).


<a class="anchor" id="image-processing"></a>
## Image processing

Now, it's all well and good to look at t-statistric values and voxel
coordinates and so on and so forth, but let's spice things up a bit and look
at some images. Let's display our peak activation location in MNI space. To
do this, we're going to resample our functional image into

```
from IPython.display import Image as Screenshot
!fsleyes render -of screenshot.png -std
```


### (Advanced) Transform coordinates with nonlinear warpfields


have to use your own dataset
