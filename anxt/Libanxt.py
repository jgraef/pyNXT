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
from ctypes import CDLL, c_void_p, c_int, c_float, c_char_p, c_long, c_ubyte, POINTER, Union, Structure

class Libanxt:
    class AnalogSensorValues(Structure):
        _fields_ = [("is_calibrated", c_int),
                    ("type", c_int),
                    ("mode", c_int),
                    ("raw", c_int),
                    ("normalized", c_int),
                    ("scaled", c_int),
                    ("calibrated", c_int)]
    class AccelerationVector(Structure):
        _fields_ = [("x", c_int),
                    ("y", c_int),
                    ("z", c_int)]
    class PSPButtons(Structure):
        _fields_ = [("left", c_int),
                    ("down", c_int),
                    ("up", c_int),
                    ("right", c_int),
                    ("r1", c_int),
                    ("l1", c_int),
                    ("r2", c_int),
                    ("l2", c_int),
                    ("r3", c_int),
                    ("l3", c_int),
                    ("square", c_int),
                    ("x", c_int),
                    ("o", c_int),
                    ("triangle", c_int)]
    class PSPJoystick(Structure):
        _fields_ = [("x", c_int),
                    ("y", c_int)]
    class CameraObject(Structure):
        _fields_ = [("id", c_int),
                    ("color", c_int),
                    ("x", c_int),
                    ("y", c_int),
                    ("x2", c_int),
                    ("y2", c_int),
                    ("w", c_int),
                    ("h", c_int)]
    class CameraColormap(Structure):
        _fields_ = [("r", (c_ubyte * 16)),
                    ("g", (c_ubyte * 16)),
                    ("b", (c_ubyte * 16))]
    
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
    def version(libanxt):
        return str(int(libanxt.nxt_version_major()))+"."+str(int(libanxt.nxt_version_minor()))

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
                      [l.nxt_get_sensor_values, c_int, c_void_p, c_int, POINTER(Libanxt.AnalogSensorValues)],
                      [l.nxt_reset_sensor, c_int, c_void_p, c_int],
                      [l.nxt_wait_after_direct_command, None],
                      [l.nxt_wait_after_communication_command, None],
                      [l.nxt_wait_extra_long_after_communication_command, None],
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
                      [l.nxt_file_open_write, c_int, c_void_p, c_char_p, c_int],
                      [l.nxt_file_open_write_linear, c_int, c_void_p, c_char_p, c_int],
                      [l.nxt_file_open_read, c_int, c_void_p, c_char_p, POINTER(c_int)],
                      [l.nxt_file_read, c_int, c_void_p, c_int, c_void_p, c_int],
                      [l.nxt_file_write, c_int, c_void_p, c_int, c_char_p, c_int],
                      [l.nxt_file_close, c_int, c_void_p, c_int],
                      [l.nxt_file_remove, c_int, c_void_p, c_char_p],
                      [l.nxt_file_find_first, c_int, c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_int)],
                      [l.nxt_file_find_next, c_int, c_void_p, c_int, POINTER(c_char_p), POINTER(c_int)],
                      # libanxt/display.c
                      [l.nxt_display_open, c_void_p, c_void_p],
                      [l.nxt_display_close, None, c_void_p],
                      [l.nxt_display_refresh, c_int, c_void_p],
                      [l.nxt_display_flush, c_int, c_void_p, c_int],
                      [l.nxt_display_clear, None, c_void_p, c_int],
                      [l.nxt_display_point, None, c_void_p, c_int, c_int, c_int],
                      [l.nxt_display_line, None, c_void_p, c_int, c_int, c_int, c_int, c_int],
                      [l.nxt_display_circle, None, c_void_p, c_int, c_int, c_int, c_int],
                      #[l.nxt_display_polygon, None, c_void_p, c_int, c_int],
                      [l.nxt_display_text_ext, c_int, c_void_p, c_int, POINTER(c_int), POINTER(c_int), c_char_p, c_int],
                      # libanxt/mod.c
                      [l.nxt_mod_first, c_int, c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_int), POINTER(c_int), POINTER(c_int)],
                      [l.nxt_mod_next, c_int, c_void_p, c_int, POINTER(c_char_p), POINTER(c_int), POINTER(c_int), POINTER(c_int)],
                      [l.nxt_mod_close, c_int, c_void_p, c_int],
                      [l.nxt_mod_read, c_int, c_void_p, c_int, c_void_p, c_int, c_int],
                      [l.nxt_mod_write, c_int, c_void_p, c_int, c_void_p, c_int, c_int],
                      # libanxt/us.c
                      [l.nxt_us_get_dist, c_int, c_void_p, c_int],
                      # libanxt/accel.c
                      [l.nxt_accel_get_sensity, c_float, c_void_p, c_int],
                      [l.nxt_accel_set_sensity, c_int, c_void_p, c_int, c_float],
                      [l.nxt_accel_get_tilt, c_int, c_void_p, c_int, POINTER(Libanxt.AccelerationVector)],
                      [l.nxt_accel_get_accel, c_int, c_void_p, c_int, POINTER(Libanxt.AccelerationVector)],
                      # libanxt/psp.c
                      [l.nxt_psp_get_mode, c_int, c_void_p, c_int],
                      [l.nxt_psp_get_buttons, c_int, c_void_p, c_int, POINTER(Libanxt.PSPButtons)],
                      [l.nxt_psp_get_joystick, c_int, c_void_p, c_int, c_int, POINTER(Libanxt.PSPJoystick)],
                      # libanxt/nxtcam.c
                      [l.nxt_cam_num_objects, c_int, c_void_p, c_int],
                      [l.nxt_cam_get_objects, c_int, c_void_p, c_int, c_int, c_int, POINTER(Libanxt.CameraObject)],
                      [l.nxt_cam_get_colormap, c_int, c_void_p, c_int, POINTER(Libanxt.CameraColormap)],
                      [l.nxt_cam_enable_tracking, None, c_void_p, c_int, c_int],
                      [l.nxt_cam_set_trackingmode, None, c_void_p, c_int, c_int],
                      [l.nxt_cam_reset, None, c_void_p, c_int],
                      [l.nxt_cam_enable_colorsort, None, c_void_p, c_int, c_int],
                      # libanxt/hid.c
                      [l.nxt_hid_set_modifier, c_int, c_void_p, c_int, c_int],
                      [l.nxt_hid_set_key, c_int, c_void_p, c_int, c_int],
                      [l.nxt_hid_transmit, c_int, c_void_p, c_int],
                      [l.nxt_hid_set_mode, c_int, c_void_p, c_int, c_int],
                      [l.nxt_hid_send_str, c_int, c_void_p, c_int, c_char_p])
                      
        for p in prototypes:
            p[0].restype = p[1]
            p[0].argtypes = p[2:]
            #print(p[0],"-",p[0].argtypes,"-",p[0].restype)
