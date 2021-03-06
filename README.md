## TO RUN:
`$ python mars_rovers.py`  
Then follow the prompts

## TO TEST:
`$ python test_mars_rovers.py`

## NOTES:
1. This project is written in python 2.7 since I work in this language daily.
2. The specification did not explain what should be done when rovers collide or run off  
    the edges, so I decided to handle both cases with an optional flag `self_preserve`  
    You will see this in the command line prompt for running the code.
    When collisions or out of bounds exceptions occur, these are considered fatal.
3. My tests exercise all methods of my code with the exception of the `result` method,  
    which simply loops over groups of moves and returns a joined list of strings.


_Let me know if you have any questions_
**- Jacob Franklin - jackobefranklin@gmail.com**


#### ORIGINAL DESCRIPTION (for reference):
> A squad of robotic rovers are to be landed by NASA on a plateau on Mars. This plateau,  
> which is curiously rectangular, must be navigated by the rovers so that their on-board  
> cameras can get a complete view of the surrounding terrain to send back to Earth.  
>   
> A rover's position and location is represented by a combination of x and y co-ordinates  
> and a letter representing one of the four cardinal compass points. The plateau is  
> divided up into a grid to simplify navigation. An example position might be 0, 0, N,  
> which means the rover is in the bottom left corner and facing North.  
>   
> In order to control a rover, NASA sends a simple string of letters. The possible letters  
> are 'L', 'R' and 'M'. 'L' and 'R' makes the rover spin 90 degrees left or right  
> respectively, without moving from its current spot. 'M' means move forward one grid  
> point, and maintain the same heading.  
>   
> Assume that the square directly North from (x, y) is (x, y+1).  
>   
> The first line of input is the upper-right coordinates of the plateau, the lower-left  
> coordinates are assumed to be 0,0. The rest of the input is information pertaining to  
> the rovers that have been deployed. Each rover has two lines of input. The first line  
> gives the rover's position, and the second line is a series of instructions telling the  
> rover how to explore the plateau.  
>   
> The position is made up of two integers and a letter separated by spaces, corresponding  
> to the x and y coordinates and the rover's orientation.  
>   
> Each rover will be finished sequentially, which means that the second rover won't start  
> to move until the first one has finished moving.  
>   
> The output for each rover should be its final coordinates and heading.  
>   
> Input:  
> 5 5  # plateau  
> 1 2 N  # position of rover 1  
> LMLMLMLMM  # movements of rover 1  
> 3 3 E  # position of rover 2  
> MMRMMRMRRM  # movements of rover 2  
>   
> Output:  
> 1 3 N  # orientation of rover 1  
> 5 1 E  # orientation of rover 2  
