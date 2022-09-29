# -*- coding: latin-1 -*-
# minimal stub


class matlablibError(Exception):
    pass


class Matfile(object):
    def Open(self,  *args, **kwargs):
        print "## [matlablib_stub] Matfile.Open:    ", args, kwargs

    def PutArray(self, *args, **kwargs):
        print "## [matlablib_stub] Matfile.PutArray:", args, kwargs

    def Close(self,  *args, **kwargs):
        print "## [matlablib_stub] Matfile.Close:   ", args, kwargs

    def GetDir(self,  *args, **kwargs):
        print "## [matlablib_stub] Matfile.GetDir:  ", args, kwargs
        return []

    def GetArray(self,  *args, **kwargs):
        print "## [matlablib_stub] Matfile.GetArray:", args, kwargs
        return []

