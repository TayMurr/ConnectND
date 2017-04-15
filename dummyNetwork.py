#!/usr/bin/env python2.7

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

# dummy data to narrow down dictionary
keys = ['dorm']
pos1 = {}
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


def add_connection(Ego, Ego_id, student_dir, G, connection):
    '''Adds students with the given connection and redraws graph'''
    # create node and edge and set node attributes
    for student in student_dir:
        i
        if Ego[connection] == student_dir[student][connection]:
            G.add_edge(Ego_id, student)
            G.node[student][connection] = connection
            #G.edge[Ego_id][str(student['cn'])]['connection4'] = 'ndcurriculum'
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

if __name__=='__main__':

    # reads json string from ND_directory.json returns list 
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
    
    #connection = ''
    #connection_Num = 0
    for student in student_dir:
        if Ego["dorm"] == student_dir[student]["dorm"]:
            G.add_edge(Ego_id, student)
            #G.node[student]['ndlevel'] = 'ndlevel'
            #connection_Num = connection_Num + 1
            #G.edge[Ego_id][student]['connection4'] = 'ndcurriculum'
        '''if Ego['postaladdress'] == student_dir[student]['postaladdress']:
            G.add_edge(Ego_id, student)
            G.node[student]['postaladdress'] = 'postaladdress'
            connection_Num = connection_Num + 1
            G.edge[Ego_id][student]['connection4'] = 'ndcurriculum'
        if Ego['ndtoplevelprimarydepartment'] == student_dir[student]['ndtoplevelprimarydepartment']:
            G.add_edge(Ego_id, student)
            G.node[student]['ndtoplevelprimarydepartment'] = 'ndtoplevelprimarydepartment'
            connection_Num = connection_Num + 1
            G.edge[Ego_id][student]['connection4'] = 'ndcurriculum'
        if Ego['ndcurriculum'] == student_dir[student]['ndcurriculum']:
            G.add_edge(Ego_id, student)
            G.node[student]['ndcurriculum'] = 'ndcurriculum'
            connection_Num = connection_Num + 1
            G.edge[Ego_id][student]['connection4'] = 'ndcurriculum'
        if connection_Num < 2 and connection_Num > 0:
            G.remove_node(student)'''
    
  

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
    print edge_labels
    print type(edge_labels)
    #nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
    #plt.savefig('this.png')
    #print pos['kforti']

    af = Annotate(G, ax=ax)
    fig.canvas.mpl_connect('motion_notify_event', af);
    plt.show()
   
    print 'Program has ended.'
