def prioritizeRowCompletion(state):
    score= 0
    for row_num in range(len(state)):
        row= state[row_num]
        filled_boxes= 0
        for number in row:
            if number == 0:
                continue
            filled_boxes+= 1
        score+= 2**filled_boxes
    return score

def prioritizeColumnCompletion(state):
    score= 0
    for column_num in range(len(state)):
        filled_boxes= 0
        for row_num in range(len(state)):
            number= state[row_num][column_num]
            if number != 0:
                filled_boxes+= 1
        score+= 2**filled_boxes
    return score


def prioritizeSubgridCompletion(state):
    score = 0
    grid_size= len(state)
    subgrid_size= len(state)//3
    for subgrid_start_row in range(0, grid_size, subgrid_size):
        for subgrid_start_col in range(0, grid_size, subgrid_size):
            filled_boxes = 0
            for row in range(subgrid_size):
                for column in range(subgrid_size):
                    number= state[subgrid_start_row+row][subgrid_start_col+column]
                    if number != 0:
                        filled_boxes += 1
            score += 2**filled_boxes
    return score


