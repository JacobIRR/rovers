#! /usr/bin/python

import unittest
from mars_rovers import *


class MarsRoverTestModule(unittest.TestCase):
    """
    We want to test each core function's ability to either:
        1. return a value
        2. raise an error
        3. set an attribute
    """

    def setUp(self):
        """
        Start out with some.......................
        """
        self.env = PlateauEnvironment()

    def test_get_rover_params(self):
        """
        Try getting rover params from sample command line inputs
        """
        args1 = ['1 2 N', 'LMLM', '1 4 E']  # odd number of args
        args2 = ['0 2 WW', 'RMLRMRLM']  # bad position string
        args3 = ['1 2 N', 'LMK']  # bad moves string
        args4 = ['1 2 E', 'RM', '1 2 W', 'LMML']  # rovers on top of each other
        args5 = ['101 101 E', 'R']  # rover outside plateau
        args6 = ['1 2 N', 'RM', '1 5 W', 'LM']  # good args

        self.env.create_plateau(100, 100)

        expected6 = [(1, 2, 'N', ['R', 'M'], 0), (1, 5, 'W', ['L', 'M'], 0)]

        self.assertRaises(ValueError, self.env.get_rover_params, args1, 0)
        self.assertRaises(ValueError, self.env.get_rover_params, args2, 0)
        self.assertRaises(ValueError, self.env.get_rover_params, args3, 0)
        self.assertRaises(ValueError, self.env.get_rover_params, args4, 0)
        self.assertRaises(ValueError, self.env.get_rover_params, args5, 0)
        self.assertEqual(self.env.get_rover_params(args6, 0), expected6)

    def test_get_plateau_dims(self):
        """
        Make sure we reject bad dimensions for plateau
        """
        args1 = '$123(@#YGHI'
        args2 = ' 5  5 '

        expected2 = (5, 5)

        self.assertRaises(ValueError, self.env.get_plateau_dims, args1)
        self.assertEqual(self.env.get_plateau_dims(args2), expected2)

    def test_rotate(self):
        """
        Check results of rover.facing in a few cases
        """
        roverN = Rover(1, 1, 'N', [], self_preserve=False)
        roverS = Rover(1, 1, 'S', [], self_preserve=False)
        roverE = Rover(1, 1, 'E', [], self_preserve=False)
        roverW = Rover(1, 1, 'W', [], self_preserve=False)

        self.assertEqual(roverN.rotate('L'), 'W')
        self.assertEqual(roverS.rotate('L'), 'E')
        self.assertEqual(roverE.rotate('R'), 'S')
        self.assertEqual(roverW.rotate('R'), 'N')

    def test_advance(self):
        """
        Check results of rover.x, rover.y in a few cases
        Then turn off self_preserve and confirm both errors get thrown
        """
        # Move one space north
        self_preserving_rover = Rover(1, 1, 'N', [], self_preserve=True)
        self.assertEqual(self_preserving_rover.advance([], 10, 10), (1, 2))
        # Now rotate East and move
        self_preserving_rover.rotate('R')
        self.assertEqual(self_preserving_rover.advance([], 10, 10), (2, 2))

        # Move/Fall off the edge
        suicidal_rover = Rover(1, 1, 'N', [], self_preserve=False)
        self.assertRaises(OutOfBoundsError, suicidal_rover.advance, [], 1, 1)
        # Crash into another rover
        suicidal_rover2 = Rover(1, 1, 'N', [], self_preserve=False)
        self.assertRaises(CollisionError, suicidal_rover2.advance, [(1, 2)], 5, 5)

    def test_create_rover(self):
        """
        Check that env.rovers is growing in length
        Also confirm that we are getting an instance of a Rover returned
        """
        # No rovers yet
        self.assertEqual(len(self.env.rovers), 0)

        # Add one and confim its type
        rover = self.env.create_rover(1, 2, 'N', ['L', 'M'], self_preserve=False)
        self.assertIsInstance(rover, Rover)

        # Add some more and check length of rover list
        self.env.create_rover(1, 3, 'N', ['R', 'M'], self_preserve=True)
        self.env.create_rover(1, 4, 'E', ['M', 'M'], self_preserve=False)
        self.assertEqual(len(self.env.rovers), 3)

    def test_create_plateau(self):
        """
        Just assertIsInstance for a plateau with its new args (w, h, rovers)
        """
        plateau = self.env.create_plateau(10000, 10000)
        self.assertIsInstance(plateau, PlateauEnvironment)

    def test_run_rover_moves_and_result(self):
        """
        Run some simple calls to run_rover_moves to ensure that both
        rotate and advance actions occur as expected
        """
        rovers = [self.env.create_rover(2, 2, 'W', ['M'], self_preserve=True),
                  self.env.create_rover(1, 2, 'S', ['R', 'M'], self_preserve=True),
                  self.env.create_rover(3, 3, 'N', ['M', 'R', 'M'], self_preserve=True)]
        self.env.create_plateau(10, 10)

        # First rover "almost collides", second rover "almost falls out of bounds"
        D = dict()
        for ndx, rover in enumerate(rovers):
            D[ndx] = self.env.run_rover_moves(rover)

        self.assertEqual(D[0], '2 2 W')  # still in place after near collision
        self.assertEqual(D[1], '0 2 W')  # still in place, but facing West after near out of bounds issue
        self.assertEqual(D[2], '4 4 E')  # moved one space up and one space right

    def tearDown(self):
        """
        This gets exectued after each test case to provide a fresh instance in setUp
        """
        del self.env

if __name__ in '__main__':
    unittest.main(verbosity=2, buffer=True)
