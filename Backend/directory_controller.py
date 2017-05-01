# Controller for handling GET and PUT 
# Author: Mimi Chen

import json
import cherrypy

class DirectoryController(object): 
	def __init__(self, sd = None): 
		self.sd = sd

	def GET_NETID(self, netid):
		'''Retrieve student information given netid'''
		output = {'result': 'success'}
		try: 
			info = self.sd.get_student(netid)
			if (info == None): 
				output['result'] = 'error'
				output['message'] = netid + ' does not exist in database'
			else: 
				for key, value in info.items(): 
					output[key] = value
		except Exception as ex: 
			output['result'] = 'error'
			output['message'] = str(ex)
		return json.dumps(output)

	def GET_ALL(self):
		'''Retrieve everything in directory'''
		output = {'result':'success'}
		try: 
			output['data'] = self.sd.get_all()
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		return json.dumps(output)

	def PUT_NETID(self, netid):
		'''Given a student's NetID and his or her information, add to the database'''
		output = {'result': 'success'}
		thebody = cherrypy.request.body.read().decode()
		try: 
		# Put everything in the body into the student_info dictionary
			student_info = json.loads(thebody)
			self.sd.add_student(netid, student_info)
			self.sd.update_file()
		except Exception as ex:
			output['result'] = 'Error'
			output['message'] = str(ex)
		return json.dumps(output)


