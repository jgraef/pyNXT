# anxt/Sensor.py
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

from ctypes import CDLL, c_int, c_void_p, c_char_p, Structure, byref
from .NXT import NXT
from .I2C import I2C, DEFAULT_I2C_ADDR


DEFAULT_DIGITAL_PORT = 4


# move into Libanxt class
class AnalogSensorValues(Structure):
    _fields_ = [("is_calibrated", c_int),
                ("type", c_int),
                ("mode", c_int),
                ("raw", c_int),
                ("normalized", c_int),
                ("scaled", c_int),
                ("calibrated", c_int)]


class Sensor:
    types = {"NONE":           0x00,
             None:             0x00,
             "SWITCH":         0x01,
             "TEMPERATURE":    0x02,
             "REFLECTION":     0x03,
             "ANGLE":          0x04,
             "LIGHT_ACTIVE":   0x05,
             "LIGHT_INACTIVE": 0x06,
             "SOUND_DB":       0x07,
             "SOUND_DBA":      0x08,
             "CUSTOM":         0x09,
             "LOWSPEED":       0x0A,
             "LOWSPEED_9V":    0x0B}
    modes = {"RAW":              0x00,
             None:               0x00,
             "BOOLEAN":          0x20,
             "TRANSITION_COUNT": 0x40,
             "PERIOD_COUNT":     0x60,
             "PERCENT":          0x80,
             "CELSIUS":          0xA0,
             "FAHRENHEIT":       0xC0,
             "ANGLE_STEP":       0xE0,
             "SLOPE_MASK":       0x1F,
             "MODE_MASK":        0xE0}
    valid_ports = (0, 1, 2, 3)

    def __init__(self, nxt, port = None):
        if (not port in self.valid_ports):
            port = self.valid_ports[0]

        self.nxt = nxt
        self.port = port
        self.type = None
        self.mode = None

    def set_sensor_type(self, type):
        if (self.nxt!=None and self.nxt.handle!=None and type in self.types):
            return set_sensor_typemode(type, self.mode)
        else:
            return False

    def set_sensor_mode(self, mode):
        if (self.nxt!=None and self.nxt.handle!=None and mode in self.modes):
            return set_sensor_typemode(self.type, mode)
        else:
            return False

    def set_sensor_typemode(self, type, mode):
        if (self.nxt!=None and self.nxt.handle!=None):
            if (int(self.nxt.libanxt.nxt_set_sensor_mode(self.nxt.handle, self.port-1, self.types[type], self.modes[mode]))==0):
                self.type = type
                self.mode = mode
        else:
            return False

    def get_values(self, update_type = True, update_mode = True):
        if (self.nxt!=None and self.nxt.handle!=None):
            values = AnalogSensorValues()
            if (int(self.nxt.libanxt.nxt_get_sensor_values(self.nxt.handle, self.port-1, byref(values)))==0):
                if (update_type):
                    self.type = values.type
                if (update_mode):
                    self.mode = values.mode
                return values
            else:
                return False
        else:
            return False


class AnalogSensor(Sensor):
    default_ports = {None:             1,
                     "LIGHT_ACTIVE":   3,
                     "LIGHT_INACTIVE": 3,
                     "SOUND_DB":       2,
                     "SOUND_DBA":      2}

    def __init__(self, nxt, port = None, type = None, mode = None):
        if (port==None):
            port = default_ports[mode]

        Sensor.__init__(self, nxt, port)
        self.set_sensor_typemode(type, mode)

    def read(self):
        values = self.get_values()
        if (values!=False):
            v = values.calibrated if values.is_calibrated else values.scaled
            if (self.mode=="BOOLEAN"):
                return (v==1)
            elif (self.mode=="PERCENT"):
                return v/100
            else:
                return v
        else:
            return False

class DigitalSensor(Sensor, I2C):
    def __init__(self, nxt, port = DEFAULT_DIGITAL_PORT, i2c_addr = DEFAULT_I2C_ADDR):
        Sensor.__init__(self, nxt, port)
        I2C.__init__(self, nxt, port, i2c_addr)

        self.set_sensor_typemode("LOWSPEED_9V", None)

    def set_addr_param(sensor_name):
        c_addr = c_int.in_dll(self.nxt.libanxt, "nxt_"+sensor_name+"_i2c_addr")
        c_addr = c_int(self.addr)

class UltraSonic(DigitalSensor):
    def __init__(self, nxt, port = 4, i2c_addr = 0x02):
        DigitalSensor.__init(self, nxt, i2c_addr)

    def read():
        self.set_addr_param("us")
        return int(self.nxt.libanxt.nxt_motor_sync(self.nxt.handle, self.port-1))

    # TODO: wrap other functions
