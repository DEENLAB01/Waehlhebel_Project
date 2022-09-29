# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : ECU_Identifikation.py
# Title   : ECU Identifikation
# Task    : Überblick aller Test- und ECU-relevanten Daten
#
# Author  : S. Stenger
# Date    : 31.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 31.05.2021 | StengerS   | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport

import functions_database


# Instantiate test environment
testenv = TestEnv()


try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    func_db = functions_database.FunctionsDB()

    # variables ###############################################################
    diag_read_parameter =    [  # [ diag job, new entry ]
                                 'ECU Serial Number',
                                 'VW Application Software Version Number',
                                 'VW Spare Part Number',
                                 'VW System Name Or Engine Type',
                                 'VW ECU Hardware Number',
                                 'VW ECU Hardware Version Number',
                                 'VW Workshop System Name',
                                 'VW FAZIT Identification String',
                                 'System Supplier Identifier',
                                 'System Supplier ECU Hardware Number',
                                 'System Supplier ECU Hardware Version Number',
                                 'System Supplier ECU Software Number',
                                 'System Supplier ECU Software Version Number',
                                 'Fingerprint And Programming Date Of Logical Software Blocks',
                             ]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+0]", ""])

    for job in diag_read_parameter:
        diag_ident = identifier_dict[job]
        job_name = diag_ident['name']

        testresult.append(["[.] Lese aktuelle %s aus"%job, ""])
        identifier = diag_ident['identifier']
        request = [0x22] + identifier
        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)
        testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])

        sw_version = ''.join(chr(i) for i in response[3:])
        testresult.append(["Aktuelle %s: %s" %(job, sw_version), ""])

        # store current data into database
        testresult.extend(func_db.writeNewParameter2Db(job_name, response[3:]))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU (KL15 aus, KL30 aus)", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
