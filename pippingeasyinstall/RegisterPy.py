# -*- encoding: utf-8 -*-
#
# script to register Python 2.0 or later for use with win32all
# and other extensions that require Python registry settings
#
# Adapted by Matt Hampton from a script
# adapted by Ned Batchelder from a script
# written by Joakim Löw for Secret Labs AB / PythonWare
#
# source:
# http://www.pythonware.com/products/works/articles/regpy20.htm

import sys

try:
    from _winreg import *
except:
    pass

# tweak as necessary
version = sys.version[:3]
installpath = sys.prefix

regpath = "SOFTWARE\\Python\\Pythoncore\\%s\\" % (version)
installkey = "InstallPath"
pythonkey = "PythonPath"
pythonpath = "%s;%s\\Lib\\;%s\\DLLs\\" % (
    installpath, installpath, installpath
)

class RegisterPy(object):

    def __enter__(self):
        self.a_set = False
        self.b_set = False
        self.created = False
        try:
            reg = OpenKey(HKEY_LOCAL_MACHINE, regpath)
        except EnvironmentError:
            reg = CreateKey(HKEY_LOCAL_MACHINE, regpath)
            self.created = True


        try:
            self.prev_values = {
                installkey: "" if self.created else QueryValue(reg, installkey),
                pythonkey: "" if self.created else QueryValue(reg, pythonkey)
            }
            if self.prev_values[installkey] != installpath:
                SetValue(reg, installkey, REG_SZ, installpath)
                self.a_set = True
            try:
                if self.prev_values[pythonkey] != pythonpath:
                    SetValue(reg, pythonkey, REG_SZ, pythonpath)
                    self.b_set = True
            except:
                if self.a_set and not self.created:
                    SetValue(reg, installkey, REG_SZ, self.prev_values[installkey])
                raise
        finally:
            CloseKey(reg)

    def __exit__(self, exc_type, exc_value, traceback):
        reg = OpenKey(HKEY_LOCAL_MACHINE, regpath)
        try:
            try:
                if self.a_set and not self.created:
                    SetValue(reg, installkey, REG_SZ, self.prev_values[installkey])
            finally:
                if self.b_set and not self.created:
                    SetValue(reg, pythonkey, REG_SZ, self.prev_values[pythonkey])
        finally:
            CloseKey(reg)

