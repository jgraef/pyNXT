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

# documentation load
def load_doc(filename = "__doc__.txt"):
    #import OS
    global __path__
    
    path = __path__[0]+"/"+filename
    try:
        f = open(path, "r")
        doc = "".join(f.readlines())
        f.close()
    except:
        doc = "Could not load documentation from \""+path+"\"\n"
        
    return doc
        

# load libraries
__libanxt__ = Libanxt.load("libanxt.so")
assert __libanxt__!=None
Libanxt.init_prototypes(__libanxt__)

if __name__!="__main__":
    # general definitions
    __version__ = "0.10"
    #__all__ = ["NXT", "NXTHandle", "Motor", "Sensor", "AnalogSensor", "DigitalSensor", "I2C", "File", "FileHandle", "Display", "DisplayHandle"]
    # load __doc__ from file
    __doc__ = load_doc()

    # check versions
    assert __version__==Libanxt.version(__libanxt__)

    # import submodules
    from .NXT import NXT, NXTHandle
    from .Motor import Motor
    from .Sensor import Sensor, AnalogSensor, TouchSensor, LightSensor, SoundSensor, DigitalSensor
    from .I2C import I2C
    from .File import File
    from .Display import Display, DisplayHandle
    from .Module import Module
    from .UltrasonicSensor import UltrasonicSensor
    from .PSPSensor import PSPSensor
    from .AccelerationSensor import AccelerationSensor
    from .CameraSensor import CameraSensor
    from .HIDSensor import HIDSensor

    # give NXT class libanxt
    NXTHandle.libanxt = __libanxt__