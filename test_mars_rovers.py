#! /usr/bin/python

import unittest
from mars_rovers import *


class MarsRoverTestModule(unittest.TestCase):
    """
    We want to test each core function's ability to:
        1. return a value
        2. raise an error
        3. set an attribute
    """

    def setUp(self):
        """
        Start out with some.......................
        """
        pass

    def test_get_rover_params(self):
        """
        Try getting rover params from sample command line inputs
        1. ValueError
        2. ValueError
        3. ValueError
        4. ValueError
        5. assertEqual rover_params actual vs expected
        """
        pass

    def get_plateau_dims(self, line):
        """
        1. assertRaises ValueError
        2. assertRaises ValueError
        3. assertEqual width, height actual vs expected
        """
        pass

    def test_rotate(self):
        """
        Check results of rover.facing in a few cases
        1. assertEqual
        2. assertEqual
        3. assertEqual
        """
        pass

    def test_advance(self):
        """
        Check results of rover.x, rover.y in a few cases
        1. assertEqual
        2. assertEqual
        3. assertEqual
        Then turn off self_preserve and confirm both errors get thrown:
        4. assertRaises
        5. assertRaises

        """
        pass

    def test_create_rover(self):
        """
        Check that env.rovers is growing in length
        Also confirm that we are getting an instance of a Rover returned
        1. x3 adds...  assertEqual(length, length_of_env_rovers)
        2. assertIsInstance(a, b)
        """
        pass

    def test_create_plateau(self):
        """
        Just assertIsInstance for a plateau with its new args (w, h, rovers)
        """
        pass

    def test_run_rover_moves(self):
        """
        Run some simple calls to run_rover_moves to ensure that both
        rotate and advance actions occur as expected
        """
        pass

    def test_result(self):
        """
        Return a final state from both `good_args1` and `good_args2`
        assertEqual final state actual vs expected
        """
        pass

    def tearDown(self):
        """
        I think this gets exectued after each test case, so be careful
        """
        pass

if __name__ in '__main__':
    unittest.main(verbosity=2, buffer=True)
