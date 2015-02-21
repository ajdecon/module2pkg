module2pkg
==========

A simple tool for building OS packages from environment modules.

        Usage: module2pkg [options]

        Options:
          -h, --help            show this help message and exit
          -t PKGTYPE, --type=PKGTYPE
                                Type of package to build
          -p PREFIX, --prefix=PREFIX
                                Package name prefix

This tool has been tested for building RPM packages. It should also be able
to build DEB packages (via FPM) but I haven't tested this yet.

Requirements
------------

* There must be a 'modulecmd' tool which can be used to query available modules.
* The [fpm](https://github.com/jordansissel/fpm) tool must be available to build
  the OS packages.

Assumptions about the Modules
-----------------------------

* Each Module should have all its files stored under a single root directory
  (e.g. /opt/sw/modulename/version)
* The Modulefile should contain a "root" variable which points to the Module's
  root directory.



