#!/usr/bin/env python2.7
# Make request to ND Online directory using multiprocessing
# Author: Mimi Chen

import requests
import json
import os
import re # Regular expressions 
import multiprocessing

def store_student(student):
	'''Return dictionary of student information from ND student directory given NetID'''
	netid = student.split("-")[1]
	number = student.split("-")[0]
	r = requests.get("http://ur.nd.edu/request/eds.php?uid={}&full_response=true".format(str(netid)))
	try: 
		resp = json.loads(r.content.decode("utf-8"))
		print "{} {}".format(number, netid)
		return resp
	except ValueError:
		print "Could not access for netid: {}".format(netid)
		pass


	
if __name__ == "__main__":
	# Open file containing all NetIDs (could contain professor and staff NetID)
	with open("full_netid.txt") as f:
		NetIDs = [ str(index) + '-' + netid.rstrip() for index, netid in enumerate(f) ] 

	# Using parallel programming
	pool = multiprocessing.Pool(6) 		# Create 6 processes
	results = pool.map(store_student, NetIDs)

	# Write to file ND_raw_directory.json
	output = open("ND_raw_directory.json", 'w')
	output.write(json.dumps(results))
	output.close()

