""" 
A search node.
State is the puzzle matrix.
Action is the action taken to make the state.
Parent is the parent node.
Children are the child nodes.
"""
class Node:
    def __init__(self, state, action, parent):
        self.state= state
        self.action= action
        self.parent= parent
        self.children= []
        self.timesSeen= 0
        self.timesSeenAndWon= 0

    def __str__(self):
        string= ""
        for row in self.state:
            string= string+str(row)+"\n"
        return string

""" 
A sudoku action.
Row, column are the coordinates of the box we want to write in.
value is the number we want to write in that box.
"""
class Action:
    def __init__(self, row,column,value):
        self.row=row
        self.column=column
        self.value=value
    def __str__(self):
        return f"{(self.column,self.row)} | {self.value}"
    
"""  
Might remove later.
A sudoku box.
Row,Column are the coordinates of the box.
"""
class Box:
    def __init__(self, row, column):
        self.row=row
        self.column=column
    def __str__(self):
        return f"{(self.row,self.column)}"