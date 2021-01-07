# Bibliotecas externas
import pygame                       # Biblioteca para a janela do jogo e evento de mouse.
import pygame.freetype              # Sub biblioteca para a fonte.
import os                           # Biblioteca para direcionamento do endereço dos arquivos.
import numpy as np                  # Biblioteca para utilizar sqrt()
import time

# Meu código
import minimax
import negamax
from trilha import *
from widgets import PushButton, Texto, Borda, Painel, Cor, ToggleButton


class Janela:
    MENU = 0
    JOGO = 1
    CONFIG = 2

    def __init__(self, botoes, paineis):
        self.botoes = botoes
        self.paineis = paineis
        self.contador_de_frames = 0
        self.completou_espera = False

    def mostrar(self, window):
        for botao in self.botoes.values():
            botao.mostrar(window)
        for painel in self.paineis.values():
            painel.mostrar(window)
        if not self.completou_espera:
            self.contador_de_frames += 1
            if self.contador_de_frames == 3:
                self.completou_espera = True


# Classe do manager do Jogo.
class Jogo:
    def __init__(self, window):
        self.width = window.get_width()
        self.height = window.get_height()
        self.window = window

        self.rodando = True
        self.pausado = False

        self.jogada = None
        self.trilha = Trilha()

        self.janela_ativa = Janela.MENU
        self.mouse_segurando_peca = False
        self.peca_segurada = [-1, -1]

        for i in range(0, 8):
            for j in range(0, 8):
                if positions[i][j]:
                    positions[i][j] = [int(positions[i][j][0]*5/6+50), int(positions[i][j][1]*5/6+50)]


        # Carregando as imagens do jogo.
        self.pecas = self.carregar_imagens_das_pecas()
        painel_cinza = pygame.image.load(os.path.join("Assets", "grey_panel.png")).convert_alpha()

        self.fundo = pygame.image.load(os.path.join("Assets", 'background.png'))
        self.fundo = pygame.transform.scale(self.fundo, (self.width, self.height))

        self.tabuleiro = pygame.image.load(os.path.join("Assets", "board.png"))
        self.tabuleiro = pygame.transform.scale(self.tabuleiro, (int(self.width*5/6), int(self.height*5/6)))

        botao_cinza = [
            pygame.image.load(os.path.join("Assets", "grey_button.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "grey_button_pushed.png")).convert_alpha()
        ]

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
        botao_esquerda = [
            pygame.image.load(os.path.join("Assets", "grey_slider_left.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "grey_slider_left_pushed.png")).convert_alpha()
        ]
        botao_direita = [
            pygame.image.load(os.path.join("Assets", "grey_slider_right.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "grey_slider_right_pushed.png")).convert_alpha()
        ]
        botao_up = [
            pygame.image.load(os.path.join("Assets", "grey_slider_up.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "grey_slider_up_pushed.png")).convert_alpha()
        ]
        botao_down = [
            pygame.image.load(os.path.join("Assets", "grey_slider_down.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "grey_slider_down_pushed.png")).convert_alpha()
        ]
        botao_cor = [
            pygame.image.load(os.path.join("Assets", "white_button.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "black_button.png")).convert_alpha()
        ]


        # Cria a fonte do jogo.
        self.font = pygame.freetype.SysFont('Comic Sans MS', 18)

        # Cria os botões
        botoes_janela_jogo = {
            'Pause': PushButton([5, 5], 40, botao_pause),
            'Fechar': PushButton([600 - 5 - 40, 5], 40, botao_fechar),
            'Play': PushButton([5, 5], 40, botao_play),
        }
        botoes_janela_principal = {
            'Fechar': PushButton([600 - 5 - 40, 5], 40, botao_fechar),
            'JogarAI': PushButton([self.width / 2 - 75, self.height / 2 - 80], [150, 40], botao_cinza,
                                  texto=Texto('vs AI', 18, Cor.PRETO)),
            'JogarPlayer': PushButton([self.width / 2 - 75, self.height / 2], [150, 40], botao_cinza, texto=Texto('vs  Jogador', 18, Cor.PRETO))
        }

        botoes_janela_config = {
            'Fechar': PushButton([600 - 5 - 40, 5], 40, botao_fechar),
            'Cor': ToggleButton([self.width / 2 + 65, self.height / 2 - 75], [30, 30], botao_cor),
            'Voltar': PushButton([40, 33], [39, 31], botao_esquerda),
            'Aumentar': PushButton([self.width / 2 + 30, self.height / 2 + 5], [int(31*0.75), int(39*0.75)], botao_up),
            'Diminuir': PushButton([self.width / 2 + 107, self.height / 2 + 5], [int(31*0.75), int(39*0.75)], botao_down),
            'Play': PushButton([self.width / 2 - 75, self.height / 2 +80], [150, 40], botao_cinza, texto=Texto('JOGAR', 18, Cor.PRETO))
        }

        botoes_janela_principal['Fechar'].conectar_acao(self.fechar_jogo)
        botoes_janela_principal['JogarAI'].conectar_acao(self.mudar_janela, Janela.CONFIG)
        botoes_janela_principal['JogarPlayer'].conectar_acao(self.iniciar_jogo, )

        botoes_janela_jogo['Fechar'].conectar_acao(self.fechar_jogo)
        botoes_janela_jogo['Pause'].conectar_acao(self.pausar_jogo)
        botoes_janela_jogo['Play'].conectar_acao(self.despausar_jogo)
        botoes_janela_jogo['Pause'].desativar()
        botoes_janela_jogo['Play'].desativar()

        botoes_janela_config['Fechar'].conectar_acao(self.fechar_jogo)
        botoes_janela_config['Voltar'].conectar_acao(self.mudar_janela, Janela.MENU)
        botoes_janela_config['Aumentar'].conectar_acao(self.mudar_nivel_da_AI, 1)
        botoes_janela_config['Diminuir'].conectar_acao(self.mudar_nivel_da_AI, -1)
        botoes_janela_config['Play'].conectar_acao(self.iniciar_jogo, True)

        paineis_janela_principal = {
            'Titulo': Painel([self.width/2 - 100, 30], [200, 40], painel_cinza, Borda(0, Cor.PRETO), Texto('Trilha', 20, Cor.PRETO))
        }

        paineis_janela_jogo = {
            'Jogada': Painel([self.width / 2 - 100, 10], [200, 30], painel_cinza, Borda(0, Cor.PRETO), Texto('Vez do Branco', 18, Cor.PRETO))
        }

        paineis_janela_config = {
            'Titulo': Painel([self.width / 2 - 100, 30], [200, 40], painel_cinza, Borda(0, Cor.PRETO), Texto('Trilha', 20, Cor.PRETO)),
            'Cor': Painel([self.width / 2 - 165, self.height / 2 - 80], [175, 40], painel_cinza, Borda(0, Cor.PRETO), Texto('Escolha sua cor:', 20, Cor.PRETO)),
            'Msg': Painel([self.width / 2 - 165, self.height / 2], [175, 40], painel_cinza, Borda(0, Cor.PRETO), Texto('Nível da AI:', 20, Cor.PRETO)),
            'Nivel': Painel([self.width / 2 + 65, self.height / 2 + 5], [30, 30], painel_cinza, Borda(0, Cor.PRETO), Texto('1', 20, Cor.PRETO))
        }

        self.janela = [
            Janela(botoes_janela_principal, paineis_janela_principal),
            Janela(botoes_janela_jogo, paineis_janela_jogo),
            Janela(botoes_janela_config, paineis_janela_config)
        ]

        self.texto_etapa_2 = ['Preto come uma peça', 'Branco come uma peça']
        self.texto_normal = ['Vez do Preto', 'Vez do Branco']
        self.texto_fim = ['Preto Venceu!', 'Branco Venceu!']

        self.profundidade = 1
        self.jogando_contra_AI = None
        self.cor_escolhida = Jogador.BRANCO

    def rodar(self):
        timer = pygame.time.Clock()
        while self.rodando:
            self.event_handler()

            if self.janela_ativa == Janela.MENU:
                self.menu()
            elif self.janela_ativa == Janela.JOGO:
                self.jogo()
            elif self.janela_ativa == Janela.CONFIG:
                self.config()

            self.janela[self.janela_ativa].mostrar(self.window)

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

    def menu(self):
        self.window.blit(self.fundo, [0, 0])

    def config(self):
        self.window.blit(self.fundo, [0, 0])

    def event_handler(self):
        self.jogada = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for botao in self.janela[self.janela_ativa].botoes.values():
                    botao.detectar_click(pygame.mouse.get_pos())
                if not self.pausado and self.janela_ativa == Janela.JOGO and self.janela[Janela.JOGO].completou_espera:
                    clicou_posicao, posicao = verificar_posicao_do_mouse(pygame.mouse.get_pos())
                    if clicou_posicao and (not self.jogando_contra_AI or self.trilha.jogador_ativo == self.cor_escolhida):
                        if self.trilha.peca_da_posicao(posicao) == self.trilha.jogador_ativo and self.trilha.etapa == 1:
                            self.mouse_segurando_peca = True
                            self.peca_segurada = posicao
                        elif self.trilha.peca_da_posicao(posicao) == 0 and self.trilha.etapa == 0:
                            self.jogada = Jogada(posicao, 'ColocarPeca')
                        elif self.trilha.peca_da_posicao(posicao) == (-1) * self.trilha.jogador_ativo and self.trilha.etapa == 2 and not self.trilha.peca_em_trilha(posicao):
                            self.jogada = Jogada(posicao, 'RemoverPeca')

            if event.type == pygame.MOUSEBUTTONUP:
                soltou_sobre_posicao, posicao_solta = verificar_posicao_do_mouse(pygame.mouse.get_pos())
                if self.mouse_segurando_peca and soltou_sobre_posicao and self.trilha.peca_da_posicao(
                        posicao_solta) == 0 and self.trilha.etapa == 1:
                    self.jogada = Jogada(self.peca_segurada, 'Movimentar', posicao_solta)
                self.mouse_segurando_peca = False
                self.peca_segurada = [-1, -1]

    def mudar_janela(self, janela):
        self.janela_ativa = janela

    def iniciar_jogo(self, contra_AI=False):
        self.jogando_contra_AI = contra_AI
        self.janela_ativa = Janela.JOGO
        if self.jogando_contra_AI:
            if self.janela[Janela.CONFIG].botoes['Cor'].estado:
                self.cor_escolhida = Jogador.PRETO
            else:
                self.cor_escolhida = Jogador.BRANCO

    def mudar_nivel_da_AI(self, dif):
        if 1 <= self.profundidade + dif <= 7:
            self.profundidade = self.profundidade + dif
            self.janela[Janela.CONFIG].paineis['Nivel'].escrever(str(self.profundidade))

    def jogo(self):
        self.window.blit(self.fundo, [0, 0])
        pygame.draw.rect(self.window, (0, 0, 0), (43, 43, 514, 514))
        pygame.draw.rect(self.window, (255, 255, 255), (44, 44, 512, 512))
        self.window.blit(self.tabuleiro, [50, 50])

        if self.trilha.game_over:
            self.janela[Janela.JOGO].paineis['Jogada'].escrever(self.texto_fim[self.trilha.indice(self.trilha.vencedor)])
        elif self.trilha.etapa == 2:
            self.janela[Janela.JOGO].paineis['Jogada'].escrever(self.texto_etapa_2[self.trilha.indice(self.trilha.jogador_ativo)])
        else:
            self.janela[Janela.JOGO].paineis['Jogada'].escrever(self.texto_normal[self.trilha.indice(self.trilha.jogador_ativo)])

        # Caso seja a vez da AI, calcula sua jogada.
        if not self.trilha.game_over:
            if self.trilha.jogador_ativo == -self.cor_escolhida and self.jogando_contra_AI:
                self.jogada = negamax.calcular_movimento(self.trilha, 5, -self.cor_escolhida)

            # Executa a jogada, seja da AI ou do jogador.
            if self.jogada and self.jogada.valida(self.trilha):
                self.trilha.executar_jogada(self.jogada)

        # Prepara o display das peças.
        for i in range(0, 8):
            for j in range(0, 8):
                if tabuleiro[i][j] and not (i == self.peca_segurada[0] and j == self.peca_segurada[1]):
                    self.mostrar_peca([i, j], tabuleiro[i][j], self.trilha.peca_em_trilha([i, j]))
        if self.mouse_segurando_peca:
            self.peca_segue_mouse(self.trilha.jogador_ativo)

    def pausar_jogo(self):
        self.pausado = True
        self.botoes['Pause'].desativar()
        self.botoes['Play'].ativar()

    def despausar_jogo(self):
        self.pausado = False
        self.botoes['Play'].desativar()
        self.botoes['Pause'].ativar()

    def fechar_jogo(self):
        self.rodando = False

    @staticmethod
    def carregar_imagens_das_pecas():
        sprite_sheet = pygame.image.load(os.path.join("Assets", "pieces_transparent.png")).convert_alpha()

        # Separa a imagem das peças em quatro peças.
        pecas = [
            {'Normal': pygame.Surface((86, 86), pygame.SRCALPHA, 32), 'Marcado': pygame.Surface((86, 86), pygame.SRCALPHA, 32)},
            {'Normal': pygame.Surface((86, 86), pygame.SRCALPHA, 32), 'Marcado': pygame.Surface((86, 86), pygame.SRCALPHA, 32)}
        ]
        pecas[Trilha.indice(Jogador.BRANCO)]['Normal'].blit(sprite_sheet, (0, 0), (0, 0, 86, 86))
        pecas[Trilha.indice(Jogador.PRETO)]['Normal'].blit(sprite_sheet, (0, 0), (86, 0, 86, 86))
        pecas[Trilha.indice(Jogador.BRANCO)]['Marcado'].blit(sprite_sheet, (0, 0), (2*86, 0, 86, 86))
        pecas[Trilha.indice(Jogador.PRETO)]['Marcado'].blit(sprite_sheet, (0, 0), (3*86, 0, 86, 86))

        for jogador in range(0, 2):
            for nome in pecas[jogador]:
                pecas[jogador][nome] = pygame.transform.scale(pecas[jogador][nome], (48, 48))
        return pecas

def verificar_posicao_do_mouse(posicao_mouse):
    for i in range(0, 8):
        for j in range(0, 8):
            if positions[i][j]:
                if quadratura(posicao_mouse, positions[i][j]) <= 25**2:
                    return True, [i, j]
    return False, [-1, -1]


def quadratura(p, q):
    return (p[0]-q[0])**2+(p[1]-q[1])**2

