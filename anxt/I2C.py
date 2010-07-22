# anxt/I2C.py
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

from .NXT import NXT


DEFAULT_I2C_ADDR = 0x02


class I2C:
    regs = {"VERSION":  0x00,
            "VENDORID": 0x08,
            "DEVICEID": 0x10,
            "COMMAND":  0x41}
    
    def __init__(self, nxt, port, addr = DEFAULT_I2C_ADDR):
        self.nxt = nxt
        self.port = port
        self.addr = addr
        
    def read(self, reg1, nreg):
        buf = (c_char * nreg)()
        nreg = self.nxt.libanxt.nxt_i2c_read(self.nxt.handle, self.port, self.addr, reg1, nreg, byref(buf))
        if (nreg>0):
            resize(buf, nreg)
            return buf
        else:
            return False

    def write(self, reg1, buf):
        nreg = sizeof(buf)
        return int(self.nxt.libanxt.nxt_i2c_write(self.nxt.handle, self.port, self.addr, reg1, nreg, byref(buf)))

    def command(self, cmd):
        return int(self.nxt.libanxt.nxt_i2c_cmd(self.nxt.handle, self.port, self.addr, cmd))

    def get_addr(self, hardware = False):
        return self.addr

    def set_addr(self, new, hardware = False):
        if (hardware):
            if (int(self.nxt.libanxt.nxt_i2c_set_i2caddr(self.nxt.handle, self.port, self.addr, new))!=0):
                return False
        self.addr = new
        return True

    def get_version(self):
        return int(self.nxt.libanxt.nxt_i2c_get_version(self.nxt.handle, self.port, self.addr))

    def get_vendorid(self):
        return int(self.nxt.libanxt.nxt_i2c_get_vendorid(self.nxt.handle, self.port, self.addr))

    def get_deviceid(self):
        return int(self.nxt.libanxt.nxt_i2c_get_deviceid(self.nxt.handle, self.port, self.addr))
