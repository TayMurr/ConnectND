#!/usr/bin/env python 2.7
import json 

def merge_two_dicts(x, y):
	z = x.copy()
	z.update(y)
	return z

def update(student):
	complete_user_keys = [ "ndlevel", "ndtoplevelprimarydepartment", "ndcurriculum", "uid", "ndformalname", "mail"]
	with open ("ND_raw_directory.json") as f: 
		old_list = json.load(f)	
	new_dic = {}
	temp_student = {}
	if student in old_list:
		 
		try: 
			# Check if the student 's keys are available 
			#if set(complete_user_keys).issubset(set(student.keys())):
			for complete_key in complete_user_keys:
				temp_student[complete_key] = student[complete_key]
					
				homestate = raw_input("Enter your homestate : " )
        			temp_student['homestate'] = homestate
        			dorm = raw_input("Enter your Dorm :  ")
        			temp_student['dorm'] = dorm
        			new_dic[student["uid"]] = temp_student  			  		
		except: 
			print "Update not possible "
			pass

	else: 
		print "{} does not exit".format(student)

	with open("ND_complete_directory.json") as f: 
		student_dir = json.load(f)

	updated_dir = merge_two_dicts(student_dir, new_dic )
	output = open ("ND_complete_directory.json", 'w')
	output.write(json.dumps( updated_dir ))
	output.close()


if __name__ == "__main__":
	with open("ND_complete_directory.json") as f: 
		student_dir = json.load(f)
	# Get keys : help to check if student is already in our database	
	keys = set()
	for student, info in student_dir.items():
		for i in info:
			keys.add(i)
	
	student  = raw_input (" input NetID : ")
	if student not in student_dir.keys():
		print "student {} not into student directory  ".format(student) 
		update(student)
	


