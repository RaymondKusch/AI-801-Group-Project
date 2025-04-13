

class Results:
    def __init__(self):
        self.heuristic= None
        self.givenPuzzle= None
        self.resultPuzzle= None
        self.solved= None
        self.emptyBoxCount= None
        self.expandedNodeCount= None
        self.searchDuration= None
        return
    
    def __str__(self):
        string= f"Result:\n\tGiven Puzzle: {self.givenPuzzle}\n\tResult: {self.resultPuzzle}\n\t"
        string= string+ f"Heuristic: {self.heuristic}\n\tSolved: {self.solved}\n\tEmpty Boxes: {self.emptyBoxCount}"
        string= string+ f"\n\tNum Expanded Nodes: {self.expandedNodeCount}\n\tSearch Duration: {self.searchDuration}"
        return string

    