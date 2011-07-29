# anxt/PSPSensor.py
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

from .I2C import DEFAULT_I2C_ADDR
from .Libanxt import Libanxt
from .Sensor import DEFAULT_DIGITAL_PORT, DigitalSensor
from ctypes import byref

class PSPSensor(DigitalSensor):
    psp_modes = {0x41: "DIGITAL",
             0x73: "ANALOG"}
    joysticks = {"LEFT": 1,
                 "RIGHT": 2,
                 "BOTH": 3}

    
    def __init__(self, nxt, port = DEFAULT_DIGITAL_PORT, i2c_addr = DEFAULT_I2C_ADDR):
        DigitalSensor.__init__(self, nxt, port, i2c_addr)

    def read(self):
        return self.get_buttons(), self.get_joystick()

    def get_mode(self):
        self.set_addr_param("psp")
        mode = int(self.nxt.libanxt.nxt_psp_get_mode(self.nxt.handle, self.port-1))
        if (mode>=0):
            return self.psp_modes[mode]
        else:
            return False

    def get_buttons(self, as_dict = False):
        self.set_addr_param("psp")
        buttons = Libanxt.PSPButtons()
        if (int(self.nxt.libanxt.nxt_psp_get_buttons(self.nxt.handle, self.port-1, byref(buttons)))==0):
            if (as_dict):
                return {"left": buttons.left!=0,
                        "down": buttons.down!=0,
                        "up": buttons.up!=0,
                        "right": buttons.right!=0,
                        "r3": buttons.r3!=0,
                        "l3": buttons.l3!=0,
                        "square": buttons.square!=0,
                        "x": buttons.x!=0,
                        "o": buttons.o!=0,
                        "triangle": buttons.triangle!=0,
                        "r1": buttons.r1!=0,
                        "l1": buttons.l1!=0,
                        "r2": buttons.r2!=0,
                        "l2": buttons.l2!=0}
            else:
                return (buttons.up!=0,
                        buttons.down!=0,
                        buttons.left!=0,
                        buttons.right!=0,
                        buttons.triangle!=0,
                        buttons.x!=0,
                        buttons.square!=0,
                        buttons.o!=0,
                        buttons.l1!=0,
                        buttons.l2!=0,
                        buttons.l3!=0,
                        buttons.r1!=0,
                        buttons.r2!=0,
                        buttons.r3!=0)
        else:
            return False

    def get_joystick(self, joy = "BOTH"):
        self.set_addr_param("psp")
        n = 2 if (joy=="BOTH") else 1
        joysticks = (Libanxt.PSPJoystick * n)()
        if (int(self.nxt.libanxt.nxt_psp_get_joystick(self.nxt.handle, self.port-1, self.joysticks[joy], joysticks))==0):
            j = []
            for joystick in joysticks:
                j.append((joystick.x, joystick.y))
            if (len(j)==1):
                return j[0]
            else:
                return tuple(j)
        else:
            return False 
