# ******************************************************************************
# -*- coding: utf-8 -*-
#
# File    : test_runner.py
# Task    : Runs a test script in a separate process, provides error cleanup
#           and socket communication to a test_control host process.
# Python  : 2.5+
# Python  : 3.6+
#
# Copyright 2012 - 2020 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name     | Description
# ------------------------------------------------------------------------------
# 1.0  | 20.11.2012 | Tremmel  | initial
# 1.1  | 29.01.2013 | Tremmel  | added support for zipped libs
# 1.2  | 07.02.2013 | Tremmel  | added version detection for libs, moved core
#                              | functionality to test_runner_base
# 1.3  | 22.07.2013 | Tremmel  | fixed base_path fallback
# 1.4  | 23.04.2015 | Tremmel  | added additional fallback to ITESTSTUDIO_PATH
# 1.5  | 12.02.2018 | Tremmel  | minor cleanup
# 1.6  | 12.09.2018 | Tremmel  | some reformatting, added doxygen package marker
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0  | 06.12.2019 | Tremmel  | compatibility tweaks to support Py2.5 to Py3.6
# 2.1  | 02.03.2020 | Tremmel  | moved test support libs farther to the front
#                              | in module search path
# 2.2  | 07.09.2020 | Tremmel  | added Python 3.8 to supported versions
# ******************************************************************************
"""
@package test_runner
Utility script wrapper for running a Python test script in a separate process.
Provides error cleanup and socket communication to a test_control host process.

This test_runner script loads support libraries suitable for the available
Python interpreter version, then hands control over to test_runner_base.main().
"""
import sys
import os
import inspect

print("# TestRunner: Python %s" % (sys.version))
_py_ver = sys.version_info[:2]
_supported = ((2, 7), (2, 5), (3, 6), (3, 8))
if _py_ver not in _supported:
    print("> Unsupported Python version: %d.%d" % _py_ver)
    print("# Currently supported Python versions: %s" % (
        ", ".join("%d.%d" % ver for ver in _supported)
    ))

## file name of version-dependent test_support libs bundle
_test_support_libs_name = "test_support%d%d.pyz" % _py_ver

# prefer libs bundle in same folder as test_runner
_base_path = os.path.dirname(inspect.currentframe().f_code.co_filename)
_test_support_libs_path = os.path.join(_base_path, _test_support_libs_name)

# fall back to libs bundle in iTestStudio's libraries folder
if not os.path.isfile(_test_support_libs_path):
    _test_support_libs_path = os.path.join(
        os.environ.get("ITESTSTUDIO_PATH", ""),
        "libraries",
        _test_support_libs_name,
    )
    print("# TestRunner: Using ITESTSTUDIO_PATH for resolving "
          'test support libraries "%s"' % (_test_support_libs_name))

# make test support libs available in module search path
try:
    sys.path.insert(1, _test_support_libs_path)
except IndexError:
    sys.path.append(_test_support_libs_path)

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__":  # pragma: no cover
    try:
        import test_runner_base
    except ImportError:
        # Python 2.5 only supports "except ImportError, ex:"
        # Python 3.6 only supports "except ImportError as ex:"
        # (Python 2.7 accepts both)
        ex = sys.exc_info()[1]
        print('> TestRunner @ "%s":' % (_base_path))
        print('> Failed to import required test support libraries: %s' % (ex))
        print('> Unable to run tests')
        sys.exit(1)

    test_runner_base.main()
# @endcond DOXYGEN_IGNORE
# #############################################################################
