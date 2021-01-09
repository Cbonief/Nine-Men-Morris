from Assets.piece_positions import *
import numpy as np


class MoveType:
    PLACE_PIECE = 1
    MOVE_PIECE = 2
    REMOVE_PIECE = 3


class Move:
    def __init__(self, position, move_type, final_position=None):
        self.move_type = move_type
        self.position = position
        self.final_position = final_position

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        a = self.move_type
        b = 10 * (self.position[0] + 1) + (self.position[1] + 1)
        if self.move_type == MoveType.MOVE_PIECE:
            c = 10 * (self.final_position[0] + 1) + (self.final_position[1] + 1)
            return 10000*a + b * 100 + c
        else:
            return 100*a + b

    def reverse(self):
        if self.move_type == MoveType.MOVE_PIECE:
            return Move(self.final_position, self.move_type, self.position)
        elif self.move_type == MoveType.PLACE_PIECE:
            return Move(self.position, MoveType.PLACE_PIECE)
        elif self.move_type == MoveType.REMOVE_PIECE:
            return Move(self.position, MoveType.REMOVE_PIECE)

    def is_valid(self, trilha):
        if self.move_type == MoveType.REMOVE_PIECE:
            return trilha.board[self.position[0]][self.position[1]] == -trilha.active_player
        elif self.move_type == MoveType.PLACE_PIECE:
            return trilha.board[self.position[0]][self.position[1]] == 0
        else:
            if trilha.is_player_flying[trilha.indice(trilha.active_player)]:
                return trilha.board[self.final_position[0]][self.final_position[1]] == 0
            else:
                return trilha.board[self.final_position[0]][self.final_position[1]] == 0 and is_position_adjacent(self.position, self.final_position)

    def __repr__(self):
        if self.move_type == MoveType.REMOVE_PIECE:
            return 'Remove piece from position {}'.format(self.position)
        elif self.move_type == MoveType.PLACE_PIECE:
            return 'Add a piece to position {}'.format(self.position)
        else:
            return 'Move piece from position {} to {}'.format(self.position, self.final_position)


def create_move_from_hash(hashed_move):
    info = []
    string = str(hashed_move)
    for c in string:
        info.append(int(c))
    move_type = info[0]
    position = [info[1]-1, info[2]-1]
    final_position = None
    if move_type == MoveType.MOVE_PIECE:
        final_position = [info[3]-1, info[4]-1]
    return Move(position, move_type, final_position)


class Player:
    WHITE = 1
    BLACK = -1
    index = {
        1: 1,
        -1: 0
    }


class GameStage:
    PLACEMENT = 0
    MOVEMENT = 1
    REMOVAL = 2


class NineMenMorris:
    def __init__(self):
        self.board = board
        self.stage = GameStage.PLACEMENT
        self.active_player = 1
        self.number_of_pieces = np.array([0, 0])
        self.number_of_placed_pieces = np.array([0, 0])
        self.pieces_in_mills = [[], []]
        self.mills = [[], []]
        self.last_stage_played = 0
        self.winner = 0
        self.is_player_flying = [False, False]
        self.game_over = False
        self.is_first_move = [True, True]

    @staticmethod
    def indice(jogador):
        return int((jogador+1)/2)

    def place_piece(self, position):
        if self.piece_from_position(position) == 0:
            self.board[position[0]][position[1]] = self.active_player
            self.number_of_pieces[Player.index[self.active_player]] += 1
            self.number_of_placed_pieces[Player.index[self.active_player]] += 1

    def remove_piece(self, position):
        self.board[position[0]][position[1]] = 0
        self.number_of_pieces[Player.index[(-1) * self.active_player]] -= 1

    def move_piece(self, starting_position, final_position):
        self.board[starting_position[0]][starting_position[1]] = 0
        self.board[final_position[0]][final_position[1]] = self.active_player

    def piece_from_position(self, position):
        return self.board[position[0]][position[1]]

    def execute_move(self, move):
        if self.is_first_move[Player.index[self.active_player]]:
            self.is_first_move[Player.index[self.active_player]] = False
        if move.move_type == MoveType.PLACE_PIECE and self.stage == GameStage.PLACEMENT:
            self.place_piece(move.position)
            if self.number_of_placed_pieces[0] == 9:
                self.stage = 1
                self.last_stage_played = GameStage.MOVEMENT
        elif move.move_type == MoveType.MOVE_PIECE and self.stage == GameStage.MOVEMENT:
            self.move_piece(move.position, move.final_position)
        elif move.move_type == MoveType.REMOVE_PIECE and self.stage == GameStage.REMOVAL:
            self.remove_piece(move.position)
            if self.last_stage_played == GameStage.MOVEMENT:
                if self.number_of_pieces[Player.index[(-1) * self.active_player]] == 2:
                    self.winner = self.active_player
                    self.game_over = True
                elif self.number_of_pieces[Player.index[(-1) * self.active_player]] == 3:
                    self.is_player_flying[Player.index[(-1) * self.active_player]] = True
            self.stage = self.last_stage_played

        if len(self.get_all_valid_moves((-1) * self.active_player)) == 0:
            self.game_over = True
            self.winner = self.active_player

        mill_created = self.check_for_new_mill()
        if mill_created:
            self.stage = GameStage.REMOVAL
            if len(self.get_all_valid_moves((-1) * self.active_player)) == 0:
                self.stage = self.last_stage_played
        else:
            self.active_player = (-1) * self.active_player

    def check_for_new_mill(self):
        mill_created = False
        pieces_in_mills, mills = self.count_active_player_mills()

        self.pieces_in_mills[Player.index[self.active_player]] = pieces_in_mills
        for mill in mills:
            if mill not in self.mills[Player.index[self.active_player]]:
                mill_created = True
        self.mills[Player.index[self.active_player]] = mills
        return mill_created

    def count_active_player_mills(self):
        pieces_in_mills = []
        mills = []
        for i in range(0, 8):
            line_sum = 0
            for j in range(0, 8):
                if self.board[i][j]:
                    line_sum += self.board[i][j]
            if line_sum == 3 * self.active_player:
                for j in range(0, 8):
                    if self.board[i][j]:
                        pieces_in_mills.append([i, j])
                mills.append(10*i)
            line_sum = 0
            for j in range(0, 8):
                if self.board[j][i]:
                    line_sum += self.board[j][i]
            if line_sum == 3 * self.active_player:
                for j in range(0, 8):
                    if self.board[j][i]:
                        pieces_in_mills.append([j, i])
                mills.append(i)
        return pieces_in_mills, mills

    def is_piece_in_mill(self, position):
        for peca in self.pieces_in_mills[self.indice(Player.BLACK)]:
            if peca[0] == position[0] and peca[1] == position[1]:
                return True
        for peca in self.pieces_in_mills[self.indice(Player.WHITE)]:
            if peca[0] == position[0] and peca[1] == position[1]:
                return True
        return False

    def get_all_valid_moves(self, player):
        moves = []
        if self.stage == GameStage.PLACEMENT:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.board[i][j] == 0:
                        moves.append(Move([i, j], MoveType.PLACE_PIECE))
        if self.stage == GameStage.MOVEMENT:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.board[i][j] == player:
                        if self.is_player_flying[self.indice(player)]:
                            for ii in range(0, 8):
                                for jj in range(0, 8):
                                    if self.board[ii][jj] == 0:
                                        moves.append(Move([i, j], MoveType.MOVE_PIECE, [ii, jj]))
                        else:
                            for adj in adjacency_list[i][j]:
                                if self.board[adj[0]][adj[1]] == 0:
                                    moves.append(Move([i, j], MoveType.MOVE_PIECE, adj))
        if self.stage == GameStage.REMOVAL:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.board[i][j] == (-1)*player and not self.is_piece_in_mill([i, j]):
                        moves.append(Move([i, j], MoveType.REMOVE_PIECE))
        return moves

    def __hash__(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        index = 0
        hashed_mill = 1
        for column in range(0, 8):
            for row in range(0, 8):
                if self.board[column][row] is not None:
                    if self.board[column][row] != 0:
                        hashed_mill = hashed_mill * np.power(primes[index], (self.board[column][row] + 3) / 2)
                    index += 1
        return int(hashed_mill * np.power(primes[index], self.stage + 1))
