import os.path as op
import            os
import            glob


def rename_subject_files(subjdir, group):
    """Renames all of the NIFTI files contained in `subjdir`, adding
    the prefix `[group]_subj_[id]`, where `[group]` is equal to the
    specified `group`, and `[id`] is gleaned from `subjdir` (assumed
    to be called `subj_[id]`).

    :arg subjdir: Directory containing NIFTI files for one subject
    :arg group:   Name of the group this subject belongs to.
    """

    # Normalise the subject directory name.
    # We pass subjdir through abspath so that
    # this function will accept relative
    # paths, and through normpath to ensure
    # that there is no trailing slash.
    subjdir = op.normpath(op.abspath(subjdir))

    # Now we can extract the subject id.
    # Note that we don't convert the subject
    # ID to a string here - this means that
    # any zero-padding will be preserved.
    subjid = op.basename(subjdir)
    subjid = subjid.split('_')[1]

    # Get a list of all nifti images
    # in the subject directory.
    imgfiles = list(glob.glob(op.join(subjdir, '*.nii')) +
                    glob.glob(op.join(subjdir, '*.nii.gz')))

    # Generate new file names
    # for all of these images
    newimgfiles = ['{}_subj_{}_{}'.format(group, subjid, op.basename(imgf))
                   for imgf in imgfiles]
    newimgfiles = [op.join(subjdir, imgf) for imgf in newimgfiles]

    # Rename all the images
    for imgfile, newimgfile in zip(imgfiles, newimgfiles):
        os.rename(imgfile, newimgfile)


def rename_all_subject_files(dirname):
    """Calls `rename_subject_files` on every subject directory in the specified
    `dirname`.

    :arg dirname: Data set directory.. Assumed to contain a sub-directory for
                  each group, which in turn contain sub-directories for each
                  subject.
    """

    # get a list of all
    # group directories
    groupdirs = glob.glob(op.join(dirname, '*'))
    groupdirs = [gdir for gdir in groupdirs if op.isdir(gdir)]

    for groupdir in groupdirs:

        # get the group name
        group = op.basename(op.normpath(groupdir))

        # get the list of subject
        # directories in this group
        subjdirs = glob.glob(op.join(groupdir, 'subj_*'))

        # apply rename_subject_files
        # to each subject dir
        for subjdir in subjdirs:
            rename_subject_files(subjdir, group)
