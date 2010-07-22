# anxt/libanxt.py
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

# import CDLL
from ctypes import CDLL, c_void_p, c_int, c_char_p, c_long, POINTER, Union

class Libanxt:
    class file_open_union(Union):
        _fields_ = [("filesize", c_int),
                    ("fs_ref", POINTER(c_int))]
    
    @staticmethod
    def load(libname):
        # import OS
        import os

        # load library
        if (os.name=="posix"):
            return CDLL(libname)
        else:
            return None

    @staticmethod
    def init_prototypes(l):
        # TODO: replace some c_void_p with correct pointer types (e.g. POINTER(c_int))
        prototypes = (# libanxt/nxt.c
                      [l.nxt_version_minor, c_int],
                      [l.nxt_version_major, c_int],
                      [l.nxt_open_net, c_void_p, c_char_p, c_char_p, c_int, c_char_p],
                      [l.nxt_close, None, c_void_p],
                      [l.nxt_error, c_int, c_void_p],
                      [l.nxt_strerror, c_char_p, c_int],
                      [l.nxt_reset_error, None, c_void_p],
                      [l.nxt_get_connection_type, c_int, c_void_p],
                      [l.nxt_send_msg, c_int, c_void_p, c_int, c_char_p],
                      [l.nxt_recv_msg, c_int, c_void_p, c_int, c_int],
                      [l.nxt_set_name, c_int, c_void_p, c_char_p],
                      [l.nxt_get_version, c_int, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p],
                      [l.nxt_get_battery, c_int, c_void_p],
                      [l.nxt_run_program, c_int, c_void_p, c_char_p],
                      [l.nxt_stop_program, c_int, c_void_p],
                      [l.nxt_get_program, c_char_p, c_void_p],
                      [l.nxt_get_devinfo, c_int, c_void_p, c_char_p, c_void_p, c_void_p],
                      [l.nxt_get_name, c_char_p, c_void_p],
                      [l.nxt_keep_alive, c_int, c_void_p],
                      [l.nxt_beep, c_int, c_void_p, c_int, c_int],
                      [l.nxt_play_sound, c_int, c_void_p, c_char_p, c_int],
                      [l.nxt_stop_sound, c_int, c_void_p],
                      [l.nxt_reset_bluetooth, c_int, c_void_p],
                      [l.nxt_delete_userflash, c_int, c_void_p],
                      [l.nxt_set_sensor_mode, c_int, c_void_p, c_int, c_int, c_int],
                      [l.nxt_get_sensor_values, c_int, c_void_p, c_int, c_void_p],
                      [l.nxt_reset_sensor, c_int, c_void_p, c_int],
                      # libanxt/motor.c
                      [l.nxt_motor_reset, c_int, c_void_p, c_int],
                      [l.nxt_motor_set_state, c_int, c_void_p, c_int],
                      [l.nxt_motor_get_state, c_int, c_void_p, c_int],
                      [l.nxt_motor_enable_autoset, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_enable_autoget, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_turn_on, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_is_turned_on, c_int, c_void_p, c_int],
                      [l.nxt_motor_use_brake, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_is_using_brake, c_int, c_void_p, c_int],
                      [l.nxt_motor_set_regulation, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_get_regulation, c_int, c_void_p, c_int],
                      [l.nxt_motor_set_power, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_get_power, c_int, c_void_p, c_int],
                      [l.nxt_motor_set_turnratio, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_get_turnratio, c_int, c_void_p, c_int],
                      [l.nxt_motor_set_runstate, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_get_runstate, c_int, c_void_p, c_int],
                      [l.nxt_motor_set_rotation, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_rotate, c_int, c_void_p, c_int, c_int, c_int],
                      [l.nxt_motor_stop, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_sync, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_reset_tacho, c_int, c_void_p, c_int, c_int],
                      [l.nxt_motor_get_tacho_count, c_int, c_void_p, c_int],
                      [l.nxt_motor_get_tacho_limit, c_int, c_void_p, c_int],
                      [l.nxt_motor_get_tacho_block_count, c_int, c_void_p, c_int],
                      [l.nxt_motor_get_rotation_count, c_int, c_void_p, c_int],
                      [l.nxt_motor_get_pid, c_int, c_void_p, c_int, c_void_p, c_void_p, c_void_p],
                      [l.nxt_motor_set_pid, c_int, c_void_p, c_int, c_int, c_int, c_int],
                      [l.nxt_motor_get_speed, c_int, c_void_p, c_int],
                      # libanxt/i2c.c
                      [l.nxt_i2c_read, c_int, c_void_p, c_int, c_int, c_int, c_int, c_void_p],
                      [l.nxt_i2c_write, c_int, c_void_p, c_int, c_int, c_int, c_int, c_void_p],
                      [l.nxt_i2c_cmd, c_int, c_void_p, c_int, c_int, c_int],
                      [l.nxt_i2c_set_i2caddr, c_int, c_void_p, c_int, c_int, c_int],
                      [l.nxt_i2c_get_version, c_int, c_void_p, c_int, c_int],
                      [l.nxt_i2c_get_vendorid, c_int, c_void_p, c_int, c_int],
                      [l.nxt_i2c_get_deviceid, c_int, c_void_p, c_int, c_int],
                      # libanxt/file.c
                      [l.nxt_file_open, c_int, c_void_p, c_char_p, c_int, Libanxt.file_open_union],
                      [l.nxt_file_read, c_int, c_void_p, c_int, c_void_p, c_int],
                      [l.nxt_file_write, c_int, c_void_p, c_int, c_char_p, c_int],
                      [l.nxt_file_close, c_int, c_void_p, c_int],
                      [l.nxt_file_remove, c_int, c_void_p, c_char_p],
                      [l.nxt_file_find_first, c_int, c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_int)],
                      [l.nxt_file_find_next, c_int, c_void_p, c_int, POINTER(c_char_p), POINTER(c_int)])
        for p in prototypes:
            p[0].restype = p[1]
            p[0].argtypes = p[2:]
            #print(p[0],"-",p[0].argtypes,"-",p[0].restype)
