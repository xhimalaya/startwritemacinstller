import win32com.client
import winshell
import os


def create_short_cut_desktop():
    userDesktop = winshell.desktop()
    shell = win32com.client.Dispatch('WScript.Shell')

    shortcut = shell.CreateShortCut(userDesktop + '\\SWTrial.lnk')
    pwd = os.getcwd()
    pwd_target = pwd + '\StartwriteDemoV0.2.exe'
    shortcut.Targetpath = pwd_target
    shortcut.WorkingDirectory = pwd
    shortcut.save()
