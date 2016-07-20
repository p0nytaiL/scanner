import os
"""Directory tree generator.

For each directory in the directory tree rooted at top (including top
itself, but excluding '.' and '..'), yields a 3-tuple

    dirpath, dirnames, filenames

dirpath is a string, the path to the directory.  dirnames is a list of
the names of the subdirectories in dirpath (excluding '.' and '..').
filenames is a list of the names of the non-directory files in dirpath.
Note that the names in the lists are just names, with no path components.
To get a full path (which begins with top) to a file or directory in
dirpath, do os.path.join(dirpath, name).

If optional arg 'topdown' is true or not specified, the triple for a
directory is generated before the triples for any of its subdirectories
(directories are generated top down).  If topdown is false, the triple
for a directory is generated after the triples for all of its
subdirectories (directories are generated bottom up).

When topdown is true, the caller can modify the dirnames list in-place
(e.g., via del or slice assignment), and walk will only recurse into the
subdirectories whose names remain in dirnames; this can be used to prune the
search, or to impose a specific order of visiting.  Modifying dirnames when
topdown is false is ineffective, since the directories in dirnames have
already been generated by the time dirnames itself is generated. No matter
the value of topdown, the list of subdirectories is retrieved before the
tuples for the directory and its subdirectories are generated.

By default errors from the os.listdir() call are ignored.  If
optional arg 'onerror' is specified, it should be a function; it
will be called with one argument, an os.error instance.  It can
report the error to continue with the walk, or raise the exception
to abort the walk.  Note that the filename is available as the
filename attribute of the exception object.

By default, os.walk does not follow symbolic links to subdirectories on
systems that support them.  In order to get this functionality, set the
optional argument 'followlinks' to true.

Caution:  if you pass a relative pathname for top, don't change the
current working directory between resumptions of walk.  walk never
changes the current directory, and assumes that the client doesn't
either.

Example:

import os
from os.path import join, getsize
for root, dirs, files in os.walk('python/Lib/email'):
    print root, "consumes",
    print sum([getsize(join(root, name)) for name in files]),
    print "bytes in", len(files), "non-directory files"
    if 'CVS' in dirs:
        dirs.remove('CVS')  # don't visit CVS directories

"""

def recursively_dir(path_root):
    path_root = '/Users/ponytail/Desktop/Shared/install'
    total = 1
    for dirpath, dirnames, eml_files in os.walk(path_root):

        for index, filename in enumerate(eml_files):
            file = os.path.join(dirpath, filename)
            if os.path.isfile(file):
                print '[%d] %s' % (total + index, file)

        total = total + len(eml_files)


'''

'''

#os.path.isfile()


if __name__ == '__main__':
    recursively_dir('')
