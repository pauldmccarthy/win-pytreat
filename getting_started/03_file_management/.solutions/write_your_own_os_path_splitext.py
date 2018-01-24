def nifti_splitext(path, exts=None):
    """Splits the given path, assumed to be a NIFTI file, into its
    prefix and suffix components.

    :arg path: Path to split
    :arg exts: List of recognised file extensions. Defaults to
               `['.nii', '.nii.gz']`, but can be overridden.

    :returns:  A tuple containing:
                - The part of `path` before the extension
                - The extension
    """
    if exts is None:
        exts = ['.nii', '.nii.gz']

    # Try and find a suffix match
    extMatches = [path.endswith(ext) for ext in exts]

    # No match - there is
    # no supported extension
    if not any(extMatches):
        return path, ''

    # Otherwise split the path
    # into its base and its extension
    extIdx = extMatches.index(True)
    extLen = len(exts[extIdx])

    return path[:-extLen], path[-extLen:]
