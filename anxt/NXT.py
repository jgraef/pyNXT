# anxt/NXT.py
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
#  along with this program.  If not, see <http://www.gnu.org

from ctypes import CDLL, c_int, c_void_p, c_char_p, byref

def NXT(name = None, host = "localhost", port = 51337, password = ""):
    nxt = NXTHandle()
    if (nxt.open(name, host, port, password)):
        return nxt
    else:
        del nxt
        return False

class NXTHandle:
    # NXT error numbers
    errors = {"SUCCESS": 0x00,
              "TRANSACTION_IN_PROGRESS": 0x20,
              "MAILBOX_EMPTY": 0x40,
              "NO_MORE_HANDLES": 0x81,
              "NO_SPACE": 0x82,
              "NO_MORE_FILES": 0x83,
              "END_OF_FILE_EXPECTED": 0x84,
              "END_OF_FILE": 0x85,
              "NOT_A_LINEAR_FILE": 0x86,
              "FILE_NOT_FOUND": 0x87,
              "HANDLE_ALREADY_CLOSED": 0x88,
              "NO_LINEAR_SPACE": 0x89,
              "UNDEFINED_ERROR": 0x8A,
              "FILE_IS_BUSY": 0x8B,
              "NO_WRITE_BUFFERS": 0x8C,
              "APPEND_NOT_POSSIBLE": 0x8D,
              "FILE_IS_FULL": 0x8E,
              "FILE_EXISTS": 0x8F,
              "MODULE_NOT_FOUND": 0x90,
              "OUT_OF_BOUNDARY": 0x91,
              "ILLEGAL_FILE_NAME": 0x92,
              "ILLEGAL_HANDLE": 0x93,
              "REQUEST_FAILED": 0xBD,
              "UNKNOWN_OPCODE": 0xBE,
              "INSANE_PACKET": 0xBF,
              "OUT_OF_RANGE": 0xC0,
              "BUS_ERROR": 0xDD,
              "NO_FREE_MEMORY_IN_BUFFER": 0xDE,
              "CHANNEL_NOT_VALID": 0xDF,
              "CHANNEL_NOT_CONFIGURED_OR_BUSY": 0xE0,
              "NO_ACTIVE_PROGRAM": 0xEC,
              "ILLEGAL_SIZE": 0xED,
              "ILLEGAL_MAILBOX_QUEUE_ID": 0xEE,
              "INVALID_FIELD_OF_STRUCTURE": 0xEF,
              "BAD_INPUT_OUTPUT": 0xF0,
              "INSUFFICIENT_MEMORY": 0xFB,
              "BAD_ARGUMENTS": 0xFF,
              # aNXT error numbers
              "CONNECTION": 0x0100}

    # NXT handle
    handle = None

    # C library "libanxt.so" (set by __init__.py)
    libanxt = None

    def __init__(self):
        pass
        
    def __del__(self):
        self.close()

    def open(self, name = None, hostname = "localhost", port = 51337, password = ""):
        self.handle = self.libanxt.nxt_open_net(name, hostname, port, password)
        return self.handle!=None

    def close(self):
        if (self.handle!=None):
            self.libanxt.nxt_close(self.handle)
            self.handle = None
            return True
        else:
            return False

    def is_connected(self):
        return self.handle!=None

    def error(self):
        if (self.handle!=None):
            return int(self.libanxt.nxt_error(self.handle))
        else:
            return False

    def strerror(self, error = None):
        if (self.handle!=None):
            if (error==None):
                error = self.error()
            strerror = self.libanxt.nxt_strerror(error)
            if (strerror==None):
                return False
            else:
                return strerror.decode()

    def reset_error(self):
        if (self.handle!=None):
            self.libanxt.nxt_reset_error(self.handle)
        else:
            return False

    def get_connection_type(self):
        if (self.handle!=None):
            connection_types = ("USB", "BLUETOOTH") 
            num = int(self.libanxt.nxt_get_connection_type(self.handle))
            return connection_types[num] if (num<len(connection_types)) else False
        else:
            return None

    def send_msg(self, mailbox, data):
        if (self.handle!=None):
            return int(self.libanxt.nxt_send_msg(self.handle, c_int(mailbox), c_char_p(data)))
        else:
            return False

    def recv_msg(self, mailbox, clear = True):
        if (self.handle!=None):
            data = self.libanxt.nxt_send_msg(self.handle, c_int(mailbox), c_int(clear))
            if (data==None):
                return False
            else:
                msg = data.decode()
                # TODO free data
                return msg
        else:
            return False

    def get_name(self):
        if (self.handle!=None):
            name = self.libanxt.nxt_get_name(self.handle)
            if (name==None):
                return False
            else:
                return name.decode()
        else:
            return False

    def set_name(self, name):
        if (self.handle!=None):
            return int(self.libanxt.nxt_send_msg(self.handle, c_char_p(name)))==0
        else:
            return False

    def get_version(self):
        if (self.handle!=None):
            # FIXME
            version = (c_int * 4)()
            if (int(self.libanxt.nxt_get_version(self.handle, byref(version[0]), byref(version[1]), byref(version[2]), byref(version[3])))==0):
                return str(int(version[0]))+"."+str(int(version[1])), str(int(version[2]))+"."+str(int(version[3]))
            else:
                return False
        else:
            return False

    def get_battery(self):
        if (self.handle!=None):
            res = int(self.libanxt.nxt_get_battery(self.handle))
            return False if res==-1 else res
        else:
            return False

    def run_program(self, program):
        if (self.handle!=None):
            return __libnxt__.nxt_run_program(self.handle, c_char_p(program))==0
        else:
            return False

    def stop_program(self):
        if (self.handle!=None):
            return __libnxt__.nxt_stop_program(self.handle)==0
        else:
            return False

    def get_program(self):
        if (self.handle!=None):
            program = self.libanxt.nxt_get_program(self.handle)
            if (program==None):
                return False
            else:
                return program.decode()
        else:
            return False

    def get_device_info(self):
        if (self.handle!=None):
            # FIXME
            bt_addr = create_buffer(6)
            bt_strength = c_int
            free_flash = c_int

            if (self.libanxt.nxt_get_devinfo(self.handle, None, byref(bt_addr), byref(bt_strength), byref(free_flash))==-1):
                return False
            else:
                return (str(bt_addr), int(bt_strength), int(free_flash))
        else:
            return False

    def keep_alive(self):
        if (self.handle!=None):
            return int(self.libanxt.nxt_keep_alive(self.handle))==0
        else:
            return False
        
    def beep(self, frequency, duration):
        if (self.handle!=None):
            return int(self.libanxt.nxt_beep(self.handle, c_int(frequency), c_int(duration)))==0
        else:
            return False

    def play_sound(self, soundfile, loop = False):
        if (self.handle!=None):
            return int(self.libanxt.nxt_play_sound(self.handle, soundfile, int(loop)))==0
        else:
            return False

    def stop_sound(self):
        if (self.handle!=None):
            return int(self.libanxt.nxt_stop_sound(self.handle))==0
        else:
            return False

    def reset_bluetooth(self):
        if (self.handle!=None):
            return int(self.libanxt.nxt_reset_bluetooth(self.handle))==0
        else:
            return False

    def delete_userflash(self):
        if (self.handle!=None):
            return int(self.libanxt.nxt_delete_userflash(self.handle))==0
        else:
            return False
