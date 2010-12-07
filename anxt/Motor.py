# anxt/Motor.py
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

from ctypes import CDLL, c_int, c_void_p, byref
from .NXT import NXT


# TODO implement security checks (nxt!=NULL, handle!=NULL)
class Motor:
    regmodes = {"NONE":  0,
                None:    0,
                "SPEED": 1,
                "SYNC":  2}
    runstates = {"IDLE":     0x00,
                 None:       0x00,
                 "RAMPUP":   0x10,
                 "RUNNING":  0x20,
                 "RAMPDOWN": 0x40}
    ports = {"A": 0,
             "B": 1,
             "C": 2}

    def __init__(self, nxt, port = None):
        self.nxt = nxt
        self.port = self.ports.get(port, 0)

    def reset(self):
        return int(self.nxt.libanxt.nxt_motor_reset(self.nxt.handle, self.port))==0

    def set_state(self):
        return int(self.nxt.libanxt.nxt_motor_set_state(self.nxt.handle, self.port))==0

    def get_state(self):
        return int(self.nxt.libanxt.nxt_motor_get_state(self.nxt.handle, self.port))==0

    def enable_autoset(self, enable = True):
        return int(self.nxt.libanxt.nxt_motor_enable_autoset(self.nxt.handle, self.port, enable))==0

    def enable_autoget(self, enable = True):
        return int(self.nxt.libanxt.nxt_motor_enable_autoget(self.nxt.handle, self.port, enable))==0

    def turn_on(self, on_off = True):
        return int(self.nxt.libanxt.nxt_motor_turn_on(self.nxt.handle, self.port, on_off))==0

    def turn_off(self):
        return self.turn_on(False)

    def is_turned_on(self):
        return int(self.nxt.libanxt.nxt_motor_is_turned_on(self.nxt.handle, self.port))==1

    def use_brake(self, on_off = True):
        return int(self.nxt.libanxt.nxt_motor_use_brake(self.nxt.handle, self.port, on_off))==0

    def is_using_brake(self):
        return int(self.nxt.libanxt.nxt_motor_is_using_brake(self.nxt.handle, self.port))==1

    def set_regulation(self, regmode):
        if (regmode in self.regmodes):
            return int(self.nxt.libanxt.nxt_motor_set_regulation(self.nxt.handle, self.port, self.regmodes[regmode]))==0
        else:
            return False

    def get_regulation(self):
        regmode = int(self.nxt.libanxt.nxt_motor_get_regulation(self.nxt.handle, self.port))
        return [k for k, v in self.regmodes.iteritems() if v == regmode][0]

    def set_power(self, power):
        return int(self.nxt.libanxt.nxt_motor_set_power(self.nxt.handle, self.port, power))==0

    def get_power(self):
        return int(self.nxt.libanxt.nxt_motor_get_power(self.nxt.handle, self.port))

    def set_turnratio(self, power):
        return int(self.nxt.libanxt.nxt_motor_set_turnratio(self.nxt.handle, self.port, turnratio))==0

    def get_turnratio(self):
        return int(self.nxt.libanxt.nxt_motor_get_turnratio(self.nxt.handle, self.port))

    def set_runstate(self, runstate):
        if (runstate in self.runstates):
            return int(self.nxt.libanxt.nxt_motor_set_runstate(self.nxt.handle, self.port, self.runstates[runstate]))==0
        else:
            return False

    def get_runstate(self):
        runstate = int(self.nxt.libanxt.nxt_motor_get_runstate(self.nxt.handle, self.port))
        return [k for k, v in self.runstates.iteritems() if v == runstate][0]

    def set_rotation(self, rotation):
        return int(self.nxt.libanxt.nxt_motor_set_rotation(self.nxt.handle, self.port, rotation))==0

    def rotate(self, power, rotation = 0):
        return int(self.nxt.libanxt.nxt_motor_rotate(self.nxt.handle, self.port, rotation, power))==0

    def stop(self, brake = False):
        return int(self.nxt.libanxt.nxt_motor_stop(self.nxt.handle, self.port, brake))==0

    def sync(self, turnratio):
        return int(self.nxt.libanxt.nxt_motor_sync(self.nxt.handle, self.port, turnratio))==0

    def run(self, power):
        return self.rotate(power)

    def reset_tacho(self, relative = False):
        return int(self.nxt.libanxt.nxt_motor_reset_tacho(self.nxt.handle, self.port, relative))==0

    def get_tacho_count(self):
        return int(self.nxt.libanxt.nxt_motor_get_tacho_count(self.nxt.handle, self.port))

    def get_tacho_limit(self):
        return int(self.nxt.libanxt.nxt_motor_get_tacho_limit(self.nxt.handle, self.port))

    def get_block_count(self):
        return int(self.nxt.libanxt.nxt_motor_get_block_count(self.nxt.handle, self.port))

    def get_rotation_count(self):
        return int(self.nxt.libanxt.nxt_motor_get_rotation_count(self.nxt.handle, self.port))

    def get_pid(self):
        p = c_int()
        i = c_int()
        d = c_int()
        if (int(self.nxt.libanxt.nxt_motor_get_pid(self.nxt.handle, self.port, byref(p), byref(i), byref(d)))==0):
            return p.value, i.value, d.value
        else:
            return False

    def set_pid(self, p, i, d):
        return int(self.nxt.libanxt.nxt_motor_set_pid(self.nxt.handle, self.port, p, i, d))==0

    def get_speed(self):
        return int(self.nxt.libanxt.nxt_motor_get_speed(self.nxt.handle, self.port))
