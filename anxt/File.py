# anxt/File.py
#  pyNXT - Python wrappers for aNXT
#  Copyright (C) 2011  Janosch Gräf <janosch.graef@gmx.net>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ctypes import CDLL, c_uint, c_int, c_void_p, c_char, c_long, c_char_p, byref, POINTER
from .Libanxt import Libanxt
from .NXTError import NXTError
import io


class RawIO(io.RawIOBase):
    def __init__(self, nxt, filename, mode = "r", filesize = None, linear = False):
        self.nxt = nxt

        self.mode = mode        
        if (mode=='r'):
            # open file for reading
            _filesize = c_int()
            self.handle = self.nxt.libanxt.nxt_file_open_read(self.nxt.handle, filename, byref(_filesize))
            self.filesize = _filesize.value
        elif (mode=='w'):
            # open file for writing
            # TODO: remove file if existing
            if (filesize==None):
                raise NXTError("Please specify the filesize you want.")
            # try to remove file (ignore error)
            #try:
            print("remove: "+filename)
            nxt.remove(filename)
            #except NXTError:
            #    pass
            # open file
            if (linear):
                self.handle = self.nxt.libanxt.nxt_file_open_write_linear(self.nxt.handle, filename, filesize)
            else:
                self.handle = self.nxt.libanxt.nxt_file_open_write(self.nxt.handle, filename, filesize)
            self.filesize = filesize
        else:
            raise NXTError("Invalid mode: "+repr(mode))

        if (self.handle<0):
            raise NXTError(self.nxt)


    def __del__(self):
        self.close()

    def close(self):
        if (self.handle!=None):
            if (int(self.nxt.libanxt.nxt_file_close(self.nxt.handle, self.handle))==0):
                self.handle = None
                return True
            else:
                return False
        else:
            return False

    def fileno(self):
        return self.handle

    def isatty(self):
        return False

    def seekable(self):
        return False

    def seek(self, offset, whence):
        raise IOError("Not seekable")

    def tell(self):
        raise IOError("Not seekable")

    def truncate(self, size = None):
        raise IOError("Not seekable")

    def readable(self):
        return self.mode=='r'

    def writable(self):
        return self.mode=='w'

    def read(self, n = -1):
        if (self.handle==None):
            raise NXTError("File not opened")

        if (n==-1):
            n = self.filesize

        buf = (c_char * n)()
        n = self.nxt.libanxt.nxt_file_read(self.nxt.handle, self.handle, byref(buf), n)
        if (n<0):
            raise NXTError(self.nxt)
        else:
            return buf

    def readall(self):
        return self.read(-1)

    def write(self, d, n = None):
        if (self.handle==None):
            raise NXTError("File not opened")
        
        if (n==None):
            n = len(d)

        n = self.nxt.libanxt.nxt_file_write(self.nxt.handle, self.handle, c_char_p(d), n)
        if (n<0):
            raise NXTError(self.nxt)
        else:
            return n


class BufferedIO(io.BytesIO):
    def __init__(self, nxt, filename, mode = 'r', linear = False):
        self.nxt = nxt
        self.filename = filename
        self.mode = mode
        self.linear = linear
        if (mode=='r' or mode=='a'):
            # read and buffer data
            raw = RawIO(nxt, filename, 'r')
            io.BytesIO.__init__(self, raw.readall())
            if (mode=='a'):
                self.seek(0, io.SEEK_END)
            raw.close()
        else:
            # setup empty buffer
            io.BytesIO.__init__(self)
            self.pos = 0

    def flush(self):
        if (self.mode=='w' or self.mode=='a'):
            buf = self.getvalue()
            raw = RawIO(self.nxt, self.filename, 'w', len(buf), self.linear)
            raw.write(buf)
            raw.close()
