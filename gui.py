#!/usr/bin/python3
# -*- coding: utf-8 -*-
# gui.py
# GUI for the ConnectND app
# Author: Alan Flores
import sys
from PyQt4 import QtGui, QtCore
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.cbook as cbook
import matplotlib.mlab as mlab
import string
import json
import numpy as np
from random import randint

class ConnectND(QtGui.QWidget):
	
	def __init__(self):
		super(ConnectND, self).__init__()
		self.initUI()
		
	def initUI(self):	  
		dmcb = QtGui.QCheckBox('Dorm', self) # setting checkboxes
		dmcb.move(400, 50)
		dmcb.toggle()
		dmcb.stateChanged.connect(self.changeBool1)
		mjcb = QtGui.QCheckBox('Major', self)
		mjcb.move(400, 100)
		mjcb.toggle()
		mjcb.stateChanged.connect(self.changeBool2)
		clcb = QtGui.QCheckBox('College', self)
		clcb.move(400, 150)
		clcb.toggle()
		clcb.stateChanged.connect(self.changeBool3)
		yrcb = QtGui.QCheckBox('Year', self)
		yrcb.move(400, 200)
		yrcb.toggle()
		yrcb.stateChanged.connect(self.changeBool4)
		jbcb = QtGui.QCheckBox('Job', self)
		jbcb.move(400, 250)
		jbcb.toggle()
		jbcb.stateChanged.connect(self.changeBool5)
		hscb = QtGui.QCheckBox('Home State', self)
		hscb.move(400, 300)
		hscb.toggle()
		hscb.stateChanged.connect(self.changeBool6)
		
		self.setGeometry(400, 400, 500, 400) # setting up the GUI
		self.setWindowTitle('ConnectND')
		self.show()

		
	def changeBool1(self, state): # function for a checkbox
		if state == QtCore.Qt.Checked:
			dm = True
		else:
			dm = False
	def changeBool2(self, state):
		if state == QtCore.Qt.Checked:
			mj = True
		else:
			mj = False
	def changeBool3(self, state):
		if state == QtCore.Qt.Checked:
			cl = True
		else:
			cl = False
	def changeBool4(self, state):
		if state == QtCore.Qt.Checked:
			yr = True
		else:
			yr = False
	def changeBool5(self, state):
		if state == QtCore.Qt.Checked:
			jb = True
		else:
			jb = False
	def changeBool6(self, state):
		if state == QtCore.Qt.Checked:
			hs = True
		else:
			hs = False
		
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	CND = ConnectND()
	sys.exit(app.exec_())
