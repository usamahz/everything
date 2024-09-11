import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from everything.config import Config

class TestConfig(unittest.TestCase):

    def test_simulation_times(self):
        self.assertEqual(Config.SIMULATION_START_TIME.hour, 7)
        self.assertEqual(Config.SIMULATION_END_TIME.hour, 22)

if __name__ == "__main__":
    unittest.main()
