# examples/melody.py
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

#import exit and sleep
from sys import exit
from time import sleep

#import aNXT
import anxt

# we have two different duration for notes
DUR1  = 0.4
DUR2  = 0.5
# pause after each note
PAUSE = 0.15

# tones and frequencies we use
tones = {"c": 264,
        "d": 297,
        "e": 330,
        "f": 352,
        "g": 396,
        "a": 440}

# "Alle meine Entchen" (German)
melody = [("c", DUR1), # Al -
          ("d", DUR1), # le
          ("e", DUR1), # mei -
          ("f", DUR1), # ne
          ("g", DUR2), # Ent -
          ("g", DUR2), # chen

          ("a", DUR1), # schwimm -
          ("a", DUR1), # en
          ("a", DUR1), # auf
          ("a", DUR1), # den
          ("g", DUR2), # See

          ("a", DUR1), # schwimm -
          ("a", DUR1), # en
          ("a", DUR1), # auf
          ("a", DUR1), # den
          ("g", DUR2), # See

          ("f", DUR1), # Koepf -
          ("f", DUR1), # chen
          ("f", DUR1), # in
          ("f", DUR1), # das
          ("e", DUR2), # Wass -
          ("e", DUR2), # er
          ("d", DUR1), # Schwaenz -
          ("d", DUR1), # chen
          ("d", DUR1), # in
          ("d", DUR1), # die
          ("c", DUR2)] # Hoeh'

# opens NXT handle
# No argument means that we that we do not care about which NXT to open
nxt = anxt.NXT()
# don't foget to check if you find a NXT
if (not nxt):
    exit("Could find NXT")

# play melody
for note in melody:
    nxt.beep(tones[note[0]], int(note[1]*1000))
    sleep(note[1]+PAUSE)    

# close NXT
# if you forget this the NXT will be closed when the object is deleted
nxt.close()
