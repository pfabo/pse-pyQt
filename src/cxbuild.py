#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Build pse to the executable form.

You have to add argument build
'''
# http://bytes.com/topic/python/answers/490563-distributing-app-frozen-cx_freeze
# http://stackoverflow.com/questions/20495620/

import sys

from cx_Freeze import setup, Executable


WINDIRLST = [(r'C:\Python34\Lib\site-packages\PyQt5\libEGL.dll', '')]

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
targetName = "PSE"

if sys.platform == "win32":
    #base = "Win32GUI"  # uncomment when you want pse without black terminal window on windows
    targetName = "PSE.exe"

Target_1 = Executable(script=r"main.py",
                      initScript=None,
                      base=base,
                      targetName=targetName,
                      # icon="icons/pse.ico"
                      )

excludes = ["pywin", "tcl", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list", "win32com.server",
            'Tkinter', 'tkinter',
            '_gtkagg', '_tkagg', '_agg2', '_wxagg',
            '_cairo', '_cocoaagg',
            '_fltkagg', '_gtk', '_gtkcairo', 'PyQt4',
            'scipy', 'h5py', 'plugins',
            'xmlrpc', 'ssl', 'lib']

includes = ["PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets",
            "numpy", 'email', 'zlib', 'matplotlib']

if sys.platform != "win32":
    pass
    # includes.extend(["win32gui", "win32com", "win32api"])

packages = ['sip', 'numpy']
path = []

include_files = []
if sys.platform == "win32":  # Add libEGL.dll
    include_files = WINDIRLST
else:
    pass
    # include_files = [(r'../plugins', '')]
                        # (r'/usr/lib64/python3.4/site-packages/h5py', '')]

setup(version='0.0.8',
      description="Python and Simulator and Editor",
      long_description="Python Simulator and Editor",
      keywords='keywords',
      url="http://www.kiwiki.info/index.php/PySimEd",
      license='GNU-GPL',
      download_url='',
      name="",
      author='',
      author_email="",
      maintainer="",
      maintainer_email="",

      options={"build_exe": {  "includes": includes,
                               "excludes": excludes,
                               "packages": packages,
                               "path": path,
                               'include_files': include_files,
                            }},
      executables=[Target_1])

# pth = os.path.join(os.curdir, r'build')
# openfile_system(pth)  # @UndefinedVariable #pylint: disable=E1101
