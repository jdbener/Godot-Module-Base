#!/usr/bin/env python

import os, sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-j", "--jobs", type="int", dest="jobs", help="The number of threads that should be used for compilation [default=1]", default="1")
parser.add_option("-p", "--platforms", type="string", dest="platforms", help="Comma separated list of platforms to compile support for [default=Detected current system platform]", default="")
parser.add_option("--submodule_name", type="string", dest="submodule_name", help="The name of the submodule provided to godot [default=game]", default="game")

(opts, args) = parser.parse_args()
if(" " in opts.submodule_name):
    print("The submodule name can't contain spaces! (Replace them with underscores!)")
    exit(-1)


print("Updating submodules ...")
os.system("git submodule update --recursive")

print("Changing submodule name ...")
for file in ["src/register_types.cpp", "src/register_types.h"]:
    f = open(file, "r").read();
    f = f.replace("register_game_types", "register_" + opts.submodule_name + "_types").replace("unregister_game_types", "unregister_" + opts.submodule_name + "_types")
    open(file, "w").write(f);

print("Creating links ...")
if sys.platform == "win32": os.system("mklink /D engine/modules/" + opts.submodule_name + " src")
else: os.system("ln -s ../../src/ engine/modules/" + opts.submodule_name)

print("Preforming initial compilation ...")
platforms = opts.platforms.split(",")
if len(opts.platforms) > 0:
    for platform in platforms:
        print("Compiling for " + platform + " ...")
        os.system("scons platform=" + platform + " -j" + str(opts.jobs))
else:
    os.system("scons -j" + str(opts.jobs))
