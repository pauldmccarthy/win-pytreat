# Callable scripts in python

In this tutorial we will cover how to write simple stand-alone scripts in python that can be used as alternatives to bash scripts.

There are some code blocks within this webpage, but for this practical we _**strongly
recommend that you write the code in an IDE or editor**_ instead and then run the scripts from a terminal.

## Contents

* [Basic script](#basic-script)
* [Calling other executables](#calling-other-executables)
* [Command line arguments](#command-line-arguments)
* [Example script](#example-script)
* [Exercise](#exercise)

---

<a class="anchor" id="basic-script"></a>
## Basic script

The first line of a python script is usually:
```
#!/usr/bin/env python
```
which invokes whichever version of python can be found by `/usr/bin/env` since python can be located in many different places.

For FSL scripts we use an alternative, to ensure that we pick up the version of python (and associated packages) that we ship with FSL.  To do this we use the line:
```
#!/usr/bin/env fslpython
```

After this line the rest of the file just uses regular python syntax, as in the other tutorials.  Make sure you make the file executable - just like a bash script.

<a class="anchor" id="calling-other-executables"></a>
## Calling other executables

The most essential call that you need to use to replicate the way a bash script calls executables is `subprocess.run()`.  A simple call looks like this:

```
import subprocess as sp
sp.run(['ls', '-la'])
```


To suppress the output do this:

```
spobj = sp.run(['ls'], stdout = sp.PIPE)
```

To store the output do this:

```
spobj = sp.run('ls -la'.split(), stdout = sp.PIPE)
sout = spobj.stdout.decode('utf-8')
print(sout)
```

> Note that the `decode` call in the middle line converts the string from a byte string to a normal string. In Python 3 there is a distinction between strings (sequences of characters, possibly using multiple bytes to store each character) and bytes (sequences of bytes). The world has moved on from ASCII, so in this day and age, this distinction is absolutely necessary, and Python does a fairly good job of it.

If the output is numerical then this can be extracted like this:
```
import os
fsldir = os.getenv('FSLDIR')
spobj = sp.run([fsldir+'/bin/fslstats', fsldir+'/data/standard/MNI152_T1_1mm_brain', '-V'], stdout = sp.PIPE)
sout = spobj.stdout.decode('utf-8')
vol_vox = float(sout.split()[0])
vol_mm = float(sout.split()[1])
print('Volumes are: ', vol_vox, ' in voxels and ', vol_mm, ' in mm')
```



An alternative way to run a set of commands would be like this:
```
commands = """
{fsldir}/bin/fslmaths {t1} -bin {t1_mask}
{fsldir}/bin/fslmaths {t2} -mas {t1_mask} {t2_masked}
"""

fsldirpath = os.getenv('FSLDIR')
commands = commands.format(t1 = 't1.nii.gz', t1_mask = 't1_mask', t2 = 't2', t2_masked = 't2_masked', fsldir = fsldirpath)

sout=[]
for cmd in commands.split('\n'):
    if cmd:   # avoids empty strings getting passed to sp.run()
        print('Running command: ', cmd)
        spobj = sp.run(cmd.split(), stdout = sp.PIPE)
        sout.append(spobj.stdout.decode('utf-8'))
```


<a class="anchor" id="command-line-arguments"></a>
## Command line arguments

The simplest way of dealing with command line arguments is use the module `sys`, which gives access to an `argv` list:
```
import sys
print(len(sys.argv))
print(sys.argv[0])
```

For more sophisticated argument parsing you can use `argparse` -  good documentation and examples of this can be found on the web.

---

<a class="anchor" id="example-script"></a>
## Example script

Here is a simple bash script (it masks an image and calculates volumes - just as a random example). DO NOT execute the code blocks here within the notebook/webpage:

```
#!/bin/bash
if [ $# -lt 2 ] ; then
  echo "Usage: $0 <input image> <output image>"
  exit 1
fi
infile=$1
outfile=$2
# mask input image with MNI
$FSLDIR/bin/fslmaths $infile -mas $FSLDIR/data/standard/MNI152_T1_1mm_brain $outfile
# calculate volumes of masked image  
vv=`$FSLDIR/bin/fslstats $outfile -V`
vol_vox=`echo $vv | awk '{ print $1 }'`
vol_mm=`echo $vv | awk '{ print $2 }'`
echo "Volumes are: $vol_vox in voxels and $vol_mm in mm"
```


And an alternative in python:

```
#!/usr/bin/env fslpython
import os, sys
import subprocess as sp
fsldir=os.getenv('FSLDIR')
if len(sys.argv)<2:
  print('Usage: ', sys.argv[0], ' <input image> <output image>')
  sys.exit(1)
infile = sys.argv[1]
outfile = sys.argv[2]
# mask input image with MNI
spobj = sp.run([fsldir+'/bin/fslmaths', infile, '-mas', fsldir+'/data/standard/MNI152_T1_1mm_brain', outfile], stdout = sp.PIPE)
# calculate volumes of masked image  
spobj = sp.run([fsldir+'/bin/fslstats', outfile, '-V'], stdout = sp.PIPE)
sout = spobj.stdout.decode('utf-8')
vol_vox = float(sout.split()[0])
vol_mm = float(sout.split()[1])
print('Volumes are: ', vol_vox, ' in voxels and ', vol_mm, ' in mm')
```

---

<a class="anchor" id="exercise"></a>
## Exercise

Write a simple version of fslstats that is able to calculate either a
mean or a _sum_ (and hence can do something that fslstats cannot!)

```
# Don't write anything here - do it in a standalone script!
```

