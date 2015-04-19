# this is a class for GaussView controlling
import os
import time
import win32api,win32gui,win32con,win32com
import subprocess

class gview:
	location = 'D:\hetanjin\professionalSoftware\g09w\gview.exe'
	hwnd = 0x00

	def __init__(self,location='D:\hetanjin\professionalSoftware\g09w\gview.exe'):
		self.location = location
		self.hwnd = 0x00

	def test(self):
		print 'test of gview'

	def openSoft(self):
		# os.system(self.location)
		cmd = []
		cmd.append(self.location)
		p = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		time.sleep(3)
		tmp_hwnd = win32gui.FindWindow(None,'warning')
		if tmp_hwnd:
			win32gui.SetForegroundWindow(tmp_hwnd)
			# key: enter
			win32api.keybd_event(13,0,0,0) 
			win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(7)

	def findHWND(self):
		self.hwnd = win32gui.FindWindow('QWidget','GaussView 5.0.8')
		return self.hwnd

	def show(self):
		if self.hwnd == 0:
			self.findHWND()
			win32gui.ShowWindow(self.hwnd,1)
			# add two lines for the pywintypes.error:(1400, 'setforegroundwindow',.....)
			# shell = win32com.client.Dispatch("WScript.Shell")
			# shell.SendKeys('%')
	    	win32gui.SetForegroundWindow(self.hwnd) 

	def showWindowInfo(self):
		self.show()
		print 'title:\t' + self.foreWindowTitle()
		print 'class:\t' + self.foreWindowClass()

	def foreWindowTitle(self):
		tmp_hwnd = win32gui.GetForegroundWindow()
		tmp_title = win32gui.GetWindowText(tmp_hwnd)
		return tmp_title

	def foreWindowClass(self):
		tmp_hwnd = win32gui.GetForegroundWindow()
		tmp_class = win32gui.GetClassName(tmp_hwnd)
		return tmp_class

	def openFile(self, directory, fileName):
		self.show()
		# key: ctrl
		win32api.keybd_event(17,0,0,0)  
		# key: o
		win32api.keybd_event(79,0,0,0)  
		win32api.keybd_event(79,0,win32con.KEYEVENTF_KEYUP,0) 
		win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(1)
		tmp_hwnd = win32gui.FindWindow('#32770','Open Files')
		tmp_hwnd2 = win32gui.FindWindowEx(tmp_hwnd, None, 'ComboBoxEx32', None)
		win32gui.SendMessage(tmp_hwnd2, win32con.WM_SETTEXT, None, directory + '\\' + fileName)
		# key: enter
		win32api.keybd_event(13,0,0,0) 
		win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(0.5)
		tmp_hwnd = win32gui.FindWindow(None,'warning')
		if tmp_hwnd:
			win32gui.SetForegroundWindow(tmp_hwnd)
			# key: enter
			win32api.keybd_event(13,0,0,0) 
			win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0) 
		time.sleep(0.5)
	
	def saveFile(self, rename):
		# key: ctrl
		win32api.keybd_event(17,0,0,0)  
		# key: s
		win32api.keybd_event(83,0,0,0)  
		win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0) 
		win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(1)
		tmp_hwnd = win32gui.FindWindow('#32770', None)
		tmp_hwnd2 = win32gui.FindWindowEx(tmp_hwnd, None, 'ComboBoxEx32', None)
		win32gui.SendMessage(tmp_hwnd2, win32con.WM_SETTEXT, None, rename)
		# key: enter
		win32api.keybd_event(13,0,0,0) 
		win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(1) 
		# key: enter
		win32api.keybd_event(13,0,0,0) 
		win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(0.5) 

	def openAndSave(self, directory, fileName, rename='result_'):
		self.openFile(directory,fileName)
		self.saveFile(rename + fileName[0:-4] + '.gjf')

	def closeSoft(self):
		win32gui.SendMessage(self.hwnd, win32con.WM_CLOSE)
		pass


