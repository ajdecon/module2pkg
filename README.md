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
          -d, --dry-run         Print FPM commands but do not execute them

This tool has been tested for building RPM packages. It should also be able
to build DEB packages (via FPM) but I haven't tested this yet.

Requirements
------------

* environment-modules must be installed (currently doesn't work with Lmod)
* The [fpm](https://github.com/jordansissel/fpm) tool must be available to build
  the OS packages.

Assumptions about the Modules
-----------------------------

* Each Module should have all its files stored under a single root directory
  (e.g. /opt/sw/modulename/version)
* The Modulefile should contain a "root" variable which points to the Module's
  root directory.

Example
-------

Here's a short example of how the script works, using some Modules built with
the amazing tool [EasyBuild](http://easybuild.readthedocs.org/en/latest/index.html).

        $ module av

        --------------------------------------------------- /opt/sw/modules/all ----------------------------------------------------
        EasyBuild/1.16.1      GCC/4.8.1             MPICH/3.0.4-GCC-4.8.1 gmpich/1.4.8

        $ ./module2pkg --prefix local --dry-run gmpich/1.4.8
        fpm -s dir -t rpm -n local-GCC -v 4.8.1 -p local-GCC-VERSION_ARCH.rpm -C / /opt/sw/software/GCC/4.8.1 /opt/sw/modules/all/GCC/4.8.1
        fpm -s dir -t rpm -n local-MPICH -v 3.0.4-GCC-4.8.1 -p local-MPICH-VERSION_ARCH.rpm -d "local-GCC = 4.8.1" -C / /opt/sw/software/MPICH/3.0.4-GCC-4.8.1 /opt/sw/modules/all/MPICH/3.0.4-GCC-4.8.1
        fpm -s dir -t rpm -n local-gmpich -v 1.4.8 -p local-gmpich-VERSION_ARCH.rpm -d "local-MPICH = 3.0.4-GCC-4.8.1" -d "local-GCC = 4.8.1" -C / /opt/sw/software/gmpich/1.4.8 /opt/sw/modules/all/gmpich/1.4.8

        $ ./module2pkg --prefix local gmpich/1.4.8
        fpm -s dir -t rpm -n local-GCC -v 4.8.1 -p local-GCC-VERSION_ARCH.rpm -C / /opt/sw/software/GCC/4.8.1 /opt/sw/modules/all/GCC/4.8.1
        no value for epoch is set, defaulting to nil {:level=>:warn}
        no value for epoch is set, defaulting to nil {:level=>:warn}
        Created package {:path=>"local-GCC-4.8.1_x86_64.rpm"}
        fpm -s dir -t rpm -n local-MPICH -v 3.0.4-GCC-4.8.1 -p local-MPICH-VERSION_ARCH.rpm -d "local-GCC = 4.8.1" -C / /opt/sw/software/MPICH/3.0.4-GCC-4.8.1 /opt/sw/modules/all/MPICH/3.0.4-GCC-4.8.1
        Package version '3.0.4-GCC-4.8.1' includes dashes, converting to underscores {:level=>:warn}
        no value for epoch is set, defaulting to nil {:level=>:warn}
        no value for epoch is set, defaulting to nil {:level=>:warn}
        Created package {:path=>"local-MPICH-3.0.4_GCC_4.8.1_x86_64.rpm"}
        fpm -s dir -t rpm -n local-gmpich -v 1.4.8 -p local-gmpich-VERSION_ARCH.rpm -d "local-MPICH = 3.0.4-GCC-4.8.1" -d "local-GCC = 4.8.1" -C / /opt/sw/software/gmpich/1.4.8 /opt/sw/modules/all/gmpich/1.4.8
        no value for epoch is set, defaulting to nil {:level=>:warn}
        no value for epoch is set, defaulting to nil {:level=>:warn}
        Created package {:path=>"local-gmpich-1.4.8_x86_64.rpm"}

        $ ls *rpm
        local-GCC-4.8.1_x86_64.rpm  local-MPICH-3.0.4_GCC_4.8.1_x86_64.rpm  local-gmpich-1.4.8_x86_64.rpm

        $ rpm -qRp local-gmpich-1.4.8_x86_64.rpm
        local-MPICH = 3.0.4-GCC-4.8.1
        local-GCC = 4.8.1
        rpmlib(PayloadFilesHavePrefix) <= 4.0-1
        rpmlib(CompressedFileNames) <= 3.0.4-1

        $ rpm -qlp local-GCC-4.8.1_x86_64.rpm | head
        /opt/sw/modules/all/GCC/4.8.1
        /opt/sw/software/GCC/4.8.1/bin/c++
        /opt/sw/software/GCC/4.8.1/bin/cpp
        /opt/sw/software/GCC/4.8.1/bin/g++
        /opt/sw/software/GCC/4.8.1/bin/gcc
        /opt/sw/software/GCC/4.8.1/bin/gcc-ar
        /opt/sw/software/GCC/4.8.1/bin/gcc-nm
        /opt/sw/software/GCC/4.8.1/bin/gcc-ranlib
        /opt/sw/software/GCC/4.8.1/bin/gcov
        /opt/sw/software/GCC/4.8.1/bin/gfortran

