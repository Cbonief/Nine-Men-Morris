positions = []
for i in range(0, 8):
    positions.append([])
    for j in range(0, 8):
        positions[i].append(None)

positions[0][0] = [24, 24]
positions[0][6] = [24, 300]
positions[0][5] = [24, 600-24]

positions[1][1] = [116, 116]
positions[1][6] = [116, 300]
positions[1][4] = [116, 600-116]

positions[2][2] = [208, 208]
positions[2][6] = [208, 300]
positions[2][3] = [208, 600-208]

positions[3][2] = [600-208, 208]
positions[3][7] = [600-208, 300]
positions[3][3] = [600-208, 600-208]

positions[4][1] = [600-116, 116]
positions[4][7] = [600-116, 300]
positions[4][4] = [600-116, 600-116]

positions[5][0] = [600-24, 24]
positions[5][7] = [600-24, 300]
positions[5][5] = [600-24, 600-24]

positions[6][0] = [300, 24]
positions[6][1] = [300, 116]
positions[6][2] = [300, 208]

positions[7][3] = [300, 600-208]
positions[7][4] = [300, 600-116]
positions[7][5] = [300, 600-24]


def adjacent_positions(position):
    if position[0] == 0 and position[1] == 0:
        return [[0, 6], [6, 0]]
    elif position[0] == 0 and position[1] == 6:
        return [[0, 0], [0, 5], [1, 6]]
    elif position[0] == 0 and position[1] == 5:
        return [[0, 6], [7, 5]]
    elif position[0] == 1 and position[1] == 1:
        return [[6, 1], [1, 6]]
    elif position[0] == 1 and position[1] == 6:
        return [[1, 1], [0, 6], [1, 4], [2, 6]]
    elif position[0] == 1 and position[1] == 4:
        return [[1, 6], [7, 4]]
    elif position[0] == 2 and position[1] == 2:
        return [[6, 2], [2, 6]]
    elif position[0] == 2 and position[1] == 6:
        return [[2, 2], [1, 6], [2, 3]]
    elif position[0] == 2 and position[1] == 3:
        return [[2, 6], [7, 3]]
    elif position[0] == 3 and position[1] == 2:
        return [[6, 2], [3, 7]]
    elif position[0] == 3 and position[1] == 7:
        return [[3, 2], [4, 7], [3, 3]]
    elif position[0] == 3 and position[1] == 3:
        return [[3, 7], [7, 3]]
    elif position[0] == 4 and position[1] == 1:
        return [[6, 1], [4, 7]]
    elif position[0] == 4 and position[1] == 7:
        return [[4, 1], [3, 7], [4, 4], [5, 7]]
    elif position[0] == 4 and position[1] == 4:
        return [[7, 4], [4, 7]]
    elif position[0] == 5 and position[1] == 0:
        return [[6, 0], [5, 7]]
    elif position[0] == 5 and position[1] == 7:
        return [[5, 0], [4, 7], [5, 5]]
    elif position[0] == 5 and position[1] == 5:
        return [[5, 7], [7, 5]]
    elif position[0] == 6 and position[1] == 0:
        return [[0, 0], [5, 0], [6, 1]]
    elif position[0] == 6 and position[1] == 1:
        return [[6, 0], [1, 1], [4, 1], [6, 2]]
    elif position[0] == 6 and position[1] == 2:
        return [[6, 1], [2, 2], [3, 2]]
    elif position[0] == 7 and position[1] == 3:
        return [[2, 3], [3, 3], [7, 4]]
    elif position[0] == 7 and position[1] == 4:
        return [[7, 3], [1, 4], [4, 4], [7, 5]]
    elif position[0] == 7 and position[1] == 5:
        return [[7, 4], [0, 5], [5, 5]]
    else:
        return None


adjacency_list = []
for i in range(0, 8):
    adjacency_list.append([])
    for j in range(0, 8):
        adjacency_list[i].append(adjacent_positions([i, j]))


def is_position_adjacent(this_position, other_position):
    for adjacente in adjacency_list[this_position[0]][this_position[1]]:
        if adjacente[0] == other_position[0] and adjacente[1] == other_position[1]:
            return True
    return False


# for i in range(0, 8):
#     print("-----------------")
#     for j in range(0, 8):
#         if adj_list[i][j]:
#             print("[{},{}] -> {}".format(i,j, adj_list[i][j]))

board = []
for i in range(0, 8):
    board.append([])
    for j in range(0, 8):
        board[i].append(None)

board[0][0] = 0
board[0][6] = 0
board[0][5] = 0

board[1][1] = 0
board[1][4] = 0
board[1][6] = 0

board[2][2] = 0
board[2][6] = 0
board[2][3] = 0

board[3][2] = 0
board[3][7] = 0
board[3][3] = 0

board[4][1] = 0
board[4][7] = 0
board[4][4] = 0

board[5][0] = 0
board[5][7] = 0
board[5][5] = 0

board[6][0] = 0
board[6][1] = 0
board[6][2] = 0

board[7][3] = 0
board[7][4] = 0
board[7][5] = 0