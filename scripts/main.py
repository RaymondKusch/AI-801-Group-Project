import os
import argparse
import time

#Local Files
import Agent
import Heuristics
import SudokuPuzzles
from DecisionTree import *
import Results

def runPuzzle(puzzle, heuristic, number):
    results= Results.Results()
    results.givenPuzzle= puzzle
    results.heuristic= heuristic.__name__

    initial_state= Node(puzzle, None,None)
    agent= Agent.Agent(initial_state, heuristic)

    start_time= time.perf_counter()
    result,solved,expanded_node_count= agent.solvePuzzle()
    end_time= time.perf_counter()

    search_duration= end_time - start_time
    results.searchDuration= search_duration

    results.resultPuzzle= result.state
    results.solved= solved
    results.expandedNodeCount= expanded_node_count

    empty_boxes= 0
    for row in result.state:
        empty_boxes= row.count(0)

    results.emptyBoxCount= empty_boxes

    return results


def main():

    heuristics= [Heuristics.prioritizeColumnCompletion, Heuristics.prioritizeRowCompletion, Heuristics.prioritizeSubgridCompletion]
    for heuristic in heuristics:
        for iteration in range(5):
            for number,puzzle in SudokuPuzzles.PATTERNED.items():
                print(f"\n\nBeginning PATTERNED Puzzle {number}!\n\n")
                results= runPuzzle(puzzle, heuristic, number)
                print(results)

            for number,puzzle in SudokuPuzzles.DENSE_RANDOM.items():
                print(f"\n\nBeginning DENSE_RANDOM Puzzle {number}!\n\n")
                results= runPuzzle(puzzle, heuristic, number)
                print(results)

            for number,puzzle in SudokuPuzzles.SPARSE_RANDOM.items():
                print(f"\n\nBeginning SPARSE_RANDOM Puzzle {number}!\n\n")
                results= runPuzzle(puzzle, heuristic, number)
                print(results)

    return

if __name__ == "__main__":
    main()