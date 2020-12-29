import pygame
import pygame.freetype
from pathlib import Path
import os
import time
import random
import numpy as np
from Assets.piece_positions import *
from minimax import *
from time import time

class Jogada:
    def __init__(self, posicao, tipo, posicao_final=None):
        self.tipo = tipo
        self.posicao = posicao
        self.posicao_final = posicao_final

    def __eq__(self, other):
        same_type = self.tipo == other.tipo
        same_pos = self.posicao[0] == other.posicao[0] and self.posicao[1] == other.posicao[1]
        same_end_pos = True
        if self.tipo == 'Movimentar' and same_type:
            same_end_pos = self.posicao_final[0] == other.posicao_final[0] and self.posicao_final[1] == other.posicao_final[1]
        return same_type and same_pos and same_end_pos

    def reversa(self):
        if self.tipo == 'Movimentar':
            return Jogada(self.posicao_final, self.tipo, self.posicao)
        else:
            return None

    def valida(self, trilha):
        if self.tipo == 'RemoverPeca':
            return trilha.tabuleiro[self.posicao[0]][self.posicao[1]] != 0
        elif self.tipo == 'ColocarPeca':
            return trilha.tabuleiro[self.posicao[0]][self.posicao[1]] == 0
        else:
            return trilha.tabuleiro[self.posicao_final[0]][self.posicao_final[1]] == 0 and posicao_adjacente(self.posicao, self.posicao_final)


class Trilha:
    def __init__(self):
        self.tabuleiro = tabuleiro
        self.etapa = 0                      #0 - Colocacao; 1 - Movimentacao, 2 - Remocao, 3 - Voando
        self.jogador_ativo = 1
        self.trilhas_branco = 0
        self.trilhas_preto = 0
        self.numero_de_pecas_branco = 0
        self.numero_de_pecas_preto = 0
        self.pecas_posicionadas_branco = 0
        self.pecas_posicionadas_preto = 0
        self.pecas_branco_em_trilha = []
        self.pecas_preto_em_trilha = []
        self.ultima_etapa = 0
        self.vencedor = 0
        self.game_over = False

    def colocar_peca(self, posicao):
        if self.peca_da_posicao(posicao) == 0:
            self.tabuleiro[posicao[0]][posicao[1]] = self.jogador_ativo
            if self.jogador_ativo == 1:
                self.numero_de_pecas_branco += 1
                self.pecas_posicionadas_branco += 1
            else:
                self.numero_de_pecas_preto += 1
                self.pecas_posicionadas_preto += 1

    def remover_peca(self, posicao):
        self.tabuleiro[posicao[0]][posicao[1]] = 0
        if self.jogador_ativo == 1:
            self.numero_de_pecas_preto -= 1
        else:
            self.numero_de_pecas_branco -= 1

    def mover_peca(self, posicao_inicial, posicao_final):
        self.tabuleiro[posicao_inicial[0]][posicao_inicial[1]] = 0
        self.tabuleiro[posicao_final[0]][posicao_final[1]] = self.jogador_ativo

    def peca_da_posicao(self, posicao):
        return self.tabuleiro[posicao[0]][posicao[1]]

    def executar_jogada(self, jogada):
        if jogada.tipo == 'ColocarPeca' and self.etapa == 0:
            self.colocar_peca(jogada.posicao)
            if self.pecas_posicionadas_preto == 9:
                self.etapa = 1
                self.ultima_etapa = self.etapa
        elif jogada.tipo == 'Movimentar' and self.etapa == 1:
            self.mover_peca(jogada.posicao, jogada.posicao_final)
        elif jogada.tipo == 'RemoverPeca' and self.etapa == 2:
            self.remover_peca(jogada.posicao)
            if self.numero_de_pecas_branco == 2:
                self.vencedor = -1
                self.game_over = True
            if self.numero_de_pecas_preto == 2:
                self.vencedor = 1
                self.game_over = True
            self.etapa = self.ultima_etapa

        houve_criacao_de_trilha = self.verificar_se_tem_trilha_nova()
        if houve_criacao_de_trilha:
            self.etapa = 2
        else:
            self.jogador_ativo = (-1) * self.jogador_ativo

    def verificar_se_tem_trilha_nova(self):
        numero_de_trilhas_atualizado = self.contar_trilhas_do_jogador_ativo()
        if self.jogador_ativo == 1:
            aux = self.trilhas_branco
            if numero_de_trilhas_atualizado != aux:
                # print("Branco tem {} trilha e tinha {} antes".format(numero_de_trilhas_atualizado, self.trilhas_branco))
                self.trilhas_branco = numero_de_trilhas_atualizado
                return numero_de_trilhas_atualizado > aux
        else:
            aux = self.trilhas_preto
            if numero_de_trilhas_atualizado != self.trilhas_preto:
                # print("Preto tem {} trilha e tinha {} antes".format(numero_de_trilhas_atualizado, self.trilhas_preto))
                self.trilhas_preto = numero_de_trilhas_atualizado
                return numero_de_trilhas_atualizado > aux
        return False

    def contar_trilhas_do_jogador_ativo(self):
        numero_de_trilhas = 0
        pecas_em_trilha = []
        for i in range(0, 8):
            soma = 0
            soma_last = 0
            for j in range(0, 8):
                if self.tabuleiro[i][j]:
                    soma += self.tabuleiro[i][j]
                if soma != soma_last:
                    soma_last = soma
            if soma == 3 * self.jogador_ativo:
                numero_de_trilhas += 1
                for j in range(0, 8):
                    if self.tabuleiro[i][j]:
                        pecas_em_trilha.append([i, j])
            soma = 0
            for j in range(0, 8):
                if self.tabuleiro[j][i]:
                    soma += self.tabuleiro[j][i]
            if soma == 3 * self.jogador_ativo:
                numero_de_trilhas += 1
                for j in range(0, 8):
                    if self.tabuleiro[j][i]:
                        pecas_em_trilha.append([j, i])
        if self.jogador_ativo == 1:
            self.pecas_branco_em_trilha = pecas_em_trilha
        else:
            self.pecas_preto_em_trilha = pecas_em_trilha
        return numero_de_trilhas

    def peca_em_trilha(self, posicao):
        for peca in self.pecas_branco_em_trilha:
            if peca[0] == posicao[0] and peca[1] == posicao[1]:
                return True
        for peca in self.pecas_preto_em_trilha:
            if peca[0] == posicao[0] and peca[1] == posicao[1]:
                return True
        return False

    def jogadas_validas(self):
        jogadas = []
        if self.etapa == 0:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.tabuleiro[i][j] == 0:
                        jogadas.append(Jogada([i, j], 'ColocarPeca'))
        if self.etapa == 1:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.tabuleiro[i][j] == self.jogador_ativo:
                        for adjacente in adj_list[i][j]:
                            if self.tabuleiro[adjacente[0]][adjacente[1]] == 0:
                                jogadas.append(Jogada([i, j], 'Movimentar', adjacente))
        if self.etapa == 2:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.tabuleiro[i][j] == -self.jogador_ativo:
                        jogadas.append(Jogada([i, j], 'RemoverPeca'))
        return jogadas


class Jogo:
    def __init__(self, window):
        self.width = window.get_width()
        self.height = window.get_height()
        self.window = window

        # Carregando as imagens do jogo.
        self.tabuleiro = pygame.image.load(os.path.join("Assets", "board.png"))
        self.tabuleiro = pygame.transform.scale(self.tabuleiro, (self.width, self.height))

        pecas = pygame.image.load(os.path.join("Assets", "pieces.png")).convert_alpha()

        self.branco = pygame.Surface((86, 86))
        self.preto = pygame.Surface((86, 86))
        self.branco_marcado = pygame.Surface((86, 86))
        self.preto_marcado = pygame.Surface((86, 86))

        self.branco.blit(pecas, (0, 0), (0, 0, 86, 86))
        self.branco = pygame.transform.scale(self.branco, (48, 48))

        self.preto.blit(pecas, (0, 0), (86, 0, 86, 86))
        self.preto = pygame.transform.scale(self.preto, (48, 48))

        self.branco_marcado.blit(pecas, (0, 0), (2*86, 0, 86, 86))
        self.branco_marcado = pygame.transform.scale(self.branco_marcado, (48, 48))

        self.preto_marcado.blit(pecas, (0, 0), (3*86, 0, 86, 86))
        self.preto_marcado = pygame.transform.scale(self.preto_marcado, (48, 48))

        self.play = True

        self.font = pygame.freetype.SysFont('Comic Sans MS', 12)

    def run(self):
        clock = pygame.time.Clock()
        trilha = Trilha()

        mouse_segurando_peca = False
        peca_segurada = [-1, -1]
        while self.play:
            self.window.blit(self.tabuleiro, [0, 0])
            if trilha.jogador_ativo == 1:
                textsurface, rect = self.font.render('Vez do Branco', (0, 0, 0))
                if trilha.etapa == 2:
                    textsurface2, rect = self.font.render('Branco come uma peça', (0, 0, 0))
                    self.window.blit(textsurface2, (480, 500))
            else:
                textsurface, rect = self.font.render('Vez do Preto', (0, 0, 0))
                if trilha.etapa == 2:
                    textsurface2, rect = self.font.render('Preto come uma peça', (0, 0, 0))
                    self.window.blit(textsurface2, (480, 500))
            self.window.blit(textsurface, (480, 540))

            clicou_posicao = False
            posicao = [-1, -1]
            jogada = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.play = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicou_posicao, posicao = verificar_posicao_do_mouse(pygame.mouse.get_pos())
                    if clicou_posicao:
                        if trilha.peca_da_posicao(posicao) == trilha.jogador_ativo and trilha.etapa == 1:
                            mouse_segurando_peca = True
                            peca_segurada = posicao
                        elif trilha.peca_da_posicao(posicao) == 0 and trilha.etapa == 0:
                            jogada = Jogada(posicao, 'ColocarPeca')
                        elif trilha.peca_da_posicao(posicao) == (-1)*trilha.jogador_ativo and trilha.etapa == 2 and not trilha.peca_em_trilha(posicao):
                            jogada = Jogada(posicao, 'RemoverPeca')

                if event.type == pygame.MOUSEBUTTONUP:
                    soltou_sobre_posicao, posicao_solta = verificar_posicao_do_mouse(pygame.mouse.get_pos())
                    if mouse_segurando_peca and soltou_sobre_posicao and trilha.peca_da_posicao(posicao_solta) == 0 and trilha.etapa == 1:
                        jogada = Jogada(peca_segurada, 'Movimentar', posicao_solta)
                    mouse_segurando_peca = False
                    peca_segurada = [-1, -1]

            if trilha.jogador_ativo == -1:
                start_time = time()
                jogada = calcular_movimento(trilha, 3, -1)
                end_time = time()
                time_taken = end_time - start_time  # time_taken is in seconds
                # print("Calculou em {} s".format(time_taken))
            if jogada and jogada.valida(trilha):
                trilha.executar_jogada(jogada)

            for i in range(0, 8):
                for j in range(0, 8):
                    if tabuleiro[i][j] and not (i == peca_segurada[0] and j == peca_segurada[1]):
                        self.mostrar_peca([i, j], tabuleiro[i][j], trilha.peca_em_trilha([i, j]))
            if mouse_segurando_peca:
                self.peca_segue_mouse(trilha.jogador_ativo)


            clock.tick(60)
            pygame.display.update()

    def mostrar_peca(self, pos, color, marcado=False):
        if color == 1:
            if marcado:
                self.window.blit(self.branco_marcado, [positions[pos[0]][pos[1]][0]-24, positions[pos[0]][pos[1]][1]-24])
            else:
                self.window.blit(self.branco,
                                 [positions[pos[0]][pos[1]][0] - 24, positions[pos[0]][pos[1]][1] - 24])
        elif color == -1:
            if marcado:
                self.window.blit(self.preto_marcado,
                                 [positions[pos[0]][pos[1]][0] - 24, positions[pos[0]][pos[1]][1] - 24])
            else:
                self.window.blit(self.preto,
                                 [positions[pos[0]][pos[1]][0] - 24, positions[pos[0]][pos[1]][1] - 24])

    def peca_segue_mouse(self, color):
        pos = pygame.mouse.get_pos()
        if color == 1:
            self.window.blit(self.branco, [pos[0] - 24, pos[1] - 24])
        elif color == -1:
            self.window.blit(self.preto, [pos[0] - 24, pos[1] - 24])


def dist(p, q):
    return np.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


def verificar_posicao_do_mouse(posicao_mouse):
    for i in range(0, 8):
        for j in range(0, 8):
            if positions[i][j]:
                if dist(posicao_mouse, positions[i][j]) <= 25:
                    return True, [i, j]
    return False, [-1, -1]


def verificar_jogadas_possiveis(trilha, jogador):
    posicoes_livres = []
    pecas_do_jogador = []
    for i in range(0, 8):
        for j in range(0, 8):
            if positions[i][j]:
                peca_da_posicao = trilha.peca_da_posicao([i, j])
                if peca_da_posicao == 0:
                    posicoes_livres.append([i,j])
                elif peca_da_posicao == jogador+1:
                    pecas_do_jogador.append([i,j])
