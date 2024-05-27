import unittest
from app import FileServiceApp
from flask import json
import base64
from dotenv import load_dotenv
import os
import io

# Load environment variables from .env file
load_dotenv()

class TestFileServiceApp(unittest.TestCase):
    def setUp(self):
        self.app = FileServiceApp().app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Retrieve authentication credentials from environment variables
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')

    def tearDown(self):
        pass

    def test_upload_file(self):
        # Open and read the file content
        with open('img.jpg', 'rb') as f:
            file_content = f.read()

        # Include file content in the request data
        response = self.client.post('/upload', 
                                    data={'file': (io.BytesIO(file_content), 'img.jpg')},  # Use io.BytesIO
                                    headers={'Authorization': self._basic_auth_header(self.username, self.password)})
        
        # Check if the response is successful (status code 201)
        self.assertEqual(response.status_code, 201)
        
        # Check the response message
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['message'], 'File uploaded successfully')

    def test_list_files(self):
        # Include authentication credentials in the request headers
        response = self.client.get('/files', 
                                   headers={'Authorization': self._basic_auth_header(self.username, self.password)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(json.loads(response.data.decode('utf-8')), list))

    def test_get_file(self):
        # Include authentication credentials in the request headers
        response = self.client.get('/files/c5f7e558180f4c2998c92614e0ed5776.jpg',
                                   headers={'Authorization': self._basic_auth_header(self.username, self.password)})
        self.assertEqual(response.status_code, 200)

    def test_health_check(self):
        response = self.client.get('/health')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'OK')

    def _basic_auth_header(self, username, password):
        """Generate Basic Authentication header."""
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return f"Basic {encoded_credentials}"

if __name__ == '__main__':
    unittest.main()
