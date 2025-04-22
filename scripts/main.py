import os
import argparse
import time
import csv

#Local Files
import Agent
import Heuristics
import SudokuPuzzles
from DecisionTree import *
import Results

def runPuzzle(puzzle, heuristic, number, group):
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
    results.puzzleGroup= group
    results.puzzleNumber= number

    empty_boxes= 0
    for row in result.state:
        empty_boxes= row.count(0)

    results.emptyBoxCount= empty_boxes

    return results

def recordResults(results):
    csv_stuff_to_write= []
    for result in results:
        group= result.puzzleGroup
        number= result.puzzleNumber
        heuristic= result.heuristic
        solved= result.solved
        empty= result.emptyBoxCount
        expanded= result.expandedNodeCount
        duration= result.searchDuration

        info= { "Group": group,
                "Puzzle Number": number,
                "Heuristic": heuristic,
                "Solved": solved,
                "Empty Box Count": empty,
                "Expanded Node Count": expanded,
                "Search Duration": duration
        }
        csv_stuff_to_write.append(info)

    print(csv_stuff_to_write)
    
    column_names= ["Group","Puzzle Number", "Heuristic", "Solved",
                   "Empty Box Count", "Expanded Node Count", "Search Duration"]
    
    with open("MCTS_results.csv", 'w', newline='') as my_csv:
        csv_writer= csv.DictWriter(my_csv, fieldnames=column_names)
        csv_writer.writeheader()
        csv_writer.writerows(csv_stuff_to_write)

    print("CSV file written to MCTS_results.csv!")



def main():

    heuristics= [Heuristics.prioritizeColumnCompletion, Heuristics.prioritizeRowCompletion, Heuristics.prioritizeSubgridCompletion]
    all_results= []
    for heuristic in heuristics:
        for iteration in range(5):
            #for number,puzzle in SudokuPuzzles.PATTERNED.items():
            #    print(f"\n\nBeginning PATTERNED Puzzle {number}!\n\n")
            #    results= runPuzzle(puzzle, heuristic, number, "PATTERNED")
            #    all_results.append(results)
            #    print(results)

            #for number,puzzle in SudokuPuzzles.DENSE_RANDOM.items():
            #    print(f"\n\nBeginning DENSE_RANDOM Puzzle {number}!\n\n")
            #    results= runPuzzle(puzzle, heuristic, number, "DENSE_RANDOM")
            #    all_results.append(results)
            #    print(results)

            for number,puzzle in SudokuPuzzles.SPARSE_RANDOM.items():
                print(f"\n\nBeginning SPARSE_RANDOM Puzzle {number}!\n\n")
                results= runPuzzle(puzzle, heuristic, number, "SPARSE_RANDOM")
                all_results.append(results)
                print(results)

    recordResults(all_results)

    return

if __name__ == "__main__":
    main()