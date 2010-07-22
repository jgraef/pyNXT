# anxt/UltrasonicSensor.py
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

class UltrasonicSensor(DigitalSensor):
    def __init__(self, nxt, port = DEFAULT_DIGITAL_PORT, i2c_addr = DEFAULT_I2C_ADDR):
        DigitalSensor.__init__(self, nxt, i2c_addr)

    def read(self):
        self.set_addr_param("us")
        dist = int(self.nxt.libanxt.nxt_us_get_dist(self.nxt.handle, self.port-1))
        return dist if (dist>=0) else False
