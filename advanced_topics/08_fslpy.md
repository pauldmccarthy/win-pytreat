# `fslpy`


[`fslpy`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/) is a
Python library which is built into FSL, and contains a range of functionality
for working with neuroimaging data from Python.


This practical highlights some of the most useful features provided by
`fslpy`. You may find `fslpy` useful if you are writing Python code to
perform analyses and image processing in conjunction with FSL.


> **Note**: `fslpy` is distinct from `fslpython` - `fslpython` is the Python
> environment that is baked into FSL. `fslpy` is a Python library which is
> installed into the `fslpython` environment.


* [The `Image` class, and other data types](#the-image-class-and-other-data-types)
  * [Creating images](#creating-images)
  * [Working with image data](#working-with-image-data)
  * [Loading other file types](#loading-other-file-types)
* [FSL atlases](#fsl-atlases)
* [The `filetree`](#the-filetree)
* [Image processing](#image-processing)
* [FSL wrapper functions](#fsl-wrapper-functions)
* [NIfTI coordinate systems](#nifti-coordinate-systems)


<a class="anchor" id="the-image-class-and-other-data-types"></a>
## The `Image` class, and other data types


The
[`fsl.data.image`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.image.html#fsl.data.image.Image)
module provides the `Image` class, which sits on top of `nibabel` and contains
some handy functionality if you need to work with coordinate transformations,
or do some FSL-specific processing. The `Image` class provides features such
as:

- Support for NIFTI1, NIFTI2, and ANALYZE image files
- Access to affine transformations between the voxel, FSL and world coordinate
  systems
- Ability to load metadata from BIDS sidecar files


Some simple image processing routines are also provided - these are covered
[below](#image-processing).


<a class="anchor" id="creating-images"></a>
### Creating images


It's easy to create an `Image` - you can create one from a file name:


```
import os.path as op
from fsl.data.image import Image

stddir = op.expandvars('${FSLDIR}/data/standard/')

# load a FSL image - the file
# suffix is optional, just like
# in real FSL-land!
img = Image(op.join(stddir, 'MNI152_T1_1mm'))
print(img)
```


You can create an `Image` from an existing `nibabel` image:


```
import nibabel as nib

# load a nibabel image, and
# convert it into an FSL image
nibimg = nib.load(op.join(stddir, 'MNI152_T1_1mm.nii.gz'))
img    = Image(nibimg)
```


Or you can create an `Image` from a `numpy` array:


```
import numpy as np

data = np.zeros((100, 100, 100))
img = Image(data, xform=np.eye(4))
```

You can save an image to file via the `save` method:


```
img.save('empty.nii.gz')
```


`Image` objects have all of the attributes you might expect:


```
stddir = op.expandvars('${FSLDIR}/data/standard/')
std1mm = Image(op.join(stddir, 'MNI152_T1_1mm'))

print('name:         ', std1mm.name)
print('file:         ', std1mm.dataSource)
print('NIfTI version:', std1mm.niftiVersion)
print('ndim:         ', std1mm.ndim)
print('shape:        ', std1mm.shape)
print('dtype:        ', std1mm.dtype)
print('nvals:        ', std1mm.nvals)
print('pixdim:       ', std1mm.pixdim)
```


and a number of useful methods:


```
std2mm  = Image(op.join(stddir, 'MNI152_T1_2mm'))
mask2mm = Image(op.join(stddir, 'MNI152_T1_2mm_mask'))

print(std1mm.sameSpace(std2mm))
print(std2mm.sameSpace(mask2mm))
print(std2mm.getAffine('voxel', 'world'))
```


An `Image` object is a high-level wrapper around a `nibabel` image object -
you can always work directly with the `nibabel` object via the `nibImage`
attribute:


```
print(std2mm)
print(std2mm.nibImage)
```


<a class="anchor" id="working-with-image-data"></a>
### Working with image data


You can get the image data as a `numpy` array via the `data` attribute:


```
data = std2mm.data
print(data.min, data.max())
```

> Note that this will give you the data in its underlying type, unlike the
> `nibabel.get_fdata` method, which up-casts image data to floating-point.


You can also read and write data directly via the `Image` object:


```
slc = std2mm[:, :, 45]
std2mm[0:10, :, :] = 0
```


Doing so has some advantages that may or may not be useful, depending on your
use-case:
 - The image data will be kept on disk - only the parts that you access will
   be loaded into RAM (you will also need to pass`loadData=False` when creating
   the `Image` to achieve this).
 - The `Image` object will keep track of modifications to the data - this can
   be queried via the `saveState` attribute.


<a class="anchor" id="loading-other-file-types"></a>
### Loading other file types


The
[`fsl.data`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.html#module-fsl.data)
package has a number of other classes for working with different types of FSL
and neuroimaging data. Most of these are higher-level wrappers around the
corresponding `nibabel` types:

* The
  [`fsl.data.bitmap.Bitmap`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.bitmap.html)
  class can be used to load a bitmap image (e.g. `jpg, `png`, etc) and
  convert it to a NIfTI image.
* The
  [`fsl.data.dicom.DicomImage`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.dicom.html)
  class uses `dcm2niix` to load NIfTI images contained within a DICOM
  directory<sup>*</sup>.
* The
  [`fsl.data.mghimahe.MGHImage`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.mghimage.html)
  class can be used too load `.mgh`/`.mgz` images (they are converted into
  NIfTI images).
* The
  [`fsl.data.dtifit`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.dtifit.html)
  module contains functions for loading and working with the output of the
  FSL `dtifit` tool.
* The
  [`fsl.data.featanalysis`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.featanalysis.html),
  [`fsl.data.featimage`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.featimage.html),
  and
  [`fsl.data.featdesign`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.featdesign.html)
  modules contain classes and functions for loading data from FEAT
  directories.
* Similarly, the
  [`fsl.data.melodicanalysis`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.melodicanalysis.html)
  and
  [`fsl.data.melodicimage`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.melodicimage.html)
  modules contain classes and functions for loading data from MELODIC
  directories.
* The
  [`fsl.data.gifti`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.gifti.html),
  [`fsl.data.freesurfer`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.freesurfer.html),
  and
  [`fsl.data.vtk`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.vtk.html)
  modules contain functionality form loading surface data from GIfTI,
  freesurfer, and VTK files respectively.


> <sup>*</sup>You must make sure that `dcm2niix` is installed on your system
> in order to use this class.


<a class="anchor" id="fsl-atlases"></a>
## FSL atlases


The
[`fsl.data.atlases`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.atlases.html)
module provides access to all of the atlas images that are stored in the
`$FSLDIR/data/atlases/` directory of a standard FSL installation. It can be
used to load and query probabilistic and label-based atlases.


The `atlases` module needs to be initialised using the `rescanAtlases` function:


```
import fsl.data.atlases as atlases
atlases.rescanAtlases()
```


You can list all of the available atlases using `listAtlases`:


```
for desc in atlases.listAtlases():
    print(desc)
```


`listAtlases` returns a list of `AtlasDescription` objects, each of which
contains descriptive information about one atlas. You can retrieve the
`AtlasDescription` for a specific atlas via the `getAtlasDescription`
function:


```
desc = atlases.getAtlasDescription('harvardoxford-cortical')
print(desc.name)
print(desc.atlasID)
print(desc.specPath)
print(desc.atlasType)
```


Each `AtlasDescription` maintains a list of `AtlasLabel` objects, each of
which represents one region that is defined in the atlas. You can access all
of the `AtlasLabel` objects via the `labels` attribute:


```
for lbl in desc.labels[:5]:
    print(lbl)
```


Or you can retrieve a specific label using the `find` method:


```
# search by region name
print(desc.find(name='Occipital Pole'))

# or by label value
print(desc.find(value=48))
```


The `loadAtlas` function can be used to load the atlas image:


```
# For probabilistic atlases, you
# can ask for the 3D ROI image
# by setting loadSummary=True.
# You can also request a
# resolution - by default the
# highest resolution version
# will be loaded.
lblatlas = atlases.loadAtlas('harvardoxford-cortical',
                             loadSummary=True,
                             resolution=2)

# By default you will get the 4D
# probabilistic atlas image (for
# atlases for which this is
# available).
probatlas = atlases.loadAtlas('harvardoxford-cortical',
                              resolution=2)

print(lblatlas)
print(probatlas)
```


`LabelAtlas` objects have a method called `label`, which can be used to
interrogate the atlas at specific locations:


```
# The label method accepts 3D
# voxel or world coordinates
val = lblatlas.label((25, 52, 43), voxel=True)
lbl = lblatlas.find(value=val)
print('Region at voxel [25, 52, 43]: {} [{}]'.format(val, lbl.name))


# or a 3D weighted or binary mask
mask = np.zeros(lblatlas.shape)
mask[30:60, 30:60, 30:60] = 1
mask = Image(mask, header=lblatlas.header)

lbls, props = lblatlas.label(mask)
print('Labels in mask:')
for lbl, prop in zip(lbls, props):
    lblname = lblatlas.find(value=lbl).name
    print('  {} [{}]: {:0.2f}%'.format(lbl, lblname, prop))
```


`ProbabilisticAtlas` objects have an analogous method called `values`:


```
vals = probatlas.values((25, 52, 43), voxel=True)
print('Regions at voxel [25, 52, 43]:')
for idx, val in enumerate(vals):
    if val > 0:
        lbl = probatlas.find(index=idx)
        print('  {} [{}]: {:0.2f}%'.format(lbl.value, lbl.name, val))

print('Average proportions of regions within mask:')
vals = probatlas.values(mask)
for idx, val in enumerate(vals):
    if val > 0:
        lbl = probatlas.find(index=idx)
        print('  {} [{}]: {:0.2f}%'.format(lbl.value, lbl.name, val))
```


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
