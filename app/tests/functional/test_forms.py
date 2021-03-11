import unittest
import os
import uuid

from app import create_app
from app.views.forms import stringdate, stringdatetime
from app.util.extensions import db
from app.models.model import User, Projects
 
class ProjectTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app = create_app('test')
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

        with app.app_context():
            db.drop_all()
            db.create_all()
 
        # executed after each test
    def tearDown(self):
        pass
 
    ########################
    #### helper methods ####
    ########################
    
    def register(self, email, password, confirm, name, site, building, room):
        return self.app.post(
        '/register',
        data=dict(email=email, password=password, confirm=password, name=name, site=site, building=building, room=room),
        follow_redirects=True
    )
        
    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    ###############
    #### tests ####
    ###############

    def test_create_project(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('account@company.tld', 'SuperStrongPw123', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.assertIn(b'Your account has been registered.', response.data)
        response = self.login('account@company.tld', 'SuperStrongPw123')
        self.assertIn(b'Your Profile', response.data)
        self.assertIn(b'account@company.tld', response.data)
        response = self.app.post('/create-project',
                                   buffered=True,
                                   content_type='multipart/form-data',
                                   data={'guid': str(uuid.uuid4()),
                                         'title': 'New Project Title',
                                         'description': 'New Project Description',
                                         'created_date': stringdate()},
                                   follow_redirects=True)
        self.assertIn(b'New project &#39;New Project Title&#39; has been created.', response.data)
        
if __name__ == '__main__':
    unittest.main()