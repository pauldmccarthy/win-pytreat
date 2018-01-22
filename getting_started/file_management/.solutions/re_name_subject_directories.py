import os.path as op
import            glob
import            shutil
import numpy   as np


def rename_subject_dirs(dirname):
    """Renames all directories in `dirname` which have the form `subj_[id]`,
    where `[id]` is an integer specifying the subject IDs.

    Each subject directory is renamed such that the subject IDs are padded
    with zeros, thus allowing the directories to be sorted alphabetically.

    :arg dirname: Data set directory.
    """

    # get a list of all
    # subject directories
    subjdirs = list(glob.glob(op.join(dirname, 'subj_*')))

    # get a list of subject IDs
    subjids = [int(sd.split('_')[1]) for sd in subjdirs]

    # figure out the maximmum
    # number of digits we need
    ndigits = int(np.ceil(np.log10(max(subjids) + 1)))

    # create a format string
    # which will pad an ID with
    # the required number of zeros
    fmtstr = 'subj_{{:0{}d}}'.format(ndigits)

    # generate new subject
    # directory names
    newsubjdirs = [op.join(dirname, fmtstr.format(sid)) for sid in subjids]

    # rename each subject dir
    for subjdir, newsubjdir in zip(subjdirs, newsubjdirs):
        shutil.move(subjdir, newsubjdir)
