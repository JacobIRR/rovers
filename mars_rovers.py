#! /usr/bin/python

import sys


class CollisionError(Exception):
    "Raise this when a non-self_preserve rover collides with another"
    pass


class OutOfBoundsError(Exception):
    "Raise this when a non-self_preserve rover runs off the edge"
    pass


class CrossedOwnPathException(Exception):
    "Raise when we cross our own path"
    pass


class Rover(object):
    """
    One of potentially many rovers on the plateau that can move and turn
    """
    def __init__(self, x, y, facing, moves, self_preserve=False):
        self.x = x
        self.y = y
        self.facing = facing
        self.moves = moves
        self.self_preserve = self_preserve
        # Rotation / movement lookup tools
        self.clockwise = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
        self.counter_clockwise = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
        self.movement_map = {'N': [0, 1], 'E': [1, 0], 'W': [-1, 0], 'S': [0, -1]}
        self.past_moves = set()

    def __str__(self):
        """
        Match the expected output of the specification, e.g. "1 1 N"
        """
        return ' '.join([str(self.x), str(self.y), self.facing])

    def rotate(self, direction):
        """
        Take an incoming Left / Right direction and based on that direction,
            assign `facing` attribute based on lookup of corresponding clockwise
            or counter_clockwise hashtable. In this hashtable, the key is
            the current direction and the value returned is the resulting direction.
        """
        if direction == 'L':
            self.facing = self.counter_clockwise[self.facing]
        if direction == 'R':
            self.facing = self.clockwise[self.facing]
        # return for use with unit tests
        return self.facing

    def advance(self, no_go_zones, width, height):
        """
        Based on current position and facing, move forward one point on the plateau.
        The `movement_map` defines which directions result in which X, Y change.
        Depending on self_preserve status, we may raise and exception when
          running off the edge or colliding with another rover.
        """
        x_change, y_change = self.movement_map[self.facing]
        test_position = (self.x + x_change, self.y + y_change)
        # Test for collisions
        if test_position in no_go_zones:
            if self.self_preserve:
                print "A rover almost bumped into another rover! Skipping this move..."
                return None
            else:
                raise CollisionError("A rover ran into another rover! MISSION FAILED")
        # Test for out of bounds error
        elif any([test_position[0] > width, test_position[0] < 0,
                  test_position[1] > height, test_position[1] < 0]):
            if self.self_preserve:
                print "A rover almost rolled off the plateau! Skipping this move..."
                return None
            else:
                raise OutOfBoundsError("A rover drove off the edge of the plateau! MISSION FAILED")

        # Throw exception if we cross our own path
        if test_position in self.past_moves:
            raise CrossedOwnPathException

        # Advance forward if both tests passed
        else:
            self.x, self.y = test_position
            self.past_moves.add(test_position)
        # return for use with unit tests
        return self.x, self.y


class PlateauEnvironment(object):
    """
    This class acts as a factory to create the plateau and rovers,
        and handles returning the result of the rover motions back to the caller
    Before initializing the Plateau and Rovers, confirm that args match the spec
    """
    def __init__(self):
        # Empty init until args are validated
        self.rovers = []
        self.width = None
        self.height = None

    def get_rover_params(self, rover_args, self_preserve):
        """
        Parse and validate command line input for rover paramters
        The X and Y coordinates of the rover are 0-indexed.
        """
        # First, make sure we have a cooresponding moves line for every x,y,facing line
        try:
            assert rover_args and len(rover_args) % 2 == 0
        except AssertionError:
            lines = '\n'.join(rover_args)
            raise ValueError("Not enough lines to create rovers: \n %s " % lines)
        # Now loop over args and validate each param
        rover_params = []
        claimed_ground = set()
        for ndx, i in enumerate(rover_args):
            if ndx % 2 == 0:
                try:
                    # odd rows (even index) has rover position and facing
                    x, y, facing = list(i.replace(' ', ''))
                    x = int(x)
                    y = int(y)
                    claimed_ground.add((x, y))
                    assert facing.upper() in ('N', 'E', 'W', 'S')
                    assert x >= 0
                    assert y >= 0
                    assert x <= self.width
                    assert y <= self.height
                except:
                    msg = 'Cannot construct rover from : %r \n'
                    msg += 'Use two positive integers between 0 and plateau size '
                    msg += 'and a Direction (N, S, E, W).'
                    raise ValueError(msg % i)
                try:
                    # skip ahead to the next line to get the moves for this rover
                    moves = list(rover_args[ndx+1].replace(' ', '').upper())
                    assert set(moves).issubset(set(['L', 'R', 'M']))
                except:
                    raise ValueError('This moves string is not valid : %r' % rover_args[ndx+1])
                # and save this tuple to the list of attrs
                rover_params.append((x, y, facing, moves, self_preserve))
            else:
                # skip even row (odd index)
                continue
        # One last check to make sure that no rovers ended up on top of others:
        if len(claimed_ground) < len(rover_params):
            raise ValueError("Rovers were placed on top of each other!")
        return rover_params

    def get_plateau_dims(self, line):
        """
        Verify that we can construct the plateau from command line input
        The width and height of the plateau must be at least 1 X 1
        """
        try:
            dims = [int(i) for i in filter(None, line.strip().split(' '))]
            if len(dims) == 2:
                width, height = dims
                assert (width + height) > 1
                return width, height
            else:
                raise Exception
        except:
            msg = "Bad input for plateau dimensions: %r."
            msg += "Use two positive integers"
            raise ValueError(msg % line)

    def create_rover(self, x, y, facing, moves, self_preserve=False):
        """
        Build and return a new Rover
        Add this rover to self.rovers
        """
        rover = Rover(x, y, facing, moves, self_preserve=self_preserve)
        self.rovers.append(rover)
        # return for use with unit tests
        return rover

    def create_plateau(self, width, height):
        """
        Here we assign the attributes for this plateau, having validated them
          as well as the rover parameters.
        """
        self.width, self.height = width, height
        # return for use with unit tests
        return self

    def run_rover_moves(self, rover):
        """
        Digest the moves of a given rover
        Reposition the rover in its final space
        Raise errors if rover.self_preserve is not set
        Skip "Illegal" moves if rover.self_preserve is set
        """

        # Because this method is called once for each rover, `no_go_zones`
        #  reflects an accurate snapshot of current rover positions
        no_go_zones = [(r.x, r.y) for r in self.rovers
                       if (r.x, r.y) != (rover.x, rover.y)]

        # Execute each move
        for step in rover.moves:
            if step == 'M':
                rover.advance(no_go_zones, self.width, self.height)
            else:
                # step is either L or R here
                rover.rotate(step)

        return rover.__str__()

    def result(self, w, h):
        """
        Run all rover moves
        Return a new line for each rover's x/y/facing attributes
        """
        
        final_state = '\n'.join([self.run_rover_moves(r) for r in self.rovers])
        return final_state


# ##############################################################################
# SETUP FUNCTIONS / COMMAND LINE CLIENT
# ##############################################################################


def main():
    """
    Main function for running direct tests from command line.
    Ctrl + C exits
    """
    # Don't expose code in tracebacks, just show the last line of the Exception
    sys.tracebacklimit = 0

    # Dispatch to setup prompts and break out with Control-C without error
    try:
        return set_up_environment()
    except KeyboardInterrupt:
        print
        sys.exit("Exiting...")


def get_bool_answer(question):
    """
    Ask a Yes/No Question and coerce to a bool value
    """
    bool_map = {'Y': True,
                'YES': True,
                'N': False,
                'NO': False}
    var = raw_input(question)
    while var.upper() not in bool_map.keys():
        var = raw_input("Please type `Y` or `N`:  ")
    return bool_map[var.upper()]


def set_up_environment():
    """
    Quickly dump in all args to create the environment
    """
    print
    print "Rovers are in danger of running into each other, or off the edge of the plateau..."
    self_preserve = get_bool_answer("Will these rovers be \"self-preserving?\" ")
    print
    print "Now, let's set up the Plateau and Rovers."
    print "Please enter the plateau size, and rover positions/movements, for example:"
    print """
            5 5  # plateau
            1 2 N  # position of rover 1
            LMLMLMLMM  # movements of rover 1
            3 3 E  # position of rover 2
            MMRMMRMRRM  # movements of rover 2

            (Hit ENTER twice when finished)
            """
    # Collect input lines for as many rovers as the user would like to create
    lines = []
    while True:
        line = raw_input(">")
        if line:
            lines.append(line)
        else:
            break

    # start up the factory/environment
    plateau = PlateauEnvironment()

    # Get plateau dimensions from the first line and create plateau
    width, height = plateau.get_plateau_dims(lines[0])
    plateau.create_plateau(width, height)

    # Get args for rovers from the remaining lines and create rovers
    rover_params = plateau.get_rover_params(lines[1:], self_preserve)
    for rover in rover_params:
        plateau.create_rover(*rover)

    # Process all the moves and return the final state
    result = plateau.result(width, height)
    print result

    # In case this gets consumed by an external service/test
    return result


if __name__ == '__main__':
    main()
