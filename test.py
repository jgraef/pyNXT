# test.py
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

import anxt
from sys import exit

print("Module:", anxt.__name__, anxt.__version__)
print()

nxt = anxt.NXT()
if (not nxt):
    print("Could not open NXT")
    exit(1)
    
print("Connected to NXT '"+nxt.get_name()+"' in Python!")
print("Battery level is: "+str(nxt.get_battery())+"mV")
print("Using "+nxt.get_connection_type()+" connection")
print()

files = anxt.File.find(nxt)
print("Listing files:")
for f in files:
    print(f[0]+" ("+str(f[1])+")")
print()

print("Reading test.txt:")
f = anxt.File.open(nxt, "test.txt", "OREAD")
if (f):
    print(f.read())
    f.close()
else:
    print("Could not open file:", nxt.strerror())


nxt.close()
