import unittest
 
from app import create_app
from app.util.extensions import db
from app.models.model import User
 
class ProjectTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app = create_app('test')
        self.app = app.test_client()
 
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
 
    ########################
    #### helper methods ####
    ########################
 
 
 
    ###############
    #### tests ####
    ###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Blocktopus Dashboard', response.data)
        self.assertIn(b'New Sketch', response.data)
        self.assertIn(b'Standard Library', response.data)
        response = self.app.get('/home', follow_redirects=True)
        self.assertIn(b'Blocktopus Dashboard', response.data)
        self.assertIn(b'New Sketch', response.data)
        self.assertIn(b'Standard Library', response.data)
        response = self.app.get('/index', follow_redirects=True)
        self.assertIn(b'Blocktopus Dashboard', response.data)
        self.assertIn(b'New Sketch', response.data)
        self.assertIn(b'Standard Library', response.data)
        response = self.app.get('/index.html', follow_redirects=True)
        self.assertIn(b'Blocktopus Dashboard', response.data)
        self.assertIn(b'New Sketch', response.data)
        self.assertIn(b'Standard Library', response.data)

    def test_main_page_english(self):
        self.app.get('/', follow_redirects=True)
        response = self.app.get('/language/en', follow_redirects=True)
        self.assertIn(b'New Sketch', response.data)
        self.assertIn(b'Create...', response.data)
        self.assertIn(b'English', response.data)

    def test_main_page_german(self):
        self.app.get('/', follow_redirects=True)
        response = self.app.get('/language/de', follow_redirects=True)
        self.assertIn(b'Neue Skizze', response.data)
        self.assertIn(b'Erstelle...', response.data)
        self.assertIn(b'Deutsch', response.data)

    def test_main_page_french(self):
        self.app.get('/', follow_redirects=True)
        response = self.app.get('/language/fr', follow_redirects=True)
        self.assertIn(b'Nouvelle esquisse', response.data)
        self.assertIn(b'Cr\xc3\xa9er...', response.data)
        self.assertIn(b'Fran\xc3\xa7ais', response.data)

    def test_404_error(self):
        response = self.app.get('/not-existing-page', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)
        self.assertIn(b'Page Not Found', response.data)

if __name__ == "__main__":
    unittest.main()