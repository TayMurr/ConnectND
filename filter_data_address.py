#!/usr/bin/env python2.7
import json
import operator

# Filter the "ND_filtered_directory.json" by "postaladdress" by determining if address is the dorm address
# of the home address

# Deleted field "postaladdress" and created "dorm" and "homestate"

if __name__ == "__main__":
	# Get the filetered student directory
	student_dir = {}
	with open("ND_filtered_directory.json") as f:
		student_dir = json.load(f)
	
	print "Size of student directory: {}".format(len(student_dir))

	all_dorms = {} 			# key: dorm, value: number of students
	all_homestates = {} 	# key: state, value: number of students

	all_years = {} 		
	all_colleges = {} 	
	all_curriculum = {}

	all_department = {}

	all_jobs = {}

	# Loop through the key value pair in dictionary "student_dir" to get dorm or homestate
	for student, info in student_dir.items():

		address = info["postaladdress"].split("$")[0] # gets the hall address (ie. 623 Pasquerilla East Hall)

		# Get people who entered their dorm address for "postaladdress"
		if (address.split()[-1] == "Hall"):
			try: 
				number = int(address.split()[0])
				dorm = " ".join(address.split()[1:]) # just get the dorm (don't need number)
				student_dir[student]["dorm"] = dorm  # create new key in student info for dorm
				del student_dir[student]["postaladdress"] # delete postaladdress key value pair

				all_dorms[dorm] = all_dorms.get(dorm, 0) + 1 # increment dictionary value for dorm

			except: # invalid dorm address
				del student_dir[student]
				continue

		# Get the student's home state (discarding all South Bend and Notre Dame address because could potentially 
		# be off campus address)
		else:
			try:
				state = info["postaladdress"].split("$")[1].split(",")[1].split()[0]
				city = info["postaladdress"].split("$")[1].split(",")[0]

				if len(state) == 2 and city != "South Bend" and city != "Notre Dame":
					student_dir[student]["homestate"] = state # create new key in student info for state
					del student_dir[student]["postaladdress"] # delete postaladdress key value pair

					all_homestates[state] = all_homestates.get(state, 0) + 1 # increment dict value for homestate

				else: # Discard South Bend and Notre Dame address
					del student_dir[student]
					continue
			except: # invalid home address
				del student_dir[student]
				continue

		# Get counts for year, college, curriculum, work department
		year = info["ndlevel"]
		all_years[year] = all_years.get(year, 0) + 1

		# Combine college and curriculum
		college = set()

		if "ndtoplevelprimarydepartment" in info.keys():
			college.add(info["ndtoplevelprimarydepartment"])
			del student_dir[student]["ndtoplevelprimarydepartment"]
		if "ndcurriculum" in info.keys():
			college.add(info["ndcurriculum"])
			del student_dir[student]["ndcurriculum"]

		student_dir[student]["college"] = college

		for c in college:
			all_colleges[c] = all_colleges.get(c, 0 ) + 1

		# Combine work departments
		work_department = set() # set to hold student work departments
		if "nddepartment" in info.keys():
			depart = info["nddepartment"]
			work_department.add(depart)
			del student_dir[student]["nddepartment"]
		if "departmentnumber" in info.keys():
			depart = info["departmentnumber"]
			work_department.add(depart)
			del student_dir[student]["departmentnumber"]

		student_dir[student]["workdepartment"] = work_department
		
		for w in work_department:
			all_department[w] = all_department.get(w, 0) + 1

		# Combine student jobs
		jobs = set() # set to hold student jobs 
		if "ndtitle" in info.keys():
			jobs.add( info["ndtitle"] )
			del student_dir[student]["ndtitle"] 
		if "title" in info.keys():
			jobs.add( info["title"])
			del student_dir[student]["title"]
		if "ndadditionaltitleinfo" in info.keys():
			jobs.add( info["ndadditionaltitleinfo"])
			del student_dir[student]["ndadditionaltitleinfo"]

		student_dir[student]["jobs"] = jobs # Create new key "jobs" with value of a set of jobs

		# Add count to dictionary all_jobs
		for job in jobs:
			all_jobs[job] = all_jobs.get(job, 0) + 1

	print "Size of student directory: {}".format(len(student_dir))


	# Print dorms and homestates
	print "Dorms:"
	for key, value in sorted(all_dorms.items(),key=operator.itemgetter(1)):
		print key, value

	print "\nStates:"
	for key, value in sorted(all_homestates.items(), key=operator.itemgetter(1)):
		print key, value

	print "\nYears:"
	for key, value in sorted(all_years.items(), key=operator.itemgetter(1)):
		print key, value
	
	print "\nCollege:"
	for key, value in sorted(all_colleges.items(), key=operator.itemgetter(1)):
		print key, value

	print "\nCurriculum:"
	for key, value in sorted(all_curriculum.items(), key=operator.itemgetter(1)):
		print key, value
	
	print "\nWork department:"
	for key, value in sorted(all_department.items(), key=operator.itemgetter(1)):
		print key, value

	print "\nJob title:"
	for key, value in sorted(all_jobs.items(), key=operator.itemgetter(1)):
		print key, value
