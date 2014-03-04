""" 

Repackaging module V0.1c
(C) Laurent Franceschetti 2014

Changes the default directory for paths, so as to avoid
the relative path.

Use this when you move the file into a subdirectory and don't want
to rewrite the import statements.

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

    import __repackage

From then on, you can access a.py as if it was in the local directory.


Note:
    If you are in mydir12, the root is 2 levels up, add this call :
        __repackage.up(2)

    You can call d.py in the following way:
        mydir2.d


If you are unsure what the situation is, call the libpath function, which
returns the current path list:
    a = __repackage.libpath()

"""

from __future__ import print_function


import sys
import os

from os.path import dirname, abspath

# personal library (could not make relative imports work)
def init_package(stepup = 1):
    """Give access to the package paths as if in root of package.
    Goes one level up
    
    Arguments:
        stepup:   no of directories up
        
    """
 
    # get directory of file from which this module was loaded
    lib_path = dirname(abspath(__file__))   

    # default, executed at first run
    lib_path = dirname(lib_path)
    sys.path.append(lib_path)
  
    return libpath

def up(stepup = 1):
    """Go up n levels (removes the previously added 1st level level path).
    Calling up(1) is optional -- done when the package is called."""
    
    # get directory of file from which this module was loaded
    lib_path = dirname(abspath(__file__))
    
    for i in range(stepup):
       # one directory up
       lib_path = dirname(lib_path)
    
    sys.path.pop() # remove path previously inserted
    sys.path.append(lib_path)
    
    return libpath


def libpath():
    "Get the current paths"
    return sys.path
    
# Execute the code a call time of the package
init_package()


# --------------------------------------------
# Testing part
# --------------------------------------------
if __name__ == '__main__':
   from pprint import pprint
   print("Directory is:")
   pprint(libpath())
   
   print("Calling upper directory:")
   up(2)
   pprint(libpath())
    
