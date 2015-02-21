#!/usr/bin/env python2

import re
import sys
import subprocess
from optparse import OptionParser

def main():
    (options, args) = getopts()
    mods = set()
    for arg in args:
        mods.add(arg)
        deps = get_dependencies(arg)
        mods = mods.union(deps)
    for mod in mods:
        build_package(mod, options.pkgtype, options.prefix)

def getopts():
    parser = OptionParser()
    parser.add_option("-t", "--type", dest="pkgtype", default="rpm",
                      help="Type of package to build")
    parser.add_option("-p", "--prefix", dest="prefix", default="",
                      help="Package name prefix")
    (options, args) = parser.parse_args()
    return (options, args)

def failmsg(msg):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)

def module2path(modname):
    modshow = subprocess.Popen(['modulecmd', 'python', 'show', modname],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()[1]
    modlines = modshow.split('\n')
    return modlines[1][:-1]

def get_root(modname):
    modulefile = module2path(modname)
    check_root = re.compile("^\s*set\s+root\s+(.+)$")
    with open(modulefile, 'r') as f:
        lines = f.readlines()
    for line in lines:
        m = check_root.match(line)
        if m:
            root = m.group(1).strip()
            break
    return root

def get_dependencies(modname):
    modulefile = module2path(modname)
    check_load = re.compile("^\s*module\s+load(.+)$")
    check_prereq = re.compile("^\s*prereq\s+(.+)$")
    deps = set()
    with open(modulefile, 'r') as f:
        lines = f.readlines()
    for line in lines:
        m = check_load.match(line)
        if m:
            deps.add(m.group(1).strip())
            continue
        m = check_prereq.match(line)
        if m:
            deps.add(m.group(1).strip())
            continue
    for dep in deps:
        deps = deps.union(get_dependencies(dep))
    return deps

def module_version(modname):
    return modname.split('/')[-1]

def module_name(modname):
    return modname.split('/')[0]

def fix_prefix(prefix):
    if prefix != "":
       if prefix[-1] != '-':
           prefix = "%s-" % prefix
    return prefix

def build_package(modname, pkgtype, prefix):
    root = get_root(modname)
    mname = module_name(modname).strip()
    version = module_version(modname).strip()
    prefix = fix_prefix(prefix)
    if mname == version: version = 'NOVERSION'
    mname = "%s%s" % (prefix, mname)
    mpath = module2path(modname)
    cmd = "fpm -s dir -t %s -n %s -v %s -p %s-VERSION_ARCH.%s -C / %s %s" % (pkgtype, mname, version, mname, pkgtype, root, mpath)
    print cmd
    p = subprocess.Popen(cmd.split())
    p.wait()

if __name__ == '__main__':
    main()
