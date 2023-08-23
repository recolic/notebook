# This module keeps target machine unlocked by one of two ways:
#   1. moving mouse by 1 pixel every 58 seconds.
#   2. press "PrintScreen" key every 58 seconds. (Pause/Break key is widely used in Powershell and Putty, it will break manything)

import time, threading
from hid import keyboard as fake_keyboard
from hid import keycodes as hid_keycodes

import os.path
import os

def wake_once_method_2(keyboard_path):
    hid_keycode = hid_keycodes.KEYCODE_PRINT_SCREEN
    hid_modifier_keycode = 0
    failed = "success"

    try:
        fake_keyboard.send_keystroke(keyboard_path, hid_modifier_keycode, hid_keycode)
    except Exception as e:
        failed = "failed " + str(e)
        pass
    
    #with open('/tmp/rlog2', 'w') as f:
    #    f.write('DEBUG: triggered! status=' + str(failed))
    
def keep_awake_daemon_func(keyboard_path):
    wake_once_method_2(keyboard_path)
    while True:
        time.sleep(60+58)
        wake_once_method_2(keyboard_path)

def send_up_enter(keyboard_path):
    failed = "success"
    try:
        fake_keyboard.send_keystroke(keyboard_path, 0, hid_keycodes.KEYCODE_UP_ARROW)
        time.sleep(1)
        fake_keyboard.send_keystroke(keyboard_path, 0, hid_keycodes.KEYCODE_ENTER)
    except Exception as e:
        failed = "failed " + str(e)
        pass

def recv_restapi_func(keyboard_path):
    prev_res = ""
    while True:
        time.sleep(1)
        if os.path.isfile('/tmp/trigger'):
            # os.remove('/tmp/trigger')
            with open('/tmp/trigger') as f:
                res = f.read()
                if res != prev_res:
                    print("DEBUG: triggered")
                    send_up_enter(keyboard_path)
                    prev_res = res

def start_keep_awake_thread(keyboard_path):
    thread = threading.Thread(target = keep_awake_daemon_func, args=(keyboard_path,))
    thread.start()
    thread = threading.Thread(target = recv_restapi_func, args=(keyboard_path,))
    thread.start()
    #with open('/tmp/rlog', 'w') as f:
    #    f.write('DEBUG: keep unlocked thread started')
    # Never join

