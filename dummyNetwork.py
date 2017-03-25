#!/usr/bin/env python2.7

import sys
import networkx as nx
import matplotlib.pyplot as plt
import string
import json
from random import randint

# dummy data to narrow down dictionary
keys = ['ndlevel', 'postaladdress', 'ndtoplevelprimarydepartment', 'ndcurriculum']


def add_connection(Ego, Ego_id, student_dir, G, connection):
    '''Adds students with the given connection and redraws graph'''
    # create node and edge and set node attributes
    
    for student in student_dir:
        if Ego[connection] == student_dir[student][connection]:
            G.add_edge(Ego_id, student)
            G.node[student][connection] = connection
            #G.edge[Ego_id][str(student['cn'])]['connection4'] = 'ndcurriculum'
    

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

def draw_graph(Ego, Ego_id, G):

    pos = nx.random_layout(G)
    labels = {}
    labels[Ego_id] = Ego_id
    nx.draw(G, pos,  node_color ='#0C2340', edge_color = '#bbbec1', node_size = 10, with_labels=False)
    nx.draw_networkx_nodes(G, pos, nodelist = [Ego_id], node_size = 100, node_color = '#C89600')
    nx.draw_networkx_labels(G, pos, labels, font_size = 16)
    
    #edge_labels = nx.get_edge_attributes(G,'connection4')
    #nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
    #plt.savefig('this.png')
    
    plt.show()

if __name__=='__main__':

    # reads json string from ND_directory.json returns list 
    with open('ND_directory.json') as f:
        student_dir_list = json.load(f)

    student_dir = {}

    for student in student_dir_list:
        try:
            if set(keys).issubset(set(student.keys())):
                student_dir[student["uid"]] = student
        except:
            pass
    
    Ego_id = raw_input("Enter valid netid: ")

    try:
        Ego = student_dir.pop(Ego_id)
    except:
        sys.exit('Not a valid netid')
    
    G = nx.Graph()
    connection = ''
    while True:
        userI = raw_input("Add(A), Remove(R) connection or Quit(Q): ")

        if userI == "A":
            connection = raw_input("Add connection: ")
            add_connection(Ego, Ego_id, student_dir, G, connection)
            draw_graph(Ego, Ego_id, G)

        if userI == "R":
            connection = raw_input("Remove connection: ")
            remove_connection(G, connection)
            draw_graph(Ego, Ego_id, G)

        if userI == "Q":
            break
    print 'ConnectND'
