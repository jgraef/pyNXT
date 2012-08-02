# anxt/CameraSensor.py
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

from io import IOBase

from .I2C import DEFAULT_I2C_ADDR
from .Libanxt import Libanxt
from .Sensor import DEFAULT_DIGITAL_PORT, DigitalSensor
from ctypes import byref, Structure, c_ubyte

# TODO split from C Colormap structure and put C structure into Libanxt (already is)
x = """
class Colormap(Structure):
    FILE_SIG = b"#aNXTCam COLORMAP\n"
    
    _fields_ = [("r", (16 * c_ubyte)),
                ("g", (16 * c_ubyte)),
                ("b", (16 * c_ubyte))]

    @staticmethod
    def load(file_or_path):
        if (isinstance(file_or_path, IOBase)):
            f = file_or_path
        else:
            f = open(file_or_path, "rb")

        sig = f.readline()
        if (sig!=Colormap.FILE_SIG):
            raise ColormapError("Invalid signature")

        r = tuple(f.read(16))
        g = tuple(f.read(16))
        b = tuple(f.read(16))

        if (f!=file_or_path):
            f.close()

        return Colormap(r, g, b)

    def save(self, file_or_path):
        if (isinstance(file_or_path, IOBase)):
            f = file_or_path
        else:
            f = open(file_or_path, "wb")

        f.write(self.FILE_SIG)

        f.write(bytes(self.r))
        f.write(bytes(self.g))
        f.write(bytes(self.b))

        if (f!=file_or_path):
            f.close()

    def get_r(self, i):
        return (self.r[i*2]<<8) | self.r[i*2+1]

    def get_g(self, i):
        return (self.g[i*2]<<8) | self.g[i*2+1]

    def get_b(self, i):
        return (self.b[i*2]<<8) | self.b[i*2+1]

    def get_average_color(self, i):
        r = self.get_r(i)
        g = self.get_g(i)
        b = self.get_b(i)

        r_sum = r_n = 0
        g_sum = g_n = 0
        b_sum = b_n = 0

        for i in range(16):
            r_sum += ((r>>(16-i))&1)*i*16
            r_n += 1
            g_sum += ((g>>(16-i))&1)*i*16
            g_n += 1
            b_sum += ((b>>(16-i))&1)*i*16
            b_n += 1

        return (r_sum/r_n,
                g_sum/g_n,
                b_sum/b_n)
"""
    


class CameraSensor(DigitalSensor):
    tracking_modes = {"OBJECT": 0x42,
                      "LINE": 0x4C}
    
    def __init__(self, nxt, port = DEFAULT_DIGITAL_PORT, i2c_addr = DEFAULT_I2C_ADDR):
        DigitalSensor.__init__(self, nxt, port, i2c_addr)

    def read(self):
        return self.get_objects()

    def get_objects(self):
        self.set_addr_param("cam")

        n = int(self.nxt.libanxt.nxt_cam_num_objects(self.nxt.handle, self.port-1))
        if (n>0):
            objbuf = (Libanxt.CameraObject * n)()
            self.nxt.wait_after_communication_command()
            n = int(self.nxt.libanxt.nxt_cam_get_objects(self.nxt.handle, self.port-1, 0, n, objbuf))
            if (n>0):
                objects = []
                for i in range(n):
                    objects.append((objbuf[i].color, (objbuf[i].x, objbuf[i].y), (objbuf[i].w, objbuf[i].h)))
                return objects
            elif (n==0):
                return []
            else:
                return False
        elif (n==0):
            return []
        else:
            return False
            
    def get_colormap(self):
        self.set_addr_param("cam")

        colormap = Libanxt.CameraColormap()
        if (int(self.nxt.libanxt.nxt_cam_get_colormap(self.nxt.handle, self.port-1, byref(colormap)))==0):
            c = ([], [], [])
            for i in range(16):
                c[0].append(colormap.r[i])
                c[1].append(colormap.g[i])
                c[2].append(colormap.b[i])
            return tuple(c[0]), tuple(c[1]), tuple(c[2])
        else:
            return False

    def enable_tracking(self, enable = True):
        self.set_addr_param("cam")
        self.nxt.libanxt.nxt_cam_enable_tracking(self.nxt.handle, self.port-1, int(enable))

    def set_trackingmode(self, mode = "OBJECT"):
        self.set_addr_param("cam")
        self.nxt.libanxt.nxt_cam_set_trackingmode(self.nxt.handle, self.port-1, self.tracking_modes[mode])

    def reset(self):
        self.set_addr_param("cam")
        self.nxt.libanxt.nxt_cam_reset(self.nxt.handle, self.port-1)

    def enable_colorsort(self, enable = True):
        self.set_addr_param("cam")
        self.nxt.libanxt.nxt_cam_enable_colorsort(self.nxt.handle, self.port-1, int(enable))
