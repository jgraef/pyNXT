# examples/morse.py
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

from sys import exit
from time import time, sleep
from threading import Thread, Lock, Event

# import aNXT
import anxt

class MorseTelegraph():
    def __init__(self, nxt = None, light = None, baud = 10, tone = 1000):
        self.thread = Thread(None, self.run, "morse")
        self.nxt = anxt.NXT() if (nxt==None) else nxt
        self.light = anxt.LightSensor(self.nxt, 3, False) if (light==None) else light
        self.set_baud(baud)
        self.tone = tone
        self.buffer = ""
        self.buffer_lock = Lock()
        self.morsecode = {}
        self.running = False
        self.thread.daemon = True
        self.thread.start()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        self.daemon = True
        while (True):
            if (self.running):
                if (not self.send_char()):
                    sleep(self.pause[2])
            else:
                sleep(self.pause[2])

    def load_morsecode(self, filename = "morsecode.txt"):
        f = open(filename)
        if (f):
            self.morsecode = dict(map(lambda l: l.split(None, 2), f.readlines()))
            return True
        else:
            return False

    def set_baud(self, baud):
        self.baud = baud
        self.length = (1/baud, 3/baud)
        self.pause = (1/baud, 2/baud, 4/baud)

    def add_buffer(self, text):
        self.buffer_lock.acquire()
        self.buffer += text
        self.buffer_lock.release()

    def send(self, text):
        self.add_buffer(text)
        for c in text:
            if (c.isspace()):
                print("  ", end="")
            else:
                m = self.get_morse(c)
                if (m):
                    print(*m, sep="", end=" ")
                else:
                    print(c, end=" ")
        print()

    def sos(self):
        self.add_buffer("SOS")

    def send_char(self, c = None):
        if (c==None):
            self.buffer_lock.acquire()
            if (self.buffer!=""):
                c = self.buffer[0]
                self.buffer = self.buffer[1:]
                self.buffer_lock.release()
            else:
                self.buffer_lock.release()
                return False
        if (c.isspace()):
            sleep(self.pause[2])
        else:
            m = self.get_morse(c)
            if (m):
                self.send_morse(m)
                return True
            else:
                return False

    def get_morse(self, c):
        if (c.isalpha()):
            c = c.upper()
        return self.morsecode[c] if (c in self.morsecode) else False

    def send_morse(self, m):
        for s in m:
            self.send_signal(s)
            sleep(self.pause[1])

    def send_signal(self, s):
        length = self.length[0 if (s=='.') else 1]
        ts = time()
        self.light.light_on()
        if (self.tone!=None):
            self.nxt.beep(self.tone, length*1000)
        self.sleep_remaining(ts, length)
        ts = time()
        self.light.light_off()
        self.sleep_remaining(ts, self.pause[0])

    def sleep_remaining(self, ts, tp):
        tr = tp+ts-time()
        if (tr>0):
            sleep(tr)

if __name__=="__main__":
    m = MorseTelegraph()
    if (m.load_morsecode()):
        m.start()
        print("Morse telegraph running. Enter '\\help' for help")
        while (True):
            line = input("Morse> ")
            if (line[0]=="\\"):
                if (line[1]=="\\"):
                    line = line[1:]
                else:
                    cmd = line[1:].split()
                    cmd[0] = cmd[0].lower()
                    line = None
                    if (cmd[0]=="help"):
                        print("Enter text to send it to the morse telegraph.\n" \
                            + "Commands are escaped with a leading '\\'\n" \
                            + "Following commands are supported:\n" \
                            + "  \\\\           Send '\\' to morse telegraph\n" \
                            + "  \\help        Show help\n" \
                            + "  \\start       Start telegraph (sending)\n" \
                            + "  \\stop        Stop telegraph (sending)\n" \
                            + "  \\quite       Send only visual signals\n" \
                            + "  \\tone [FREQ] Set tone to FREQ or show current tone frequency\n" \
                            + "  \\baud [BAUD] Set baudrate to BAUD or show current baudrate\n" \
                            + "  \\quit        Quit morse telegraph\n" \
                            + "  \\exit        Alias for \\quit\n")
                    elif (cmd[0]=="start"):
                        m.start()
                    elif (cmd[0]=="stop"):
                        m.stop()
                    elif (cmd[0]=="quite"):
                        m.tone = None
                    elif (cmd[0]=="tone"):
                        if (len(cmd)==1):
                            print(m.tone)
                        else:
                            m.tone = int(cmd[1])
                    elif (cmd[0]=="baud"):
                        if (len(cmd)==1):
                            print(m.baud)
                        else:
                            m.set_baud(int(cmd[1]))
                    elif (cmd[0]=="exit" or cmd[0]=="quit"):
                        break
            if (line):
                m.send(line)
    else:
        print("Could not load morsecode")
