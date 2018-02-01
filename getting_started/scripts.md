# Callable scripts in python

In this tutorial we will cover how to write simple stand-alone scripts in python that can be used as alternatives to bash scripts.

There are some code blocks within this webpage, but we recommend that you write the code in an IDE or editor instead and then run the scripts from a terminal.

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

After this line the rest of the file just uses regular python syntax, as in the other tutorials.

## Calling other executables

The most essential call that you need to use to replicate the way a bash script calls executables is `subprocess.run()`.  A simple call looks like this:

```
import subprocess
subprocess.run(["ls","-la"])
```


To suppress the output do this:

```
sp=subprocess.run(["ls"],stdout=subprocess.PIPE)
```

To store the output do this:

```
sp=subprocess.run("ls -la".split(),stdout=subprocess.PIPE)
sout=sp.stdout.decode('utf-8')
print(sout)
```

Note that the `decode` call in the middle line converts the string from a byte string to a normal string.

If the output is numerical then this can be extracted like this:
```
import os
fsldir=os.getenv('FSLDIR')
sp=subprocess.run([fsldir+'/bin/fslstats',fsldir+'/data/standard/MNI152_T1_1mm_brain','-V'],stdout=subprocess.PIPE)
sout=sp.stdout.decode('utf-8')
vol_vox=float(sout.split()[0])
vol_mm=float(sout.split()[1])
print('Volumes are: ',vol_vox,' in voxels and ',vol_mm,' in mm')
```


## Command line arguments

The simplest way of dealing with command line arguments is use the module `sys`, which gives access to an `argv` list:
```
import sys
print(len(sys.argv))
print(sys.argv[0])
```

There are also some modules that are useful for parsing arguments:
 - `getopt`
 - `argparse`
 and you can find good documentation and examples of these on the web.


## Example script

Here is a simple bash script (it masks an image and calculates volumes - just as random examples):

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
import os, sys, subprocess
fsldir=os.getenv('FSLDIR')
if len(sys.argv)<2:
  print('Usage: ',sys.argv[0],' <input image> <output image>')
  sys.exit(1)
infile=sys.argv[1]
outfile=sys.argv[2]
# mask input image with MNI
sp=subprocess.run([fsldir+'/bin/fslmaths',infile,'-mas',fsldir+'/data/standard/MNI152_T1_1mm_brain',outfile],stdout=subprocess.PIPE)
# calculate volumes of masked image  
sp=subprocess.run([fsldir+'/bin/fslstats',outfile,'-V'],stdout=subprocess.PIPE)
sout=sp.stdout.decode('utf-8')
vol_vox=float(sout.split()[0])
vol_mm=float(sout.split()[1])
print('Volumes are: ',vol_vox,' in voxels and ',vol_mm,' in mm')
```

