#!/usr/bin/python
import serial
import sys
import ast
from Xlib import X, display
import Xlib.ext.xtest

d = display.Display()
s = d.screen()
root = s.root

def moveMouseRelative(xIncrease,yIncrease):
	mouseX = root.query_pointer()._data["root_x"]
	mouseY = root.query_pointer()._data["root_y"]
	newMouseX = mouseX
	newMouseY = mouseY
	factor = 6
	sensibility = 5
	if xIncrease > sensibility or xIncrease < -sensibility:
		newMouseX = mouseX+(xIncrease/factor)
	if yIncrease > sensibility or yIncrease < -sensibility:
		newMouseY = mouseY-(yIncrease/factor)
	root.warp_pointer(newMouseX,newMouseY)
	d.sync()

def mousePress(button):
	Xlib.ext.xtest.fake_input(d,Xlib.X.ButtonPress, button)
	d.sync()

def mouseRelease(button):
	Xlib.ext.xtest.fake_input(d,Xlib.X.ButtonRelease, button)
	d.sync()

def mouseWheelUp():
	Xlib.ext.xtest.fake_input(d,Xlib.X.ButtonPress, 4)
	Xlib.ext.xtest.fake_input(d,Xlib.X.ButtonRelease, 4)
	d.sync()

def mouseWheelDown():
	Xlib.ext.xtest.fake_input(d,Xlib.X.ButtonPress, 5)
	Xlib.ext.xtest.fake_input(d,Xlib.X.ButtonRelease, 5)
	d.sync()

def processNunChuckInput(input):
	try:
		nunChuckInput = ast.literal_eval(nunChuckInputString)
	except SyntaxError:
		return
	cPressed = nunChuckInput['c'] == 1
	zPressed = nunChuckInput['z'] == 1
	if cPressed:
		mousePress(3)
	else:
 		mouseRelease(3)
	if zPressed:
		mousePress(1)
	else:
		mouseRelease(1)
	rollLimitValue = 70
	if nunChuckInput['r'] > rollLimitValue:
		mouseWheelUp()
	if nunChuckInput['r'] < -rollLimitValue:
		mouseWheelDown()
	moveMouseRelative(nunChuckInput['x'],nunChuckInput['y'])

try:
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	ser.readline()
except SerialException:
	ser = serial.Serial('/dev/ttyUSB1', 9600)

while 1:
	nunChuckInputString = ser.readline()
	processNunChuckInput(nunChuckInputString)
