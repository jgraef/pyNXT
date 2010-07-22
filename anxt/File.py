# anxt/File.py
#  pyNXT - Python wrappers for aNXT
#  Copyright (C) 2010  Janosch Gräf
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ctypes import CDLL, c_int, c_void_p, c_char, c_long, c_char_p, byref, POINTER, cast
from .Libanxt import Libanxt

class File:
    oflags = {"OWFRAG": 0,
              "OWLINE": 1,
              "OAPPND": 2,
              "OREAD":  4,
              "OWOVER": 8}

    def __init__(self, nxt):
        self.nxt = nxt
        self.handle = None

    def __del__(self):
        self.close()

    def open(self, file, oflags, filesize = None):
        if (self.handle!=None):
            return False

        oflag = 0
        for f in oflags:
            oflag |= self.oflags.get(f, 0)

        fsize = Libanxt.FileOpenUnion()
        
        if (oflag&4!=0 or oflag&2!=0):
            ret_filesize = c_int(0)
            fsize.fs_ref = cast(byref(ret_filesize), POINTER(c_int))
            self.handle = int(self.nxt.libanxt.nxt_file_open(self.nxt.handle, file, oflag, fsize))
            self.filesize = ret_filesize.value
        else:
            fsize.filesize = filesize
            self.handle = int(self.nxt.libanxt.nxt_file_open(self.nxt.handle, file, oflag, fsize))
            self.filesize = filesize

        if (self.handle==-1):
            self.handle = None
            return False
        else:
            return True

    def close(self):
        if (self.handle!=None):
            if (int(self.nxt.libanxt.nxt_file_close(self.nxt.handle, self.handle))==0):
                self.handle = None
                return True
            else:
                return False
        else:
            return False

    def read(self, n = None, raw = False):
        if (self.handle==None):
            return False
        
        if (n==None):
            n = self.filesize
            
        buf = (c_char * n)()
        if (int(self.nxt.libanxt.nxt_file_read(self.nxt.handle, self.handle, byref(buf), n))>0):
            if (raw):
                return buf
            else:
                return "".join(map(lambda c: c.decode(), buf))

    def write(self, d, n = None):
        if (self.handle==None):
            return False
        
        if (n==None):
            n = len(d)

        n = int(self.nxt.libanxt.nxt_file_write(self.nxt.handle, self.handle, c_char_p(d), n))
        return n if (n>=0) else False
