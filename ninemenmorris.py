import numpy as np

from Assets.piece_positions import *

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


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
        if self.move_type == MoveType.MOVE_PIECE:
            return primes[self.final_position]*primes[self.position]**(a+1)
        else:
            return primes[self.position]**(a+1)

    def reverse(self):
        if self.move_type == MoveType.MOVE_PIECE:
            return Move(self.final_position, self.move_type, self.position)
        elif self.move_type == MoveType.PLACE_PIECE:
            return Move(self.position, MoveType.PLACE_PIECE)
        elif self.move_type == MoveType.REMOVE_PIECE:
            return Move(self.position, MoveType.REMOVE_PIECE)

    def is_valid(self, trilha):
        if self.move_type == MoveType.REMOVE_PIECE:
            return trilha.board[self.position] == -trilha.active_player
        elif self.move_type == MoveType.PLACE_PIECE:
            return trilha.board[self.position] == 0
        else:
            if trilha.is_player_flying[trilha.indice(trilha.active_player)]:
                return trilha.board[self.final_position] == 0
            else:
                return trilha.board[self.final_position] == 0 and is_position_adjacent(self.position, self.final_position)

    def __repr__(self):
        if self.move_type == MoveType.REMOVE_PIECE:
            return 'Remove piece from position {}'.format(self.position)
        elif self.move_type == MoveType.PLACE_PIECE:
            return 'Add a piece to position {}'.format(self.position)
        else:
            return 'Move piece from position {} to {}'.format(self.position, self.final_position)


def create_move_from_hash(hashed_move):
    aux = hashed_move
    move_type = MoveType.PLACE_PIECE
    position = 0
    final_position = None
    for index, prime in enumerate(primes):
        total_division = 0
        while aux % prime == 0:
            total_division += 1
            aux = aux / prime
        if total_division >= 2:
            position = index
            if total_division == 3:
                move_type = MoveType.MOVE_PIECE
            elif total_division == 4:
                move_type = MoveType.REMOVE_PIECE
        if total_division == 1:
            final_position = index
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
        self.active_player = Player.WHITE
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
            self.board[position] = self.active_player
            self.number_of_pieces[Player.index[self.active_player]] += 1
            self.number_of_placed_pieces[Player.index[self.active_player]] += 1

    def remove_piece(self, position):
        self.board[position] = 0
        self.number_of_pieces[Player.index[(-1) * self.active_player]] -= 1

    def move_piece(self, starting_position, final_position):
        self.board[starting_position] = 0
        self.board[final_position] = self.active_player

    def piece_from_position(self, position):
        return self.board[position]

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
            if len(self.get_all_valid_moves(self.active_player)) == 0:
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
        for mill_index, mill in enumerate(possible_mills):
            mill_found = True
            for position in mill:
                if not self.board[position] == self.active_player:
                    mill_found = False
                    break
            if mill_found:
                mills.append(mill_index)
                pieces_in_mills.extend(position for position in mill if position not in pieces_in_mills)
        return pieces_in_mills, mills

    def is_piece_in_mill(self, position):
        for piece in self.pieces_in_mills[self.indice(Player.BLACK)]:
            if piece == position:
                return True
        for piece in self.pieces_in_mills[self.indice(Player.WHITE)]:
            if piece == position:
                return True
        return False

    def get_all_valid_moves(self, player):
        moves = []
        if self.stage == GameStage.PLACEMENT:
            for position in range(0, 24):
                if self.board[position] == 0:
                    moves.append(Move(position, MoveType.PLACE_PIECE))
        if self.stage == GameStage.MOVEMENT:
            for position in range(0, 24):
                if self.board[position] == player:
                    if self.is_player_flying[self.indice(player)]:
                        for final_position in range(0, 24):
                            if self.board[final_position] == 0:
                                moves.append(Move(position, MoveType.MOVE_PIECE, final_position))
                    else:
                        for adj_pos in adjacency_list[position]:
                            if self.board[adj_pos] == 0:
                                moves.append(Move(position, MoveType.MOVE_PIECE, adj_pos))
        if self.stage == GameStage.REMOVAL:
            for position in range(0, 24):
                if self.board[position] == (-1)*player and not self.is_piece_in_mill(position):
                    moves.append(Move(position, MoveType.REMOVE_PIECE))
        return moves

    def __hash__(self):
        hashed_mill = 1
        for position in range(0, 24):
            if self.board[position] != 0:
                hashed_mill = hashed_mill * np.power(primes[position], (self.board[position] + 3) / 2)
        return int(hashed_mill * np.power(primes[24], self.stage + 1))
