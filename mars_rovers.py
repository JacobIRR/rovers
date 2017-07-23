#! /usr/bin/python

import sys

"""

DESCRIPTION:
A squad of robotic rovers are to be landed by NASA on a plateau on Mars. This plateau,
which is curiously rectangular, must be navigated by the rovers so that their on-board
cameras can get a complete view of the surrounding terrain to send back to Earth.

A rover's position and location is represented by a combination of x and y co-ordinates
and a letter representing one of the four cardinal compass points. The plateau is
divided up into a grid to simplify navigation. An example position might be 0, 0, N,
which means the rover is in the bottom left corner and facing North.

In order to control a rover, NASA sends a simple string of letters. The possible letters
are 'L', 'R' and 'M'. 'L' and 'R' makes the rover spin 90 degrees left or right
respectively, without moving from its current spot. 'M' means move forward one grid
point, and maintain the same heading.

Assume that the square directly North from (x, y) is (x, y+1).

The first line of input is the upper-right coordinates of the plateau, the lower-left
coordinates are assumed to be 0,0. The rest of the input is information pertaining to
the rovers that have been deployed. Each rover has two lines of input. The first line
gives the rover's position, and the second line is a series of instructions telling the
rover how to explore the plateau.

The position is made up of two integers and a letter separated by spaces, corresponding
to the x and y coordinates and the rover's orientation.

Each rover will be finished sequentially, which means that the second rover won't start
to move until the first one has finished moving.

The output for each rover should be its final coordinates and heading.

Input:
5 5  # plateau
1 2 N  # position of rover 1
LMLMLMLMM  # movements of rover 1
3 3 E  # position of rover 2
MMRMMRMRRM  # movements of rover 2

Output:
1 3 N  # orientation of rover 1
5 1 E  # orientation of rover 2

TO DO:
0. If this gets finished as a python app, consider doing it in Java
1. Define classes and methods
    -class Plateau
        attrs: width, length, rover_positions, etc
        methods: any? update_rover_positions?
    -class Rover
        attrs: x_position, y_position, facing, moves, self_preserve?
        methods: move, turn, stop?
    -class Visualizer
        attrs: plateau, rovers_present
        methods: draw_current_state
    -class CollisionError
    -class OutOfBoundsError
    -corner cases:
        running into another rover
        running off the edge
            (allow param "is this rover smart enough not to destroy itself")

2. Set up arg parsing from file in main()
    - get plateau dimensions
    - how many rovers are there?
    - are they self_preserve (won't run off the edge or into each other)
    - enter position of rover X (repeat as needed)
    - enter movements for rover X (repeat as needed)
    - {{if plateau dimensions are small enough}}: would you like to see a visualization of the rover movements?
2.5 - Watch Raymond Hettinger video about classes properties and static methods
3. Write unit tests to catch all possible cases
4. Setup proper import/folder structure
5. Make a README.md file with instructions for both unit tests and manual tests


"""


class CollisionError(Exception):
    "Raise this when a non-self_preserve rover collides with another"
    pass


class OutOfBoundsError(Exception):
    "Raise this when a non-self_preserve rover runs off the edge"
    pass


class Plateau(object):
    """
    An X, Y grid to keep track of its present rovers
    """
    def __init__(self, width, height, rovers):
        self.width = width
        self.height = height
        self.rovers = rovers  # responsible for keeping track of no-go-zones


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

    def __str__(self):
        return ' '.join([str(self.x), str(self.y), self.facing])

    def __repr__(self):
        return ' '.join([str(self.x), str(self.y), self.facing])


class Environment(object):
    """
    This class acts as a factory to create the plateau and rovers,
    Provides an optional visualization client,
    And handles returning the result of the rover motions back to the caller

    Before initializing the Plateau and Rovers, confirm that args match the spec
    """
    def __init__(self, visualization=False):
        self.visualization = visualization
        self.rovers = []
        self.plateau = None

    def get_rover_params(self, rover_args, self_preserve):
        """
        Parse and validate command line input for rover paramters
        """
        rover_params = []
        for ndx, i in enumerate(rover_args):
            if ndx % 2 == 0:
                try:
                    # odd rows (even index) has rover position and facing
                    x, y, facing = list(i.replace(' ', ''))
                    x = int(x)
                    y = int(y)
                    assert facing.upper() in ('N', 'E', 'W', 'S')
                except:
                    raise ValueError('Cannot construct rover from : %r' % i)
                try:
                    # skip ahead to the next line to get the moves for this rover
                    moves = list(rover_args[ndx+1].replace(' ', '').upper())
                    print 'moves is : %s' % moves
                    assert set(moves).issubset(set(['L', 'R', 'M']))
                except:
                    raise ValueError('This moves string is not valid : %r' % rover_args[ndx+1])
                # and save this tuple to the list of attrs
                rover_params.append((x, y, facing, moves, self_preserve))
            else:
                # skip even row (odd index)
                continue
        return rover_params

    def get_plateau_dims(self, line):
        """
        Verify that we can construct the plateau from command line input
        """
        try:
            dims = [int(i) for i in filter(None, line.strip().split(' '))]
            print "dims is : %s " % dims
            if len(dims) == 2:
                width, height = dims
                assert (width + height) > 2
                return width, height
            else:
                raise ValueError('''Bad input for plateau dimensions: %r.
                                    Use two positive integers''' % line)
        except:
                raise ValueError('''Bad input for plateau dimensions: %r.
                                    Use two positive integers''' % line)

    # Factory should Check the inits here and raise ValueError/TypeError if needed
    # assertRaises in unittest
    # be sure to create all rovers first, then add those rovers to the plateau
    def create_rover(self, x, y, facing, moves, self_preserve=False):
        """
        Build and return a new Rover
        Caller must try/except and raise ValueError during failure
        """
        try:
            arg_type_map = {
                int(x): int,
                int(y): int,
                bool(self_preserve): bool,
            }
        except ValueError:
            print "Rover arguments were not valid"
            raise
        for k, v in arg_type_map.items():
            if not isinstance(k, v):
                print '%s was not a %s' % (k, v)
                raise TypeError
        # Now check facing position and movement commands
        if facing.upper() not in ('N', 'E', 'W', 'S'):
            # Needs custom message
            raise ValueError
        ########## USE A SET HERE!!!!
        if not set(moves).issubset(set(['L', 'R', 'M'])):
            # Needs custom message
            print
            print "Rover moves were not valid. Must use 'L', 'R', 'M' only."
            print "You used: %s" % ''.join(moves)
            print
            raise ValueError
        rover = Rover(x, y, facing, moves, self_preserve=self_preserve)
        self.rovers.append(rover)
        # return for use with unit tests
        return rover

    def create_plateau(self, width, height, rovers):
        """
        Build and return a new Plateau
        Caller must try/except and raise ValueError during failure
        """
        for rover in rovers:
            if not isinstance(rover, Rover):
                # Needs custom message
                raise TypeError
        self.plateau = Plateau(width, height, rovers)
        # return for use with unit tests
        return self.plateau

    def visualize(self):
        """
        Dispatch off to Visualizer using the Environment
        """
        v = Visualizer(self)
        # v.run_sequence()

    def run_moves(self, rover):
        """
        Digest the moves of a given rover
        Reposition the rover in its final spaces
        Raise errors if rover.self_preserve is not set
        Skip "Illegal" moves if rover.self_preserve is set
        """
        print "running moves for rover..."
        print rover
        return rover.__str__()

    def result(self):
        """
        Run all rover moves
        Return a new line for each rover's x/y/facing attributes
        """
        final_state = '\n'.join([self.run_moves(r) for r in self.rovers])
        return final_state


class Visualizer(object):
    """
    Create a visual representation of moves for each rover on a plateau
    """
    def __init__(self, environment):
        self.environment = environment

# ##############################################################################
# SETUP FUNCTIONS / COMMAND LINE CLIENT
# ##############################################################################


def main():
    """
    Main function for running direct tests from command line
    """
    sys.tracebacklimit = 99
    try:
        return fast_input()
        # may ditch this fast / vs granular setup...
        # fast = get_bool_answer("Would you like to use fast setup? (Y/N):  ")
        # if fast:
        #     return fast_input()
        # else:
        #     return granular_input()
    except KeyboardInterrupt:
        sys.exit()


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


def fast_input():
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

            (Hit ENTER twice to submit entry)
            """
    lines = []
    while True:
        line = raw_input(">")
        if line:
            lines.append(line)
        else:
            break

    # start up the factory/environment
    env = Environment()

    # Get plateau dimensions from the first line
    width, height = env.get_plateau_dims(lines[0])

    # Get args for rovers from the remaining lines
    rover_params = env.get_rover_params(lines[1:], self_preserve)

    # After validation steps, create the plateau and rovers
    for rover in rover_params:
        env.create_rover(*rover)
    env.create_plateau(width, height, env.rovers)

    # Process all the moves and return the final state
    return env.result()


def granular_input():
    """
    Slower, more granular method of creating the environment
    """
    print "Let's set up the Plateau and Rovers..."
    print
    width = int(raw_input("How wide is the Plateau?:  "))
    height = int(raw_input("How long is the Plateau?:  "))
    viz = False  # no Visualizer by default
    if (width * height) < 360:
        viz = get_bool_answer("Would you like to see a visualization of the rover movements? ")
    num_rovers = raw_input("How many rovers are there?:  ")
    print "Are they self_preserve?"
    self_preserve = get_bool_answer("(i.e. Will they run into each other or off the edge?):  ")
    count = 1
    rover_attrs = []
    for rover in range(0, num_rovers):
        x = raw_input("What is the X coordinate or Rover #%d ?  ") % count
        y = raw_input("What is the Y coordinate or Rover #%d ?  ") % count
        facing = raw_input("Which way is it facing? (N, S, E, W):  ")
        moves = raw_input("Enter a string of movements (M) and L/R turns:  ")
        moves = moves.replace(' ', '').upper()
        rover_attrs.append((x, y, facing, moves, self_preserve))
        count += 1
    env = Environment(viz)
    env.rovers = []
    for rover in rover_attrs:
        env.create_rover(*rover)
    env.create_plateau(width, height, env.rovers)
    return env.result()


if __name__ == '__main__':
    # Collect args with raw inputs
    main()
