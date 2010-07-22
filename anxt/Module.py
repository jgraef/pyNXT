# anxt/Module.py
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

from ctypes import c_int, c_char, c_char_p, byref

class Module:
    def __init__(self, nxt, modid, modsize = None):
        self.nxt = nxt
        self.modid = modid
        self.modsize = modsize

    def read(self, offset = 0, n = None, raw = False):
        if (n==None):
            if (modsize==None):
                return False
            else:
                n = self.modsize

        buf = (c_char * n)()
        if (int(self.nxt.libanxt.nxt_mod_read(self.nxt.handle, self.modid, byref(buf), offset, n))>0):
            if (raw):
                return buf
            else:
                return "".join(map(lambda c: c.decode(), buf))

    def write(self, d, offset = 0, n = None):
        if (n==None):
            n = len(d)

        n = int(self.nxt.libanxt.nxt_mod_write(self.nxt.handle, self.modid, c_char_p(d), offset, n))
        return n if (n>=0) else False
