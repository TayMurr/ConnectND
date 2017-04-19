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
		output = {'result': 'success'}
		try: 
			output['all_students'] = self.sd
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		return json.dumps(output)

