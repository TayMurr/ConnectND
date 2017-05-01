#!/usr/bin/env python2.7
# Program to analyze the data inside our database
# Author: Mimi Chen
import json

def print_all_keys(keys):
	'''Print all the keys'''
	print "All keys:" 
	for k in keys: 
		print "- {}".format(k)

def get_values_given_key(desired_key):	
	'''Print and return a set of all the values associated with desired key'''
	values = set()
	for student, info in student_dir.items(): 
		# Student has the desired key
		if desired_key in info.keys():	
			# Values are a list
			if desired_key == "jobs" or desired_key == "college" or desired_key == "workdepartment": 
				for i in info[desired_key]: 
					values.add(i)
			else: 
				values.add(info[desired_key])

	print "All values associated with the key {}".format(desired_key)

	for v in values:
		#print "-{}".format(v)
		print "\"{}\",".format(v),
	print "\n"

	return values


if __name__ == "__main__": 
	with open("ND_complete_directory.json") as f: 
		student_dir = json.load(f)
		#print "Opened student directory: {} students".format(len(student_dir))

	# Get all the keys and print them out
	keys = set()
	for student, info in student_dir.items(): 
		for i in info: 
			keys.add(i)

	print("Welcome to the ND Student Directory!")

	while 1:
		selection = raw_input('''Choose an action: 
1.) Enter a NetID and get information associated with the NetID if it exists
2.) Get all keys for student information
3.) Get all values associated with the given key for student information
4.) Get all students associated with a key value pair of student information
5.) Exit program\n''')
		if selection == "1":
			student = raw_input("Get more details of a student. Enter a netid: ")
			if student not in student_dir.keys():
				print "Student {} is not in the student directory".format(student)
			else:
				print student_dir[student]
		elif selection == "2": 
			print_all_keys(keys)
		elif selection == "3":
			print_all_keys(keys)
			desired_key = raw_input("Enter desired key: ")
			while (desired_key not in keys): 
				desired_key = raw_input("Invalid key. Enter desired key: ")
			values = get_values_given_key(desired_key)
		elif selection == "4":
			print_all_keys(keys)

			desired_key = raw_input("Enter desired key: ")
			while (desired_key not in keys): 
				desired_key = raw_input("Invalid key. Enter desired key: ")

			values = get_values_given_key(desired_key)
			desired_value = raw_input("Enter desired value: ")
			while (desired_value not in values):
				desired_value = raw_input("Invalid value. Enter desired value: ")

			# Find all netids with associated key value pair
			netid = []
			for student, info in student_dir.items():
				if desired_key in info.keys():
					if desired_key == "jobs" or desired_key == "college" or desired_key == "workdepartment": 
						for i in info[desired_key]: 
							if i == desired_value: 
								netid.append(student)
								break
					else: 
						if info[desired_key] == desired_value: 
							netid.append(student)
			for i,n in enumerate(netid):
				print "{} {}".format(i, n)
		elif selection == "5":
			break
		else:
			print "Invalid selection. Enter 1, 2, 3, 4, or 5."

	print "Exiting program . . ."
		
	
	'''
	ndformalname is a string
	uid is a string
	dorm is a string
	mail is string
	ndlevel is a string
	homestate is a string
	ndaffiliation is a string

	jobs is a list
	workdepartment is a list
	college is a list
	'''
