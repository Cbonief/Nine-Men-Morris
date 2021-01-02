import copy
import numpy as np
from time import time_ns


def calcular_movimento(trilha, profundidade, cor_do_jogador):
	score, jogada = minimax(trilha, profundidade, -np.inf, np.inf, True, cor_do_jogador)
	return jogada


def minimax(trilha, profundidade, alpha, beta, jogador_maximizador, cor_do_jogador):
	if trilha.game_over:
		if trilha.vencedor == cor_do_jogador:
			return 100, None
		else:
			return -100, None

	if profundidade == 0:
		return trilha.numero_de_pecas[trilha.indice(cor_do_jogador)] - trilha.numero_de_pecas[trilha.indice((-1)*cor_do_jogador)], None

	if jogador_maximizador:
		maximo = -np.inf
		jogadas_validas = trilha.jogadas_validas(cor_do_jogador)
		if len(jogadas_validas) > 0:
			chosen_move = jogadas_validas[0]
		else:
			return maximo, None
		for jogada in jogadas_validas:
			trilha_filha = copy.deepcopy(trilha)
			trilha_filha.executar_jogada(jogada)
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
		jogadas_validas = trilha.jogadas_validas(cor_do_jogador)
		if len(jogadas_validas) > 0:
			chosen_move = jogadas_validas[0]
		else:
			return minimo, None
		for jogada in jogadas_validas:
			trilha_filha = copy.deepcopy(trilha)
			trilha_filha.executar_jogada(jogada)
			resultado, _ = minimax(trilha_filha, profundidade - 1, alpha, beta, True, cor_do_jogador)
			if resultado < minimo:
				minimo = resultado
				chosen_move = jogada
			beta = min(beta, minimo)
			if beta <= alpha:
				break
		return minimo, chosen_move
