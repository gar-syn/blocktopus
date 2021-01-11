from twisted.application.service import ServiceMaker

octopus_editor = ServiceMaker(
<<<<<<< HEAD
    name = 'octopus-editor', 
	module = 'octopus.blocktopus.server.tap', 
	description = 'Run the octopus editor service.', 
	tapname = 'octopus-editor'
=======
    name='octopus-editor',
    module='octopus.blocktopus.server.tap',
    description='Run the octopus editor service.',
    tapname='octopus-editor'
>>>>>>> bad-master
)
