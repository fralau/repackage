===================
Package: Repackage
===================

Laurent Franceschetti
March/June 2013 - 2017
MIT License.

Purpose
===========
This module allows any Python program to call a non-registered package in a reliable way. With this module, you may call "non-official" repositories, including with relative paths.

**CAUTION:** *This form is an alternative to system of relative paths for
python imports
([PEP 328](https://www.python.org/dev/peps/pep-0328/#rationale-for-relative-imports))
and as such it is largely redundant. It can, however, be interesting because
it shows how such a problem could be solved.*


Install
=======
If you are using pip:
::

   pip install repackage

The problem
===========
In Python, registered packages are called by name in import instructions,
and lower directories may be treated for all purposes as packages.

Two practical problems arise:
a) How to easily call unregistered packages which have been dumped
in an adjacent directory?
b) How to easily move python files into a sub-directory without messing up
the import statements?

There are complicated issues with relative imports (see PEP366). The basic idea
here is to add the source directory of the package to the lib path (thanks to
a call to sys.path.append).

But the probem, is how to programmatically find the source directory, from a
relative path?

Two often advocated methods to determine the path are:
a. from current directory or
b. from __FILE__ .

Both those methods have a flaw:
  * The first does not take into account the file where the import is made,
    hence will fail if the project is using more than one directory.
  * The second does not allow to delegate those operations to a module that
    would handle those issues (as __FILE__ is going to point now to point to
    the module and not the caller).

The solution
============
This package uses a simple strategy that is likely to work
in a good range of cases: it inspects the stack to determine which file
is the caller and works out the relative path from there.
The only delicate part consisted in working out how many
steps down the stack this is, but the answer should be invariant and
can be computed both by reasoning and by trial and error (in this case: 3).

Usage
=====
Situation 1) Moving the files into a lower directory. From the module you want to make the call, just use the following statement
before the imports:
::

	import repackage
	repackage.up()

It should work without changing the imports that were previously
pointing to the upper directory.

If it's two directories up, write:
::

  	import repackage
	repackage.up(2)

Situation 2) Calling a non-registered directory somewhere else (absolute or relative path):
::

	import repackage
	repackage.add("../../otherdir")

Clearly, repackage.up() would be equivalent to repackage.add("..") .
I prefer the first because it is more terse and syntactically more robust.


Limitations
===========
If at some points in the execution, you attempt to add
several times the same directory to the lib path, this should remain without
effect (this is a feature of sys.path.append).

This module has worked reliably for a while, so it is a beta version.
The method seems robust so far, but not all ins and outs
have been explored. One precaution might be to ensure that the repackaging
always points to the same source directory of a package
(not to subdirectories of the same package), so as to avoid possible
ambiguities in the lib path. (If this really turned out to be a problem,
this could be checked on the fly and a warning issued?).

If you find bugs, or even find this approach useless, essentially flawed or against the Zen of Python, I will be glad to hear about it.
Similarly, if you liked it or have ideas on how to improve it, let me know.
