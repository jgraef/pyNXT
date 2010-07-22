# anxt/CameraSensor.py
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

from .I2C import DEFAULT_I2C_ADDR
from .Libanxt import Libanxt
from .Sensor import DEFAULT_DIGITAL_PORT, DigitalSensor
from ctypes import byref

class CameraSensor(DigitalSensor):
    tracking_modes = {"OBJECT": 0x42,
                      "LINE": 0x4C}
    
    def __init__(self, nxt, port = DEFAULT_DIGITAL_PORT, i2c_addr = DEFAULT_I2C_ADDR):
        DigitalSensor.__init__(self, nxt, i2c_addr)

    def read(self):
        return self.get_objects()

    def get_objects(self):
        self.set_addr_param("psp")

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
        self.set_addr_param("psp")

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
        self.set_addr_param("psp")
        self.nxt.libanxt.nxt_cam_enable_tracking(self.nxt.handle, self.port-1, 1 if enable else 0)

    def set_trackingmode(self, mode = "OBJECT"):
        self.set_addr_param("psp")
        self.nxt.libanxt.nxt_cam_set_trackingmode(self.nxt.handle, self.port-1, self.tracking_modes[mode])

    def reset(self):
        self.set_addr_param("psp")
        self.nxt.libanxt.nxt_cam_reset(self.nxt.handle, self.port-1)

    def nxt_cam_enable_colorsort(self, enable = True):
        self.set_addr_param("psp")
        self.nxt.libanxt.nxt_cam_enable_colorsort(self.nxt.handle, self.port-1, 1 if enable else 0)
