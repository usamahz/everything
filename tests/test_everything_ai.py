import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from everything.everything import EVERYTHING
from user_data.user_data import UserData
from device_data.device_data import DeviceData
from everything.config import Config

class TestEverythingAI(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.user = UserData(name="Dan")
        self.devices = DeviceData(user=self.user)
        self.config = Config()
        self.everything = EVERYTHING(user=self.user, devices=self.devices, config=self.config)

    async def test_simulate_day(self):
        result = await self.everything.simulate_day()
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()