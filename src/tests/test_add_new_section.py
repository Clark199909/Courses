import unittest
import requests


class TestAddSection(unittest.TestCase):

    def test_successful_add(self):
        # Given
        section_added = {
            "year": "2022",
            "semester": "Fall",
            "day": "MW",
            "start_hr": "9",
            "start_min": "10",
            "end_hr": "10",
            "end_min": "25",
            "professor": "Donald Ferguson",
            "classroom": "ABC123",
            "section_type": "CVN"
        }

        # When
        response = requests.post('http://localhost:5013/api/sections/new_section',
                                 json=section_added)

        # Then
        self.assertEqual(200, response.status_code)
