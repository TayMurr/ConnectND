#!/usr/bin/python2.7
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
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

keys = ['dorm']
pos1 = {}
Ego_id =''


with open('ND_complete_directory.json') as f:
	student_big_dir = json.load(f)

student_dir = {}

for student in student_big_dir:
	try:
		if set(keys).issubset(set(student_big_dir[student].keys())):
			student_dir[student_big_dir[student]["uid"]] = student_big_dir[student]
	except:
		pass

Ego_id = raw_input("Enter valid netid: ")

try:
	Ego = student_dir.pop(Ego_id)
except:
	sys.exit('Not a valid netid')

G = nx.Graph()
#print 'student dorm'
#print student_dir["amonn"]["dorm"]
#connection = ''
#connection_Num = 0
#for student in student_dir:
#	if Ego["dorm"] == student_dir[student]["dorm"]:
#		G.add_edge(Ego_id, student)
	    #G.node[student]['ndlevel'] = 'ndlevel'
	    #connection_Num = connection_Num + 1
	    #G.edge[Ego_id][student]['connection4'] = 'ndcurriculum'


class Annotate(object):
	"""Annoate when rolling over a node"""
	def __init__(self,G, ax=None):
		if ax is None:
			self.ax = plt.gca()
		else:
			self.ax = ax

		self.annotations = {} # create dicionary of annotations with nodes as keys
		#print G.nodes()
		for node in G.nodes():
			#print student_dir[node]["dorm"]
			#print 'positions dict'
			#print pos1
			self.annotations[node] = self.annotate(node, pos1[node][0], pos1[node][1])

	def annotate(self, node, x1, y1):
        #get info about node create a string. if you have name of node you can do anyting
		try:
			get_node = '{}\n{}'.format(node, edge_labels[Ego_id][node])
		except:
			get_node = '{}'.format(node)

		annotation = self.ax.annotate(get_node, xy=(x1,y1), bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha=0.5))
		annotation.set_visible(False)
		return annotation

	def __call__(self, event):
		x, y = event.xdata, event.ydata
		if x is not None:
            # make the other annotations invisible
			for ann in self.annotations.values():
				ann.set_visible(False)
		for node in pos1:
			if np.abs(x - pos1[node][0]) < 0.01 and np.abs( y - pos1[node][1]) < 0.01:
				annotation = self.annotations[node]
				annotation.set_visible(True)
                    #print '{} is positioned at {}, {}'.format(node, x, y)
				event.canvas.draw()

def draw_graph(ax):
	pos = nx.random_layout(G)
	pos1.update(pos)
	labels = {}
	labels[Ego_id] = Ego_id
	print ax
	nx.draw(G, pos, node_color = '#0C2340', edge_color = '#bbbec1', node_size = 10, with_label = False)
	nx.draw_networkx_nodes(G, pos, nodelist = [Ego_id], node_size = 100, node_color = '#C89600')
	nx.draw_networkx_labels(G, pos, labels, font_size = 12)
	#af= Annotate(G, ax=ax)
	


class ConnectND(QtGui.QWidget):
	
	def __init__(self):
		super(ConnectND, self).__init__()
		self.initUI()
		#pos1 = {}
		#pos = nx.random_layout(G)
		#labels = {}
		#labels[Ego_id] = Ego_id
		#nx.draw(G, pos,  node_color ='#0C2340', edge_color = '#bbbec1', node_size = 10, with_labels=False, ax=self.ax)
		#nx.draw_networkx_nodes(G, pos, nodelist = [Ego_id], node_size = 100, node_color = '#C89600', ax=self.ax)
		#nx.draw_networkx_labels(G, pos, labels, font_size = 12, ax=self.ax)

		#pos1.update(pos)
		#print G.nodes()
		af = Annotate(G, ax=self.ax)
		self.fig.canvas.mpl_connect('motion_notify_event', af)

		
	def initUI(self):
                self.fig = plt.figure()
		#plt.close(self.fig)
                self.canvas = FigureCanvas(self.fig)
		self.ax = self.fig.add_subplot(111)
		#self.canvas.draw()
		dmcb = QtGui.QCheckBox('Dorm', self) # setting checkboxes
		dmcb.move(400, 50)
		#dmcb.toggle()
		dmcb.stateChanged.connect(self.changeBool1)
		clcb = QtGui.QCheckBox('College', self)
		clcb.move(400, 100)
		#clcb.toggle()
		clcb.stateChanged.connect(self.changeBool2)
		nlcb = QtGui.QCheckBox('ND Level', self)
		nlcb.move(400, 150)
		#nlcb.toggle()
		nlcb.stateChanged.connect(self.changeBool3)
		nacb = QtGui.QCheckBox('ND Affiliation', self)
		nacb.move(400, 200)
		#nacb.toggle()
		nacb.stateChanged.connect(self.changeBool4)
		self.setGeometry(400, 400, 500, 400) # setting up the GUI
		self.setWindowTitle('ConnectND')
		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.canvas)
		layout.addWidget(dmcb)
		layout.addWidget(clcb)
		layout.addWidget(nlcb)
		layout.addWidget(nacb)
		self.setLayout(layout)

		#self.show()
	
	def changeBool1(self, state): # function for a checkbox
		if state == QtCore.Qt.Checked:
			dm = True
		    # create node and edge and set node attributes
			for student in student_dir:
				if Ego["dorm"] == student_dir[student]["dorm"]:
					G.add_edge(Ego_id, student)
					G.node[student]["dorm"] = "dorm"
		else:
			dm = False
			delete_nodes = []
			for node_1 in G.nodes_iter():
				try:
					if "dorm" in G.node[node_1].keys():
						delete_nodes.append(node_1)
				except:
					pass
			#print delete_nodes
			G.remove_nodes_from(delete_nodes)
			#plt.show()
		self.fig.clf()
		draw_graph(self.ax)
		print pos1
		af = Annotate(G, ax=self.ax)
                self.fig.canvas.mpl_connect('motion_notify_event', af)
		self.canvas.draw()

	def changeBool2(self, state):
		if state == QtCore.Qt.Checked:
			cg = True
                        for student in student_dir:
                                if Ego["college"] == student_dir[student]["college"]:
                                        G.add_edge(Ego_id, student)
		else:
			cg = False
                        delete_nodes = []
                        for node_1 in G.nodes_iter():
                        	try:
                                	if "college" in G.node[node_1].keys():
                                		delete_nodes.append(node_1)
                        	except:
                                	pass
                        G.remove_nodes_from(delete_nodes)
		draw_graph()
		self.canvas.draw()

	def changeBool3(self, state):
		if state == QtCore.Qt.Checked:
			nl = True
                        for student in student_dir:
                                if Ego["ndlevel"] == student_dir[student]["ndlevel"]:
                                        G.add_edge(Ego_id, student)
		else:
			nl = False
                        delete_nodes = []
                        for node_1 in G.nodes_iter():
                        	try:
                                	if "ndlevel" in G.node[node_1].keys():
                                		delete_nodes.append(node_1)
				except:
                                	pass
                        G.remove_nodes_from(delete_nodes)
		draw_graph()
		self.canvas.draw()

	def changeBool4(self, state):
		if state == QtCore.Qt.Checked:
			na = True
                        for student in student_dir:
                                if Ego["ndaffiliation"] == student_dir[student]["ndaffiliation"]:
                                        G.add_edge(Ego_id, student)
		else:
			na = False
                        delete_nodes = []
                        for node_1 in G.nodes_iter():
                        	try:
                                	if "ndaffiliation" in G.node[node_1].keys():
                                		delete_nodes.append(node_1)
				except:
                                	pass
                        G.remove_nodes_from(delete_nodes)
		draw_graph()
		self.canvas.draw()

'''	def changeBool5(self, state):
		if state == QtCore.Qt.Checked:
			jb = True
                        for student in student_dir:
                                if Ego[connection] == student_dir[student][connection]:
                                        G.add_edge(Ego_id, student)
		else:
			jb = False
                        delete_nodes = []
                        for node_1 in G.nodes_iter():
                        try:
                                if connection in G.node[node_1].keys():
                                delete_nodes.append(node_1)
                        except:
                                pass
                        G.remove_nodes_from(delete_nodes)
		self.fig.canvas.draw()
	def changeBool6(self, state):
		if state == QtCore.Qt.Checked:
			hs = True
                        for student in student_dir:
                                if Ego[connection] == student_dir[student][connection]:
                                        G.add_edge(Ego_id, student)
		else:
			hs = False
                        delete_nodes = []
                        for node_1 in G.nodes_iter():
                        try:
                                if connection in G.node[node_1].keys():
                                delete_nodes.append(node_1)
                        except:
                                pass
                        G.remove_nodes_from(delete_nodes)
		self.fig.canvas.draw()
'''
if __name__ == '__main__':
	#print G.nodes()
	app = QtGui.QApplication(sys.argv)
	CND = ConnectND()
	CND.show()
	sys.exit(app.exec_())
