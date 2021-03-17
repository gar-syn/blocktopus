import unittest
import os
 
from app import create_app
from app.util.extensions import db
from app.models.model import User

class TestFlaskAppConfigProduction(unittest.TestCase):
     
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app = create_app('prod')
        self.app = app.test_client()
 
    # executed after each test
    def tearDown(self):
        pass   
    
    ###############
    #### tests ####
    ###############
    
    def test_app_is_production(self):
        self.assertTrue(self.app.application.config['ENV'] == 'prod')
        self.assertTrue(self.app.application.config['DEBUG'] is False)
        self.assertTrue(self.app.application.config['DB_NAME'] == 'blocktopus.sqlite')

class TestFlaskAppConfigDevelopment(unittest.TestCase):
     
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app = create_app('dev')
        self.app = app.test_client()
 
    # executed after each test
    def tearDown(self):
        pass   
    
    ###############
    #### tests ####
    ###############
    
    def test_app_is_production(self):
        self.assertTrue(self.app.application.config['ENV'] == 'dev')
        self.assertTrue(self.app.application.config['DEBUG'] is True)
        self.assertTrue(self.app.application.config['TESTING'] is False)
        self.assertTrue(self.app.application.config['DB_NAME'] == 'db.sqlite')

class TestFlaskAppConfigTesting(unittest.TestCase):
     
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app = create_app('test')
        self.app = app.test_client()
 
    # executed after each test
    def tearDown(self):
        pass   
    
    ###############
    #### tests ####
    ###############
    
    def test_app_is_production(self):
        self.assertTrue(self.app.application.config['ENV'] == 'test')
        self.assertTrue(self.app.application.config['TESTING'] is True)
        self.assertTrue(self.app.application.config['DEBUG'] is False)
        self.assertTrue(self.app.application.config['DB_NAME'] == 'testing.sqlite')

if __name__ == '__main__':
    unittest.main()
