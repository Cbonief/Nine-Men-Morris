import numpy as np
import copy
from trilha import *
import os
import json

with open(os.path.join("Assets", "primeiras_jogadas.json"), "r") as read_file:
    primeiras_jogadas = json.load(read_file)


class Flag:
    EXACT = 0
    LOWERBOUND = 1
    UPPERBOUND = 1


class Dado:
    def __init__(self, profundidade, score, jogada, flag):
        self.flag = flag
        self.profundidade = profundidade
        self.score = score
        self.jogada = jogada


tabela_de_transposicao = {}


def verificar_tabela_de_transposicao(trilha):
    if hash(trilha) in tabela_de_transposicao.keys():
        return tabela_de_transposicao[hash(trilha)]
    else:
        return None


def adicionar_dado(trilha, dado):
    tabela_de_transposicao[hash(trilha)] = dado


def calcular_movimento(trilha, profundidade, cor_do_jogador):
    if trilha.primeira_jogada[trilha.indice(cor_do_jogador)]:
        if cor_do_jogador == Jogador.PRETO:
            jogada = criar_jogada_a_partir_do_codigo(primeiras_jogadas[trilha.indice(Jogador.PRETO)][profundidade-1][str(hash(trilha))])
        else:
            jogada = criar_jogada_a_partir_do_codigo(primeiras_jogadas[trilha.indice(Jogador.BRANCO)][profundidade-1])
    else:
        _, jogada = negamax(trilha, profundidade, -np.inf, np.inf, cor_do_jogador)
    return jogada


def negamax(trilha, profundidade, alpha, beta, cor_do_jogador):
    alpha0 = alpha

    dado = verificar_tabela_de_transposicao(trilha)
    if dado is not None and dado.profundidade >= profundidade:
        if dado.flag == Flag.EXACT:
            return dado.score, dado.jogada
        elif dado.flag == Flag.LOWERBOUND:
            alpha = max(alpha, dado.score)
        elif dado.flag == Flag.UPPERBOUND:
            beta = min(beta, dado.score)

        if alpha >= beta:
            return dado.score, dado.jogada

    if trilha.game_over:
        if trilha.vencedor == cor_do_jogador:
            return 100, None
        else:
            return -100, None

    if profundidade == 0:
        return trilha.numero_de_pecas[trilha.indice(cor_do_jogador)] - trilha.numero_de_pecas[
            trilha.indice((-1) * cor_do_jogador)], None

    maximo = -np.inf
    jogadas_validas = trilha.jogadas_validas(cor_do_jogador)
    if len(jogadas_validas) > 0:
        jogada_escolhida = jogadas_validas[0]
    else:
        return maximo, None
    for jogada in jogadas_validas:
        trilha_filha = copy.deepcopy(trilha)
        trilha_filha.executar_jogada(jogada)
        resultado, _ = negamax(trilha_filha, profundidade - 1, -beta, -alpha, -cor_do_jogador)
        resultado = - resultado
        if resultado > maximo:
            maximo = resultado
            jogada_escolhida = jogada
        alpha = max(alpha, maximo)
        if beta <= alpha:
            break

    novo_dado = Dado(profundidade, maximo, jogada_escolhida, None)
    if maximo <= alpha0:
        novo_dado.flag = Flag.UPPERBOUND
    elif maximo >= beta:
        novo_dado.flag = Flag.LOWERBOUND
    else:
        novo_dado.flag = Flag.EXACT
    adicionar_dado(trilha, novo_dado)

    return maximo, jogada_escolhida
