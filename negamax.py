import copy
import json
import os

from ninemenmorris import *

with open(os.path.join("Assets", "primeiras_jogadas.json"), "r") as read_file:
    first_moves = json.load(read_file)


class Flag:
    EXACT = 0
    LOWERBOUND = 1
    UPPERBOUND = 1


class Data:
    def __init__(self, depth, score, best_move, flag):
        self.flag = flag
        self.depth = depth
        self.score = score
        self.best_move = best_move


transposition_table = [
    {},
    {}
]


def lookup_table(player, mill):
    try:
        return transposition_table[Player.index[player]][hash(mill)]
    except KeyError:
        return None


def add_data_to_table(player, mill, new_data):
    transposition_table[Player.index[player]][hash(mill)] = new_data


def calculate_movement(mill, depth, player_color):
    _, move = negamax(mill, depth, -np.inf, np.inf, player_color)
    return move


def negamax(mill, depth, alpha, beta, player_color, called=0):
    alpha0 = alpha
    called += 1
    # print(called)

    data = lookup_table(player_color, mill)
    if data is not None and data.depth >= depth:
        if data.flag == Flag.EXACT:
            return data.score, data.best_move
        elif data.flag == Flag.LOWERBOUND:
            alpha = max(alpha, data.score)
        elif data.flag == Flag.UPPERBOUND:
            beta = min(beta, data.score)

        if alpha >= beta:
            return data.score, data.best_move

    if mill.game_over:
        if mill.winner == player_color:
            return 100, None
        else:
            return -100, None

    if depth == 0:
        return mill.number_of_pieces[mill.indice(player_color)] - mill.number_of_pieces[mill.indice((-1) * player_color)], None

    maximum = -np.inf
    valid_moves = mill.get_all_valid_moves(player_color)
    if len(valid_moves) > 0:
        chosen_move = valid_moves[0]
    else:
        return maximum, None
    for move in valid_moves:
        child_mill = copy.deepcopy(mill)
        child_mill.execute_move(move)
        if child_mill.active_player == player_color:
            result, _ = negamax(child_mill, depth, alpha, beta, child_mill.active_player, called)
        else:
            result, _ = negamax(child_mill, depth - 1, -beta, -alpha, -player_color, called)
            result = - result
        if result > maximum:
            maximum = result
            chosen_move = move
        alpha = max(alpha, maximum)
        if beta <= alpha:
            break

    new_data = Data(depth, maximum, chosen_move, None)
    if maximum <= alpha0:
        new_data.flag = Flag.UPPERBOUND
    elif maximum >= beta:
        new_data.flag = Flag.LOWERBOUND
    else:
        new_data.flag = Flag.EXACT
    add_data_to_table(player_color, mill, new_data)

    return maximum, chosen_move
