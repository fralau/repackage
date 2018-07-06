"""

Repackaging module
(C) Laurent Franceschetti 2014, 2017

Calls a package in any directory, with a relative path.

Use this when you move the file into a subdirectory and don't want
to rewrite the import statements.

NEW: *It inserts the directory at the beginning of the list of available ones,
so as to give precedence to the packages in that directory
over other ones with the same name.*

If you have:
Parent
   |--a.py
   |--mydir1
   |  |--b.py
   |  |--mydir12
   |     |--c.py
   |--mydir2
      |--d.py

Just dump this module in mydir1 and call:

    import repackage
    repackage.up()

From then on, you can access a.py as if it was in the local directory.

Note:
    If you are in mydir12, the root is 2 levels up, add this call :
        repackage.up(2)

    You can call d.py in the following way:
        mydir2.d


You can also call it this way:
    import repackage
    repackage.add(../../other_dir/mypackage)

If you are unsure what the situation is, call the lib_path function, which
returns the current path list:
    a = repackage.lib_path()

"""

from __future__ import print_function


import sys
import os

from os.path import dirname, abspath, normpath, join

import inspect


import os
from distutils.spawn import find_executable




def __caller():
    "Filename of the caller"
    # you have to add 2 to the stack
    try:
        return inspect.stack()[3][1]
    except IndexError:
        # called from command line
        return ""

def __caller_path():
    "The path of the directory of the caller"
    if __caller != '':
        return dirname(abspath(__caller()))
    else:
        # command line
        return os.getcwd()


# flag to remove the default
default_dir = False

# print("Caller:", caller)



def up(stepup = 1):
    """
    Go up n levels (removes the previously added 1st level level path).
    """


    # get directory of file from which this module was loaded
    source_path = __caller_path()

    for i in range(stepup):
       # one directory up
       source_path = dirname(source_path)

    # add at the beginning:
    sys.path.insert(0, source_path)
    return source_path





def add(relative_path):
    "Adds a directory from a relative path (from the caller file)"

    # join the caller path and the relative_path, and then normalize:
    new_path = normpath(join(__caller_path(), relative_path))
    if os.path.exists(new_path):
        # add at the beginning:
        sys.path.insert(0, new_path)
        return new_path
    else:
        # fail noisily
        raise ImportError("Directory %s does not exist." % new_path)



def lib_path():
    "Get the current paths"
    return sys.path


def _follow_link(filename):
    "Check if file is symlink and if yes, follow to its end"
    while os.path.islink(filename):
        target = os.readlink(filename)
        # if relative, complete:
        if not os.path.isabs(target):
            target = os.path.join(os.path.dirname(filename), target)
        filename = target
        # print("Follow link:", filename)
    return filename

def _which(exec_name):
    """
    Get the the executable referenced in the PATH ('which') .
    If it is a symlink, it will follow it to its destination.
    """
    # 1. check in the PATH:
    executable = find_executable(exec_name) or exec_name
    # print("Executable:", executable)
    # 2. check whether the exec_name is a symlink:
    executable = _follow_link(executable)
    return executable

def add_path(module_filename):
    """
    Adds the directory of a module,
    if the module can be found in the PATH.

    It was designed to follow symlinks: if you have, in your PATH,
    a symlink foo -> /my/dir/foo.py
    (this gives an additional mechanism to the normal import paths of Python).

    You should declare the module name as the filename that actually appears
    in the path ('foo.py'; if a symlink, it might be 'foo')

    This is tested for *NIX machines (Linux and MacOS).
    """
    dirname = os.path.dirname(_which(module_filename))
    return add(dirname)

# --------------------------------------------
# Testing part
# --------------------------------------------
if __name__ == '__main__':
    from pprint import pprint
    up(1)
    print("Directory is:")
    pprint(lib_path())

    print("Calling upper directory:")
    up(2)
    pprint(lib_path())

    print("Adding the 'ls' module (supposing...)")
    add_path('ls')
    assert '/bin' in lib_path()


    item = 'vi'
    print("Adding the '%s' module (supposing...)" % item)
    add_path('%s' % item)
    print(lib_path()[0])
