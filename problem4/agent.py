'''
 @file agent.py
 @author Kiersten Campbell (kscamp3@emory.edu)
 @version 0.1
 @date 2023-11-05
 
 Agent object to represent individuals in an agent-based model
'''
import random

class Agent:

    # Agent status can be susceptible (S), infected (I), or recovered (R)
    # Agent location is a tuple representing current (x,y) position in community
    # Agent recent_inf status is a boolean to represent if this agent was infected in current timestep
    def __init__(self, status, location):
        self.status = status
        self.location = location
        self.recent_inf = False

    # In a timestep, agents can stay in place (path 0), move up (path 1), move down (path 2)
    # move left (path 3) or move right (path 4). 
    # Agents cannot move outside of the grid boundary. If the randomly selected movement moves the agent outside the grid,
    # the move function is called recursively until a valid path is selected.
    def move(self, boundary):
        path = random.randint(0, 4)
        curr_x, curr_y = self.location

        # Stay in place
        if(path == 0):
            self.location = self.location
        
        # Move up (increment y by 1)
        elif(path == 1):
            if(curr_y < boundary-1):
                self.location = (curr_x, curr_y+1)
            else:
                self.move(boundary)

        # Move down (decrement y by 1)
        elif(path == 2):
            if(curr_y > 0):
                self.location = (curr_x, curr_y-1)
            else:
                self.move(boundary)
        
        # Move right (increment x by 1)
        elif(path == 3):
            if(curr_x < boundary-1):
                self.location = (curr_x + 1, curr_y)
            else:
                self.move(boundary)
        
        else:
            if(curr_x > 0):
                self.location = (curr_x-1, curr_y)
            else:
                self.move(boundary)

        return self.location
        