import win32api
import os
import time
for a in range(4):
    win32api.ShellExecute(0,"print","test.pdf",None,None,0)
    time.sleep(30)