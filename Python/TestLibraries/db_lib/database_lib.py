#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : database_lib.py
# Task    : Read/Write data from/to a database
#
# Author  : Anna Neumann
# Date    : 25.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 25.06.2021 | A. Neumann | Initial
#******************************************************************************

from __future__ import with_statement
import sqlite3 as sqlite
import datetime

# CONSTANTS

DB_FILE_NAME = "waehlhebel_database.db"

# lookup tables for values and variables
lookup_diag_parameter = {
    "TABLE":                "waehlhebel_diag_parameter",
    "NAME":                 "diag_name",
    "JOB":                  "diag_job",
    "PARAMETER":            "diag_parameter",
    }


class DbInterface(object):
    """ Class for a ecu data database """
    def __init__(self, db_path):
        """ Constructor
            Parameters:
                self    - self
                db_path - path to database
        """
        self.conn = sqlite.connect(db_path)
        self.c = self.conn.cursor()
    
    # -------------------------------------------------------------------------
    # Functions for Values Database "clar_we_values"
    # -------------------------------------------------------------------------
    def getDiagJob(self, name, field="JOB"):
        """ Get the Value from database
                
            Parameters:
                self        - self
                name        - name of the constant
                field       - name of the column (default = JOB)
            Return:
                Value as a string
        """
        return self._getData(name, lookup_diag_parameter, lookup_diag_parameter[field])

    def getDiagParameter(self, name, field="PARAMETER"):
        """ Get the Unit from database
                
            Parameters:
                self        - self
                name        - name of the constant (Value)
                field       - name of the column (default = PARAMETER)
            Return:
                Unit as string
        """
        return self._getData(name, lookup_diag_parameter, lookup_diag_parameter[field])
    
    def checkIfEntryExist(self, check_name):
        """ Check if entry in value db with this name exist
        
            Parameters:
                self        - self
                name        - name of the constant (Value)
        """
        return self._checkIfNameExist(check_name, lookup_diag_parameter)
    
    
    def changeParameterEntry(self, name, new_entry, change_field = 'PARAMETER'):
        """ Check if entry in value db with this name exist
        
            Parameters:
                self        - self
                name        - name of the constant (Value)
        """
        return self._changeEntry(name, lookup_diag_parameter, change_field, new_entry)

    
    # def addValueEntry(self, name, value, dataformat, unit, description):
    #
    #
        # query = """INSERT INTO %s (name, value, dataformat, unit, description) VALUES(\"%s\", \"%s\", \"%s\", \"%s\", \"%s\")""" %(lookup_values['TABLE'], name, value, dataformat, unit, description)
        #
        # return self._commit(query)
    
       # -------------------------------------------------------------------------
    # internal functions
    # -------------------------------------------------------------------------
    def _getData(self, name, lookuptable, field):
        """ Get data of a unique field from database.
            If data not available raises an exception
            Parameters:
                self        - self
                name        - name of the variable
                field       - target field of database
                
            Return: data from database or exception
        """
        
        query = "SELECT %s FROM %s\
             WHERE %s = \"%s\";" % (field,
                                lookuptable["TABLE"],
                                lookuptable["NAME"],
                                name)
        
        dbresponse = self._sendQuery(query)
        if len(dbresponse) == 0: # expected a list with a tuple: [(mydata),]
            raise Exception("Registry %s not found in database!"%name)
        if len(dbresponse) > 1: # expected a list with a tuple: [(mydata),]
            raise Exception("Database inconsistency! More than one result")
        else:
            return dbresponse[0][0]
    
    def _getDataById(self, id, lookuptable, field):
        """ Get data of a unique field from database.
            If data not available raises an exception
            Parameters:
                self        - self
                name        - name of the variable
                field       - target field of database
                
            Return: data from database or exception
        """
        
        query = "SELECT %s FROM %s\
             WHERE %s = \"%s\";" % (field,
                                lookuptable["TABLE"],
                                lookuptable["ID"],
                                id)
        
        dbresponse = self._sendQuery(query)
        if len(dbresponse) == 0: # expected a list with a tuple: [(mydata),]
            raise Exception("Registry %s not found in database!"%id)
        if len(dbresponse) > 1: # expected a list with a tuple: [(mydata),]
            raise Exception("Database inconsistency! More than one result")
        else:
            return dbresponse[0][0]

    
    def _sendQuery(self, query):
        """ Run a query
            Parameters:
                self    - self
                query   - sql query
        """
        self.c.execute(query)
        return self.c.fetchall()
    
    def _commit(self, query):
        """ Commit changes into database
            Parameters:
                self    - self
                query   - sql query
        """
        print "Send query: %s" % (query)
        self.c.execute(query)
        self.conn.commit()
    
    def _convertToString(self, lst):
        """ Convert a list of integers into a string with format: "[0x1A,0x12...]"
        
            Parameters:
                self      - self
                lst       - list of integers
            
            Return:
                List formated as string: e.g: "[0x1A,0x12,0xAA...]"
        """
        return ",".join("0x%02X" % i for i in lst)
    
    def _checkIfNameExist(self, name, lookup_table):
        """ Check if entry in value db with this name exist
        
            Parameters:
                self         - self
                name         - name of the constant (Value)
                lookup_table - name of the database table
            
            Return:
                True if exist, False if not exist
        """
        query = "SELECT %s FROM %s\
             WHERE %s = ?" % (lookup_table["NAME"],
                                lookup_table["TABLE"],
                                lookup_table["NAME"])
        self.c.execute(query, (name,))
        exists = self.c.fetchall()
        if not exists:
            return False
        else: 
            return True
        
    def _checkIfIdExist(self, id, lookup_table):
        """ Check if entry in value db with this name exist
        
            Parameters:
                self         - self
                name         - name of the constant (Value)
                lookup_table - name of the database table
            
            Return:
                True if exist, False if not exist
        """
        query = "SELECT %s FROM %s\
             WHERE %s = ?" % (lookup_table["NAME"],
                                lookup_table["TABLE"],
                                lookup_table["NAME"])
        self.c.execute(query, (id,))
        exists = self.c.fetchall()
        if not exists:
            return False
        else: 
            return True
    
    def _changeEntry(self, name, lookup_table, field, new_entry):
        """
            Parameters: 
                self          - self
                name          - name of the constant (Value)
                lookup_table  - name of the database table
                change_field  - name of the change field (e.g. value, dataformat, ..)
                new_entry     - new entry in database
            
            Return:
                
        """
        
        query = "UPDATE %s SET %s = \"%s\" WHERE %s = \"%s\";" %(lookup_table["TABLE"],
                                lookup_table[field.upper()], new_entry,
                                lookup_table["NAME"], name)
        
        self._commit(query)
        
        
    def __del__(self):
        """ Destructor. Close the databse connection
            Parameters:
                self    - self
        """
        self.conn.close()

