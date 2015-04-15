# -*- coding: cp936 -*-

import win32api,win32gui,win32con

self='SE_SogouExplorerFrame'
self='QWidget'
def show(self):  
    # windows handlers  
    #hwnd = self.window.handle
    hwnd = win32gui.FindWindow(self,'GaussView 5.0.8')
    win32gui.ShowWindow(hwnd,1) 

    win32gui.SetForegroundWindow(hwnd)  
    #win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)    
    #X11LockScreenWindow.show(self)  
show(self)
#send key
# win32api.keybd_event(18,0,0,0)  
# win32api.keybd_event(115,0,0,0)  
# win32api.keybd_event(115,0,win32con.KEYEVENTF_KEYUP,0) 
# win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)

# win32api.keybd_event(65,0,0,0)  
# win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0) 
# win32api.keybd_event(65,0,0,0)  
# win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)
# win32api.keybd_event(65,0,0,0)  
# win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)
# win32api.keybd_event(65,0,0,0)  
# win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)
# win32api.keybd_event(65,0,0,0)  
# win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)
# win32api.keybd_event(65,0,0,0)  
# win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)