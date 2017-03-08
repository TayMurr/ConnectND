import json

if __name__ == "__main__":
	
	with open("ND_directory.json") as f:
		student_dir_list = json.load(f)
	
	# print type(student_dir_list)
	# student_dir_list is ia list

	student_dir = {}
	# Iterate through the list
	for student in student_dir_list:
		student_dir[student["uid"]] = student
		break

	print student_dir

	
