#!/usr/bin/python
import serial
import sys
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
	sensibility = 10
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

ser = serial.Serial('/dev/ttyUSB0', 9600)
while 1:
	coordinates = ser.readline()
	splittedCoords = coordinates.partition("&")[0].partition("|")
	x = splittedCoords[0]
	y = splittedCoords[2]
	try:
		x = int(splittedCoords[0])
	except ValueError:
		x = 0
	try:
		y = int(splittedCoords[2])
	except ValueError:
		y = 0
	splittedButtonState = coordinates.partition("&")[2].partition("|")
	try:
		pressedLeft = int(splittedButtonState[0])
	except ValueError:
		pressedLeft = 0
	try:
		pressedRight = int(splittedButtonState[2])
	except ValueError:
		pressedRight = 0
	if pressedLeft == 1:
		mousePress(3)
	else:
		mouseRelease(3)
	if pressedRight == 1:
		mousePress(1)
	else:
		mouseRelease(1)
	moveMouseRelative(x,y)
