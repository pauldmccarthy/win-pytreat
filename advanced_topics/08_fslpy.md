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
  * [NIfTI coordinate systems](#nifti-coordinate-systems)
  * [Image processing](#image-processing)
* [The `filetree`](#the-filetree)
* [FSL wrapper functions](#fsl-wrapper-functions)
* [FSL atlases](#fsl-atlases)
  * [Querying atlases](#querying-atlases)
  * [Loading atlas images](#loading-atlas-images)
  * [Working with atlases](#working-with-atlases)


Let's start with some standard imports and environment set-up:


```
%matplotlib inline
import matplotlib.pyplot as plt
import os
import os.path as op
import nibabel as nib
import numpy as np
import warnings
warnings.filterwarnings("ignore")
```


And a little function that we can use to generate a simple orthographic plot:


```
def ortho(data, voxel, fig=None, **kwargs):
    """Simple orthographic plot of a 3D array using matplotlib.

    :arg data:  3D numpy array
    :arg voxel: XYZ coordinates for each slice
    :arg fig:   Existing figure and axes for overlay plotting

    All other arguments are passed through to the `imshow` function.

    :returns:   The figure and axes (which can be passed back in as the
                `fig` argument to plot overlays).
    """
    x, y, z = voxel
    xslice  = np.flipud(data[x, :, :].T)
    yslice  = np.flipud(data[:, y, :].T)
    zslice  = np.flipud(data[:, :, z].T)

    if fig is None:
        fig = plt.figure()
        xax = fig.add_subplot(1, 3, 1)
        yax = fig.add_subplot(1, 3, 2)
        zax = fig.add_subplot(1, 3, 3)
    else:
        fig, xax, yax, zax = fig

    xax.imshow(xslice, **kwargs)
    yax.imshow(yslice, **kwargs)
    zax.imshow(zslice, **kwargs)

    for ax in (xax, yax, zax):
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout(pad=0)

    return (fig, xax, yax, zax)
```


And another function which uses FSLeyes for more complex plots:


```
import shlex
import IPython.display as display
from fsleyes.render import main

def render(cmdline):
    prefix = '-of screenshot.png -hl -c 2 '
    main(shlex.split(prefix + cmdline))
    return display.Image('screenshot.png')
```


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
# load a nibabel image, and
# convert it into an FSL image
nibimg = nib.load(op.join(stddir, 'MNI152_T1_1mm.nii.gz'))
img    = Image(nibimg)
```


Or you can create an `Image` from a `numpy` array:


```
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
mask2mm = Image(op.join(stddir, 'MNI152_T1_2mm_brain_mask'))

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
print(data.min(), data.max())
```

> Note that this will give you the data in its underlying type, unlike the
> `nibabel.get_fdata` method, which up-casts image data to floating-point.


You can also read and write data directly via the `Image` object:


```
slc = std2mm[:, :, 45]
std2mm[0:10, :, :] *= 2
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


<a class="anchor" id="nifti-coordinate-systems"></a>
### NIfTI coordinate systems


The `Image.getAffine` method gives you access to affine transformations which
can be used to convert coordinates between the different coordinate systems
associated with a NIfTI image. Have some MNI coordinates you'd like to convert
to voxels? Easy!


```
stddir = op.expandvars('${FSLDIR}/data/standard/')
std2mm = Image(op.join(stddir, 'MNI152_T1_2mm'))

mnicoords = np.array([[0,   0,  0],
                      [0, -18, 18]])

world2vox = std2mm.getAffine('world', 'voxel')
vox2world = std2mm.getAffine('voxel', 'world')

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
featdir = op.join(op.join('08_fslpy', 'fmri.feat'))

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


So we've now got some voxel coordinates from our functional data, and an
affine to transform into MNI world coordinates. The rest is easy:


```
mnicoords = transform(peakvox, funcvox2mni)
mnivoxels = transform(mnicoords, std.getAffine('world', 'voxel'))
mnivoxels = [int(round(v)) for v in mnivoxels]
print('Peak activation (MNI coordinates):', mnicoords)
print('Peak activation (MNI voxels):     ', mnivoxels)
```


> Note that in the above example we are only applying a linear transformation
> into MNI space - in reality you would also want to apply your non-linear
> structural-to-standard transformation too. But this is left as [an exercise
> for the
> reader](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.transform.fnirt.html).


<a class="anchor" id="image-processing"></a>
### Image processing


Now, it's all well and good to look at t-statistic values and voxel
coordinates and so on and so forth, but let's spice things up a bit and look
at some images. Let's display our peak activation location in MNI space. To do
this, we're going to resample our functional image into MNI space, so we can
overlay it on the MNI template. This can be done using some handy functions
from the
[`fsl.utils.image.resample`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.image.resample.html)
module:


```
from fsl.transform.flirt import fromFlirt
from fsl.utils.image.resample import resampleToReference

featdir = op.join(op.join('08_fslpy', 'fmri.feat'))
tstat1  = Image(op.join(featdir, 'stats', 'tstat1'))
std     = Image(op.expandvars(op.join('$FSLDIR', 'data', 'standard', 'MNI152_T1_2mm')))

# Load the func2standard FLIRT matrix, and adjust it
# so that it transforms from functional *world*
# coordinates into standard *world* coordinates -
# this is what is expected by the resampleToReference
# function, used below
func2std = np.loadtxt(op.join(featdir, 'reg', 'example_func2standard.mat'))
func2std = fromFlirt(func2std, tstat1, std, 'world', 'world')

# All of the functions in the resample module
# return a numpy array containing the resampled
# data, and an adjusted voxel-to-world affine
# transformation. But when using the
# resampleToReference function, the affine will
# be the same as the MNI152 2mm affine, so we
# can ignore it.
std_tstat1 = resampleToReference(tstat1, std, func2std)[0]
std_tstat1 = Image(std_tstat1, header=std.header)
```


Now that we have our t-statistic image in MNI152 space, we can plot it in
standard space using `matplotlib`:


```
stddir = op.expandvars('${FSLDIR}/data/standard/')
std2mm = Image(op.join(stddir, 'MNI152_T1_2mm'))

std_tstat1 = std_tstat1.data
std_tstat1 = np.ma.masked_where(std_tstat1 < 3, std_tstat1)

fig = ortho(std2mm,     mnivoxels, cmap=plt.cm.gray)
fig = ortho(std_tstat1, mnivoxels, cmap=plt.cm.inferno, fig=fig)
```


There are a few other useful functions tucked away in the
[fsl.utils.image](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.image.html)
package, with more to be added in the future. The [`fsl.transform`]() package
also contains a wealth of functionality for working with linear (FLIRT) and
non-linear (FNIRT) transformations.


<a class="anchor" id="the-filetree"></a>
## The `filetree`


<a class="anchor" id="fsl-wrapper-functions"></a>
## FSL wrapper functions


The
[fsl.wrappers](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.wrappers.html)
package is the home of "wrapper" functions for a range of FSL tools. You can
use them to call an FSL tool from Python code, without having to worry about
constructing a command-line, or saving/loading input/output images.


You can use the FSL wrapper functions with file names:

```
from fsl.wrappers import bet, robustfov, LOAD
os.chdir('08_fslpy')
robustfov('bighead', 'bighead_cropped')
render('bighead bighead_cropped -cm blue')
```

Or, if you have images in memory, you can pass the `Image` objects in,
and have the results automatically loaded in too:

```
cropped = Image('bighead_cropped')
betted = bet(cropped, LOAD)['output']

fig = ortho(cropped, (80, 112, 85))
fig = ortho(betted,  (80, 112, 85), fig=fig, cmap=plt.cm.inferno)
```


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


<a class="anchor" id="querying-atlases"></a>
### Querying atlases


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


<a class="anchor" id="loading-atlas-images"></a>
### Loading atlas images


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


<a class="anchor" id="working-with-atlases"></a>
### Working with atlases


Both `LabelAtlas` and `ProbabilisticAtlas` objects have a method called `get`,
which can be used to extract ROI images for a specific region:


```
stddir = op.expandvars('${FSLDIR}/data/standard/')
std2mm = Image(op.join(stddir, 'MNI152_T1_2mm'))

frontal = lblatlas.get(name='Frontal Pole').data
frontal = np.ma.masked_where(frontal < 1, frontal)

fig = ortho(std2mm,  (45, 54, 45), cmap=plt.cm.gray)
fig = ortho(frontal, (45, 54, 45), cmap=plt.cm.winter, fig=fig)
```


Calling `get` on a :meth:`ProbabilisticAtlas` will return a probability image:


```
stddir = op.expandvars('${FSLDIR}/data/standard/')
std2mm = Image(op.join(stddir, 'MNI152_T1_2mm'))

frontal = probatlas.get(name='Frontal Pole')
frontal = np.ma.masked_where(frontal < 1, frontal)

fig = ortho(std2mm,  (45, 54, 45), cmap=plt.cm.gray)
fig = ortho(frontal, (45, 54, 45), cmap=plt.cm.inferno, fig=fig)
```


The `get` method can be used to retrieve an image for a region by:
- an `AtlasLabel` object
- The region index
- The region value
- The region name


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
