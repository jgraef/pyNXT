# examples/sos.py
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
#  along with this program.  If not, see <http:#www.gnu.org/licenses/>.

# import exit and sleep
from sys import exit
from time import sleep

# import aNXT
import anxt

# frequency of tone
FREQ  = 1000
# pause between signals
PAUSE = 0.200
# short and long duration of tone/light
DUR   = (0.150, 0.400)

# function to send a signal
def signal(nxt, s, freq, dur, pause):
    nxt.beep(freq, dur*1000)
    s.light_on()
    sleep(dur)
    s.light_off()
    sleep(pause)

# opens NXT handle
# No argument means that we that we do not care about which NXT to open
nxt = anxt.NXT()
# don't forget to check if you found a NXT
if (not nxt):
    exit("Could find NXT")

# prepare sensor
s = anxt.LightSensor(nxt, 1, False)

# three times short signal
for i in range(3):
    signal(nxt, s, FREQ, DUR[0], PAUSE)

# three times long signal
for i in range(3):
    signal(nxt, s, FREQ, DUR[1], PAUSE)

# three times short signal
for i in range(3):
    signal(nxt, s, FREQ, DUR[0], PAUSE)

# close NXT
# if you forget this the NXT will be closed when the object is deleted
nxt.close()
