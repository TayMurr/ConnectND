#!/usr/bin/env python2.7
import json

# Filter the "ND_filtered_directory.json" by "postaladdress" by determining if address is the dorm address
# of the home address

# Deleted field "postaladdress" and created "dorm" and "homestate"

if __name__ == "__main__":
	# Get the filetered student directory
	student_dir = {}
	with open("ND_filtered_directory.json") as f:
		student_dir = json.load(f)
	
	print "Size of student directory: {}".format(len(student_dir))

	# Loop through the key value pair in dictionary "student_dir"
	for student, info in student_dir.items():
		address = info["postaladdress"].split("$")[0] # gets the hall address (ie. 623 Pasquerilla East Hall)
		# Get people who entered their dorm address for "postaladdress"
		if (address.split()[-1] == "Hall"):
			try: 
				number = int(address.split()[0])
				dorm = " ".join(address.split()[1:]) # just get the dorm (don't need number)
				student_dir[student]["dorm"] = dorm  # create new key in student info for dorm
				del student_dir[student]["postaladdress"] # delete postaladdress key value pair
			except: # invalid dorm address
				del student_dir[student]
		else:
			try:
				# Get the student's home state (discarding all South Bend and Notre Dame address because could potentially 
				# be off campus address)
				state = info["postaladdress"].split("$")[1].split(",")[1].split()[0]
				city = info["postaladdress"].split("$")[1].split(",")[0]
				if len(state) == 2 and city != "South Bend" and city != "Notre Dame":
					student_dir[student]["homestate"] = state # create new key in student info for state
					del student_dir[student]["postaladdress"] # delete postaladdress key value pair
				else: # Discard South Bend and Notre Dame address
					del student_dir[student]
			except: # invalid home address
				del student_dir[student]

	print "Size of student directory: {}".format(len(student_dir))
