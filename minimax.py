import copy
import numpy as np
from time import time_ns
from queue import Queue
from threading import Thread
from mills import Player, create_move_from_hash
import os
import json

with open(os.path.join("Assets", "primeiras_jogadas.json"), "r") as read_file:
	primeiras_jogadas = json.load(read_file)


def calcular_movimento(trilha, profundidade, cor_do_jogador):
	if trilha.is_first_move[trilha.indice(cor_do_jogador)]:
		if cor_do_jogador == Player.BLACK:
			jogada = create_move_from_hash(primeiras_jogadas[trilha.indice(Player.BLACK)][profundidade - 1][str(hash(trilha))])
		else:
			jogada = create_move_from_hash(primeiras_jogadas[trilha.indice(Player.WHITE)][profundidade - 1])
	else:
		_, jogada = minimax(trilha, profundidade, -np.inf, np.inf, True, cor_do_jogador)
	return jogada


def minimax(trilha, profundidade, alpha, beta, jogador_maximizador, cor_do_jogador):
	if trilha.game_over:
		if trilha.winner == cor_do_jogador:
			return 100, None
		else:
			return -100, None

	if profundidade == 0:
		return 2 * trilha.number_of_pieces[trilha.indice(cor_do_jogador)] - trilha.number_of_pieces[trilha.indice((-1) * cor_do_jogador)], None

	if jogador_maximizador:
		maximo = -np.inf
		jogadas_validas = trilha.get_all_valid_moves(cor_do_jogador)
		if len(jogadas_validas) > 0:
			chosen_move = jogadas_validas[0]
		else:
			return maximo, None
		for jogada in jogadas_validas:
			trilha_filha = copy.deepcopy(trilha)
			trilha_filha.execute_move(jogada)
			resultado, _ = minimax(trilha_filha, profundidade - 1, alpha, beta, False, cor_do_jogador)
			if resultado > maximo:
				maximo = resultado
				chosen_move = jogada
			alpha = max(alpha, maximo)
			if beta <= alpha:
				break
		return maximo, chosen_move
	else:
		minimo = np.inf
		jogadas_validas = trilha.get_all_valid_moves(cor_do_jogador)
		if len(jogadas_validas) > 0:
			chosen_move = jogadas_validas[0]
		else:
			return minimo, None
		for jogada in jogadas_validas:
			trilha_filha = copy.deepcopy(trilha)
			trilha_filha.execute_move(jogada)
			resultado, _ = minimax(trilha_filha, profundidade - 1, alpha, beta, True, cor_do_jogador)
			if resultado < minimo:
				minimo = resultado
				chosen_move = jogada
			beta = min(beta, minimo)
			if beta <= alpha:
				break
		return minimo, chosen_move
