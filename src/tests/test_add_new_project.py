import unittest
import requests


class TestAddProject(unittest.TestCase):

    def test_successful_add(self):
        # Given
        project_added = {
            "project_name":"Donald's Fans",
            "team_name":"Cloud Computing Team 3"
        }

        # When
        # make sure the call_no has been added to the database
        response = requests.post('http://localhost:5013/api/sections/10001/new_project',
                                 json=project_added)

        # Then
        self.assertEqual(200, response.status_code)
