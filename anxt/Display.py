# anxt/Display.py
#  pyNXT - Python wrappers for aNXT
#  Copyright (C) 2011  Janosch Gräf <janosch.graef@gmx.net>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ctypes import c_int, POINTER, cast, byref

def Display(nxt):
    display = DisplayHandle(nxt)
    if (display.open()):
        return display
    else:
        del display
        return False

class DisplayHandle:
    colors = {"WHITE": 0,
              "BLACK": 1}
    
    def __init__(self, nxt):
        self.nxt = nxt
        self.handle = None

    def __del__(self):
        self.close()

    def open(self):
        if (self.handle==None):
            self.display = self.nxt.libanxt.nxt_display_open(self.nxt.handle)
            return self.display!=None
        else:
            return False

    def close(self):
        if (self.display!=None):
            self.nxt.libanxt.nxt_display_close(self.display)
            self.display = None
            return True
        else:
            return False

    def refresh(self):
        if (self.display==None):
            return False
        return int(self.nxt.libanxt.nxt_display_refresh(self.display))==0

    def flush(self, notdirty = False):
        return int(self.nxt.libanxt.nxt_display_flush(self.display, (1 if notdirty else 0)))==0

    def clear(self, color = "WHITE"):
        self.nxt.libanxt.nxt_display_clear(self.display, self.colors[color])

    def point(self, p, color = "BLACK"):
        self.nxt.libanxt.nxt_display_point(self.display, self.colors[color], p[0], p[1])

    def line(self, p1, p2, color = "BLACK"):
        self.nxt.libanxt.nxt_display_line(self.display, self.colors[color], p1[0], p1[1], p2[0], p2[1])

    def circle(self, p, r, color = "BLACK"):
        self.nxt.libanxt.nxt_display_circle(self.display, self.colors[color], p[0], p[1], r)

    def text(self, p, text, color = "BLACK", beep = False):
        x1 = c_int(p[0])
        y1 = c_int(p[1])

        n = int(self.nxt.libanxt.nxt_display_text_ext(self.display, self.colors[color], cast(byref(x1), POINTER(c_int)), cast(byref(y1), POINTER(c_int)), text, beep))

        return n, (x1.value, y1.value)

    def polygon(self, points, color = "BLACK"):
        if (len(points)<2):
            return False

        p1 = p_last = points[0]

        for p in points[1:]:
            self.line(p_last, p, color)
            p_last = p
        self.line(p_last, p1, color)

    def triangle(self, p1, p2, p3, color = "BLACK"):
        self.polygon([p1, p2, p3], color)

    def rectangle(self, p1, p2, color = "BLACK"):
        self.polygon([p1, (p1[0], p2[1]), p2, (p2[0], p1[1])], color)
