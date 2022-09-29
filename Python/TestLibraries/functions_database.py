#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : functions_database.py
# Task    : functions for common use of database
#
# Author  : A.Neumann
# Date    : 25.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.1   | 25.06.2021 | NeumannA   | initial 
#******************************************************************************

from db_lib.database_lib import DbInterface
import data_common
from functions_diag import HexList


class FunctionsDB(object):
    
    def __init__(self):
        """ Constructor
        
            Parameters:
                -
            Return:
                -
        """
        self.ecudb = DbInterface(data_common.db_path_key) # create the database connection

        # get objects
        
    def getParamList(self, job_name):
        """
            Parameter:
                job_name     - name of diagnostic job
            Info:
                read from database the parameter of this job in a list e.g. [0x1, 0x2]
            return:
                parameter_list
        """
        
        check = self.ecudb.checkIfEntryExist(check_name=job_name)
        
        if check:
            
            param_string = self.ecudb.getDiagParameter(job_name)
            param_string_list = param_string.split(', ')
            param_list = []
            for param in param_string_list:
                if param:
                    param_list.append(int(param.replace('0x', ''), 16))
            
            return param_list
        
        else: 
            raise NameError("Diagnostic Job not found in Database")
        
    def compareResponseWithStoredParam(self, job_name, response, check = False):
        """
            Parameter:
                job_name     - name of diagnostic job
                response     - current response of job
                check        - if False only INFO-verdict, otherwise PASSED/FAILED
            Info:
                read out parameter from db and compare with current response
                write Information if changed or not
            return:
                description, verdict
        """
        verdict = "INFO"
        param_list = self.getParamList(job_name)
        
        if param_list != response:
            verdict = "FAILED" if check else verdict
            description = "Ausgelesene Parameter und Parameter aus der Datenbank weichen voneinander ab"
        else:
            verdict = "PASSED" if check else verdict
            description = "Ausgelesene Parameter und Parameter aus der Datenbank stimmen überein"
        
        db_param_str = str(HexList(param_list))
        resp_param_str = str(HexList(response))
        description += "\nAusgelesene Parameter: %s\nDatenbank Parameter: %s"%(resp_param_str, db_param_str)
        
        return description, verdict
        
    def writeNewParameter2Db(self, job_name, response, check = False):
        """
            Parameter:
                job_name     - name of diagnostic job
                response     - current response of job
                check        - if False only INFO-verdict, otherwise PASSED/FAILED
            Info:
                read out parameter from db and compare with current response
                write Information if changed or not
            return:
                testresult
        """
        
        testresult = []
        description, verdict = self.compareResponseWithStoredParam(job_name, response, check)
        testresult.append([description, verdict])
        
        resp_param_str = str(HexList(response)).replace('[', '').replace(']', '')
        verdict = "INFO"
        try:
            self.ecudb.changeParameterEntry(
                name = job_name, 
                new_entry = resp_param_str)
            
            description = "Neue Parameterwerte in Datenbank geschrieben"
            verdict = "PASSED" if check else verdict
        except:
            verdict = "FAILED" if check else verdict
            description = "Beim Schreiben in die Datenbank ist ein Fehler aufgetreten"
        
        testresult.append([description, verdict])
        
        return testresult
    