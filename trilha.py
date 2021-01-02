from Assets.piece_positions import *
import numpy as np


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
        elif self.tipo == 'ColocarPeca':
            return Jogada(self.posicao, 'ColocarPeca')
        elif self.tipo == 'RemoverPeca':
            return Jogada(self.posicao, 'RemoverPeca')

    def valida(self, trilha):
        if self.tipo == 'RemoverPeca':
            return trilha.tabuleiro[self.posicao[0]][self.posicao[1]] == -trilha.jogador_ativo
        elif self.tipo == 'ColocarPeca':
            return trilha.tabuleiro[self.posicao[0]][self.posicao[1]] == 0
        else:
            if trilha.jogar_voando[trilha.indice(trilha.jogador_ativo)]:
                return trilha.tabuleiro[self.posicao_final[0]][self.posicao_final[1]] == 0
            else:
                return trilha.tabuleiro[self.posicao_final[0]][self.posicao_final[1]] == 0 and posicao_adjacente(self.posicao, self.posicao_final)

    def __repr__(self):
        if self.tipo == 'RemoverPeca':
            return 'Remover Peça da posição {}'.format(self.posicao)
        elif self.tipo == 'ColocarPeca':
            return 'Colocar Peça na Posição {}'.format(self.posicao)
        else:
            return 'Mover a Peça da Posição {} para {}'.format(self.posicao, self.posicao_final)


class Jogador:
    BRANCO = 1
    PRETO = -1


class Trilha:
    def __init__(self):
        self.tabuleiro = tabuleiro
        self.etapa = 0                      #0 - Colocacao; 1 - Movimentacao, 2 - Remocao, 3 - Voando
        self.jogador_ativo = 1
        self.numero_de_pecas = np.array([0, 0])
        self.pecas_posicionadas = np.array([0, 0])
        self.pecas_em_trilha = [[], []]
        self.trilhas = [[], []]
        self.ultima_etapa = 0
        self.vencedor = 0
        self.jogar_voando = [False, False]
        self.game_over = False
        self.ultima_jogada = None

    @staticmethod
    def indice(jogador):
        return int((jogador+1)/2)

    def colocar_peca(self, posicao):
        if self.peca_da_posicao(posicao) == 0:
            self.tabuleiro[posicao[0]][posicao[1]] = self.jogador_ativo
            self.numero_de_pecas[self.indice(self.jogador_ativo)] += 1
            self.pecas_posicionadas[self.indice(self.jogador_ativo)] += 1

    def remover_peca(self, posicao):
        self.tabuleiro[posicao[0]][posicao[1]] = 0
        self.numero_de_pecas[self.indice((-1)*self.jogador_ativo)] -= 1

    def mover_peca(self, posicao_inicial, posicao_final):
        self.tabuleiro[posicao_inicial[0]][posicao_inicial[1]] = 0
        self.tabuleiro[posicao_final[0]][posicao_final[1]] = self.jogador_ativo

    def peca_da_posicao(self, posicao):
        return self.tabuleiro[posicao[0]][posicao[1]]

    def executar_jogada(self, jogada):
        self.ultima_jogada = jogada
        if jogada.tipo == 'ColocarPeca' and self.etapa == 0:
            self.colocar_peca(jogada.posicao)
            if self.pecas_posicionadas[0] == 9:
                self.etapa = 1
                self.ultima_etapa = 1
        elif jogada.tipo == 'Movimentar' and self.etapa == 1:
            self.mover_peca(jogada.posicao, jogada.posicao_final)
        elif jogada.tipo == 'RemoverPeca' and self.etapa == 2:
            self.remover_peca(jogada.posicao)
            if self.ultima_etapa == 1:
                if self.numero_de_pecas[self.indice((-1)*self.jogador_ativo)] == 2:
                    self.vencedor = self.jogador_ativo
                    self.game_over = True
                elif self.numero_de_pecas[self.indice((-1)*self.jogador_ativo)] == 3:
                    self.jogar_voando[self.indice((-1)*self.jogador_ativo)] = True
                    print("Jogador voando")
            self.etapa = self.ultima_etapa

        if len(self.jogadas_validas((-1)*self.jogador_ativo)) == 0:
            self.game_over = True
            self.vencedor = self.jogador_ativo
        trilha_nova = self.verificar_se_tem_trilha_nova()
        if trilha_nova:
            self.etapa = 2
            if len(self.jogadas_validas((-1)*self.jogador_ativo)) == 0:
                self.etapa = self.ultima_etapa
        else:
            self.jogador_ativo = (-1) * self.jogador_ativo

    def verificar_se_tem_trilha_nova(self):
        foi_criado_trilha = False
        pecas_em_trilha, trilhas = self.contar_trilhas_do_jogador_ativo()

        self.pecas_em_trilha[self.indice(self.jogador_ativo)] = pecas_em_trilha
        for trilha in trilhas:
            if trilha not in self.trilhas[self.indice(self.jogador_ativo)]:
                foi_criado_trilha = True
        self.trilhas[self.indice(self.jogador_ativo)] = trilhas
        return foi_criado_trilha

    def contar_trilhas_do_jogador_ativo(self):
        pecas_em_trilha = []
        trilhas = []
        for i in range(0, 8):
            soma = 0
            soma_last = 0
            for j in range(0, 8):
                if self.tabuleiro[i][j]:
                    soma += self.tabuleiro[i][j]
                if soma != soma_last:
                    soma_last = soma
            if soma == 3 * self.jogador_ativo:
                for j in range(0, 8):
                    if self.tabuleiro[i][j]:
                        pecas_em_trilha.append([i, j])
                trilhas.append(10*i)
            soma = 0
            for j in range(0, 8):
                if self.tabuleiro[j][i]:
                    soma += self.tabuleiro[j][i]
            if soma == 3 * self.jogador_ativo:
                for j in range(0, 8):
                    if self.tabuleiro[j][i]:
                        pecas_em_trilha.append([j, i])
                trilhas.append(i)
        return pecas_em_trilha, trilhas

    def peca_em_trilha(self, posicao):
        for peca in self.pecas_em_trilha[self.indice(Jogador.PRETO)]:
            if peca[0] == posicao[0] and peca[1] == posicao[1]:
                return True
        for peca in self.pecas_em_trilha[self.indice(Jogador.BRANCO)]:
            if peca[0] == posicao[0] and peca[1] == posicao[1]:
                return True
        return False

    def jogadas_validas(self, jogador):
        jogadas = []
        if self.etapa == 0:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.tabuleiro[i][j] == 0:
                        jogadas.append(Jogada([i, j], 'ColocarPeca'))
        if self.etapa == 1:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.tabuleiro[i][j] == jogador:
                        if self.jogar_voando[self.indice(jogador)]:
                            for ii in range(0, 8):
                                for jj in range(0, 8):
                                    if self.tabuleiro[ii][jj] == 0:
                                        jogadas.append(Jogada([i, j], 'Movimentar', [ii, jj]))
                        else:
                            for adjacente in adj_list[i][j]:
                                if self.tabuleiro[adjacente[0]][adjacente[1]] == 0:
                                    jogadas.append(Jogada([i, j], 'Movimentar', adjacente))
        if self.etapa == 2:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.tabuleiro[i][j] == (-1)*jogador and not self.peca_em_trilha([i, j]):
                        jogadas.append(Jogada([i, j], 'RemoverPeca'))
        return jogadas

