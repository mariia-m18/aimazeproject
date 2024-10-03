# NAME(S): [Mariia Maksymenko, Caleb Thurston]
# COLLABORATION: We did everything together and we wish to have the same grade
# APPROACH:
# The approach we took after numerous tests of different methods is 
# trying to implement an algorithm like a Depth First Search (with 
# additional features) since it gave us better results more consistenly 
# than Breadth First search or our attempt at A*. First, we used a combination 
# of a set to track visited cells, a dictionary to count how many times each 
# cell has been visited, and a list to keep track of the path for backtracking.
# So, each time the agent receives new percepts, it updates its current state, including
# its position and visit counts and also checks if the exit is reachable and starts
# going in that direction immediately. And if it is not immediately reachable, the 
# agent should move to either unvisited cells or cells that have been visited the 
# least number of times.We utilize the coordinate system by keeping track of the 
# agent's current position with a (x,y) pair, and appending to a dictionary the 
# coordinates of where it just was, as well as the direction it moved to get there.
# We also needed a form of backtracking to previously visited locations, but not too
# much, since it caused wasting turns on already explored "regions". If the agent 
# exhausts its options, it defaults to a random direction, which is not ideal, but it
# needs to exist as an option. We also tried to take measures to avoid running into 
# walls and make it so the agent doesn’t get trapped in loops. Loops are the biggest
# problem to us, however our agent seems to do a good job around 90% of the time. 
# With# how we've programmed it, it'll consistently run really well for a long time, 
# and then all of a sudden it'll try a direction that completely throws off the run, 
# or get into a loop. This version has the most consistency but every now and then it 
# will have a couple really bad runs. 


import random

class AI:
    def __init__(self):
        
        self.visited = set()  # Set to keep track of visited cells
        self.path = []  # Stack for "backtracking"
        self.visit_count = {}  # To track how many times a cell has been visited
        self.turn = 0  # Counter for the number of turns taken
        self.directions = ['N', 'E', 'S', 'W']  # Possible movement directions
        self.delta = {  # Changes in coordinates based on the directions
            'N': (0, 1),  
            'E': (1, 0),   
            'S': (0, -1),   
            'W': (-1, 0)   
        }
        self.current_position = (0, 0)  # Initial position of the agent
        self.exit_position = None  # Stores exit position if detected

    def update(self, percepts):
        """
        This method decides on the next move based on the percepts received and prioritizes moving 
        towards the exit and avoids revisiting the same cells unnecessarily
        """
        self.turn += 1  # Increments the turn count
        
        # Marks the current position as visited and update visit count
        self.visited.add(self.current_position)  # Adds the current position to the visited set
        if self.current_position in self.visit_count:
            self.visit_count[self.current_position] += 1  # Increments visit count if already visited
        else:
            self.visit_count[self.current_position] = 1  # Initializes visit count to 1 for new cell

        # Checks if the current position has the exit
        if percepts['X'] == ['r']:  
            return 'U'  # Exits immediately when standing on the exit

        # Checks if the exit is visible in any of the directions and moves towards it
        for direction in self.directions:
            if percepts[direction][0] == 'r': 
                next_position = self.move_to(self.current_position, direction) 
                self.current_position = next_position
                return direction  # Returns the direction towards the exit

        # Prioritizes moving to unvisited cells or cells visited fewer times
        best_direction = None  # Stores the best direction to move
        lowest_visit_count = float('inf')  # We want to find the direction where the AI has visited 
        # the least so starting with an infinitely high number makes sure that any real number will be lower
        for direction in self.directions:
            if percepts[direction][0] != 'w':  # Checks the direction so its not a wall
                next_position = self.move_to(self.current_position, direction)  # Calculates next position
                # Checks if the cells have been visited fewer than twice
                if next_position not in self.visited or self.visit_count.get(next_position, 0) < 2:
                    # Checks if this cell has been visited fewer times than the current best
                    if self.visit_count.get(next_position, 0) < lowest_visit_count:
                        lowest_visit_count = self.visit_count.get(next_position, 0)  # Updates lowest count
                        best_direction = direction

        if best_direction:
            # Moves to the least visited or unvisited cell
            self.path.append(self.current_position)  # Adds current position to path for backtracking
            self.current_position = self.move_to(self.current_position, best_direction)  # Updates position
            return best_direction

        # If no better options, backtrack to a previous position
        if self.path:
            backtrack_position = self.path[-1]  # Peek the last element
            self.current_position = self.path.pop()  # Pops the last position from the path
            return self.which_direction(backtrack_position)  # Determines direction to the backtracked position

        # If everything fails, goes this direction because picking random directions led to bad paths and other problems
        # and North and West directions proved to be consistently better choices
        return 'N'

    def move_to(self, position, direction):
        """
        THis method returns the next position as a tuple given a current position 
        and a direction.
        """
        dx, dy = self.delta[direction]  # Gets the movement change (delta) for the direction
        return (position[0] + dx, position[1] + dy)  # Calculates and returns the new position

    def which_direction(self, next_position):
        """
        This method returns the direction to move from the current position to the 
        next position.
        """
        dx = next_position[0] - self.current_position[0]  # Calculates the change in x
        dy = next_position[1] - self.current_position[1]  # Calculates the change in y
        for direction, (dx_, dy_) in self.delta.items():
            if (dx_, dy_) == (dx, dy):  # Checks if the calculated direction matches, _ to differentiate
                return direction  # Returns the matching direction
        return random.choice(['N', 'E', 'S', 'W'])  # Defaults to a random direction if not found

