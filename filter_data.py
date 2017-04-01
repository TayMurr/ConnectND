#!/usr/bin/env python2.7
import json

# Keys that a student must have to be defined as a complete user
complete_user_keys = ["ndlevel", "postaladdress", "ndtoplevelprimarydepartment", "ndcurriculum", "uid", "ndformalname", "mail"] 
# Keys that are desired and added to our student directory
optional_keys = ["ndadditionaltitleinfo", "ndaffiliation", "title", "nddepartment", "ndtitle", "departmentnumber" ] 

if __name__ == "__main__":
	# In "ND_directory.json", each student is stored as an element in the list (a list of dictionaries)
	with open("ND_directory.json") as f: 
		print "Opening raw ND directory. . . "
		student_dir_list = json.load(f)

	print "Done opening raw ND directory!"

	# Use a dictionary to hold the student data
	student_dir = {}

	# Loop through the student directory list 
	for student in student_dir_list: 
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
	print "\nFinished processing raw student directory - {} in filtered directory\n".format(len(student_dir))

	# Write the dictionary as a JSON object to the file "ND_filtered_directory.json"
	output = open("ND_filtered_directory.json", 'w')
	output.write(json.dumps(student_dir))
	output.close()
	print "Finished writing filtered directory to file \"ND_filtered_directory.json\""
