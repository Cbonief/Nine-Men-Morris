# Bibliotecas externas
import pygame                       # Biblioteca para a janela do jogo e evento de mouse.
import pygame.freetype              # Sub biblioteca para a fonte.
import os                           # Biblioteca para direcionamento do endereço dos arquivos.
import numpy as np                  # Biblioteca para utilizar sqrt()
import time

# Meu código
from minimax import *
from trilha import *


# Classe do botão
class Botao:
    def __init__(self, posicao, tamanho, imagens, tipo='Circular', frames_apertados=5, texto=None):
        self.ativo = True
        self.funcao = None
        self.texto = None
        self.tamanho = tamanho
        self.posicao = posicao
        self.imagens = []
        for imagem in imagens:
            if tipo == 'Retangular':
                self.imagens.append(pygame.transform.scale(imagem, self.tamanho))
            else:
                self.imagens.append(pygame.transform.scale(imagem, [self.tamanho, self.tamanho]))
        self.foi_apertado = False
        self.tipo = 'Circular'
        self.frames_apertados = frames_apertados
        self.contador_de_frame = 0
        self.atividade_modificada = False

    def conectar_acao(self, funcao):
        self.funcao = funcao

    def detectar_click(self, posicao_do_mouse):
        if self.ativo and not self.atividade_modificada:
            if self.tipo == 'Retangular':
                if self.posicao[0] <= posicao_do_mouse[0] <= self.posicao[0] + self.tamanho[0] and self.posicao[1] <= \
                        posicao_do_mouse[1] <= self.posicao[1] + self.tamanho[1]:
                    self.foi_apertado = True
                    self.funcao()
            else:
                if dist(posicao_do_mouse, self.posicao) <= self.tamanho:
                    self.foi_apertado = True
                    self.funcao()

    def mostrar(self, window):
        if self.ativo:
            if self.foi_apertado:
                window.blit(self.imagens[1], self.posicao)
                self.contador_de_frame += 1
                if self.contador_de_frame == self.frames_apertados:
                    self.contador_de_frame = 0
                    self.foi_apertado = False
            else:
                window.blit(self.imagens[0], self.posicao)
            if self.atividade_modificada:
                self.contador_de_frame += 1
                if self.contador_de_frame == 1:
                    self.contador_de_frame = 0
                    self.atividade_modificada = False

    def desativar(self):
        self.ativo = False
        self.atividade_modificada = True

    def ativar(self):
        self.ativo = True
        self.atividade_modificada = True


# Classe do manager do Jogo.
class Jogo:
    def __init__(self, window):
        self.width = window.get_width()
        self.height = window.get_height()
        self.window = window

        for i in range(0, 8):
            for j in range(0, 8):
                if positions[i][j]:
                    positions[i][j] = [int(positions[i][j][0]*5/6+50), int(positions[i][j][1]*5/6+50)]

        # Carregando as imagens do jogo.
        self.fundo = pygame.image.load(os.path.join("Assets", 'background.png'))
        self.fundo = pygame.transform.scale(self.fundo, (self.width, self.height))

        self.tabuleiro = pygame.image.load(os.path.join("Assets", "board.png"))
        self.tabuleiro = pygame.transform.scale(self.tabuleiro, (int(self.width*5/6), int(self.height*5/6)))

        botao_pause = [
            pygame.image.load(os.path.join("Assets", "pausar_idle.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "pausar_apertado.png")).convert_alpha()
        ]
        botao_fechar = [
            pygame.image.load(os.path.join("Assets", "fechar_idle.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "fechar_apertado.png")).convert_alpha()
        ]
        botao_play = [
            pygame.image.load(os.path.join("Assets", "play_idle.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "play_apertado.png")).convert_alpha()
        ]

        pecas = pygame.image.load(os.path.join("Assets", "pieces_transparent.png")).convert_alpha()

        # Separa a imagem das peças em quatro peças.
        self.pecas = [
            {'Normal': pygame.Surface((86, 86), pygame.SRCALPHA, 32), 'Marcado': pygame.Surface((86, 86), pygame.SRCALPHA, 32)},
            {'Normal': pygame.Surface((86, 86), pygame.SRCALPHA, 32), 'Marcado': pygame.Surface((86, 86), pygame.SRCALPHA, 32)}
        ]
        self.pecas[Trilha.indice(Jogador.BRANCO)]['Normal'].blit(pecas, (0, 0), (0, 0, 86, 86))
        self.pecas[Trilha.indice(Jogador.PRETO)]['Normal'].blit(pecas, (0, 0), (86, 0, 86, 86))
        self.pecas[Trilha.indice(Jogador.BRANCO)]['Marcado'].blit(pecas, (0, 0), (2*86, 0, 86, 86))
        self.pecas[Trilha.indice(Jogador.PRETO)]['Marcado'].blit(pecas, (0, 0), (3*86, 0, 86, 86))

        for jogador in range(0, 2):
            for nome in self.pecas[jogador]:
                self.pecas[jogador][nome] = pygame.transform.scale(self.pecas[jogador][nome], (48, 48))

        self.jogando = True
        self.pausado = False

        # Cria a fonte do jogo.
        self.font = pygame.freetype.SysFont('Comic Sans MS', 18)

        # Cria os botões
        self.botoes = {
            'Pause': Botao([5, 5], 40, botao_pause),
            'Fechar': Botao([600-5-40, 5], 40, botao_fechar),
            'Play': Botao([5, 5], 40, botao_play)
        }
        self.botoes['Pause'].conectar_acao(self.pausar_jogo)
        self.botoes['Fechar'].conectar_acao(self.fechar_jogo)
        self.botoes['Play'].conectar_acao(self.despausar_jogo)
        self.botoes['Play'].desativar()

    def jogar(self):
        timer = pygame.time.Clock()
        trilha = Trilha()

        mouse_segurando_peca = False
        peca_segurada = [-1, -1]

        texto_etapa_2 = ['Preto come uma peça', 'Branco come uma peça']
        texto_normal = ['Vez do Preto', 'Vez do Branco']
        texto_fim = ['Preto Venceu!', 'Branco Venceu!']
        deslocamento_texto_normal = [[], [], []]
        while self.jogando:
            self.window.blit(self.fundo, [0, 0])
            pygame.draw.rect(self.window, (0, 0, 0), (43, 43, 514, 514))
            pygame.draw.rect(self.window, (255, 255, 255), (44, 44, 512, 512))
            self.window.blit(self.tabuleiro, [50, 50])

            # Display dos textos.
            pygame.draw.rect(self.window, (0, 0, 0), (199, 7, 202, 32))
            pygame.draw.rect(self.window, (255, 255, 255), (200, 8, 200, 30))

            if trilha.game_over:
                renderizador_do_texto, _ = self.font.render(texto_fim[trilha.indice(trilha.vencedor)], (0, 0, 0))
            elif trilha.etapa == 2:
                renderizador_do_texto, _ = self.font.render(texto_etapa_2[trilha.indice(trilha.jogador_ativo)], (0, 0, 0))
            else:
                renderizador_do_texto, _ = self.font.render(texto_normal[trilha.indice(trilha.jogador_ativo)], (0, 0, 0))
            rect = renderizador_do_texto.get_rect(center=(self.width // 2, 24))
            self.window.blit(renderizador_do_texto, rect)

            jogada = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.jogando = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for botao in self.botoes.values():
                        botao.detectar_click(pygame.mouse.get_pos())
                    if not self.pausado:
                        clicou_posicao, posicao = verificar_posicao_do_mouse(pygame.mouse.get_pos())
                        if clicou_posicao and trilha.jogador_ativo == 1:
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

            # Caso seja a vez da AI, calcula sua jogada.
            if not trilha.game_over:
                if trilha.jogador_ativo == Jogador.PRETO:
                    jogada = calcular_movimento(trilha, 3, Jogador.PRETO)

                # Executa a jogada, seja da AI ou do jogador.
                if jogada and jogada.valida(trilha):
                    trilha.executar_jogada(jogada)

            # Prepara o display das peças.
            for i in range(0, 8):
                for j in range(0, 8):
                    if tabuleiro[i][j] and not (i == peca_segurada[0] and j == peca_segurada[1]):
                        self.mostrar_peca([i, j], tabuleiro[i][j], trilha.peca_em_trilha([i, j]))
            if mouse_segurando_peca:
                self.peca_segue_mouse(trilha.jogador_ativo)
            for botao in self.botoes.values():
                botao.mostrar(self.window)

            # Atualiza o display e seta o frame-rate.
            timer.tick(60)
            pygame.display.update()

    def mostrar_peca(self, pos, jogador, marcado=False):
        if marcado:
            self.window.blit(self.pecas[Trilha.indice(jogador)]['Marcado'], [positions[pos[0]][pos[1]][0] - 24, positions[pos[0]][pos[1]][1] - 24])
        else:
            self.window.blit(self.pecas[Trilha.indice(jogador)]['Normal'], [positions[pos[0]][pos[1]][0] - 24, positions[pos[0]][pos[1]][1] - 24])

    def peca_segue_mouse(self, jogador):
        pos = pygame.mouse.get_pos()
        self.window.blit(self.pecas[Trilha.indice(jogador)]['Normal'], [pos[0] - 24, pos[1] - 24])

    def menu_inicial(self):
        x=2

    def pausar_jogo(self):
        self.pausado = True
        self.botoes['Pause'].desativar()
        self.botoes['Play'].ativar()

    def despausar_jogo(self):
        self.pausado = False
        self.botoes['Play'].desativar()
        self.botoes['Pause'].ativar()

    def fechar_jogo(self):
        self.jogando = False


def dist(p, q):
    return np.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


def verificar_posicao_do_mouse(posicao_mouse):
    for i in range(0, 8):
        for j in range(0, 8):
            if positions[i][j]:
                if dist(posicao_mouse, positions[i][j]) <= 25:
                    return True, [i, j]
    return False, [-1, -1]


