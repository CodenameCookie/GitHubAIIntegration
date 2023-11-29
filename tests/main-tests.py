import unittest
from flask import Flask
from flask.testing import FlaskClient
from main import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
     

    def test_get_user_info(self):
        response = self.app.post('/get_user_info', json={'username': 'example_user'})
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data

if __name__ == '__main__':
    unittest.main()
