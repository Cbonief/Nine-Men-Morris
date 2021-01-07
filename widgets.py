import pygame
import pygame.freetype
import pygame

pygame.freetype.init()


class Cor:
    PRETO = (0, 0, 0)


class Borda:
    def __init__(self, grossura, cor):
        self.grossura = grossura
        self.cor = cor
        self.vertices = None


class Texto:
    def __init__(self, text, pt, cor, font='Comic Sans MS'):
        self.txt = text
        self.pt = pt
        self.cor = cor
        self.font = pygame.freetype.SysFont(font, pt)


def quadratura(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


class ToggleButton:
    def __init__(self, posicao, tamanho, imagens, texto=None):
        self.visivel = True
        self.clickavel = True
        self.funcao = None
        self.texto = texto
        tipo = 'Circular'
        if type(tamanho) != int:
            tipo = 'Retangular'
        self.tamanho = tamanho
        self.posicao = posicao
        self.imagens = []
        for imagem in imagens:
            if tipo == 'Retangular':
                self.imagens.append(pygame.transform.scale(imagem, self.tamanho))
            else:
                self.imagens.append(pygame.transform.scale(imagem, [self.tamanho, self.tamanho]))
        self.estado = False
        self.tipo = tipo
        self.contador_de_frame = 0
        self.atividade_modificada = False

    def conectar_acao(self, funcao):
        self.funcao = funcao

    def detectar_click(self, posicao_do_mouse):
        if self.clickavel and not self.atividade_modificada:
            if self.tipo == 'Retangular':
                if self.posicao[0] <= posicao_do_mouse[0] <= self.posicao[0] + self.tamanho[0] and self.posicao[1] <= posicao_do_mouse[1] <= self.posicao[1] + self.tamanho[1]:
                    self.estado = not self.estado
                    if self.funcao:
                        self.funcao()
            else:
                if quadratura(posicao_do_mouse, self.posicao) <= self.tamanho**2:
                    self.estado = not self.estado
                    if self.funcao:
                        self.funcao()

    def mostrar(self, window):
        if self.visivel:
            if self.estado:
                window.blit(self.imagens[1], self.posicao)
            else:
                window.blit(self.imagens[0], self.posicao)
            if self.atividade_modificada:
                self.contador_de_frame += 1
                if self.contador_de_frame == 1:
                    self.contador_de_frame = 0
                    self.atividade_modificada = False
            if self.texto:
                renderizador_do_texto, _ = self.texto.font.render(self.texto.txt, self.texto.cor)
                rect = renderizador_do_texto.get_rect(
                    center=(self.posicao[0] + self.tamanho[0] // 2, self.posicao[1] + self.tamanho[1] / 2))
                window.blit(renderizador_do_texto, rect)

    def desativar(self):
        self.clickavel = False
        self.visivel = False
        self.atividade_modificada = True

    def ativar(self):
        self.clickavel = True
        self.visivel = True
        self.atividade_modificada = True

    def desativar_click(self):
        self.clickavel = False

    def ativar_click(self):
        self.clickavel = True


# Classe do botão
class PushButton:
    def __init__(self, posicao, tamanho, imagens, frames_apertados=5, texto=None):
        self.visivel = True
        self.clickavel = True
        self.funcao = None
        self.texto = texto
        tipo = 'Circular'
        if type(tamanho) != int:
            tipo = 'Retangular'
        self.tamanho = tamanho
        self.posicao = posicao
        self.imagens = []
        for imagem in imagens:
            if tipo == 'Retangular':
                self.imagens.append(pygame.transform.scale(imagem, self.tamanho))
            else:
                self.imagens.append(pygame.transform.scale(imagem, [self.tamanho, self.tamanho]))
        self.foi_apertado = False
        self.tipo = tipo
        self.frames_apertados = frames_apertados
        self.contador_de_frame = 0
        self.atividade_modificada = False
        self.args = None

    def conectar_acao(self, funcao, args=None):
        self.funcao = funcao
        self.args = args

    def detectar_click(self, posicao_do_mouse):
        if self.clickavel and not self.atividade_modificada:
            if self.tipo == 'Retangular':
                if self.posicao[0] <= posicao_do_mouse[0] <= self.posicao[0] + self.tamanho[0] and self.posicao[1] <= \
                        posicao_do_mouse[1] <= self.posicao[1] + self.tamanho[1]:
                    self.foi_apertado = True
            else:
                if quadratura(posicao_do_mouse, self.posicao) <= self.tamanho**2:
                    self.foi_apertado = True

    def acionar_funcao(self):
        print("Botao do argumento {}".format(self.args))
        if self.funcao:
            if self.args is not None:
                self.funcao(self.args)
            else:
                self.funcao()


    def mostrar(self, window):
        if self.visivel:
            if self.foi_apertado:
                window.blit(self.imagens[1], self.posicao)
                self.contador_de_frame += 1
                if self.contador_de_frame == self.frames_apertados:
                    self.contador_de_frame = 0
                    self.acionar_funcao()
                    self.foi_apertado = False
            else:
                window.blit(self.imagens[0], self.posicao)
            if self.atividade_modificada:
                self.contador_de_frame += 1
                if self.contador_de_frame == 1:
                    self.contador_de_frame = 0
                    self.atividade_modificada = False
            if self.texto:
                renderizador_do_texto, _ = self.texto.font.render(self.texto.txt, self.texto.cor)
                rect = renderizador_do_texto.get_rect(
                    center=(self.posicao[0] + self.tamanho[0] // 2, self.posicao[1] + self.tamanho[1] / 2))
                window.blit(renderizador_do_texto, rect)

    def desativar(self):
        self.clickavel = False
        self.visivel = False
        self.atividade_modificada = True

    def ativar(self):
        self.clickavel = True
        self.visivel = True
        self.atividade_modificada = True

    def desativar_click(self):
        self.clickavel = False

    def ativar_click(self):
        self.clickavel = True


class Painel:
    def __init__(self, posicao, tamanho, imagem, borda=Borda(0, (0, 0, 0)), texto=Texto('None', 0, Cor.PRETO)):
        self.ativo = True
        self.texto = texto
        self.tamanho = tamanho
        self.posicao = posicao
        self.imagem = pygame.transform.scale(imagem, self.tamanho)
        self.borda = borda
        self.borda.vertices = (self.posicao[0]-borda.grossura, self.posicao[1]-borda.grossura, self.tamanho[0]+borda.grossura, self.tamanho[1]+borda.grossura)

    def mostrar(self, window):
        if self.ativo:
            if self.borda.grossura != 0:
                pygame.draw.rect(window, self.borda.cor, self.borda.vertices)
            window.blit(self.imagem, self.posicao)
            renderizador_do_texto, _ = self.texto.font.render(self.texto.txt, self.texto.cor)
            rect = renderizador_do_texto.get_rect(center=(self.posicao[0] + self.tamanho[0] // 2, self.posicao[1]+self.tamanho[1]/2))
            window.blit(renderizador_do_texto, rect)

    def desativar(self):
        self.ativo = False

    def ativar(self):
        self.ativo = True

    def escrever(self, novo_texto):
        self.texto.txt = novo_texto
