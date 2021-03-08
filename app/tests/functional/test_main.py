import unittest
 
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

if __name__ == "__main__":
    unittest.main()