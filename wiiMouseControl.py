#!/usr/bin/python
import serial
import sys
import ast
from Xlib import X,XK, display
import Xlib.ext.xtest

d = display.Display()
s = d.screen()
root = s.root

def joystickOutsideRestingArea(value):
	sensibility = 5
	return valueInside(sensibility,value)

def valueInside(sensibility,value):
	return value > sensibility or value < -sensibility

def moveMouseRelative(xIncrease,yIncrease):
	mouseX = root.query_pointer()._data["root_x"]
	mouseY = root.query_pointer()._data["root_y"]
	newMouseX = mouseX
	newMouseY = mouseY
	factor = 6
	if joystickOutsideRestingArea(xIncrease):
		newMouseX = mouseX+(xIncrease/factor)
	if joystickOutsideRestingArea(yIncrease):
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

def mouseWheel(value):
	if joystickOutsideRestingArea(value):
		if value > 0:
			mouseWheelUp()
		else:
			mouseWheelDown()

control = 37

def ctrlPlus():
	plus = 21 
	shift = 50

	Xlib.ext.xtest.fake_input(d, Xlib.X.KeyPress, control)	
	Xlib.ext.xtest.fake_input(d, Xlib.X.KeyPress, shift)
	Xlib.ext.xtest.fake_input(d, Xlib.X.KeyPress, plus)

	Xlib.ext.xtest.fake_input(d, Xlib.X.KeyRelease, control)
	Xlib.ext.xtest.fake_input(d, Xlib.X.KeyRelease, shift)
	Xlib.ext.xtest.fake_input(d, Xlib.X.KeyRelease, plus)	
	d.sync()

def ctrlMinus():
	minus = 20
	Xlib.ext.xtest.fake_input(d, Xlib.X.KeyPress, control)
	Xlib.ext.xtest.fake_input(d, Xlib.X.KeyPress, minus)
  
	Xlib.ext.xtest.fake_input(d, Xlib.X.KeyRelease, control)
	Xlib.ext.xtest.fake_input(d, Xlib.X.KeyRelease, minus) 

	d.sync()

def ctrl(value):
	if valueInside(90,value):
		if value > 0:
			ctrlPlus()
		else:
			ctrlMinus()

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
	rollingUp = nunChuckInput['r'] > rollLimitValue
	rollingDown = nunChuckInput['r'] < -rollLimitValue
	if rollingUp or rollingDown:
		mouseWheel(nunChuckInput['y'])
		ctrl(nunChuckInput['x'])
	else:
		moveMouseRelative(nunChuckInput['x'],nunChuckInput['y'])

try:
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	ser.readline()
except SerialException:
	ser = serial.Serial('/dev/ttyUSB1', 9600)

while 1:
	nunChuckInputString = ser.readline()
	processNunChuckInput(nunChuckInputString)
