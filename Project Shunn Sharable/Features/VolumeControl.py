from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
from time import sleep
import pyautogui

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def check_odd(number):
    if number % 2 != 0:
        return True

def set_volume(set_volume):
    if set_volume>100:
        set_volume = 100
    current_volume = round(100 * volume.GetMasterVolumeLevelScalar())
    if check_odd(current_volume):
        current_volume = current_volume + 1
    if check_odd(set_volume):
        set_volume = set_volume + 1
    while set_volume!=current_volume:
        if set_volume > current_volume:
            pyautogui.hotkey('volumeup')
            sleep(.15)
        elif set_volume < current_volume:
            pyautogui.hotkey('volumedown')
            sleep(.15)
        current_volume = round(100 * volume.GetMasterVolumeLevelScalar())
