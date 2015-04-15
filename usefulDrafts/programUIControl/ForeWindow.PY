import sys
import subprocess
import os
import signal
import time
import win32api,win32gui,win32con

soft_name='QWidget'
def show(soft_name):  
    # windows handlers  
    #hwnd = soft_name.window.handle
    hwnd = win32gui.FindWindow(None,'GaussView 5.0.8')
    print hwnd
    win32gui.ShowWindow(hwnd,1) 

    win32gui.SetForegroundWindow(hwnd)  
    #win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)    
    #X11LockScreenWindow.show(soft_name)  


cmd = ['D:\hetanjin\professionalSoftware\g09w\gview.exe']

p = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print p.poll()
# time.sleep(5)
show(soft_name)
win32api.keybd_event(17,0,0,0)  
win32api.keybd_event(79,0,0,0)  
win32api.keybd_event(79,0,win32con.KEYEVENTF_KEYUP,0) 
win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
print p.poll()
time.sleep(1)
# p.stdin.write('C5P.log')
# win32api.keybd_event(65,0,0,0) 
# win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0) 
# tmp=win32gui.GetForegroundWindow()
hn1 = win32gui.FindWindow('#32770','Open Files')
hn2 = win32gui.FindWindowEx(hn1,None,'ComboBoxEx32',None)
win32gui.SendMessage(hn2,win32con.WM_SETTEXT,None,'test')
