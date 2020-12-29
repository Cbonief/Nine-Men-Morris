import copy
from time import time_ns

def calcular_movimento(trilha, profundidade, cor_do_jogador):
	score, jogada = minimax(trilha, profundidade, -10000, 10000, True, cor_do_jogador)
	return jogada


def minimax(trilha, profundidade, alpha, beta, jogador_maximizador, cor_do_jogador):
	if trilha.game_over:
		if trilha.vencedor == cor_do_jogador:
			return 100, None
		else:
			return -100, None

	if profundidade == 0:
		if cor_do_jogador == 1:
			return trilha.numero_de_pecas_branco**2 - trilha.numero_de_pecas_preto**2, None
		else:
			return trilha.numero_de_pecas_preto**2 - trilha.numero_de_pecas_branco**2, None

	if jogador_maximizador:
		maximo = -1000
		for jogada in trilha.jogadas_validas():
			trilha_filha = copy.deepcopy(trilha)
			trilha_filha.executar_jogada(jogada)
			avaliacao, _ = minimax(trilha_filha, profundidade - 1, alpha, beta, False, cor_do_jogador)
			if avaliacao > maximo:
				maximo = avaliacao
				chosen_move = jogada
			alpha = max(alpha, avaliacao)
			if beta <= alpha:
				break
		return maximo, chosen_move
	else:
		minimo = 1000
		for jogada in trilha.jogadas_validas():
			trilha_filha = copy.deepcopy(trilha)
			trilha_filha.executar_jogada(jogada)
			avaliacao, _ = minimax(trilha_filha, profundidade - 1, alpha, beta, True, cor_do_jogador)
			if avaliacao < minimo:
				minimo = avaliacao
				chosen_move = jogada
			beta = min(beta, avaliacao)
			if beta <= alpha:
				break
	return minimo, chosen_move
