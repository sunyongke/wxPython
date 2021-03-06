#!/usr/bin/env python
###############################################################################
# Name: setup.py                                                              #
# Purpose: Setup/build script for Editra                                      #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
 Editra Setup Script

 USAGE:

   1) Windows:
      - python setup.py py2exe

   2) MacOSX:
      - python setup.py py2app

   3) Boil an Egg
      - python setup.py bdist_egg

   4) Install as a python package
      - python setup.py install

 @summary: Used for building the editra distribution files and installations

"""
__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#---- Imports ----#
import os
import sys
import glob
import src.info as info
import src.syntax.synextreg as synextreg # So we can get file extensions

#---- System Platform ----#
__platform__ = os.sys.platform

#---- Global Settings ----#
APP = ['src/Editra.py']
AUTHOR = "Cody Precord"
AUTHOR_EMAIL = "staff@editra.org"
YEAR = 2008

CLASSIFIERS = [
            'Development Status :: 3 - Alpha',
            'Environment :: MacOS X',
            'Environment :: Win32 (MS Windows)',
            'Environment :: X11 Applications :: GTK',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved',
            'Natural Language :: English',
            'Natural Language :: Chinese (Simplified)',
            'Natural Language :: Chinese (Traditional)',
            'Natural Language :: Czech',
            'Natural Language :: Dutch',
            'Natural Language :: French',
            'Natural Language :: German',
            'Natural Language :: Italian',
            'Natural Language :: Japanese',
            'Natural Language :: Norwegian',
            'Natural Language :: Portuguese (Brazilian)',
            'Natural Language :: Russian',
            'Natural Language :: Serbian',
            'Natural Language :: Spanish',
            'Natural Language :: Turkish',
            'Natural Language :: Ukranian',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: Text Editors'
            ]

def GenerateBinPackageFiles():
    """Generate the list of files needed for py2exe/py2app package files"""
    data = [("include/python2.5",
               glob.glob("include/python2.5/%s/*" % __platform__)),
              ("pixmaps/theme/Default", ["pixmaps/theme/Default/README"]),
              ("pixmaps/theme/Tango",["pixmaps/theme/Tango/AUTHORS",
                                      "pixmaps/theme/Tango/COPYING"]),
              ("pixmaps/theme/Tango/toolbar",
               glob.glob("pixmaps/theme/Tango/toolbar/*.png")),
              ("pixmaps/theme/Tango/menu",
               glob.glob("pixmaps/theme/Tango/menu/*.png")),
              ("pixmaps/theme/Tango/mime",
               glob.glob("pixmaps/theme/Tango/mime/*.png")),
              ("pixmaps/theme/Tango/other",
               glob.glob("pixmaps/theme/Tango/other/*.png")),
              ("styles", glob.glob("styles/*.ess")),
              ("tests/syntax", glob.glob("tests/syntax/*")),
              ("docs", glob.glob("docs/*.txt")), "AUTHORS", "FAQ", "INSTALL",
              "README","CHANGELOG","COPYING", "NEWS", "THANKS", "TODO",
              "setup.cfg"
            ]

    # Get the locale files
    for loc_dir in os.listdir("locale"):
        tmp = "locale/" + loc_dir + "/LC_MESSAGES"
        if os.path.isdir(tmp):
            tmp2 = tmp + "/Editra.mo"
            if os.path.exists(tmp2):
                data.append((tmp, [tmp2]))

    # Only bundle the plugins for the running version of python being used for
    # the build.
    data.append(("plugins",
                 glob.glob("plugins/*py%d.%d.egg" % sys.version_info[:2])))

    # Get platform specific icons
    pixlist = ["pixmaps/editra.png", "pixmaps/editra_doc.png"]

    if "darwin" in sys.platform:
        data.append("pixmaps/editra_doc.icns")
        pixlist.extend(["pixmaps/editra.icns", "pixmaps/editra_doc.icns"])
    elif sys.platform.startswith("win"):
        pixlist.append("pixmaps/editra.ico")

    data.append(("pixmaps", pixlist))

    return data

def GenerateSrcPackageFiles():
    """Generate the list of files to include in a source package dist/install"""
    data = [ "src/*.py", "src/syntax/*.py", "src/autocomp/*.py", 
             "src/eclib/*.py", "docs/*.txt", "pixmaps/*.png", "pixmaps/*.ico",
             'Editra',
             "src/extern/*.py", "src/extern/pygments/*.py",
             "src/extern/pygments/formatters/*.py",
             "src/extern/pygments/filters/*.py",
             "src/extern/pygments/lexers/*.py",
             "src/extern/pygments/styles/*.py",
             "pixmaps/*.icns",
             "pixmaps/theme/Default/README",
             "pixmaps/theme/Tango/AUTHOR",
             "pixmaps/theme/Tango/COPYING",
             "pixmaps/theme/Tango/toolbar/*.png",
             "pixmaps/theme/Tango/menu/*.png",
             "pixmaps/theme/Tango/mime/*.png",
             "pixmaps/theme/Default/README",
             "pixmaps/theme/Tango/other/*.png",
             "styles/*.ess", "tests/syntax/*",
             "AUTHORS", "CHANGELOG","COPYING", "FAQ", "INSTALL", "NEWS", 
             "README", "THANKS", "TODO", "setup.cfg" ]

    # Get the local files
    for loc_dir in os.listdir("locale"):
        tmp = "locale/" + loc_dir
        if os.path.isdir(tmp):
            tmp = tmp + "/LC_MESSAGES/Editra.mo"
            if os.path.exists(tmp):
                data.append(tmp)

    # NOTE: plugins selected to package in build step
    
    return data


DESCRIPTION = "Developer's Text Editor"

LONG_DESCRIPT = \
r"""
========
Overview
========
Editra is a multi-platform text editor with an implementation that focuses on
creating an easy to use interface and features that aid in code development.
Currently it supports syntax highlighting and variety of other useful features
for over 60 programing languages. For a more complete list of features and
screenshots visit the projects homepage at `Editra.org
<http://www.editra.org/>`_.

============
Dependancies
============
  * Python 2.4+
  * wxPython 2.8.3+ (Unicode build suggested)
  * setuptools 0.6+

"""

ICON = { 'Win' : "pixmaps/editra.ico",
         'WinDoc' : "pixmaps/editra_doc.ico",
         'Mac' : "pixmaps/Editra.icns"
}

# Explicitly include some libraries that are either loaded dynamically
# or otherwise not able to be found by py2app/exe
INCLUDES = ['syntax.*', 'ed_log', 'shutil', 'subprocess', 'zipfile',
            'pygments.*', 'pygments.lexers.*', 'pygments.formatters.*',
            'pygments.filters.*', 'pygments.styles.*']
if sys.platform.startswith('win'):
    INCLUDES.extend(['ctypes'])
else:
    INCLUDES.extend(['pty', 'tty'])

LICENSE = "wxWindows"

NAME = "Editra"

URL = "http://editra.org"

VERSION = info.VERSION

MANIFEST_TEMPLATE = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24
#---- End Global Settings ----#

#---- Setup Windows EXE ----#
if __platform__ == "win32" and 'py2exe' in sys.argv:
    from distutils.core import setup
    try:
        import py2exe
    except ImportError:
        print "\n!! You dont have py2exe installed. !!\n"
        exit()

    # put package on path for py2exe
    sys.path.append(os.path.abspath('src/'))
    sys.path.append(os.path.abspath('src/extern'))

    setup(
        name = NAME,
        version = VERSION,
        options = {"py2exe" : {"compressed" : 1,
                               "optimize" : 1,
                               "bundle_files" : 2,
                               "includes" : INCLUDES }},
        windows = [{"script": "src/Editra.py",
                    "icon_resources": [(0, ICON['Win'])],
                    "other_resources" : [(RT_MANIFEST, 1,
                                          MANIFEST_TEMPLATE % dict(prog=NAME))],
                  }],
        description = NAME,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        maintainer = AUTHOR,
        maintainer_email = AUTHOR_EMAIL,
        license = LICENSE,
        url = URL,
        data_files = GenerateBinPackageFiles(),
        )

#---- Setup MacOSX APP ----#
elif __platform__ == "darwin" and 'py2app' in sys.argv:
    # Check for setuptools and ask to download if it is not available
    import src.extern.ez_setup as ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

    PLIST = dict(CFBundleName = info.PROG_NAME,
             CFBundleIconFile = 'Editra.icns',
             CFBundleShortVersionString = info.VERSION,
             CFBundleGetInfoString = info.PROG_NAME + " " + info.VERSION,
             CFBundleExecutable = info.PROG_NAME,
             CFBundleIdentifier = "org.editra.%s" % info.PROG_NAME.title(),
             CFBundleDocumentTypes = [dict(CFBundleTypeExtensions=synextreg.GetFileExtensions(),
                                           CFBundleTypeIconFile='editra_doc',
                                           CFBundleTypeRole="Editor"
                                          ),
                                     ],
             CFBundleTypeMIMETypes = ['text/plain',],
             CFBundleDevelopmentRegion = 'English',
# TODO Causes errors with the system menu translations and text rendering
#             CFBundleLocalizations = ['English', 'Spanish', 'French', 'Japanese'],
#             ['de_DE', 'en_US', 'es_ES', 'fr_FR',
#                                      'it_IT', 'ja_JP', 'nl_NL', 'nn_NO',
#                                      'pt_BR', 'ru_RU', 'sr_SR', 'tr_TR',
#                                      'uk_UA', 'zh_CN'],
       #      NSAppleScriptEnabled="YES",
             NSHumanReadableCopyright = u"Copyright %s 2005-%d" % (AUTHOR, YEAR)
             )

    PY2APP_OPTS = dict(iconfile = ICON['Mac'],
                       argv_emulation = True,
                       optimize = True,
                       includes = INCLUDES,
                       plist = PLIST)

    # Add extra mac specific files
    DATA_FILES = GenerateBinPackageFiles()
    DATA_FILES.append("scripts/editramac.sh")

    # Put extern package on path for py2app
    sys.path.append(os.path.abspath('src/extern'))

    setup(
        app = APP,
        version = VERSION,
        options = dict( py2app = PY2APP_OPTS),
        description = DESCRIPTION,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        maintainer = AUTHOR,
        maintainer_email = AUTHOR_EMAIL,
        license = LICENSE,
        url = URL,
        data_files = DATA_FILES,
        setup_requires = ['py2app'],
        )

#---- Other Platform(s)/Source module install ----#
else:

    # Get the package data
    DATA = GenerateSrcPackageFiles()

    # Force optimization
    if 'install' in sys.argv and ('O1' not in sys.argv or '02' not in sys.argv):
        sys.argv.append('-O2')

        # Install the plugins for this version of Python
        DATA.append("plugins/*py%d.%d.egg" % sys.version_info[:2])

    # Import proper setup function
    if 'bdist_egg' in sys.argv:
        try:
            from setuptools import setup

            # Only bundle eggs for the given python version
            DATA.append("plugins/*py%d.%d.egg" % sys.version_info[:2])
        except ImportError:
            print "To build an egg setuptools must be installed"
    else:
        from distutils.core import setup

    setup(
        name = NAME,
        scripts = ['Editra', 'Editra.pyw'],
        version = VERSION,
        description = DESCRIPTION,
        long_description = LONG_DESCRIPT,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        maintainer = AUTHOR,
        maintainer_email = AUTHOR_EMAIL,
        url = URL,
        download_url = "http://editra.org/?page=download",
        license = LICENSE,
        platforms = [ "Many" ],
        packages = [ NAME ],
        package_dir = { NAME : '.' },
        package_data = { NAME : DATA },
        classifiers= CLASSIFIERS,
        )
