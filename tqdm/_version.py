# Definition of the version number
import os
from io import open as io_open

__all__ = ["__version__"]

# major, minor, patch, -extra
version_info = 4, 11, 1

# Nice string for the version
__version__ = '.'.join(map(str, version_info))


# auto -extra based on commit hash (if not tagged as release)
scriptdir = os.path.dirname(__file__)
gitdir = os.path.abspath(os.path.join(scriptdir, "..", ".git"))
if os.path.isdir(gitdir):
    extra = None
    # Open config file to check if we are in tqdm project
    with io_open(os.path.join(gitdir, "config"), 'r') as fh_config:
        if 'tqdm' in fh_config.read():
            # Open the HEAD file
            with io_open(os.path.join(gitdir, "HEAD"), 'r') as fh_head:
                extra = fh_head.readline().strip()
            # in a branch => HEAD points to file containing last commit
            if 'ref:' in extra:
                # reference file path
                ref_file = extra[5:]
                branch_name = ref_file.rsplit('/', 1)[-1]

                ref_file_path = os.path.abspath(os.path.join(gitdir, ref_file))
                # check that we are in git folder
                # (by stripping the git folder from the ref file path)
                if os.path.relpath(
                        ref_file_path, gitdir).replace('\\', '/') != ref_file:
                    # out of git folder
                    extra = None
                else:
                    # open the ref file
                    with io_open(ref_file_path, 'r') as fh_branch:
                        commit_hash = fh_branch.readline().strip()
                        extra = commit_hash[:8]
                        if branch_name != "master":
                            extra += '.' + branch_name

            # detached HEAD mode, already have commit hash
            else:
                extra = extra[:8]

    # Append to version string
    if extra is not None:
        __version__ += '-' + extra
