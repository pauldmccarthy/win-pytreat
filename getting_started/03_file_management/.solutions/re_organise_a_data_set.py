import            os
import os.path as op
import            glob
import            shutil


def reorganise_data_set(dirname, groupLabels, groups):
    """Re-organises the subject directories in the given `dirname` by group,
    according to the labels in `groupLabels`, and the group definitions in
    `groups`.

    :arg dirname:     Data set directory.
    :arg groupLabels: Sequence of labels, one for each group
    :arg groups:      Sequence of group definitions - each group is defined
                      by a sequence of subject IDs.
    """

    # Get lists of subject directories
    # and corresponding subject IDs
    subjdirs = list(glob.glob(op.join(dirname, 'subj_*')))
    subjids  = [int(sd.split('_')[1]) for sd in subjdirs]

    # For each group
    for glabel, group in zip(groupLabels, groups):

        # Make the group directory
        groupdir = op.join(dirname, glabel)
        os.mkdir(groupdir)

        # For each subject in this group
        for sid in group:

            # Lookup the subject directory,
            # and move it into the group dir
            subjdir = subjdirs[subjids.index(sid)]
            shutil.move(subjdir, groupdir)
