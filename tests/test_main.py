import unittest
from flask import Flask
from flask.testing import FlaskClient
from main import app  # Import your Flask app instance from main.py

class FlaskTest(unittest.TestCase):

    # Set up method
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test for the root endpoint
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # Test for /validate endpoint
    def test_validate(self):
        # Test with correct password
        response = self.app.get('/validate?password=12345')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

        # Test with incorrect password
        response = self.app.get('/validate?password=wrongpassword')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid password', response.data)

    # Test for /list_repos endpoint
    def test_list_repos(self):
        # Test without authorization
        response = self.app.get('/list_repos?password=wrongpassword')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Unauthorized', response.data)

        # Test with authorization
        response = self.app.get('/list_repos?password=12345')
        self.assertEqual(response.status_code, 200)
        # Assuming the response is a list of repos
        self.assertIsInstance(response.json, list)

    # Test for /repo_contents endpoint
    def test_repo_contents(self):
        # Replace 'sample_repo' with a valid repo name for testing
        valid_repo_name = 'GitHubAIIntegration'

        # Test without authorization
        response = self.app.get(f'/repo_contents?password=wrongpassword&repo={valid_repo_name}')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Unauthorized', response.data)

        # Test with authorization but invalid repo name
        response = self.app.get('/repo_contents?password=12345&repo=invalid_repo')
        self.assertNotEqual(response.status_code, 200)

        # Test with authorization and valid repo name
        response = self.app.get(f'/repo_contents?password=12345&repo={valid_repo_name}')
        self.assertEqual(response.status_code, 200)
        # Add further checks based on expected response structure

    # Test for /get_user_info endpoint
    def test_get_user_info(self):
        # Replace 'sample_user' with a valid GitHub username for testing
        valid_username = 'Wrong user made up'

        # Test with valid username
        response = self.app.post('/get_user_info', data={'username': valid_username})
        self.assertEqual(response.status_code, 200)  # Expecting success here
     
        # Test with invalid username (should fail)
        #response = self.app.post('/get_user_info', data={'username': 'invalid_user'})
        #self.assertNotEqual(response.status_code, 200)  # Expecting failure here



if __name__ == "__main__":
    unittest.main()
