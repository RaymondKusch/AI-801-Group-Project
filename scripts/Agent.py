from DecisionTree import *
import math
import random
import copy

VALID_NUMBERS= [1,2,3,4,5,6,7,8,9]


"""
This is the guy that will solve the sudoku puzzle.
When declaring it, give it a puzzle and run solvePuzzle.

WORK IN PROGRESS
"""
class Agent:
    """  
    Constructor
    Takes in a Node (puzzle) and a function (heuristic)
    """
    def __init__(self, puzzle, heuristic):
        self.currentState= puzzle
        self.initialStae= puzzle
        self.heuristic= heuristic
        self.solution= None

    """
    The main MCTS loop
    Loops so long as the puzzle is solvable
    Returns the solved puzzle (if found)
    """
    def solvePuzzle(self):
        # A puzzle can still be solved if there are no violations and there are still empty boxes to be filled
        solvable= not self.puzzleIsFilled(self.currentState.state) and self.stateIsValid(self.currentState.state)

        # So long as there is hope of solving the puzzle, keep trying
        # TODO: Add iteration limit
        while solvable:
            # This is the main MCTS loop
            # It runs N search attempts to build up the knowledge base
            # After exiting, the best action is applied
            for iteration in range(100): 
                # Step 1: Selection
                best_action= self.determineNextAction(self.currentState)
                if not best_action:
                    print("Best action invalid!")
                    print(self.currentState)
                    return None
                    
                # Step 2: Expansion
                follow_up_action= self.determineStateChildren(best_action)
                if not follow_up_action:
                    print("Follow up action invalid!")
                    print(self.currentState)
                    return None
                
                # Step 3: Simulation
                simulation_found_solution, simulation_puzzle= self.runPartialSimulation(follow_up_action)#self.runFullSimulation(follow_up_action)
                if simulation_found_solution:
                    print("Solution randomly found")
                    print(simulation_puzzle)
                    self.solution= simulation_puzzle

                # Step 4: Backpropagation
                self.updateSearchTree(follow_up_action, simulation_found_solution)

            # The previous 100 loops have built up information about the search nodes (actions)
            # Use that informaiton to make an informed decision about what to do next
            action_to_take= self.determineNextAction(self.currentState)
            if action_to_take == self.currentState:
                print(f"No valid move to make.")
                print(self.currentState)
                break

            # Do the action (write a number in a box)
            self.currentState= action_to_take

            print("Game board updated:")
            print(self.currentState)

            # Check if the puzzle is still solvable
            solvable= not self.puzzleIsFilled(self.currentState.state) and self.stateIsValid(self.currentState.state)
        
        # Return the search results
        # May or may not be a solved puzzle
        return self.currentState

    """
    Go through all the search nodes and update how many times we've searched each one
    This is the backpropagation function
    """
    def updateSearchTree(self, state, simulation_solved):
        # Loop through every node we have seen
        node_to_update= state
        while node_to_update is not None:
            # Update the Node, then move on to its' parent
            node_to_update.timesSeen += 1
            if simulation_solved:
                node_to_update.timesSeenAndWon += 1
            node_to_update= node_to_update.parent

    """
    Peform the random simulation on the given puzzle
    Return a bool, True if the simulation found the solution
    False if the simulation did not find the solution
    """
    def runFullSimulation(self, puzzle):
        # Copy the puzzle so we don't make changes to the original while simulating
        simulated_puzzle= copy.deepcopy(puzzle)
        solvable= self.stateIsValid(simulated_puzzle.state) and not self.puzzleIsFilled(simulated_puzzle.state)
    
        # So long as there is hope of solving the puzzle, keep simulating
        while solvable:
            # Get the possible actions
            possible_actions= self.getPossibleActions(simulated_puzzle.state)
            if possible_actions == []:
                break

            # Randomly simulate an action
            randomly_chosen_action= random.choice(possible_actions)
            row= randomly_chosen_action.row
            col= randomly_chosen_action.column
            number= randomly_chosen_action.value

            # Apply the random action
            simulated_puzzle.state[row][col]= number

            # Check if the puzzle is solved
            if self.puzzleIsSolved(simulated_puzzle):
                return True, simulated_puzzle #Puzzle solved!

            # Puzzle is not solved, see if it is still solvable
            solvable= self.stateIsValid(simulated_puzzle.state) and not self.puzzleIsFilled(simulated_puzzle.state)
        
        # Puzzle not solved
        return False, None
    

    #WIP NOT FUNCTIONING YET
    def runPartialSimulation(self, puzzle):
        simulated_puzzle= copy.deepcopy(puzzle)
        
        action= simulated_puzzle.action
        if action is None:
            return False, simulated_puzzle
        row= action.row
        column= action.column

        valid_numbers= set(range(1,10)) # 1 - 9
        numbers_in_row= set(simulated_puzzle.state[row])
        available_numbers= valid_numbers - numbers_in_row
        available_numbers= list(available_numbers)

        for box in range(len(simulated_puzzle.state[row])):
            if simulated_puzzle.state[row][box] != 0 or available_numbers == []:
                continue # This box already has a value in it

            # Box is empty and needs to be filled
            number= random.choice(available_numbers)
            available_numbers.remove(number)
            simulated_puzzle.state[row][box]= number


        state_valid= self.stateIsValid(simulated_puzzle.state)

        return state_valid, simulated_puzzle
            

    
    """
    Figure out what action is the best action to take
    This is the selection step
    Returns a Node with information about the action/new state
    """
    def determineNextAction(self, state) -> Node:
        # If the node has no children, just use the node
        if state.children == []:
            return state
        
        # Loop through every child node and compare their scores
        best_action= state
        best_action_score= -math.inf
        for child_node in state.children:
            # Check the action for validity
            valid= self.stateIsValid(child_node.state)
            filled= self.puzzleIsFilled(child_node.state)
            if valid and filled:
                return child_node #valid and filled means it is solved!
            if not valid:
                continue #don't consider nodes that break rules

            # Score the action
            # TODO: We may want to change this formula, it is recommended for most monte carlo environments, but doesn't make much sense in sudoku
            score= 0
            if child_node.timesSeen != 0:
                score= ((child_node.timesSeenAndWon)/child_node.timesSeen) + math.sqrt(2) * - math.sqrt(math.log(state.timesSeen)/child_node.timesSeen) # Upper Confidence Bound Formula

            # Apply heuristic to score
            if self.heuristic is not None:
                score += self.heuristic(child_node.state)

            # If this action is better than the previous action, choose this action instead
            if score > best_action_score:
                best_action= child_node
                best_action_score= score
            elif score == best_action_score:
                if best_action.timesSeen > child_node.timesSeen and best_action.timesSeenAndWon <= 0:
                    best_action= child_node

        # Return the Node with the best score
        return best_action

    """
    Populate a Node's children
    This is the expansion state
    Return a random child of the given Node
    """
    def determineStateChildren(self, state):
        if state.children != []:# node already expanded, just pick something
            return state#random.choice(state.children)
        
        """ 
        TODO: There is an unnecessary loop here.  If we build the nodes when we get the actions, we can avoid having to loop over get possible actions again.

            Also don't use deepcopy, that's slow.  Find a faster way of copying the state.
        """
        # Get every possible action that can be done from the given state
        possible_actions= self.getPossibleActions(state.state)

        # Populate the given Node with it's children (possible actions that can be done)
        for action in possible_actions:
            child_state= copy.deepcopy(state.state)
            child_state[action.row][action.column]= action.value # Apply the action to build the child state
            
            # Put the child node in the child node list
            child_node= Node(child_state, action, state) 
            state.children.append(child_node)
        
        # If no possible action can be taken, return the given state
        if state.children == []:
            return state
        # There are children, Return a random possible action
        # TODO: Try only expanding the node, no random choice
        else:
            return state#random.choice(state.children)

    """
    Use a given state (puzzle matrix, not Node) to find every possible action
    Returns a list of Action objects
    """
    def getPossibleActions(self, state) -> list:
        possible_actions= []

        # Go through every box in the matrix/puzzle
        for row_num in range(len(state)):
            for box_num in range(len(state[row_num])):
                # Check if the box is already filled.  If it is, skip it
                current_value_in_box= state[row_num][box_num]
                if current_value_in_box != 0:
                    continue
                
                # Box is empty
                # Determine every possible action that can be performed on this one box
                for number in VALID_NUMBERS:
                    #######
                    # TODO: Prune invalid actions (columns and boxes)
                    #######
                    if number in state[row_num]:
                        continue
                    action= Action(row_num,box_num,number)
                    possible_actions.append(action)
            
        # Return the list of actions that can be done from the given state
        return possible_actions

    """
    Check if the given Node contains the solution
    This is a goal state check
    Returns True if the puzzle is solved
    Returns False if the puzzle is NOT solved
    """
    def puzzleIsSolved(self, state) -> bool:
        # A puzzle is solved if every box is filled and there are no violations
        if self.puzzleIsFilled(state.state) and self.stateIsValid(state.state):
            return True
        return False
    
    def printState(self, state_node):
        state= state_node.state
        for row in state:
            print(state)


    # VALIDATION FUNCTIONS (Used to check states)
    """
    TODO: The validation functions are killing the speed.
    I've heard sets might be faster than list looping, look into those.
    We just really need to simplify these
    """


    """ 
    Check if every box in the puzzle is filled.
    Does NOT check if the puzzle is valid, only checks for empty boxes.
    Return True if there are no empty boxes
    Return False if there is 1+ empty box(es)
    """
    def puzzleIsFilled(self, state) -> bool:
        # A puzzle is filled if there are no empty boxes
        for row in state:
            if 0 in row:
                return False # Empty box found, puzzle not filled
        return True

    """
    Checks if the state is valid (no broken rules)
    Does NOT check if the puzzle is complete, only valid
    Return True if there are no broken rules
    Return False if there a broken rule is found
    """
    def stateIsValid(self, state) -> bool:
        # Check each row
        if self.validateRows(state) == False:
            return False
        # If we get here, the rows are valid

        # Check the columns
        if self.validateColumns(state) == False:
            return False
        # If we get here, the columns AND rows are valid

        # Check the sub 3x3 grids
        if self.validateSubGrids(state) == False:
            return False

        return True
    
    def validateRows(self, state) -> bool:
        for row in state:
            numbers_in_row= []
            for number in row:
                if number == 0: continue
                if number in numbers_in_row:
                    return False
                numbers_in_row.append(number)
        return True
    def validateColumns(self, state) -> bool:
        for column in range(len(state)):
            numbers_in_column= []
            for row in range(len(state)):
                number= state[row][column]
                if number == 0: continue
                if number in numbers_in_column:
                    return False
                numbers_in_column.append(number)
        return True
    def validateSubGrids(self, state) -> bool:
        for row in range(0,9,3):
            for column in range(0,9,3):
                numbers_in_subgrid= []
                for subgrid_row in range(row,row+3):
                    for subgrid_column in range(column,column+3):
                        number= state[subgrid_row][subgrid_column]
                        if number == 0: continue
                        if number in numbers_in_subgrid:
                            return False
                        numbers_in_subgrid.append(number)
        return True
    # END VALIDATION FUNCTIONS
