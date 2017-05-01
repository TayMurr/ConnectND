#!/usr/bin/env python2.7
import json

# Keys that a student must have to be defined as a complete user
complete_user_keys = ["ndlevel", "postaladdress", "ndtoplevelprimarydepartment", "ndcurriculum", "uid", "ndformalname", "mail"] 
# Keys that are desired and added to our student directory
optional_keys = ["ndadditionaltitleinfo", "ndaffiliation", "title", "nddepartment", "ndtitle", "departmentnumber" ] 

def primary_filter(raw_directory):
	'''Given a dictionary containing the raw student directory, return a 
	dictionary of students that meet our definition of a complete user'''
	student_dir = {}
	# Loop through the student directory list 
	for student in raw_directory: 
		try: 
			# Check if the student is a complete user (has the complete user keys)
			if set(complete_user_keys).issubset(set(student.keys())):
				cur_student = {}
				# Get all key value pairs of fields that define a complete user
				for complete_key in complete_user_keys:
					cur_student[complete_key] = student[complete_key]
				# If the key value pair of an optional field exists, get it
				for optional_key in optional_keys: 
					if optional_key in student.keys():
						cur_student[optional_key] = student[optional_key]
				# Add filtered down student to student directory
				student_dir[student["uid"]] = cur_student
				print "{} - {} was added".format(len(student_dir), student["uid"])
			else:
				print "Skipped - {}".format(student["uid"])
		except: 
			print "Error accessing {}".format(student)
			pass
	print "\nFinished primary filtering of raw student directory! Size: {}".format(len(student_dir))
	return student_dir

def secondary_filter(directory):
	'''Given a dictionary containing only complete users, parse the address to 
	get the home state or dorm, combine jobs, combine work departments, and 
	combine college and curriculum'''

	# Loop through the key value pair in dictionary "student_dir" to get dorm or homestate
	for student, info in directory.items():

		address = info["postaladdress"].split("$")[0] # gets the hall address (ie. 623 Pasquerilla East Hall)

		# Get people who entered their dorm address for "postaladdress"
		if (address.split()[-1] == "Hall"):
			try: 
				number = int(address.split()[0])
				dorm = " ".join(address.split()[1:]) # just get the dorm (don't need number)
				directory[student]["dorm"] = dorm  # create new key in student info for dorm
				del directory[student]["postaladdress"] # delete postaladdress key value pair

			except: # invalid dorm address
				del directory[student]
				continue

		# Get the student's home state (discarding all South Bend and Notre Dame address because could potentially 
		# be off campus address)
		else:
			try:
				state = info["postaladdress"].split("$")[1].split(",")[1].split()[0]
				city = info["postaladdress"].split("$")[1].split(",")[0]

				if len(state) == 2 and city != "South Bend" and city != "Notre Dame":
					directory[student]["homestate"] = state # create new key in student info for state
					del directory[student]["postaladdress"] # delete postaladdress key value pair

				else: # Discard South Bend and Notre Dame address
					del directory[student]
					continue
			except: # invalid home address
				del directory[student]
				continue

		# Combine college and curriculum
		college = set()

		if "ndtoplevelprimarydepartment" in info.keys():
			college.add(info["ndtoplevelprimarydepartment"])
			del directory[student]["ndtoplevelprimarydepartment"]
		if "ndcurriculum" in info.keys():
			college.add(info["ndcurriculum"])
			del directory[student]["ndcurriculum"]

		directory[student]["college"] = list(college)

		# Combine work departments
		work_department = set() # set to hold unique student work departments
		if "nddepartment" in info.keys():
			depart = info["nddepartment"]
			work_department.add(depart)
			del directory[student]["nddepartment"]
		if "departmentnumber" in info.keys():
			depart = info["departmentnumber"]
			work_department.add(depart)
			del directory[student]["departmentnumber"]

		directory[student]["workdepartment"] = list(work_department)
		
		# Combine student jobs
		jobs = set() # set to hold unique student jobs 
		if "ndtitle" in info.keys():
			jobs.add( info["ndtitle"] )
			del directory[student]["ndtitle"] 
		if "title" in info.keys():
			jobs.add( info["title"])
			del directory[student]["title"]
		if "ndadditionaltitleinfo" in info.keys():
			jobs.add( info["ndadditionaltitleinfo"])
			del directory[student]["ndadditionaltitleinfo"]

		directory[student]["jobs"] = list(jobs) # Create new key "jobs" with value of a set of jobs
	print "Finished secondary filter on student directory! Size: {}".format(len(directory))
	return directory

if __name__ == "__main__":
	# In "ND_raw_directory.json", each student is stored as an element in the list (a list of dictionaries)
	with open("ND_raw_directory.json") as f: 
		print "Opening raw ND directory. . . "
		raw = json.load(f)

	print "Done opening raw ND directory! Size: {}".format(len(raw))

	# Get directory with only the complete users 
	almost_complete_directory = primary_filter(raw)

	# Get directory where users' addresses are processed and certain fields are joined 
	final_directory = secondary_filter(almost_complete_directory)

	# Write the dictionary as a JSON object to the file "ND_complete_directory.json"
	output = open("ND_complete_directory.json", 'w')
	output.write(json.dumps(final_directory))
	output.close()
	print "Finished writing final directory to file \"ND_complete_directory.json\""
