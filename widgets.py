import pygame
import pygame.freetype

pygame.freetype.init()


# Enumerador de cores. Adicionar as que forem necessárias.
class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


# Classe que determina uma borda:
# Contém uma grossura, e cor, além disso é necessário calcular os vértices de seu retângulo depois.
class Border:
    def __init__(self, width, color):
        self.width = width
        self.color = color
        self.vertices = None

    def calculate_vertices(self, rect):
        self.vertices = (rect.position[0] - self.width, rect.position[1] - self.width, rect.size[0] + self.width,
         rect.size[1] + self.width)


class Text:
    def __init__(self, text, pt, color, font='Comic Sans MS'):
        self.txt = text
        self.pt = pt
        self.color = color
        self.font = pygame.freetype.SysFont(font, pt)


# Retorna o quadratura de dois vetores p, q, ou seja, o quadrado da distância entre eles.
def quadrature(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


# Determina se uma posição está dentro do retângulo, definido pela posição do vértice superior esquerdo
# e o tamanho de suas arestas.
def is_in_rect(position, rect):
    if rect.position[0] <= position[0] <= rect.position[0] + rect.size[0]:
        if rect.position[1] <= position[1] <= rect.position[1] + rect.size[1]:
            return True
        else:
            return False
    else:
        return False


# Determina se uma posição está dentro do círculo, definido pela posição do centro e o seu raio.
def is_in_circle(position, circle):
    return quadrature(position, circle.position) <= circle.size**2


class ToggleButton:
    def __init__(self, position, size, images, hint_text=None):
        self.visible = True
        self.clickable = True
        self.connected_function = None
        self.args = None
        self.hint_text = hint_text
        shape = 'Circular'
        if type(size) != int:
            shape = 'Retangular'
        self.size = size
        self.position = position
        self.images = []
        for img in images:
            if shape == 'Retangular':
                self.images.append(pygame.transform.scale(img, self.size))
            else:
                self.images.append(pygame.transform.scale(img, [self.size, self.size]))
        self.is_pressed = False
        self.shape = shape
        self.frame_counter = 0
        self.properties_changed = False

    def connect_function(self, function, args=None):
        self.connected_function = function
        self.args = args

    def detect_click(self, mouse_position):
        if self.clickable and not self.properties_changed:
            if self.shape == 'Retangular':
                if is_in_rect(mouse_position, self):
                    self.is_pressed = not self.is_pressed
                    if self.connected_function:
                        self.connected_function()
            else:
                if is_in_circle(mouse_position, self):
                    self.is_pressed = not self.is_pressed
                    if self.connected_function:
                        self.connected_function()

    def show(self, window):
        if self.visible:
            if self.is_pressed:
                window.blit(self.images[1], self.position)
            else:
                window.blit(self.images[0], self.position)
            if self.properties_changed:
                self.frame_counter += 1
                if self.frame_counter == 1:
                    self.frame_counter = 0
                    self.properties_changed = False
            if self.hint_text:
                text_render, _ = self.hint_text.font.render(self.hint_text.txt, self.hint_text.color)
                rect = text_render.get_rect(
                    center=(self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] / 2))
                window.blit(text_render, rect)

    def disable(self):
        self.clickable = False
        self.visible = False
        self.properties_changed = True

    def enable(self):
        self.clickable = True
        self.visible = True
        self.properties_changed = True

    def make_unclickable(self):
        self.clickable = False

    def make_clickable(self):
        self.clickable = True


# Classe do botão
class PushButton:
    def __init__(self, position, size, images, pressed_animation_length=5, hint_text=None):
        self.visible = True
        self.clickable = True
        self.connected_function = None
        self.hint_text = hint_text
        shape = 'Circular'
        if type(size) != int:
            shape = 'Retangular'
        self.size = size
        self.position = position
        self.images = []
        for img in images:
            if shape == 'Retangular':
                self.images.append(pygame.transform.scale(img, self.size))
            else:
                self.images.append(pygame.transform.scale(img, [self.size, self.size]))
        self.pressed = False
        self.shape = shape
        self.pressed_animation_length = pressed_animation_length
        self.frame_counter = 0
        self.properties_changed = False
        self.args = None

    def connect_function(self, function, args=None):
        self.connected_function = function
        self.args = args

    def detect_click(self, mouse_position):
        if self.clickable and not self.properties_changed:
            if self.shape == 'Retangular':
                if self.position[0] <= mouse_position[0] <= self.position[0] + self.size[0] and self.position[1] <= \
                        mouse_position[1] <= self.position[1] + self.size[1]:
                    self.pressed = True
            else:
                if quadrature(mouse_position, self.position) <= self.size**2:
                    self.pressed = True

    def activate_connected_function(self):
        if self.connected_function:
            if self.args is not None:
                self.connected_function(self.args)
            else:
                self.connected_function()

    def show(self, window):
        if self.visible:
            if self.pressed:
                window.blit(self.images[1], self.position)
                self.frame_counter += 1
                if self.frame_counter == self.pressed_animation_length:
                    self.frame_counter = 0
                    self.activate_connected_function()
                    self.pressed = False
            else:
                window.blit(self.images[0], self.position)
            if self.properties_changed:
                self.frame_counter += 1
                if self.frame_counter == 1:
                    self.frame_counter = 0
                    self.properties_changed = False
            if self.hint_text:
                text_render, _ = self.hint_text.font.render(self.hint_text.txt, self.hint_text.color)
                rect = text_render.get_rect(
                    center=(self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] / 2))
                window.blit(text_render, rect)

    def disable(self):
        self.clickable = False
        self.visible = False
        self.properties_changed = True

    def enable(self):
        self.clickable = True
        self.visible = True
        self.properties_changed = True

    def make_unclickable(self):
        self.clickable = False

    def make_clickable(self):
        self.clickable = True


class Panel:
    def __init__(self, position, size, image, border=Border(0, (0, 0, 0)), text=Text('None', 0, Color.BLACK)):
        self.enabled = True
        self.text = text
        self.size = size
        self.position = position
        self.image = pygame.transform.scale(image, self.size)
        self.border = border
        self.border.calculate_vertices(self)

    def show(self, window):
        if self.enabled:
            if self.border.width != 0:
                pygame.draw.rect(window, self.border.color, self.border.vertices)
            window.blit(self.image, self.position)
            text_render, _ = self.text.font.render(self.text.txt, self.text.color)
            rect = text_render.get_rect(center=(self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] / 2))
            window.blit(text_render, rect)

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def set_text(self, new_text):
        self.text.txt = new_text


class Window:
    MENU = 0
    MATCH = 1
    CONFIG = 2

    def __init__(self, buttons, panels):
        self.buttons = buttons
        self.panels = panels
        self.frame_counter = 0
        self.wait_complete = False

    def show(self, window):
        for button in self.buttons.values():
            button.show(window)
        for panel in self.panels.values():
            panel.show(window)
        if not self.wait_complete:
            self.frame_counter += 1
            if self.frame_counter == 3:
                self.wait_complete = True
