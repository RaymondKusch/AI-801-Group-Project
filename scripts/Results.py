

class Results:
    def __init__(self):
        self.heuristic= None
        self.givenPuzzle= None
        self.resultPuzzle= None
        self.solved= None
        self.emptyBoxCount= None
        self.expandedNodeCount= None
        self.searchDuration= None
        self.puzzleGroup= None
        self.puzzleNumber= None
        return
    
    def __str__(self):
        string= f"Result:\n"
        string= string+ f"\tHeuristic: {self.heuristic}\n\tSolved: {self.solved}\n\tEmpty Boxes: {self.emptyBoxCount}"
        string= string+ f"\n\tNum Expanded Nodes: {self.expandedNodeCount}\n\tSearch Duration: {self.searchDuration}\n\\n\tNumber: {self.puzzleNumber}"
        return string

    