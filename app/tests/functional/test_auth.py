import unittest
import os
 
from ... import create_app
from ...util.extensions import db
from ...models.model import User
from ...util.config import TestConfig

 
class ProjectTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app = create_app(TestConfig)
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

        
        self.assertEqual(app.debug, False)
 
        # executed after each test
    def tearDown(self):
        pass

 
    ########################
    #### helper methods ####
    ########################
    
    def register(self, email, password, name, site, building, room):
        return self.app.post(
        'register/',
        data=dict(email=email, password=password, name=name, site=site, building=building, room=room),
        follow_redirects=True
    )
 
    ###############
    #### tests ####
    ###############
 
    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'Remember Me', response.data)
        self.assertIn(b'Need an account?', response.data)
        
    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign up', response.data)
        self.assertIn(b'Register', response.data)


if __name__ == '__main__':
    unittest.main()
    app = create_app(TestConfig)
    app.run()
