import os
import argparse

#Local Files
import Agent
import Heuristics
from DecisionTree import *

def main():

    """
     TODO: Known problems and possible solutions:
     
     Right now there are two main problems:
      1) The sudoku environment is incredibly large, and makes things super slow.  
      2) Monte Carlo is not guaranteed to deliver a solved puzzle.
         It is good at reaching a state that only has 1 or 2 blank boxes left, but that puzzle is unsolvable

    Possible Solutions:
      1) Find a way to opitmize the code and limit the number of loops we have to do over a given state.  Also consider limiting the random simulation (just 1 row, just 1 column ?)
      2) Heuristics (the focus of the project, duh).  Or allow the puzzle to "undo" numbers to try and find a solution (this introduces new problems though).  Or increase iterations (makes it take longer though).  Consider giving it the power to reset rows (minus the given values), if there are no valid values for that row?

      Another thing to consider is potentially limiting the random simulations.  Right now, if given puzzle with 2+ blank rows, the simulations are fairly useless.  
      
    """

    # The puzzle we want to solve
    # Simpler puzzles go faster
    # Change this to change the puzzle we solve
    solution = [ # Currently not used
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]

    puzzle = [ # Currently not used
        [5, 3, 4, 6, 7, 8, 9, 0, 0],
        [6, 7, 2, 1, 9, 5, 3, 0, 0],
        [1, 9, 8, 3, 4, 2, 5, 0, 0],
        [8, 5, 9, 7, 6, 1, 4, 0, 0],
        [4, 2, 6, 8, 5, 3, 7, 0, 0],
        [7, 1, 3, 9, 2, 4, 8, 0, 0],
        [9, 6, 1, 5, 3, 7, 2, 0, 0],
        [2, 8, 7, 4, 1, 9, 6, 0, 0],
        [3, 4, 5, 2, 8, 6, 1, 0, 0]
    ]

    puzzle1 = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    
    initial_state= Node(puzzle1,None,None)

    # Make the agent and give it the puzzle
    agent= Agent.Agent(initial_state, Heuristics.prioritizeColumnCompletion)

    # solve the puzzle
    solution= agent.solvePuzzle()
    print("\n\nSolved Puzzle:")
    print(solution)

    return

if __name__ == "__main__":
    main()