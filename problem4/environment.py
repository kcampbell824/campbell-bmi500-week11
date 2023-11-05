'''
 @file environment.py
 @author Kiersten Campbell (kscamp3@emory.edu)
 @version 0.1
 @date 2023-11-05
 
 Environment object to represent a community in an agent-based model. 
 An environment is grid containing multiple agents. 
 In a simulation, the environment is updated iteratively to reflect interactions between agents
'''
import random
from agent import Agent
from collections import Counter

class Environment:

    # Environment in a size x size grid
    # p represents infection rate (likelihood an S agent is infected when sharing a cell with an I agent)
    # q represents recover rate (likelihood an I agent recovers)
    def __init__(self, size, p, q):
        self.size = size
        self.grid = {}
        self.p = p
        self.q = q

    # Environment is a size x size grid
    # Populate the grid with agents at random positions
    # grid is a dictionary with (x,y) location keys and lists of agents as values
    # n_sus = starting number of susceptible agents
    # n_inf = starting number of infected agents
    # n_recov = starting number of recovered agents
    def populate_all(self, n_sus, n_inf, n_recov):
        self.grid = {(i, j) : [] for i in range(0, self.size) for j in range(0, self.size)}

        self.populate_generic(n_sus, "S")
        self.populate_generic(n_inf, "I")
        self.populate_generic(n_recov, "R")

    # Given n agents with a given status, populate the environment grid with these n agents at random (x,y) positions
    def populate_generic(self, n, status):
        max_coord = self.size

        for i in range(0, n):
            x = random.randint(0, max_coord-1)
            y = random.randint(0, max_coord-1)
            self.grid[(x,y)].append(Agent(status, (x,y)))

    # Run a simulation w/ provided number of timesteps
    # Wrapper that executes a single simulation step multiple times iteratively
    # Returns a dictionary with keys representing timestep number and values are dictionaries with agent counts in each status
    def run_simulation(self, timesteps):
        results = {0:self.population_status()}
        for i in range(1, timesteps):
            results[i] = self.one_step()
        return results

    # In a single timestep:
    # 1. Move agents randomly
    # 2. Check transmissions across cells
    # 3. Check recoveries across cells
    # 4. Calculate number of agents in each status at end of timestep 
    # Returns a dictionary with agent counts in each status
    def one_step(self):
        self.move_agents()
        self.check_transmissions(self.p)
        self.check_recoveries(self.q)
        return self.population_status()
    
    # Randomly moves all agents in the grid
    def move_agents(self):
        next_grid = {(i, j) : [] for i in range(0, self.size) for j in range(0, self.size)}
        for i in range(0, self.size):
            for j in range(0, self.size):
                for agent in self.grid[(i, j)]:
                    new_pos = agent.move(self.size)
                    next_grid[new_pos].append(agent)
        self.grid = next_grid

    # In each cell of the grid, if a cell contains an I agent, all S agents have probability p of being infected
    # If an S individual is infected, recent_inf is set to True
    # Recently infected agents cannot recover in the same timestep (tracked via recent_inf)
    def check_transmissions(self, p):
        for i in range(0, self.size):
            for j in range(0, self.size):

                # Get current number of S, I, R in this cell
                cell_composition = self.cell_status((i,j))

                # If there is an infected person in this cell, need to simulate infection transmission
                if cell_composition['I'] > 0:
                    susceptible = [agent for agent in self.grid[(i,j)] if agent.status == 'S']
                    for agent in susceptible:
                        if(random.random() < p):
                            agent.status = "I"
                            agent.recent_inf = True

    # In each cell of the grid, all I agents have probability q of recovering
    # Recently infected agents cannot recover in the same timestep (tracked via recent_inf)
    def check_recoveries(self, q):
        for i in range(0, self.size):
            for j in range(0, self.size):
                    infected = [agent for agent in self.grid[(i,j)] if agent.status == 'I']
                    for agent in infected:

                        # Agents not infected in current timestep are eligible to recover
                        if agent.recent_inf != True:
                            if(random.random() < q):
                                agent.status = "R"
                        # Recently infected agents cannot recover in this timestep
                        # Set recent_inf to false so they may recover in the next timestep
                        else:
                            agent.recent_inf = False

    # Count number of agents in each status in a given cell
    def cell_status(self, location):
        cell_counts = Counter()

        for agent in self.grid[location]:
            cell_counts[agent.status] += 1
        return cell_counts
    
    # Iterate over all cells in grid to count number of agents in each status across entire environment
    def population_status(self):
        pop_counts = Counter()
        for i in range(0, self.size):
            for j in range(0, self.size):
                pop_counts = pop_counts + self.cell_status((i, j))
        return pop_counts
