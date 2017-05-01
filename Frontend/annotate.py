#!/usr/bin/env python2.7
# ConnectND Annotate
# NetworkX Author: Taylor Murray
# Database Adding Author: Mimi Chen

# The purpose of this program in addition to our final project is to show that the Annotate class is working correctly
# when the program prompts you for a valid netid use the netid mchen6
import warnings
warnings.filterwarnings("ignore")
import sys
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.cbook as cbook
import matplotlib.mlab as mlab
import string
import json
import numpy as np
from random import randint
import requests

CONNECTIONS = ['dorm', 'homestate']
ALL_DORMS = ["Carroll Hall", "Knott Hall", "Flaherty Hall", "Sorin Hall", "Howard Hall", "Duncan Hall", "Breen-Phillips Hall", "Siegfried Hall", "Flanner Hall","Fisher Hall", "Badin Hall", "Lyons Hall", "Cavanaugh Hall", "Morrissey Hall","Pasquerilla West Hall", "McGlinn Hall", "Lewis Hall", "Dillon Hall", "Farley Hall", "Pasquerilla East Hall", "Welsh Family Hall", "O'Neill Hall", "Stanford Hall", "Keenan Hall", "Zahm Hall", "Keough Hall", "St. Edward's Hall","Dunne Hall", "Pangborn Hall", "Alumni Hall", "Ryan Hall", "Off-campus"]
STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
ALL_KEYS = ["ndlevel", "ndtoplevelprimarydepartment", "ndcurriculum", "uid", "ndformalname", "mail", "ndadditionaltitleinfo", "ndaffiliation", "title", "nddepartment", "ndtitle", "departmentnumber" ]

pos1 = {}
student_dir = {}
Ego_id =''
class Annotate(object):
    """Annoate when rolling over a node"""
    def __init__(self,G, ax=None):
        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax

        self.annotations = {} # create dicionary of annotations with nodes as keys

        for node in G.nodes():
            self.annotations[node] = self.annotate(node, pos1[node][0], pos1[node][1])

    def annotate(self, node, x1, y1):
        #get info about node create a string. if you have name of node you can do anyting
        try:
		
            get_node = 'Connection:\n{}\n{}\n{}\n{}\n{}'.format(student_dir[node]['ndformalname'],  student_dir[node]['ndlevel'], student_dir[node]['college'][0], student_dir[node]['dorm'],  student_dir[node]['mail'])
        except:
            get_node = '{}\n{}\n{}\n{}\n{}\n'.format(Ego['ndformalname'],  Ego['ndlevel'], Ego['college'][0], Ego['dorm'],  Ego['mail'])

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
                    event.canvas.draw()


def add_connection(Ego, Ego_id, student_dir, G, connection):
    '''Adds students with the given connection and redraws graph'''
    # create node and edge and set node attributes
    for student in student_dir:
        if Ego[connection] == student_dir[student][connection]:
            G.add_edge(Ego_id, student)
            G.node[student][connection] = connection
            
    # add nodes and edges from graph

def remove_connection(G, connection):
    '''Remove nodes with given attribute and redraws graph'''
    delete_nodes = []
    for node_1 in G.nodes_iter():
        try:
            if connection in G.node[node_1].keys():
                delete_nodes.append(node_1)
        except:
            pass
    G.remove_nodes_from(delete_nodes)

def add_new_user(server, netid):
	try:
		r = requests.get("http://ur.nd.edu/request/eds.php?uid={}&full_response=true".format(str(netid)))
		raw_student_info = json.loads(r.content.decode("utf-8"))
		info = {}
		for k in ALL_KEYS:
			if k in raw_student_info.keys():
				info[k] = raw_student_info[k]

		# Combine college and curriculum
		college = set()

		if "ndtoplevelprimarydepartment" in info.keys():
			college.add(info["ndtoplevelprimarydepartment"])
			del info["ndtoplevelprimarydepartment"]
		if "ndcurriculum" in info.keys():
			college.add(info["ndcurriculum"])
			del info["ndcurriculum"]

		info["college"] = list(college)

		# Combine work departments
		work_department = set() # set to hold unique student work departments
		if "nddepartment" in info.keys():
			depart = info["nddepartment"]
			work_department.add(depart)
			del info["nddepartment"]
		if "departmentnumber" in info.keys():
			depart = info["departmentnumber"]
			work_department.add(depart)
			del info["departmentnumber"]

		info["workdepartment"] = list(work_department)
		
		# Combine student jobs
		jobs = set() # set to hold unique student jobs 
		if "ndtitle" in info.keys():
			jobs.add( info["ndtitle"] )
			del info["ndtitle"] 
		if "title" in info.keys():
			jobs.add( info["title"])
			del info["title"]
		if "ndadditionaltitleinfo" in info.keys():
			jobs.add( info["ndadditionaltitleinfo"])
			del info["ndadditionaltitleinfo"]
		info["jobs"] = list(jobs) # Create new key "jobs" with value of a set of jobs	

		if (server): 
			r = requests.put("http://ash.campus.nd.edu:40440/students/"+netid, data = json.dumps(info))
		else: 
			with open("ND_database.json") as f: 
				student_big_dir = json.load(f)
			student_big_dir[netid] = info
			output = open("ND_database.json", "w")
			output.write(json.dumps(student_big_dir))
			output.close()

		if (add_dorm(server, netid)):
			return -1
		if (add_homestate(server, netid)):
			return -1
		return 0

	except Exception as ex:
		print "Error adding new user: {}".format(ex)
		return -1


def add_dorm(server, netid):
	if (server):
		try:
			r = requests.get("http://ash.campus.nd.edu:40440/students/"+netid)
			student_info = json.loads(r.content.decode("utf-8"))["data"]
			dorm = raw_input("Enter dorm: ")
			while (dorm not in ALL_DORMS):
				print "Invalid dorm. Below are the valid options"
				for d in ALL_DORMS:
					print "- {}".format(d)
				dorm = raw_input("Enter dorm: ")
			student_info["dorm"] = dorm
			r = requests.put("http://ash.campus.nd.edu:40440/students/"+netid, data = json.dumps(student_info))
		except Exception as ex:
			print "Error adding dorm: {}".format(ex)
			return -1
	else:
		with open("ND_database.json") as f: 
			student_big_dir = json.load(f)
		#student_big_dir[netid] = student_info
		student_info = student_big_dir[netid]


		dorm = raw_input("Enter dorm: ")
		while (dorm not in ALL_DORMS):
			print "Invalid dorm. Below are the valid options"
			for d in ALL_DORMS:
				print "- {}".format(d)
			dorm = raw_input("Enter dorm: ")
		student_info["dorm"] = dorm

		output = open("ND_database.json", "w")
		output.write(json.dumps(student_big_dir))
		output.close()
	return 0


def add_homestate(server, netid):
	if (server):
		try:
			r = requests.get("http://ash.campus.nd.edu:40440/students/"+netid)
			student_info = json.loads(r.content.decode("utf-8"))["data"]
			state = raw_input("Enter homestate abbreviation: ")
			while (state not in STATES):
				print "Invalid dorm. Below are the valid options"
				for s in STATES:
					print "- {}".format(s)
				state = raw_input("Enter homestate abbreviation: ")
			student_info["homestate"] = state
			r = requests.put("http://ash.campus.nd.edu:40440/students/"+netid, data = json.dumps(student_info))
		except Exception as ex:
			print "Error adding homestate: {}".format(ex)
			return -1

	else:
		with open("ND_database.json") as f: 
			student_big_dir = json.load(f)
		student_info = student_big_dir[netid]
		state = raw_input("Enter homestate abbreviation: ")
		while (state not in STATES):
			print "Invalid dorm. Below are the valid options"
			for s in STATES:
				print "- {}".format(s)
			state = raw_input("Enter homestate abbreviation: ")
		student_info["homestate"] = state
		output = open("ND_database.json", "w")
		output.write(json.dumps(student_big_dir))
		output.close()
	return 0
	
def init_get_directory():
	server = True
    # Try to load data from server
	try:
		r = requests.get("http://ash.campus.nd.edu:40440/students/")
		student_big_dir = json.loads(r.content.decode("utf-8"))["data"]
		print "Loading data from server"

	# If server is down, load from file
	except: 
		with open("ND_database.json") as f: 
			student_big_dir = json.load(f)
		print "Loading data from file"
		server = False
	return server, student_big_dir

def get_directory(server):
	if (server):
		try:
		# Try to load data from server
			r = requests.get("http://ash.campus.nd.edu:40440/students/")
			student_big_dir = json.loads(r.content.decode("utf-8"))["data"]
			print "Loading data from server"
		except: 
			print "Error loading from server"
	else:
		with open("ND_database.json") as f: 
			student_big_dir = json.load(f)
		print "Loading data from file"
	return student_big_dir

if __name__=='__main__':

	server, student_big_dir = init_get_directory()
	student_dir = {}

	Ego_id = raw_input("Enter valid netid: ")
	# Check if user is in the online database
	if (Ego_id not in student_big_dir.keys()):
		status = add_new_user(server, Ego_id)
		if (status != 0):
			sys.exit(1)
		student_big_dir = get_directory(server)
	# Check if user has dorm field
	elif ("dorm" not in student_big_dir[Ego_id].keys()):
		status = add_dorm(server, Ego_id)
		if (status != 0): 
			sys.exit(1)
		student_big_dir = get_directory(server)
	# Check if user has home state field
	elif ("homestate" not in student_big_dir[Ego_id].keys()):
		status = add_homestate(server, Ego_id)
		if (status != 0):
			sys.exit(1)
		student_big_dir = get_directory(server)

	# Ask user which connection to see
	connection = raw_input("Enter a connection type: ")
	while (connection not in CONNECTIONS):
		print "Invalid connections. Below are valid connections:"
		for c in CONNECTIONS:
			print "- {}".format(c)
		connection = raw_input("Enter a connection type: ")

	# Create dictionary of all students who share the desired connection
	for student in student_big_dir:
		try:
			if connection in student_big_dir[student].keys():
				student_dir[student] = student_big_dir[student]
		except:
			pass

	try:
		Ego = student_dir.pop(Ego_id)
	except Exception as ex:
		sys.exit('Not a valid netid')
	
	G = nx.Graph()
	for student in student_dir:
		#if Ego["dorm"] == student_dir[student]["dorm"]:
		if Ego[connection] == student_dir[student][connection]:
			G.add_edge(Ego_id, student)
	
                          
	fig = figure()
	ax = fig.add_subplot(111)
	pos = nx.random_layout(G)
	labels = {}
	labels[Ego_id] = Ego_id
	nx.draw(G, pos,  node_color ='#0C2340', edge_color = '#bbbec1', node_size = 10, with_labels=False, ax=ax)
	nx.draw_networkx_nodes(G, pos, nodelist = [Ego_id], node_size = 100, node_color = '#C89600', ax=ax)
	nx.draw_networkx_labels(G, pos, labels, font_size = 12, ax=ax)

	pos1.update(pos)

	edge_labels = nx.get_edge_attributes(G,'connection4')

	af = Annotate(G, ax=ax)
	fig.canvas.mpl_connect('motion_notify_event', af);
	plt.show()

	print 'Program has ended.'

