import os.path as op
import            os
import            re
import            glob



def get_image(dirname, group, subjID, modality):
    """Finds the NIFTI image for the given `modality, in the specified
    `dirname`, which is for the specified `subjID`.

    :arg dirname:  Data set directory
    :arg group:    Group label
    :arg subjID:   Subject ID
    :arg modality: Image modality
    :returns:      The path to the specified image, or `None` if it cannot be
                   found.
    """

    # Get the group directory, and
    # list of all subject directories
    groupdir = op.join(dirname, group)
    subjdirs = list(glob.glob(op.join(groupdir, 'subj_*')))

    # Define a regex which we can
    # use to identify the appropriate
    # subject directory
    subjpat   = re.compile('subj_(0*{})'.format(subjID))
    padsubjID = None

    # Look for the relevant subject
    # directory. When we find it, we
    # store the zero-padded version
    # of the subject ID, so we can
    # use it to construct the final
    # file name.
    for subjdir in subjdirs:
        match = subjpat.fullmatch(op.basename(subjdir))
        if match is not None:
            padsubjID = match.groups(0)[0]
            break

    # Could not identify
    # subject directory
    else:
        return None

    # Construct and return
    # the relevant file name
    fname = '{}_subj_{}_{}.nii.gz'.format(group, padsubjID, modality)
    fname = op.join(subjdir, fname)

    if op.exists(fname):
        return fname
    else:
        return None


def get_image_nogroup(dirname, subjID, modality):
    """Finds the NIFTI image for the given `modality, in the specified
    `dirname`, which is for the specified `subjID`, who is in the specified
    `group`.

    :arg dirname:  Data set directory
    :arg subjID:   Subject ID
    :arg modality: Image modality
    :returns:      The path to the specified image, or `None` if it cannot be
                   found.
    """

    # Define a regex which we can
    # use to identify the appropriate
    # subject directory
    subjpat = re.compile('subj_(0*{})'.format(subjID))

    # Look for the relevant subject
    # directory. When we find it, we
    # store the zero-padded version
    # of the subject ID, so we can
    # use it to construct the final
    # file name.
    subjdir   = None
    padsubjID = None
    for root, dirs, files in os.walk(dirname):
        for d in dirs:
            match = subjpat.fullmatch(d)
            if match is not None:
                subjdir   = op.join(root, d)
                padsubjID = match.groups(0)[0]

    if subjdir is None:
        return None

    # Get the name of the group
    # this subject is in
    group = op.basename(op.dirname(subjdir))

    # Construct and return
    # the relevant file name
    fname = '{}_subj_{}_{}.nii.gz'.format(group, padsubjID, modality)
    fname = op.join(subjdir, fname)

    if op.exists(fname):
        return fname
    else:
        return None
