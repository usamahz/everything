import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from device_data.device_data import DeviceData
from user_data.user_data import UserData
from datetime import datetime

class TestDeviceData(unittest.TestCase):

    def setUp(self):
        self.user = UserData(name="Dan")
        self.device_data = DeviceData(user=self.user)

    def test_generate_events(self):
        current_time = datetime.now()
        events = self.device_data.generate_events(current_time)
        self.assertIsInstance(events, list)

if __name__ == "__main__":
    unittest.main()
