#!/usr/bin/python

import commands
import glob
import optparse
import os
import shutil
import string
import sys
import types

version = "2.8"
version_nodot = version.replace(".", "")

option_dict = { 
            "clean"     : (False, "Clean all files from build directories"),
            "debug"     : (False, "Build wxPython with debug symbols"),
            "reswig"    : (False, "Re-generate the SWIG wrappers"),
            "unicode"   : (False, "Build wxPython with unicode support"),
            "no_config" : (False, "Don't run configure when building."),
            "install"   : (False, "Install the built wxPython into installdir"),
            "install_dir": ("", "Directory to install wxPython to."),
            "build_dir" : ("", "Directory to store wx build files."),
          }

parser = optparse.OptionParser(usage="usage: %prog [options]", version="%prog 1.0")

for opt in option_dict:
    default = option_dict[opt][0]
    
    action = "store"
    if type(default) == types.BooleanType:
        action = "store_true"
    parser.add_option("--" + opt, default=default, action=action, dest=opt, help=option_dict[opt][1])

options, arguments = parser.parse_args()

# for cleaning up
def deleteIfExists(deldir):
    if os.path.exists(deldir) and os.path.isdir(deldir):
        shutil.rmtree(deldir)
        
def delFiles(fileList):
    for afile in fileList:
        os.remove(afile)

scriptDir = os.path.abspath(sys.path[0])
scriptName = os.path.basename(sys.argv[0])

SWIGDIR = ""
WXWIN = os.path.abspath(os.path.join(scriptDir, ".."))
myenv = os.environ

if myenv.has_key("WXWIN"):
    WXWIN = myenv["WXWIN"]

if myenv.has_key("SWIGDIR"):
    SWIG_DIR = myenv["SWIGDIR"]

# Windows extension build stuff
build_type_ext = "h"

if options.debug:
    build_type_ext = "d"
    
dll_type = build_type_ext
if options.unicode:
    dll_type = "u" + dll_type
    
# clean the wxPython build files, this part is platform-agnostic
# we do the platform-specific clean below.
if options.clean:
    deleteIfExists(os.path.join(scriptDir, "build"))    
    deleteIfExists(os.path.join(scriptDir, "build.unicode"))
        
    files = glob.glob(os.path.join(scriptDir, "wx", "*.pyd")) + \
            glob.glob(os.path.join(scriptDir, "wx", "*.so"))

    delFiles(files)

print "wxWidgets directory is: %s" % WXWIN

if sys.platform.startswith("win"):
    dllDir = os.path.join(WXWIN, "lib", "vc_dll")

    if options.clean:    
        deleteIfExists(os.path.join(dllDir, "msw" + dll_type + ""))
        delFiles(glob.glob(os.path.join(dllDir, "wx*" + version_nodot + dll_type + "*.*")))
        delFiles(glob.glob(os.path.join(dllDir, "*%s.*" % dll_type)))
        delFiles(glob.glob(os.path.join(dllDir, "*%s.*" % build_type_ext)))
        sys.exit(0)
    
    # FIXME: add code to handle Cygwin case
    if myenv.has_key("SWIGDIR"):
        myenv["PATH"] = myenv["SWIGDIR"] + ";%PATH%"
          
else:
    WXPY_BUILD_DIR = os.path.join(os.getcwd(), "wxpy-bld")
    WXPY_INSTALL_DIR = os.path.join(os.environ["HOME"], "wxpython-" + version)
    
    if options.build_dir != "":
        WXPY_BUILD_DIR = options.build_dir
    
    if options.install_dir != "":
        WXPY_INSTALL_DIR = options.install_dir
        
    if options.clean:
        deleteIfExists(WXPY_BUILD_DIR)
        deleteIfExists(WXPY_INSTALL_DIR)
        sys.exit(0)

    if not os.path.exists(WXPY_BUILD_DIR):
        os.mkdir(WXPY_BUILD_DIR)
        
    os.chdir(WXPY_BUILD_DIR)
    
# now that we've done platform setup, start the common build process
build_options = []
wxpy_build_options = []
if options.unicode:
    build_options.append("--unicode")
    wxpy_build_options.append("UNICODE=1")
    
if options.debug:
    build_options.append("--debug")
    
if options.no_config:
    build_options.append("--no_config")

if not sys.platform.startswith("win") and options.install:    
    build_options.append('--installdir="%s"' % WXPY_INSTALL_DIR)
    build_options.append("--install")

retval = os.system(WXWIN + "/build/tools/build-wxwidgets.py --wxpython %s" % string.join(build_options, " "))
if retval != 0:
    print "ERROR: failed building wxWidgets"
    sys.exit(1)

if sys.platform.startswith("win"):
    dlls = glob.glob(os.path.join(dllDir, "wx*" + version_nodot + dll_type + "*.dll"))
    for dll in dlls:
        shutil.copyfile(dll, os.path.join(WXWIN, "wxPython", "wx", os.path.basename(dll)))

os.chdir(os.path.join(WXWIN, "wxPython"))

USE_SWIG = 0
if sys.platform.startswith("win"):
    SWIG_BIN = 'C:\\SWIG-1.3.29\swig.exe'
else:
    SWIG_BIN = commands.getoutput("which swig")

if options.reswig:
    if os.path.exists(SWIGDIR):
        SWIG_BIN = os.path.join(SWIGDIR, "swig")
    
    if not os.path.exists(SWIG_BIN) and not sys.platform.startswith("win"):
        wxpy_build_options.append('SWIG_BIN="%s"' % "/opt/swig/bin/swig")
        
    if os.path.exists(SWIG_BIN):
        wxpy_build_options.append('SWIG_BIN="%s"' % SWIG_BIN)
        wxpy_build_options.append("USE_SWIG=%d" % 1)
    else:
        wxpy_build_options.append("USE_SWIG=%d" % 0)
        print "WARNING: Unable to find SWIG binary. Not re-SWIGing files."

build_mode = "build_ext --inplace"

if not sys.platform.startswith("win"):
    if options.install:
        wxpy_build_options.append("WX_CONFIG=%s/bin/wx-config" % WXPY_INSTALL_DIR)
    else:
        wxpy_build_options.append("WX_CONFIG=%s/wx-config" % WXPY_BUILD_DIR)

os.chdir(scriptDir)
command = sys.executable + " ./setup.py %s %s" % \
            (build_mode, string.join(wxpy_build_options, " "))
print command
retval = os.system(command)

if retval != 0:
    print "ERROR: failed building wxPython."
    sys.exit(retval)

# update the language files
retval = os.system(sys.executable + " " + os.path.join(WXWIN, "wxPython", "distrib", "makemo.py"))
    
if retval != 0:
    print "ERROR: failed generating language files"
    sys.exit(1)  


print "------------ BUILD FINISHED ------------"
print ""
print "To run the wxPython demo:"
print ""
print " - Set your PYTHONPATH variable to %s." % WXWIN
if not sys.platform.startswith("win") and not options.install:
    print " - Set your (DY)LD_LIBRARY_PATH to %s" % WXPY_BUILD_DIR + "/lib"
print " - Run python demo/demo.py"
print ""

