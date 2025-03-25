def prioritizeRowCompletion(state):
    score= 0
    for row_num in range(len(state)):
        row= state[row_num]
        filled_boxes= 0
        for number in row:
            if number == 0:
                continue
            filled_boxes += 1
        score += 2**filled_boxes
    return score

def prioritizeColumnCompletion(state):
    score= 0
    return score

def prioritizeSubGridCompletion(state):
    score= 0
    return score


