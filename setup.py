from distutils.core import setup


# -------------------------
# Setup
# -------------------------
setup(name='repackage',
      version='0.7',
      description= ("Repackaging, call a non-registered package in any "
                    "directory (with relative call). "
                    "Used either by modules moved into to a subdirectory "
                    "or to prepare the import of a non-registered package "
                    "(in any relative path)."),
      url='https://www.settlenext.com',
      author='Laurent Franceschetti',
      author_email='developer@settlenext.com',
      keywords ="package relative path module import library",
      license='MIT',
      packages=['repackage'],
      long_description=open('README.txt').read(),
      classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License"
      ])
