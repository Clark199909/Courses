import unittest
import requests

# clear the database before doing this test


class TestGetProjectsInSection(unittest.TestCase):

    def test_empty_response(self):
        response = requests.get('http://localhost:5013/api/sections/<call_no>/projects')
        self.assertEqual(response.text, '[]\n')
        self.assertEqual(response.status_code, 200)

    def test_response(self):
        # Given

        response = requests.get('http://localhost:5013/api/sections/<call_no>/projects')

        # Then
        print(response.text)
        self.assertEqual(200, response.status_code)
