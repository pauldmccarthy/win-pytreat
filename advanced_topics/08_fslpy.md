# `fslpy`


**Important:** Portions of this practical require `fslpy` 2.9.0, due to be
released with FSL 6.0.4, in Spring 2020.


[`fslpy`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/) is a
Python library which is built into FSL, and contains a range of functionality
for working with FSL and with neuroimaging data from Python.


This practical highlights some of the most useful features provided by
`fslpy`. You may find `fslpy` useful if you are writing Python code to
perform analyses and image processing in conjunction with FSL.


* [The `Image` class, and other data types](#the-image-class-and-other-data-types)
  * [Creating images](#creating-images)
  * [Working with image data](#working-with-image-data)
  * [Loading other file types](#loading-other-file-types)
  * [NIfTI coordinate systems](#nifti-coordinate-systems)
  * [Transformations and resampling](#transformations-and-resampling)
* [FSL wrapper functions](#fsl-wrapper-functions)
  * [In-memory images](#in-memory-images)
  * [Loading outputs into Python](#loading-outputs-into-python)
  * [The `fslmaths` wrapper](#the-fslmaths-wrapper)
* [The `FileTree`](#the-filetree)
  * [Describing your data](#describing-your-data)
  * [Using the `FileTree`](#using-the-filetree)
  * [Building a processing pipeline with `FileTree`](#building-a-processing-pipeline-with-filetree)
  * [The `FileTreeQuery`](#the-filetreequery)
* [Calling shell commands](#calling-shell-commands)
  * [The `runfsl` function](#the-runfsl-function)
  * [Submitting to the cluster](#submitting-to-the-cluster)
  * [Redirecting output](#redirecting-output)
* [FSL atlases](#fsl-atlases)
  * [Querying atlases](#querying-atlases)
  * [Loading atlas images](#loading-atlas-images)
  * [Working with atlases](#working-with-atlases)


> **Note**: `fslpy` is distinct from `fslpython` - `fslpython` is the Python
> environment that is baked into FSL. `fslpy` is a Python library which is
> installed into the `fslpython` environment.


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
def ortho(data, voxel, fig=None, cursor=False, **kwargs):
    """Simple orthographic plot of a 3D array using matplotlib.

    :arg data:   3D numpy array
    :arg voxel:  XYZ coordinates for each slice
    :arg fig:    Existing figure and axes for overlay plotting
    :arg cursor: Show a cursor at the `voxel`

    All other arguments are passed through to the `imshow` function.

    :returns:   The figure and orthogaxes (which can be passed back in as the
                `fig` argument to plot overlays).
    """

    voxel = [int(round(v)) for v in voxel]

    data            = np.asanyarray(data, dtype=np.float)
    data[data <= 0] = np.nan

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

    if cursor:
        cargs = {'color' : (0, 1, 0), 'linewidth' : 1}
        xax.axvline(                y, **cargs)
        xax.axhline(data.shape[2] - z, **cargs)
        yax.axvline(                x, **cargs)
        yax.axhline(data.shape[2] - z, **cargs)
        zax.axvline(                x, **cargs)
        zax.axhline(data.shape[1] - y, **cargs)

    for ax in (xax, yax, zax):
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout(pad=0)

    return (fig, xax, yax, zax)
```


And another function which uses FSLeyes for more complex plots:


```
def render(cmdline):

    import shlex
    import IPython.display as display

    prefix = '-of screenshot.png -hl -c 2 '

    try:
        from fsleyes.render import main
        main(shlex.split(prefix + cmdline))

    except ImportError:
        # fall-back for macOS - we have to run
        # FSLeyes render in a separate process
        from fsl.utils.run import runfsl
        prefix = 'render ' + prefix
        runfsl(prefix + cmdline, env={})

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


> The `Image` class behaves differently to the `nibabel.Nifti1Image`. For
> example, when you create an `Image` object, the default behaviour is to load
> the image data into memory. This is configurable however; take a look at
> [the
> documentation](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.image.html#fsl.data.image.Image)
> to explore all of the options.


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
std1mm = Image(op.join(stddir, 'MNI152_T1_1mm'))
print(std1mm)
```


You can create an `Image` from an existing `nibabel` image:


```
# load a nibabel image, and
# convert it into an FSL image
nibimg = nib.load(op.join(stddir, 'MNI152_T1_1mm.nii.gz'))
std1mm = Image(nibimg)
```


Or you can create an `Image` from a `numpy` array:


```
data = np.zeros((182, 218, 182))
img = Image(data, xform=np.eye(4))
```

If you have generated some data from another `Image` (or from a
`nibabel.Nifti1Image`) you can use the `header` option to set
the header information on the new image:


```
img = Image(data, header=std1mm.header)
```


You can save an image to file via the `save` method:


```
img.save('empty')
!ls
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
ortho(data, (45, 54, 45))
```


> Note that `Image.data` will give you the data in its underlying type, unlike
> the `nibabel.get_fdata` method, which up-casts image data to floating-point.


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
  [`fsl.data.mghimage.MGHImage`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.data.mghimage.html)
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
  freesurfer, and ASCII VTK files respectively.


> <sup>*</sup>You must make sure that
> [`dcm2niix`](https://github.com/rordenlab/dcm2niix/) is installed on your
> system in order to use this class.


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
```


The code above is a bit fiddly, so instead of figuring it out, you can just
use the
[`affine.transform`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.transform.affine.html#fsl.transform.affine.transform)
function:


```
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
featdir = op.join('08_fslpy', 'fmri.feat')

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

> In the next section we will use the
> [`fsl.transform.flirt.fromFlirt`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.transform.flirt.html#fsl.transform.flirt.fromFlirt)
> function, which does all of the above for us.


So we've now got some voxel coordinates from our functional data, and an
affine to transform into MNI world coordinates. The rest is easy:


```
mnicoords = transform(peakvox, funcvox2mni)
mnivoxels = transform(mnicoords, std.getAffine('world', 'voxel'))
mnivoxels = [int(round(v)) for v in mnivoxels]
print('Peak activation (MNI coordinates):', mnicoords)
print('Peak activation (MNI voxels):     ', mnivoxels)
```


Note that in the above example we are only applying a linear transformation
into MNI space - in reality you would also want to apply your non-linear
structural-to-standard transformation too. This is covered in the next
section.


<a class="anchor" id="transformations-and-resampling"></a>
### Transformations and resampling


Now, it's all well and good to look at t-statistic values and voxel
coordinates and so on and so forth, but let's spice things up a bit and look
at some images. Let's display our peak activation location in MNI space. To do
this, we're going to resample our functional image into MNI space, so we can
overlay it on the MNI template. This can be done using some handy functions
from the
[`fsl.transform.flirt`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.transform.flirt.html)
and
[`fsl.utils.image.resample`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.image.resample.html)
modules.


Let's make sure we've got our source and reference images loaded:


```
featdir = op.join(op.join('08_fslpy', 'fmri.feat'))
tstat1  = Image(op.join(featdir, 'stats', 'tstat1'))
std     = Image(op.expandvars(op.join('$FSLDIR', 'data', 'standard', 'MNI152_T1_2mm')))
```


Now we'll load the `example_func2standard` FLIRT matrix, and adjust it so that
it transforms from functional *world* coordinates into standard *world*
coordinates - this is what is expected by the `resampleToReference` function,
used below:


```
from fsl.transform.flirt import fromFlirt

func2std = np.loadtxt(op.join(featdir, 'reg', 'example_func2standard.mat'))
func2std = fromFlirt(func2std, tstat1, std, 'world', 'world')
```


Now we can use `resampleToReference` to resample our functional data into
MNI152 space. This function returns a `numpy` array containing the resampled
data, and an adjusted voxel-to-world affine transformation. But in this case,
we know that the data will be aligned to MNI152, so we can ignore the affine:

```
from fsl.utils.image.resample import resampleToReference

std_tstat1 = resampleToReference(tstat1, std, func2std)[0]
std_tstat1 = Image(std_tstat1, header=std.header)
```


Now that we have our t-statistic image in MNI152 space, we can plot it in
standard space using `matplotlib`:


```
stddir = op.expandvars('${FSLDIR}/data/standard/')
std2mm = Image(op.join(stddir, 'MNI152_T1_2mm'))

std_tstat1                 = std_tstat1.data
std_tstat1[std_tstat1 < 3] = 0

fig = ortho(std2mm.data, mnivoxels, cmap=plt.cm.gray)
fig = ortho(std_tstat1,  mnivoxels, cmap=plt.cm.inferno, fig=fig, cursor=True)
```


In the example above, we resampled some data from functional space into
standard space using a linear transformation. But we all know that this is not
how things work in the real world - linear transformations are for kids. The
real world is full of lions and tigers and bears and warp fields.


The
[`fsl.transform.fnirt`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.transform.fnirt.html#fsl.transform.fnirt.fromFnirt)
and
[`fsl.transform.nonlinear`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.transform.nonlinear.html)
modules contain classes and functions for working with FNIRT-style warp fields
(modules for working with lions, tigers, and bears are still under
development).


Let's imagine that we have defined an ROI in MNI152 space, and we want to
project it into the space of our functional data.  We can do this by combining
the nonlinear structural to standard registration produced by FNIRT with the
linear functional to structural registration generated by FLIRT.  First of
all, we'll load images from each of the functional, structural, and standard
spaces:


```
featdir = op.join('08_fslpy', 'fmri.feat')
func    = Image(op.join(featdir, 'reg', 'example_func'))
struc   = Image(op.join(featdir, 'reg', 'highres'))
std     = Image(op.expandvars(op.join('$FSLDIR', 'data', 'standard', 'MNI152_T1_2mm')))
```


Now, let's say we have obtained our seed location in MNI152 coordinates. Let's
convert them to MNI152 voxels just to double check:


```
seedmni    = [-48, -74, -9]
seedmnivox = transform(seedmni, std.getAffine('world', 'voxel'))
ortho(std.data, seedmnivox, cursor=True)
```


Now we'll load the FNIRT warp field, which encodes a nonlinear transformation
from structural space to standard space. FNIRT warp fields are often stored as
*coefficient* fields to reduce the file size, but in order to use it, we must
convert the coefficient field into a *deformation* (a.k.a. *displacement*)
field. This takes a few seconds:


```
from fsl.transform.fnirt     import readFnirt
from fsl.transform.nonlinear import coefficientFieldToDeformationField

struc2std = readFnirt(op.join(featdir, 'reg', 'highres2standard_warp'), struc, std)
struc2std = coefficientFieldToDeformationField(struc2std)
```

We'll also load our FLIRT functional to structural transformation, adjust it
so that it transforms between voxel coordinate systems instead of the FSL
coordinate system, and invert so it can transform from structural voxels to
functional voxels:


```
from fsl.transform.affine import invert
func2struc = np.loadtxt(op.join(featdir, 'reg', 'example_func2highres.mat'))
func2struc = fromFlirt(func2struc, func, struc, 'voxel', 'voxel')
struc2func = invert(func2struc)
```


Now we can transform our seed coordinates from MNI152 space into functional
space in two stages. First, we'll use our deformation field to transform from
MNI152 space into structural space:


```
seedstruc = struc2std.transform([seedmni], 'world', 'voxel')[0]
seedfunc  = transform(seedstruc, struc2func)

print('Seed location in MNI coordinates:  ', seedmni)
print('Seed location in functional voxels:', seedfunc)
ortho(func.data, seedfunc, cursor=True)
```


> FNIRT warp fields kind of work backwards - we can use them to transform
> reference coordinates into source coordinates, but would need to invert the
> warp field using `invwarp` if we wanted to transform from source coordinates
> into referemce coordinates.


Of course, we can also use our deformation field to resample an image from
structural space into MNI152 space. The `applyDeformation` function takes an
`Image` and a `DeformationField`, and returns a `numpy` array containing the
resampled data.


```
from fsl.transform.nonlinear import applyDeformation

strucmni = applyDeformation(struc, struc2std)

# remove low-valued voxels,
# just for visualisation below
strucmni[strucmni < 1] = 0

fig = ortho(std.data, [45, 54, 45], cmap=plt.cm.gray)
fig = ortho(strucmni, [45, 54, 45], fig=fig)
```


The `premat` option to `applyDeformation` can be used to specify our linear
functional to structural transformation, and hence resample a functional image
into MNI152 space:


```
tstatmni = applyDeformation(tstat1, struc2std, premat=func2struc)
tstatmni[tstatmni < 3] = 0

fig = ortho(std.data, [45, 54, 45], cmap=plt.cm.gray)
fig = ortho(tstatmni, [45, 54, 45], fig=fig)
```


There are a few other useful functions tucked away in the
[`fsl.utils.image`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.image.html)
and
[`fsl.transform`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.transform.html)
packages, with more to be added in the future.


<a class="anchor" id="fsl-wrapper-functions"></a>
## FSL wrapper functions


The
[fsl.wrappers](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.wrappers.html)
package is the home of "wrapper" functions for a range of FSL tools. You can
use them to call an FSL tool from Python code, without having to worry about
constructing a command-line, or saving/loading input/output images.


> The `fsl.wrappers` functions also allow you to submit jobs to be run on the
> cluster - this is described [below](#submitting-to-the-cluster).


You can use the FSL wrapper functions with file names, similar to calling the
corresponding tool via the command-line:


```
from fsl.wrappers import bet, robustfov, LOAD

robustfov('08_fslpy/bighead', 'bighead_cropped')

render('08_fslpy/bighead bighead_cropped -cm blue')
```


The `fsl.wrappers` functions strive to provide an interface which is as close
as possible to the command-line tool - most functions use positional arguments
for required options, and keyword arguments for all other options, with
argument names equivalent to command line option names. For example, the usage
for the command-line `bet` tool is as follows:


> ```
> Usage:    bet <input> <output> [options]
>
> Main bet2 options:
>   -o          generate brain surface outline overlaid onto original image
>   -m          generate binary brain mask
>   -s          generate approximate skull image
>   -n          don't generate segmented brain image output
>   -f <f>      fractional intensity threshold (0->1); default=0.5; smaller values give larger brain outline estimates
>   -g <g>      vertical gradient in fractional intensity threshold (-1->1); default=0; positive values give larger brain outline at bottom, smaller at top
>   -r <r>      head radius (mm not voxels); initial surface sphere is set to half of this
>   -c <x y z>  centre-of-gravity (voxels not mm) of initial mesh surface.
> ...
> ```


So to use the `bet()` wrapper function, pass `<input>` and `<output>` as
positional arguments, and pass the additional options as keyword arguments:


```
bet('bighead_cropped', 'bighead_cropped_brain', f=0.3, m=True, s=True)

render('bighead_cropped             -b 40 '
       'bighead_cropped_brain       -cm hot '
       'bighead_cropped_brain_skull -ot mask -mc 0.4 0.4 1 '
       'bighead_cropped_brain_mask  -ot mask -mc 0   1   0 -o -w 5')
```


> Some FSL commands accept arguments which cannot be used as Python
> identifiers - for example, the `-2D` option to `flirt` cannot be used as an
> identifier in Python, because it begins with a number. In situations like
> this, an alias is used. So to set the `-2D` option to `flirt`, you can do this:
>
> ```
> # "twod" applies the -2D flag
> flirt('source.nii.gz', 'ref.nii.gz', omat='src2ref.mat', twod=True)
> ```
>
> Some of the `fsl.wrappers` functions also support aliases which may make
> your code more readable. For example, when calling `bet`, you can use either
> `m=True` or `mask=True` to apply the `-m` command line flag.


<a class="anchor" id="in-memory-images"></a>
### In-memory images


It can be quite awkward to combine image processing with FSL tools and image
processing in Python. The `fsl.wrappers` package tries to make this a little
easier for you - if you are working with image data in Python, you can pass
`Image` or `nibabel` objects directly into `fsl.wrappers` functions - they will
be automatically saved to temporary files and passed to the underlying FSL
command:


```
cropped = Image('bighead_cropped')

bet(cropped, 'bighead_cropped_brain')

betted = Image('bighead_cropped_brain')

fig = ortho(cropped.data, (80, 112, 85), cmap=plt.cm.gray)
fig = ortho(betted .data, (80, 112, 85), cmap=plt.cm.inferno, fig=fig)
```


<a class="anchor" id="loading-outputs-into-python"></a>
### Loading outputs into Python


By using the special `fsl.wrappers.LOAD` symbol, you can also have any output
files produced by the tool automatically loaded into memory for you:


```
cropped = Image('bighead_cropped')

# The loaded result is called "output",
# because that is the name of the
# argument in the bet wrapper function.
betted  = bet(cropped, LOAD).output

fig = ortho(cropped.data, (80, 112, 85), cmap=plt.cm.gray)
fig = ortho(betted .data, (80, 112, 85), cmap=plt.cm.inferno, fig=fig)
```


You can use the `LOAD` symbol for any output argument - any output files which
are loaded will be available through the return value of the wrapper function:


```
from fsl.wrappers import flirt

std2mm   = Image(op.expandvars(op.join('$FSLDIR', 'data', 'standard', 'MNI152_T1_2mm')))
tstat1   = Image(op.join('08_fslpy', 'fmri.feat', 'stats', 'tstat1'))
func2std = np.loadtxt(op.join('08_fslpy', 'fmri.feat', 'reg', 'example_func2standard.mat'))

aligned = flirt(tstat1, std2mm, applyxfm=True, init=func2std, out=LOAD)

# Here the resampled tstat image
# is called "out", because that
# is the name of the flirt argument.
aligned = aligned.out.data
aligned[aligned < 1] = 0

peakvox = np.abs(aligned).argmax()
peakvox = np.unravel_index(peakvox, aligned.shape)

fig = ortho(std2mm .data, peakvox, cmap=plt.cm.gray)
fig = ortho(aligned.data, peakvox, cmap=plt.cm.inferno, fig=fig, cursor=True)
```


For tools like `bet` and `fast`, which expect an output *prefix* or
*basename*, you can just set the prefix to `LOAD` - all output files with that
prefix will be available in the object that is returned:


```
img    = Image('bighead_cropped')
betted = bet(img, LOAD, f=0.3, mask=True)

fig = ortho(img               .data, (80, 112, 85), cmap=plt.cm.gray)
fig = ortho(betted.output     .data, (80, 112, 85), cmap=plt.cm.inferno, fig=fig)
fig = ortho(betted.output_mask.data, (80, 112, 85), cmap=plt.cm.summer,  fig=fig, alpha=0.5)
```


<a class="anchor" id="the-fslmaths-wrapper"></a>
### The `fslmaths` wrapper


*Most* of the `fsl.wrappers` functions aim to provide an interface which is as
close as possible to the underlying FSL tool. Ideally, if you read the
command-line help for a tool, you should be able to figure out how to use the
corresponding wrapper function. The wrapper for the `fslmaths` command is a
little different, however. It provides more of an object-oriented interface,
which is hopefully a little easier to use from within Python.


You can apply an `fslmaths` operation by specifying the input image,
*chaining* method calls together, and finally calling the `run()` method. For
example:


```
from fsl.wrappers import fslmaths
fslmaths('bighead_cropped')            \
  .mas(  'bighead_cropped_brain_mask') \
  .run(  'bighead_cropped_brain')

render('bighead_cropped bighead_cropped_brain -cm hot')
```


Of course, you can also use the `fslmaths` wrapper with in-memory images:


```
wholehead   = Image('bighead_cropped')
brainmask   = Image('bighead_cropped_brain_mask')

eroded      = fslmaths(brainmask).ero().ero().run()
erodedbrain = fslmaths(wholehead).mas(eroded).run()

fig = ortho(wholehead  .data, (80, 112, 85), cmap=plt.cm.gray)
fig = ortho(brainmask  .data, (80, 112, 85), cmap=plt.cm.summer,  fig=fig)
fig = ortho(erodedbrain.data, (80, 112, 85), cmap=plt.cm.inferno, fig=fig)
```


<a class="anchor" id="the-filetree"></a>
## The `FileTree`


The
[`fsl.utils.filetree`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.filetree.html)
library provides functionality which allows you to work with *structured data
directories*, such as HCP or BIDS datasets. You can use `filetree` for both
reading and for creating datasets.


This practical gives a very brief introduction to the `filetree` library -
refer to the [full
documentation](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.filetree.html)
to get a feel for how powerful it can be.


<a class="anchor" id="describing-your-data"></a>
### Describing your data


To introduce `filetree`, we'll begin with a small example. Imagine that we
have a dataset which looks like this:


> ```
> mydata
> ├── sub_A
> │   ├── ses_1
> │   │   └── T1w.nii.gz
> │   ├── ses_2
> │   │   └── T1w.nii.gz
> │   └── T2w.nii.gz
> ├── sub_B
> │   ├── ses_1
> │   │   └── T1w.nii.gz
> │   ├── ses_2
> │   │   └── T1w.nii.gz
> │   └── T2w.nii.gz
> └── sub_C
>     ├── ses_1
>     │   └── T1w.nii.gz
>     ├── ses_2
>     │   └── T1w.nii.gz
>     └── T2w.nii.gz
> ```


(Run the code cell below to create a dummy data set with the above structure):


```
%%bash
for sub in A B C; do
  subdir=mydata/sub_$sub/
  mkdir -p $subdir
  cp $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz $subdir/T2w.nii.gz
  for ses in 1 2; do
    sesdir=$subdir/ses_$ses/
    mkdir $sesdir
    cp $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz $sesdir/T1w.nii.gz
  done
done
```


To use `filetree` with this dataset, we must first describe its structure - we
do this by creating a `.tree` file:


```
%%writefile mydata.tree
sub_{subject}
  T2w.nii.gz
  ses_{session}
    T1w.nii.gz
```


A `.tree` file is simply a description of the structure of your data
directory - it describes the *file types* (also known as *templates*) which
are present in the dataset (`T1w` and `T2w`), and the *variables* which are
implicitly present in the structure of the dataset (`subject` and `session`).


<a class="anchor" id="using-the-filetree"></a>
### Using the `FileTree`


Now that we have a `.tree` file which describe our data, we can create a
`FileTree` to work with it:


```
from fsl.utils.filetree import FileTree

# Create a FileTree, giving
# it our tree specification,
# and the path to our data.
tree = FileTree.read('mydata.tree', 'mydata')
```

We can list all of the T1 images via the `FileTree.get_all` method. The
`glob_vars='all'` option tells the `FileTree` to fill in the `T1w` template
with all possible combinations of variables. The `FileTree.extract_variables`
method accepts a file path, and gives you back the variable values contained
within:


```
for t1file in tree.get_all('T1w', glob_vars='all'):
    fvars = tree.extract_variables('T1w', t1file)
    print(t1file, fvars)
```


The `FileTree.update` method allows you to "fill in" variable values; it
returns a new `FileTree` object which can be used on a selection of the
data set:


```
treeA = tree.update(subject='A')
for t1file in treeA.get_all('T1w', glob_vars='all'):
    fvars = treeA.extract_variables('T1w', t1file)
    print(t1file, fvars)
```


<a class="anchor" id="building-a-processing-pipeline-with-filetree"></a>
### Building a processing pipeline with `FileTree`


Let's say we want to run BET on all of our T1 images. Let's start by modifying
our `.tree` definition to include the BET outputs:


```
%%writefile mydata.tree
sub_{subject}
  T2w.nii.gz
  ses_{session}
    T1w.nii.gz
    T1w_brain.nii.gz
    T1w_brain_mask.nii.gz
```


Now we can use the `FileTree` to generate the relevant file names for us,
which we can then pass on to BET.  Here we'll use the `FileTree.get_all_trees`
method to create a sub-tree for each subject and each session:


```
from fsl.wrappers import bet
tree = FileTree.read('mydata.tree', 'mydata')
for subtree in tree.get_all_trees('T1w', glob_vars='all'):
    t1file  = subtree.get('T1w')
    t1brain = subtree.get('T1w_brain')
    print('Running BET: {} -> {} ...'.format(t1file, t1brain))
    bet(t1file, t1brain, mask=True)
print('Done!')

example = tree.update(subject='A', session='1')
render('{} {} -ot mask -o -w 2 -mc 0 1 0'.format(
    example.get('T1w'),
    example.get('T1w_brain_mask')))

```


<a class="anchor" id="the-filetreequery"></a>
### The `FileTreeQuery`


The `filetree` module contains another class called the
[`FileTreeQuery`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.filetree.query.html),
which provides an interface that is more convenient if you are reading data
from large datasets with many different file types and variables.


When you create a `FileTreeQuery`, it scans the entire data directory and
identifies all of the values that are present for each variable defined in the
`.tree` file:


```
from fsl.utils.filetree import FileTreeQuery
tree = FileTree.read('mydata.tree', 'mydata')
query = FileTreeQuery(tree)
print('T1w variables:', query.variables('T1w'))
print('T2w variables:', query.variables('T2w'))
```


The `FileTreeQuery.query` method will return the paths to all existing files
which match a set of variable values:


```
print('All files for subject A')
for template in query.templates:
    print('  {} files:'.format(template))
    for match in query.query(template, subject='A'):
        print('   ', match.filename)
```


<a class="anchor" id="calling-shell-commands"></a>
## Calling shell commands


The
[`fsl.utils.run`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.run.html)
module provides the `run` and `runfsl` functions, which are wrappers around
the built-in [`subprocess`
library](https://docs.python.org/3/library/subprocess.html).


The default behaviour of `run` is to return the standard output of the
command:


```
from fsl.utils.run import run

# You can pass the command
# and its arguments as a single
# string, or as a sequence
print('Lines in this notebook:', run('wc -l 08_fslpy.md').strip())
print('Words in this notebook:', run(['wc', '-w', '08_fslpy.md']).strip())
```


But you can control what `run` returns, depending on your needs. Let's create
a little script to demonstrate the options:


```
%%writefile mycmd
#!/usr/bin/env bash
exitcode=$1

echo "Standard output!"
echo "Standard error :(" >&2

exit $exitcode
```


And let's not forget to make it executable:


```
!chmod a+x mycmd
```


You can use the `stdout`, `stderr` and `exitcode` arguments to control the
return value:


```
print('run("./mycmd 0"):                                          ',
       run("./mycmd 0").strip())
print('run("./mycmd 0", stdout=False):                            ',
       run("./mycmd 0", stdout=False))
print('run("./mycmd 0",                            exitcode=True):',
       run("./mycmd 0",                            exitcode=True))
print('run("./mycmd 0", stdout=False,              exitcode=True):',
       run("./mycmd 0", stdout=False,              exitcode=True))
print('run("./mycmd 0",               stderr=True):               ',
       run("./mycmd 0",               stderr=True))
print('run("./mycmd 0", stdout=False, stderr=True):               ',
       run("./mycmd 0", stdout=False, stderr=True).strip())
print('run("./mycmd 0",               stderr=True, exitcode=True):',
       run("./mycmd 0",               stderr=True, exitcode=True))

print('run("./mycmd 1",                            exitcode=True):',
       run("./mycmd 1",                            exitcode=True))
print('run("./mycmd 1", stdout=False,              exitcode=True):',
       run("./mycmd 1", stdout=False,              exitcode=True))
```


So if only one of `stdout`, `stderr`, or `exitcode` is `True`, `run` will only
return the corresponding value. Otherwise `run` will return a tuple which
contains the requested outputs.


If you run a command which returns a non-0 exit code, the default behaviour
(if you don't set `exitcode=True`) is for a `RuntimeError` to be raised:


```
run("./mycmd 99")
```


<a class="anchor" id="the-runfsl-function"></a>
### The `runfsl` function


The `runfsl` function is a wrapper around `run` which simply makes sure that
the command you are calling is inside the `$FSLDIR/bin/` directory. It has the
same usage as the `run` function:


```
from fsl.utils.run import runfsl
runfsl('bet bighead_cropped bighead_cropped_brain')
runfsl('fslroi bighead_cropped_brain bighead_slices 0 -1 0 -1 90 3')
runfsl('fast -o bighead_fast bighead_slices')

render('-vl 80 112 91 -xh -yh '
       'bighead_cropped '
       'bighead_slices.nii.gz -cm brain_colours_1hot -b 30 '
       'bighead_fast_seg.nii.gz -ot label -o')
```


<a class="anchor" id="submitting-to-the-cluster"></a>
### Submitting to the cluster


Both the `run` and `runfsl` accept an argument called `submit`, which allows
you to submit jobs to be executed on the cluster via the FSL `fsl_sub`
command.


> Cluster submission is handled by the
> [`fsl.utils.fslsub`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.fslsub.html)
> module - it contains lower level functions for managing and querying jobs
> that have been submitted to the cluster. The functions defined in this
> module can be used directly if you have more complicated requirements.


The semantics of the `run` and `runfsl` functions are slightly different when
you use the `submit` option - when you submit a job, the `run`/`runfsl`
functions will return immediately, and will return a string containing the job
ID:


```
jobid  = run('ls', submit=True)
print('Job ID:', jobid)
```


Once the job finishes, we should be able to read the usual `.o` and `.e`
files:


```
stdout = f'ls.o{jobid}'
print('Job output')
print(open(stdout).read())
```


All of the `fsl.wrappers` functions also accept the `submit` argument:


```
jobid = bet('08_fslpy/bighead', 'bighead_brain', submit=True)
print('Job ID:', jobid)
```


> But an error will occur if you try to pass in-memory images, or `LOAD` any
> outputs when you call a wrapper function with `submit=True`.


After submitting a job, you can use the `wait` function to wait until a job
has completed:


```
from fsl.utils.run import wait
jobid = bet('08_fslpy/bighead', 'bighead_brain', submit=True)
print('Job ID:', jobid)
wait(jobid)
print('Done!')
render('08_fslpy/bighead bighead_brain -cm hot')
```


When you use `submit=True`, you can also specify cluster submission options -
you can include any arguments that are accepted by the
[`fslsub.submit`](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.fslsub.html#fsl.utils.fslsub.submit)
function


```
jobs = []
jobs.append(runfsl('robustfov -i 08_fslpy/bighead -r bighead_cropped',    submit=True, queue='short.q'))
jobs.append(runfsl('bet bighead_cropped bighead_brain',                   submit=True, queue='short.q', wait_for=jobs[-1]))
jobs.append(runfsl('fslroi bighead_brain bighead_slices 0 -1 111 3 0 -1', submit=True, queue='short.q', wait_for=jobs[-1]))
jobs.append(runfsl('fast -o bighead_fast bighead_slices',                 submit=True, queue='short.q', wait_for=jobs[-1]))
print('Waiting for', jobs, '...')
wait(jobs)

render('-vl 80 112 91 -xh -zh -hc '
       'bighead_brain '
       'bighead_slices.nii.gz -cm brain_colours_1hot -b 30 '
       'bighead_fast_seg.nii.gz -ot label -o')
```


<a class="anchor" id="redirecting-output"></a>
### Redirecting output


The `log` option, accepted by both `run` and `fslrun`, allows for more
fine-grained control over what is done with the standard output and error
streams.


You can use `'tee'` to redirect the standard output and error streams of the
command to the standard output and error streams of the calling command (your
python script):


```
print('Teeing:')
_ = run('./mycmd 0', log={'tee' : True})
```


Or you can use `'stdout'` and `'stderr'` to redirect the standard output and
error streams of the command to files:


```
with open('stdout.log', 'wt') as o, \
     open('stderr.log', 'wt') as e:
     run('./mycmd 0', log={'stdout' : o, 'stderr' : e})
print('\nRedirected stdout:')
!cat stdout.log
print('\nRedirected stderr:')
!cat stderr.log
```


Finally, you can use `'cmd'` to log the command itself to a file (useful for
pipeline logging):


```
with open('commands.log', 'wt') as cmdlog:
     run('./mycmd 0',         log={'cmd' : cmdlog})
     run('wc -l 08_fslpy.md', log={'cmd' : cmdlog})

print('\nCommand log:')
!cat commands.log
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

fig = ortho(std2mm.data, (45, 54, 45), cmap=plt.cm.gray)
fig = ortho(frontal,     (45, 54, 45), cmap=plt.cm.winter, fig=fig)
```


Calling `get` on a `ProbabilisticAtlas` will return a probability image:


```
stddir = op.expandvars('${FSLDIR}/data/standard/')
std2mm = Image(op.join(stddir, 'MNI152_T1_2mm'))

frontal = probatlas.get(name='Frontal Pole').data
frontal = np.ma.masked_where(frontal < 1, frontal)

fig = ortho(std2mm.data, (45, 54, 45), cmap=plt.cm.gray)
fig = ortho(frontal,     (45, 54, 45), cmap=plt.cm.inferno, fig=fig)
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
