#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : verdicts.py
# Package : ttk_checks
# Task    : defined test status verdicts (interface to _verdicts.py)
# Type    : Interface
#
# Author  : J.Tremmel 
# Copyright 2011 - 2017 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date       | Author  | Description
#------------------------------------------------------------------------------
# 1.0  | 28.10.2011 | Tremmel | initial
# 1.1  | 22.08.2012 | Tremmel | added convenience function getResultingVerdict()
# 1.2  | 04.02.2014 | Felkl   | review correction
# 1.3  | 17.12.2015 | Tremmel | split into interface and base implementation
# 1.4  | 08.09.2017 | Tremmel | improved documentation
#******************************************************************************
""" 
@package ttk_checks.verdicts
Interface wrapper for defined test status verdicts in ttk_checks._verdicts.

Defined test status verdicts are 
 * `PASSED        ` -- ttk_checks._verdicts.PASSED
 * `FAILED        ` -- ttk_checks._verdicts.FAILED
 * `ERROR         ` -- ttk_checks._verdicts.ERROR
 * `RETEST PASSED ` -- ttk_checks._verdicts.RETEST_PASSED

See ttk_checks._verdicts for detailed definitions.

### Test Verdicts, Ordered By Priority

Verdict       | Description                                     | Verdict Class
:------------:|:------------------------------------------------|:------------:
FAILED        | Test step failed                                | Failed
ERROR         | Error during test execution (in tool, script)   | Failed
RETEST PASSED | A manual re-test of a test step was passed      | Passed
PASSED        | Test step successfully completed                | Passed
NOT TESTED    | Test step currently not evaluated               | n/a
NOT SPECIFIED | Test step currently has no specification        | n/a
NOT PLANNED   | Evaluation of this test step is not planned     | n/a
INFO          | Test step only contain information              | n/a

Standard -- and commonly used -- verdicts are `PASSED`, `FAILED` and `ERROR`.

Other verdicts such as `INFO` or `TODO` (or even a blank verdict) __will__
appear in the test report, but will __not__ be evaluated or influence the 
overall test result.

See also https://wiki.isyst.de/wiki/Testbewertungen
"""
import _verdicts

## defined test status verdicts
from _verdicts import PASSED, FAILED, ERROR, RETEST_PASSED

## Verdict categories.
# all verdicts not in those categories are considered to be "information only"
from _verdicts import PASS_VERDICTS, FAIL_VERDICTS # @UnusedImport


# #############################################################################
def getResultingVerdict(verdicts):
    """ Get the resulting verdict for a set or sequence of verdicts.
        Priority of actual pass/fail verdicts is determined by PASS_VERDICTS
        and FAIL_VERDICTS.
        
        Parameters:
            verdicts - a verdict set/sequence (list, tuple, dict (keys))
            
        Returns `FAILED` if at least one result is failed,   
            `ERROR` if errors occurred without an explicit failed result,  
            `PASSED` (or `RETEST PASSED`, if applicable) if passed results
             exist without any failed results, otherwise an empty verdict.  
    """
    return _verdicts.getResultingVerdict(verdicts)


# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################   
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    print
    print "# getResultingVerdict #############################################"
    # see unittest_verdicts.py
    print PASSED, "=>", getResultingVerdict(['FOO', 'BAR', 'BAZ', PASSED])
    print FAILED, "=>", getResultingVerdict(['FOO', FAILED, 'BAR', 'BAZ'])
    print FAILED, "=>", getResultingVerdict(['FOO', FAILED, 'BAR', 'BAZ', ERROR])
    print FAILED, "=>", getResultingVerdict(['FOO', FAILED, 'BAR', PASSED])
    print RETEST_PASSED, "=>", getResultingVerdict(['FOO', RETEST_PASSED, 'BAR', PASSED])
    print "<nothing>",   "=>", getResultingVerdict(['FOO', 'BAR', 'BAZ'])
    
    print
    print "# Verdict Categories  #############################################"
    print '# Note: verdicts are defined in order of "override" priority inside one category'
    print '#       e.g.  RETEST_PASSED > PASSED'
    print "PASS VERDICTS:", PASS_VERDICTS
    print "FAIL VERDICTS:", FAIL_VERDICTS
    
# @endcond DOXYGEN_IGNORE
# #############################################################################