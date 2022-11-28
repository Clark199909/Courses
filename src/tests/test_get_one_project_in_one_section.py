import unittest
import requests

# clear the database before doing this test


class TestGetOneProjectInOneSection(unittest.TestCase):

    def test_empty_response(self):
        response = requests.get('http://localhost:5013/api/sections/1/projects/2')
        self.assertEqual(response.text, '"Section/Project does not exist!"\n')
        self.assertEqual(response.status_code, 400)

    def test_response(self):
        # Given

        response = requests.get('http://localhost:5013/api/sections/1/projects/2')

        # Then
        print(response.text)
        self.assertEqual(200, response.status_code)
