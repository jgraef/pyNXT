# anxt/NXTError.py
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


class NXTError(Exception):
    def __init__(self, nxt_or_string):
        if (type(nxt_or_string)==str):
            self.error_code = None
            self.error_msg = nxt_or_string
        else: # nxt_or_string must be of type NXT
            nxt = nxt_or_string
            self.error_code = nxt.error()
            self.error_msg = nxt.strerror(self.error_code)

    def __str__(self):
        if (self.error_code!=None):
            return "NXT Error [#"+str(self.error_code)+"]: "+self.error_msg
        else:
            return "NXT Error: "+self.error_msg
 
