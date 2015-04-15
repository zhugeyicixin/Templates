#! /usr/bin/env python
# -*- coding: utf-8 -*-
from win32gui import *
titles = set()
def foo(hwnd,mouse):
	# if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
	titles.add(GetWindowText(hwnd))
	# t = GetWindowText(hwnd)
	# print t
	# if t == 'gview':
		# print GetClassName(hwnd)
		# print t
EnumWindows(foo, 0)
print titles
lt = [t for t in titles if t]
lt.sort()
for t in lt:
	print t