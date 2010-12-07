# anxt/AccelerationSensor.py
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

""" This module implements an interface to the Mindsensors Acceleration Sensor.
"""

from .I2C import DEFAULT_I2C_ADDR
from .Libanxt import Libanxt
from .Sensor import DEFAULT_DIGITAL_PORT, DigitalSensor
from ctypes import byref

class AccelerationSensor(DigitalSensor):
    """ This class implements an interface to the Mindsensors Acceleration Sensor.
        It inherits from the DigitalSensor class.
    """

    def __init__(self, nxt, port = DEFAULT_DIGITAL_PORT, i2c_addr = DEFAULT_I2C_ADDR):
        """ Initializes the sensor
        """
        DigitalSensor.__init__(self, nxt, port, i2c_addr)

    def read(self):
        """ Reads sensor value (in this case it is the acceleration vector)
        """
        return self.get_acceleration()

    def get_sensity(self):
        """ Gets the configured sensity from the sensor
        """
        self.set_addr_param("accel")
        sensity = self.nxt.libanxt.nxt_accel_get_sensity(self.nxt.handle, self.port-1)
        # correct error
        return ceil(sensity*10)/10

    def set_sensity(self, sensity):
        """ Sets sensity for sensor. Accepted values are: 2.5, 3.3, 6.7 and 10.0
        """
        self.set_addr_param("accel")
        return self.nxt.libanxt.nxt_accel_set_sensity(self.nxt.handle, self.port-1, c_float(sensity))==0

    def get_tilt(self):
        """ Gets tilt vector from sensor.
        """
        self.set_addr_param("accel")
        tilt = Libanxt.AccelerationVector()
        if (self.nxt.libanxt.nxt_accel_get_tilt(self.nxt.handle, self.port-1, byref(tilt))==0):
            # TODO scale
            return (tilt.x-128, tilt.y-128, tilt.z-128)
        else:
            return False

    def get_acceleration(self):
        """ Gets acceleration data. Values are in G (1G equates to 9.81 m/s^2)
            If e.g. Z axis points to earth, the Z value will be about 1 due to
            earth's gravitation.
        """
        self.set_addr_param("accel")
        acceleration = Libanxt.AccelerationVector()
        if (self.nxt.libanxt.nxt_accel_get_accel(self.nxt.handle, self.port-1, byref(acceleration))==0):
            return (acceleration.x/1000, acceleration.y/1000, acceleration.z/1000)
        else:
            return False
 
