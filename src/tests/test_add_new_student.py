import unittest
import requests


class TestAddStudent(unittest.TestCase):

    def test_successful_add(self):
        # Given
        student_added = {
            "uni": "tk1024",
            "project_id": 2
        }

        # When
        # make sure the call_no has been added to the database
        response = requests.post('http://localhost:5013/api/sections/10001/new_student',
                                 json=student_added)

        # Then
        self.assertEqual(200, response.status_code)
