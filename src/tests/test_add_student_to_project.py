import unittest
import requests


class TestAddStudentToProject(unittest.TestCase):

    def test_successful_add(self):
        # Given
        student_added = {
            "uni": "df989"
        }

        # When
        # make sure the call_no = 10001 has been added to the database
        # make sure the project_id = 1 has been added to the database
        response = requests.post('http://localhost:5013/api/sections/10001/projects/1/new_student"',
                                 json=student_added)

        # Then
        self.assertEqual(200, response.status_code)
