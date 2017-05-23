# Start cherrypy service for student directory database
# Author: Mimi Chen

import cherrypy

from _student_database import _student_database
from directory_controller import DirectoryController

def start_service(): 
	'''Start web service'''
	# Create and load database from files
	sd = _student_database()
	#sd.load_directory("ND_complete_directory.json")
	sd.load_directory("ND_database.json")


	# Create controllers
	directoryController = DirectoryController(sd)

	# Create a dispatcher 
	dispatcher = cherrypy.dispatch.RoutesDispatcher()

	# Connect resources to controllers
	dispatcher.connect('get_all', '/students/', controller=directoryController, 
			action = 'GET_ALL', conditions=dict(method=['GET']))
	dispatcher.connect('get_one', '/students/:netid', controller=directoryController,
			action = 'GET_NETID', conditions=dict(method=['GET']))
	dispatcher.connect('set_one', '/students/:netid', controller=directoryController, action = 'PUT_NETID', conditions=dict(method=['PUT']))

	# Settings for cherrypy and start server and event loop
	conf = { 'global' : {
		'server.socket_host': '127.0.0.1',
		'server.socket_port'  : 40440, 
		},
		'/' : { 'request.dispatch': dispatcher } 
		}

	cherrypy.config.update(conf)
	app = cherrypy.tree.mount(None, config = conf)
	cherrypy.quickstart(app)

if __name__ == '__main__':
	start_service()
