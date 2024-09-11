import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from user_data.user_data import UserData

class TestUserData(unittest.TestCase):

    def setUp(self):
        self.user_data = UserData(name="Dan")

    def test_load_profile(self):
        profile = self.user_data.load_profile()
        self.assertIn("name", profile)
        self.assertEqual(profile["name"], "Dan")

    def test_load_location_data(self):
        locations = self.user_data.load_location_data()
        self.assertIsInstance(locations, list)

    def test_load_calendar(self):
        events = self.user_data.load_calendar()
        self.assertIsInstance(events, list)

if __name__ == "__main__":
    unittest.main()
