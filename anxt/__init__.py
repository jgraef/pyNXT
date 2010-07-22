# anxt/__init__.py
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

# import Libanxt class
from .Libanxt import Libanxt

# load libraries
__libanxt__ = Libanxt.load("libanxt.so")
assert __libanxt__!=None
Libanxt.init_prototypes(__libanxt__)

if __name__!="__main__":
    # general definitions
    __doc__ = "This is a python module for the LEGO Mindstorms NXT"
    __version__ = str(int(__libanxt__.nxt_version_major()))+"."+str(int(__libanxt__.nxt_version_minor()))

    # import submodules
    from .NXT import NXT, NXTHandle
    from .Motor import Motor
    from .Sensor import Sensor, AnalogSensor, DigitalSensor
    from .I2C import I2C
    # TODO see File.py
    from .File import File, FileHandle

    # give NXT class libanxt
    NXTHandle.libanxt = __libanxt__
