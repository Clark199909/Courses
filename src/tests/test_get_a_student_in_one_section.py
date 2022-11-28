import unittest
import requests

# clear the database before doing this test


class TestGetStudentsInSection(unittest.TestCase):

    def test_empty_response(self):
        response = requests.get('http://localhost:5013/api/sections/<call_no>/students/<uni>')
        self.assertEqual(response.text, '"No record found!"\n')
        self.assertEqual(response.status_code, 400)

    def test_response(self):
        # Given

        response = requests.get('http://localhost:5013/api/sections/<call_no>/students/<uni>')

        # Then
        print(response.text)
        self.assertEqual(200, response.status_code)
