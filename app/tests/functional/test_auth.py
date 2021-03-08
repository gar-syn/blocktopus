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
    
    def register(self, email, password, name, site, building, room):
        return self.app.post(
        '/register',
        data=dict(email=email, password=password, name=name, site=site, building=building, room=room),
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

    ############### Registration Process ###############
    def test_user_registration_page(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign up', response.data)
        self.assertIn(b'Register', response.data)
        
    def test_valid_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been registered.', response.data)
        self.assertIn(b'Please log in:', response.data)
        
    def test_missing_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', '')
        self.assertIn(b'This field is required.', response.data)
        
    def test_invalid_user_registration_duplicate_email(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.assertIn(b'Your account has been registered.', response.data)
        self.app.get('/register', follow_redirects=True)
        response = self.register('account@company.tld', 'SuperStrongPw123', 'anotherName', 'Another Site', 'Another Building', 'Room')
        self.assertIn(b'Email address (account@company.tld) is already registered!', response.data)

    ############### Login Process ###############
    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'Remember Me', response.data)
        self.assertIn(b'Need an account?', response.data)

    def test_valid_user_login(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.assertIn(b'Your account has been registered.', response.data)
        response = self.login('account@company.tld', 'SuperStrongPw123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Profile', response.data)
        self.assertIn(b'account@company.tld', response.data)
        self.assertIn(b'myName', response.data)
        self.assertIn(b'Change your Email', response.data)
        
    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('unregistered_email@company.tld', 'NotExistingPassword123')
        self.assertIn(b'Invalid username or password.', response.data)
        self.assertIn(b'Please check your login credentials.', response.data)

    ############### Logout Process ###############
    def test_valid_logout(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.assertIn(b'Your account has been registered.', response.data)
        response = self.login('account@company.tld', 'SuperStrongPw123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Profile', response.data)
        self.assertIn(b'account@company.tld', response.data)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Blocktopus Dashboard', response.data)
        self.assertIn(b'New Sketch', response.data)
        
    def test_invalid_logout_within_being_logged_in(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)

    ############### User Profile Process (changing items) ###############
    def test_change_email_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.login('account@company.tld', 'SuperStrongPw123')
        response = self.app.get('/change-email', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Change your Email', response.data)
        self.assertIn(b'Your current Email is: account@company.tld', response.data)

    def test_change_email(self):
        self.app.get('/register', follow_redirects=True)
        self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.login('account@company.tld', 'SuperStrongPw123')
        response = self.app.post('/change-email', data=dict(email='new-account@company.tld'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your email has been changed', response.data)
        self.assertIn(b'new-account@company.tld', response.data)

    def test_change_password_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.login('account@company.tld', 'SuperStrongPw123')
        response = self.app.get('/change-password', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Change your Password', response.data)

    def test_change_password(self):
        self.app.get('/register', follow_redirects=True)
        self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.login('account@company.tld', 'SuperStrongPw123')
        response = self.app.post('/change-password', data=dict(password='NewSuperStrongPw321'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your password has been changed', response.data)

    def test_change_current_site_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.login('account@company.tld', 'SuperStrongPw123')
        response = self.app.get('/change-site', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Change your Site', response.data)
        self.assertIn(b'Your current Site is: Site', response.data)

    def test_change_current_site(self):
        self.app.get('/register', follow_redirects=True)
        self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.login('account@company.tld', 'SuperStrongPw123')
        response = self.app.post('/change-site', data=dict(site='New Site'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your site has been changed', response.data)
        self.assertIn(b'New Site', response.data)

    def test_change_current_building_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.login('account@company.tld', 'SuperStrongPw123')
        response = self.app.get('/change-building', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Change your Building', response.data)
        self.assertIn(b'Your current Building is: Building', response.data)

    def test_change_current_building(self):
        self.app.get('/register', follow_redirects=True)
        self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.login('account@company.tld', 'SuperStrongPw123')
        response = self.app.post('/change-building', data=dict(building='New Building'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your building has been changed', response.data)
        self.assertIn(b'New Building', response.data)

    def test_change_current_room_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.login('account@company.tld', 'SuperStrongPw123')
        response = self.app.get('/change-room', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Change your Room', response.data)
        self.assertIn(b'Your current Room is: Room', response.data)

    def test_change_current_room(self):
        self.app.get('/register', follow_redirects=True)
        self.register('account@company.tld', 'SuperStrongPw123', 'myName', 'Site', 'Building', 'Room')
        self.login('account@company.tld', 'SuperStrongPw123')
        response = self.app.post('/change-room', data=dict(room='New Room'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your room has been changed', response.data)
        self.assertIn(b'New Room', response.data)
        
if __name__ == '__main__':
    unittest.main()