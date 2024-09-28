# NAME(S): [Mariia Maksymenko, Caleb Thurston]
#
# APPROACH: [WRITE AN OVERVIEW OF YOUR APPROACH HERE.]
#     Please use multiple lines (< ~80-100 char) for you approach write-up.
#     Keep it readable. In other words, don't write
#     the whole damned thing on one super long line.
#
#     In-code comments DO NOT count as a description of
#     of your approach.
#
# Our code is to try to implement an algorithm thats like a 
# Breadth First Search. Our agent is coded to take in it's percepts
# and at certain intervals (like when there is multiple paths for
# it to go down) decide which path to go down based on if it
# is stored as a location that it has already been too. To 
# implement this, we have a coordinate system for keeping track
# of where the agent is in regards to where it started, aka it's
# origin. We also have a list to store places where it has already been
# as well as a list to store where it has seen cells that are
# unexplored. 

import random

# Comemnt for Caleb: have everything BUT need to add stuff to the environment map func. Need to check the percepts, 
# calculate the position of the cells, update the map with new cells and mark them as unexplored if they are not walls
# queue unexplored cells for future exploration and also do an if check for a wall so you dont add it to the unexplored set

class AI:
    def __init__(self):
        """
        Called once before the sim starts. You may use this function
        to initialize any data or data structures you need.
        """
        self.turn = 0
        self.position = (0, 0)
        # Dictionary represents what the environment looks like, with keys being the coordinates (x, y) 
        # and values representing 'g', 'w', and 'r'
        self.map = {}
        self.visited = set() # Set that tracks all visited cells
        # A first in first out queue for BFS to keep track of the cells the agent has seen but hasn't visited
        self.unexplored = [] 
        self.exit_found = False # Checks if the agent found the exit
    
    def update(self, percepts):
        """
        PERCEPTS:
        Called each turn. Parameter "percepts" is a dictionary containing
        nine entries with the following keys: X, N, NE, E, SE, S, SW, W, NW.
        Each entry's value is a single character giving the contents of the
        map cell in that direction. X gives the contents of the cell the agent
        is in.

        COMAMND:
        This function must return one of the following commands as a string:
        N, E, S, W, U

        N moves the agent north on the map (i.e. up)
        E moves the agent east
        S moves the agent south
        W moves the agent west
        U uses/activates the contents of the cell if it is useable. For
        example, stairs (o, b, y, p) will not move the agent automatically
        to the corresponding hex. The agent must 'U' the cell once in it
        to be transported.

        The same goes for goal hexes (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).
        """
        self.turn += 1 # Increments the turn every move

        # Updates the environment we created based on the current percepts
        self.update_environment(percepts)

        # Checks if the agent is currently on the exit cell
        if percepts['X'][0] == 'r':
            self.exit_found = True  # Marks that the exit has been found
            return 'U'  # Uses the exit if the agent is on the exit cell
        
        # Decides the next move based on unexplored areas or random movement
        next_move = self.next_move()

        # Updates the change in agent's position based on the chosen move
        change_x, change_y = self.get_changeInDirection(next_move)
        current_x, current_y = self.position
        self.position = (current_x + change_x, current_y + change_y)
        
        #shit ton of print statements for debugging
        # print(next_move)
        # print(self.position)
        # print(self.visited)
        # print(self.map)
        # print(self.unexplored)
        # print(next_move)
        # print(next_move)

        
        return next_move  # Returns the 'N', 'S', 'E', or 'W' as a move command
        
        
    def update_environment(self, percepts):

        directions = ['N', 'E', 'S', 'W']
        current_x, current_y = self.position  # Gets the position of the agent

        # Checks if the current cell was visited and stores the type of the cell
        if self.position not in self.visited:                                                                                                           #Changed by cat
            self.visited.add((current_x, current_y))  # Adds the current cell to the visited set if there is a need for that
            self.map[(current_x, current_y)] = percepts['X'][0]  # Stores the cell type

        # Here is supposed to be a for loop (or rather nested loops and an if?) for checking the percepts in each direction and updating the map in general
        # Checks the cells in percepts in each of the four directions
        for i, dir in enumerate(directions):
            # Gets the coordinate change for the direction
            change_x, change_y = self.get_changeInDirection(dir)
            for distance, cell in enumerate(percepts[dir]):
                # Calculates the position of the cell in that direction
                new_x = current_x + (change_x * (distance + 1))
                new_y = current_y + (change_y * (distance + 1))
                
                if (new_x, new_y) not in self.map:
                    # Updates the map of the environment with new cells and marks them as unexplored if they are not walls
                    self.map[(new_x, new_y)] = cell
                    if cell != 'w':  # Ignores walls for the unexplored cells
                        self.unexplored.append((new_x, new_y))  # Queues unexplored cells for the future movement
        
        

    # Helper functions below

    # This functions gets the change (delta) in coordinates for a specific direction
    # It returns a tuple that represents the movement in that direction
    def get_changeInDirection(self, direction):
        # 1 and -1 represent movement up, down, left and right on a coordinate plane
        changes = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
        return changes[direction]


    # This function figures out which direction the agent should move to get from its current position to the
    # target cell by comparing the coordinates. It returns the direction to reach the given cell
    def which_direction(self, next_position):

        current_x, current_y = self.position
        next_x, next_y = next_position
        
        if next_x > current_x:
            return 'E' # The target cell is to the right (next x direction is larger)
        elif next_x < current_x:    
            return 'W' # The target cell is to the left of the agent (the x coordinate is smaller)
        elif next_y < current_y:
            return 'S' # The target cell is below the agent on the y-axis (the y coordinate is smaller)
        elif next_y > current_y:
            return 'N' # The target cell is above the agent (the y coordinate is larger)
        else:
            return random.choice(['N', 'S', 'E', 'W'])  # In case of no valid move

    # Move stuff

    # This function decides the next move based on the unexplored cells. If there are any unexplore cells,
    # it moves towards the closest one. If there are no unexplored cells, chooses random direction to move
    # It returns a move command (Zach's line)
    def next_move(self):

        if self.unexplored:
            next_position = self.unexplored.pop(0) # Gets the next unexplored cell from the queue by popping it
            # Gets information on which direction to move to reach the unexplored cell from a helper function
            move = self.which_direction(next_position)
            return move
        
        # Picks a random direction to move if there are no cells left
        return random.choice(['N', 'S', 'E', 'W'])

