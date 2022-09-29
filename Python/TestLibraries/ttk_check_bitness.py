#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : ttk_check_bitness.py
# Task    : Check bitness/architecture of the present TestToolkit release 
#           (on Windows)
#
# Author  : JoTremmel
# Date    : 21.04.2020
# Copyright 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 21.04.2020 | JoTremmel  | initial
#******************************************************************************
import os
import time
import struct

# https://docs.microsoft.com/en-us/windows/win32/debug/pe-format
# Signature (Image Only)
#  After the MS-DOS stub, at the file offset specified at offset 0x3c, is a 
#  4-byte signature that identifies the file as a PE format image file. 
#  This signature is "PE\0\0" (the letters "P" and "E" followed by two null bytes).
#
# COFF File Header (Object and Image)
#  At the beginning of an object file, or immediately after the signature of an 
#  image file, is a standard COFF file header in the following format. 
#  Note that the Windows loader limits the number of sections to 96.

# Offset  Size  Field                 Description
#   0       2   Machine               The number that identifies the type of target machine. 
#   2       2   NumberOfSections      The number of sections. This indicates the size of the section table, 
#                                     which immediately follows the headers.
#   4       4   TimeDateStamp         The low 32 bits of the number of seconds since 00:00 January 1, 1970
#                                     (a C run-time time_t value), that indicates when the file was created.
#   8       4   PointerToSymbolTable  The file offset of the COFF symbol table, or zero if no COFF symbol table is present. 
#                                     This value should be zero for an image because COFF debugging information is deprecated.
#  12       4   NumberOfSymbols       The number of entries in the symbol table. 
#                                     This data can be used to locate the string table, which immediately follows the symbol table. 
#                                     This value should be zero for an image because COFF debugging information is deprecated.
#  16       2   SizeOfOptionalHeader  The size of the optional header, which is required for executable files but not for object files. 
#                                     This value should be zero for an object file.
#  18       2   Characteristics       The flags that indicate the attributes of the file.
#                                     For specific flag values, see Characteristics. 
pe_signature = "PE\0\0"
pe_fmt = "4sHHLLLHH"

machine_types = {
    0x0000: "unknown", # The contents of this field are assumed to be applicable to any machine type
    0x01d3: "Matsushita AM33",
    0x8664: "x64",
    0x01c0: "ARM little endian",
    0xaa64: "ARM64 little endian",
    0x01c4: "ARM Thumb-2 little endian",
    0x0ebc: "EFI byte code",
    0x014c: "x86", # "Intel 386 or later processors and compatible processors",
    0x0200: "Intel Itanium processor family",
    0x9041: "Mitsubishi M32R little endian",
    0x0266: "MIPS16",
    0x0366: "MIPS with FPU",
    0x0466: "MIPS16 with FPU",
    0x01f0: "Power PC little endian",
    0x01f1: "Power PC with floating point support",
    0x0166: "MIPS little endian",
    0x5032: "RISC-V 32-bit address space",
    0x5064: "RISC-V 64-bit address space",
    0x5128: "RISC-V 128-bit address space",
    0x01a2: "Hitachi SH3",
    0x01a3: "Hitachi SH3 DSP",
    0x01a6: "Hitachi SH4",
    0x01a8: "Hitachi SH5",
    0x01c2: "Thumb",
    0x0169: "MIPS little-endian WCE v2"
}


# #############################################################################
def getPEHeader(file_path):
    """ Get contents of PE header from file at supplied path. """
    with open(file_path, "rb") as f:
        # just reading a big chunk is a bit brute-force, 
        # but should be sufficient for now:
        header = f.read(1024)
        pe_start = header.find(pe_signature)
        if pe_start < 0:
            return None

        pe_header = header[pe_start:pe_start + len(pe_signature) + 20]
        fields = struct.unpack(pe_fmt, pe_header)
        
        # (pe_marker, machine, number_of_sections, time_date_stamp,
        #  pointer_to_symbol_table, number_of_symbols,
        #  size_of_optional_header, characteristics) = fields
        return fields[1:]


# #############################################################################
if __name__ == '__main__':
    import inspect
    base_path = os.path.abspath(inspect.currentframe().f_code.co_filename)
    base_path = os.path.dirname(base_path)
    
    file_path = os.path.join(base_path, "ttk_base", "_init_.pyd")
 
    machine, number_of_sections, time_date_stamp = getPEHeader(file_path)[:3]
    architecture = machine_types.get(machine, "unexpected: 0x%X"%(machine))
    datetime     = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time_date_stamp))
    
    #print("File:         %s"%(os.path.basename(file_path)))
    print("# TestToolkit #####################################################")
    print("Architecture: %s"%(architecture))
    print("Created on:   %s"%(datetime))
