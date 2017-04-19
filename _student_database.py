import operator

class _student_database(object):

	def __init__init(self): 
		self.directory = {} 

	
	def load_directory(self, directory_file):
		'''Load the directory data from directory_file into database'''
		with open(directory_file) as f: 
			self.directory = json.load(f)
	
	def add_student(self, netid, student_info): 
		'''Written by thibault -- student_info is a dictionary'''
		self.directory[netid] = student_info 

	def get_student(self, netid): 
		'''Return dictionary of student information'''
		if netid not in self.directory.keys(): 
			return None
		return self.directory[netid]

	def get_all(self): 
		return self.directory
