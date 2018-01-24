import os.path as op
import            os
import            gzip


def compress_all(dirname):
    """Recursively scans through `dirname`, and compresses all `.nii` files
    with gzip, replacing them with `.nii.gz` files.

    :arg dirname: Directory to scan for `.nii` files.
    """

    for root, dirs, files in os.walk(dirname):

        uncmpfiles = [f for f in files if f.endswith('.nii')]

        infiles  = [op.join(root, uf)  for  uf  in uncmpfiles]
        outfiles = ['{}.gz'.format(inf) for inf in infiles]

        for infile, outfile in zip(infiles, outfiles):
            with open(     infile,  'rb') as inf, \
                 gzip.open(outfile, 'wb') as outf:
                outf.write(inf.read())
            os.remove(infile)
