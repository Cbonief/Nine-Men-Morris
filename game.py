# Bibliotecas externas
import os  # Biblioteca para direcionamento do endereço dos arquivos.
import threading

import pygame  # Biblioteca para a janela do jogo e evento de mouse.
import pygame.freetype  # Sub biblioteca para a fonte.

# Meu código
import negamax
from ninemenmorris import *
from widgets import PushButton, Text, Border, Panel, Color, ToggleButton, Window


# Classe do manager do Jogo.
class Game:
    def __init__(self, window):
        self.width = window.get_width()
        self.height = window.get_height()
        self.window = window

        self.running = True
        self.paused = False

        self.move = None
        self.mill = NineMenMorris()

        self.active_window = Window.MENU
        self.piece_being_held = False
        self.held_piece = -1

        # Faz o rescaling das posições da tela. O jogo foi originalmente feito para o tabuleiro ter 600x600.
        # Mas com a adição UI foi modificado para ter 500x500.
        for position in range(0, 24):
            tile_positions[position] = [int(tile_positions[position][0] * 5 / 6 + 50), int(tile_positions[position][1] * 5 / 6 + 50)]

        # Carregando as imagens do jogo.
        self.pieces_sprites = self.load_pieces_sprites()
        grey_panel = pygame.image.load(os.path.join("Assets", "grey_panel.png")).convert_alpha()

        self.background_sprite = pygame.image.load(os.path.join("Assets", 'background.png'))
        self.background_sprite = pygame.transform.scale(self.background_sprite, (self.width, self.height))

        self.board_sprite = pygame.image.load(os.path.join("Assets", "board.png"))
        self.board_sprite = pygame.transform.scale(self.board_sprite, (int(self.width * 5 / 6), int(self.height * 5 / 6)))

        grey_button_sprites = [
            pygame.image.load(os.path.join("Assets", "grey_button.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "grey_button_pushed.png")).convert_alpha()
        ]

        pause_button_sprites = [
            pygame.image.load(os.path.join("Assets", "pausar_idle.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "pausar_apertado.png")).convert_alpha()
        ]
        close_button_sprites = [
            pygame.image.load(os.path.join("Assets", "fechar_idle.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "fechar_apertado.png")).convert_alpha()
        ]
        play_button_sprites = [
            pygame.image.load(os.path.join("Assets", "play_idle.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "play_apertado.png")).convert_alpha()
        ]
        left_arrow_button_sprites = [
            pygame.image.load(os.path.join("Assets", "grey_slider_left.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "grey_slider_left_pushed.png")).convert_alpha()
        ]
        right_arrow_button_sprites = [
            pygame.image.load(os.path.join("Assets", "grey_slider_right.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "grey_slider_right_pushed.png")).convert_alpha()
        ]
        up_arrow_button_sprites = [
            pygame.image.load(os.path.join("Assets", "grey_slider_up.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "grey_slider_up_pushed.png")).convert_alpha()
        ]
        down_arrow_button_sprites = [
            pygame.image.load(os.path.join("Assets", "grey_slider_down.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "grey_slider_down_pushed.png")).convert_alpha()
        ]
        color_toggle_button_sprites = [
            pygame.image.load(os.path.join("Assets", "white_button.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "black_button.png")).convert_alpha()
        ]

        # Cria a fonte do jogo.
        self.font = pygame.freetype.SysFont('Comic Sans MS', 18)

        # Cria os botões
        game_window_buttons = {
            'Pause': PushButton([5, 5], 40, pause_button_sprites),
            'Close': PushButton([600 - 5 - 40, 5], 40, close_button_sprites),
            'Resume': PushButton([5, 5], 40, play_button_sprites),
        }
        main_window_buttons = {
            'Close': PushButton([600 - 5 - 40, 5], 40, close_button_sprites),
            'PlayAI': PushButton([self.width / 2 - 75, self.height / 2 - 80], [150, 40], grey_button_sprites,
                                  hint_text=Text('vs AI', 18, Color.BLACK)),
            'PlayHuman': PushButton([self.width / 2 - 75, self.height / 2], [150, 40], grey_button_sprites, hint_text=Text('vs  Jogador', 18, Color.BLACK))
        }

        config_window_buttons = {
            'Close': PushButton([600 - 5 - 40, 5], 40, close_button_sprites),
            'Color': ToggleButton([self.width / 2 + 65, self.height / 2 - 75], [30, 30], color_toggle_button_sprites),
            'Return': PushButton([40, 33], [39, 31], left_arrow_button_sprites),
            'Increase': PushButton([self.width / 2 + 30, self.height / 2 + 5], [int(31*0.75), int(39*0.75)], up_arrow_button_sprites),
            'Decrease': PushButton([self.width / 2 + 107, self.height / 2 + 5], [int(31*0.75), int(39*0.75)], down_arrow_button_sprites),
            'Play': PushButton([self.width / 2 - 75, self.height / 2 +80], [150, 40], grey_button_sprites, hint_text=Text('JOGAR', 18, Color.BLACK))
        }

        main_window_buttons['Close'].connect_function(self.close_game)
        main_window_buttons['PlayAI'].connect_function(self.change_active_window, Window.CONFIG)
        main_window_buttons['PlayHuman'].connect_function(self.start_match, )

        game_window_buttons['Close'].connect_function(self.close_game)
        game_window_buttons['Pause'].connect_function(self.pause_match)
        game_window_buttons['Resume'].connect_function(self.resume_match)
        game_window_buttons['Resume'].disable()

        config_window_buttons['Close'].connect_function(self.close_game)
        config_window_buttons['Return'].connect_function(self.change_active_window, Window.MENU)
        config_window_buttons['Increase'].connect_function(self.change_ai_depth_level, 1)
        config_window_buttons['Decrease'].connect_function(self.change_ai_depth_level, -1)
        config_window_buttons['Play'].connect_function(self.start_match, True)

        main_window_panels = {
            'Title': Panel([self.width / 2 - 100, 30], [200, 40], grey_panel, Border(0, Color.BLACK), Text('Trilha', 20, Color.BLACK))
        }

        game_window_panels = {
            'Move': Panel([self.width / 2 - 100, 10], [200, 30], grey_panel, Border(0, Color.BLACK), Text('Vez do Branco', 18, Color.BLACK))

        }

        config_window_panels = {
            'Title': Panel([self.width / 2 - 100, 30], [200, 40], grey_panel, Border(0, Color.BLACK), Text('Trilha', 20, Color.BLACK)),
            'Color': Panel([self.width / 2 - 165, self.height / 2 - 80], [175, 40], grey_panel, Border(0, Color.BLACK), Text('Escolha sua cor:', 20, Color.BLACK)),
            'Msg': Panel([self.width / 2 - 165, self.height / 2], [175, 40], grey_panel, Border(0, Color.BLACK), Text('Nível da AI:', 20, Color.BLACK)),
            'AiLevel': Panel([self.width / 2 + 65, self.height / 2 + 5], [30, 30], grey_panel, Border(0, Color.BLACK), Text('1', 20, Color.BLACK))
        }

        self.window_manager = [
            Window(main_window_buttons, main_window_panels),
            Window(game_window_buttons, game_window_panels),
            Window(config_window_buttons, config_window_panels)
        ]

        self.text_stage_2 = ['Preto come uma peça', 'Branco come uma peça']
        self.text_normal = ['Vez do Preto', 'Vez do Branco']
        self.text_game_over = ['Preto Venceu!', 'Branco Venceu!']

        self.ai_depth_level = 1
        self.playing_vs_ai = None
        self.player_color = Player.WHITE

        simulation_thread = threading.Thread(target=self.ai_calculation, daemon=True)
        simulation_thread.start()

    def run(self):
        timer = pygame.time.Clock()
        while self.running:
            self.event_handler()

            if self.active_window == Window.MENU:
                self.menu()
            elif self.active_window == Window.MATCH:
                self.match()
            elif self.active_window == Window.CONFIG:
                self.config()

            self.window_manager[self.active_window].show(self.window)

            timer.tick(60)
            pygame.display.update()

    def show_piece(self, position, player, piece_in_mill=False):
        if piece_in_mill:
            self.window.blit(self.pieces_sprites[Player.index[player]]['Marcado'], [tile_positions[position][0] - 24, tile_positions[position][1] - 24])
        else:
            self.window.blit(self.pieces_sprites[Player.index[player]]['Normal'], [tile_positions[position][0] - 24, tile_positions[position][1] - 24])

    def show_piece_following_mouse(self, jogador):
        pos = pygame.mouse.get_pos()
        self.window.blit(self.pieces_sprites[NineMenMorris.indice(jogador)]['Normal'], [pos[0] - 24, pos[1] - 24])

    def menu(self):
        self.window.blit(self.background_sprite, [0, 0])

    def config(self):
        self.window.blit(self.background_sprite, [0, 0])

    def event_handler(self):
        self.move = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.window_manager[self.active_window].buttons.values():
                    button.detect_click(pygame.mouse.get_pos())
                if not self.paused and self.active_window == Window.MATCH and self.window_manager[Window.MATCH].wait_complete:
                    clicked_a_position, position_clicked = check_mouse_position(pygame.mouse.get_pos())
                    if clicked_a_position and (not self.playing_vs_ai or self.mill.active_player == self.player_color):
                        if self.mill.piece_from_position(position_clicked) == self.mill.active_player and self.mill.stage == GameStage.MOVEMENT:
                            self.piece_being_held = True
                            self.held_piece = position_clicked
                        elif self.mill.piece_from_position(position_clicked) == 0 and self.mill.stage == GameStage.PLACEMENT:
                            self.move = Move(position_clicked, MoveType.PLACE_PIECE)
                        elif self.mill.piece_from_position(position_clicked) == (-1) * self.mill.active_player and self.mill.stage == GameStage.REMOVAL and not self.mill.is_piece_in_mill(position_clicked):
                            self.move = Move(position_clicked, MoveType.REMOVE_PIECE)

            if event.type == pygame.MOUSEBUTTONUP:
                dropped_over_a_position, position_dropped = check_mouse_position(pygame.mouse.get_pos())
                if self.piece_being_held and dropped_over_a_position and self.mill.piece_from_position(position_dropped) == 0 and self.mill.stage == GameStage.MOVEMENT:
                    self.move = Move(self.held_piece, MoveType.MOVE_PIECE, position_dropped)
                self.piece_being_held = False
                self.held_piece = -1

    def change_active_window(self, new_window):
        self.active_window = new_window

    def start_match(self, is_vs_ai=False):
        self.playing_vs_ai = is_vs_ai
        self.active_window = Window.MATCH
        if self.playing_vs_ai:
            if self.window_manager[Window.CONFIG].buttons['Color'].is_pressed:
                self.player_color = Player.BLACK
            else:
                self.player_color = Player.WHITE

    def change_ai_depth_level(self, dif):
        if 1 <= self.ai_depth_level + dif <= 7:
            self.ai_depth_level = self.ai_depth_level + dif
            self.window_manager[Window.CONFIG].panels['AiLevel'].set_text(str(self.ai_depth_level))

    def ai_calculation(self):
        x = 2
        # while True:
        #     if self.mill.active_player == -self.player_color and self.playing_vs_ai:
        #         self.move = negamax.calculate_movement(self.mill, self.ai_depth_level, -self.player_color)

    def match(self):
        self.window.blit(self.background_sprite, [0, 0])
        pygame.draw.rect(self.window, (0, 0, 0), (43, 43, 514, 514))
        pygame.draw.rect(self.window, (255, 255, 255), (44, 44, 512, 512))
        self.window.blit(self.board_sprite, [50, 50])

        if self.mill.game_over:
            self.window_manager[Window.MATCH].panels['Move'].set_text(self.text_game_over[self.mill.indice(self.mill.winner)])
        elif self.mill.stage == 2:
            self.window_manager[Window.MATCH].panels['Move'].set_text(self.text_stage_2[self.mill.indice(self.mill.active_player)])
        else:
            self.window_manager[Window.MATCH].panels['Move'].set_text(self.text_normal[self.mill.indice(self.mill.active_player)])

        # Caso seja a vez da AI, calcula sua jogada.
        if not self.mill.game_over:
            if self.mill.active_player == -self.player_color and self.playing_vs_ai:
                self.move = negamax.calculate_movement(self.mill, self.ai_depth_level, -self.player_color)

            # Executa a jogada, seja da AI ou do jogador.
            if self.move and self.move.is_valid(self.mill):
                self.mill.execute_move(self.move)

        # Prepara o display das peças.
        for position in range(0, 24):
            if position != self.held_piece and self.mill.board[position] != 0:
                self.show_piece(position, self.mill.board[position], self.mill.is_piece_in_mill(position))
        if self.piece_being_held:
            self.show_piece_following_mouse(self.mill.active_player)

    def pause_match(self):
        self.paused = True
        self.window_manager[Window.MATCH].buttons['Pause'].disable()
        self.window_manager[Window.MATCH].buttons['Resume'].enable()

    def resume_match(self):
        self.paused = False
        self.window_manager[Window.MATCH].buttons['Resume'].disable()
        self.window_manager[Window.MATCH].buttons['Pause'].enable()

    def close_game(self):
        self.running = False

    @staticmethod
    def load_pieces_sprites():
        sprite_sheet = pygame.image.load(os.path.join("Assets", "pieces_transparent.png")).convert_alpha()

        # Separa a imagem das peças em quatro peças.
        pieces = [
            {'Normal': pygame.Surface((86, 86), pygame.SRCALPHA, 32), 'Marcado': pygame.Surface((86, 86), pygame.SRCALPHA, 32)},
            {'Normal': pygame.Surface((86, 86), pygame.SRCALPHA, 32), 'Marcado': pygame.Surface((86, 86), pygame.SRCALPHA, 32)}
        ]
        pieces[NineMenMorris.indice(Player.WHITE)]['Normal'].blit(sprite_sheet, (0, 0), (0, 0, 86, 86))
        pieces[NineMenMorris.indice(Player.BLACK)]['Normal'].blit(sprite_sheet, (0, 0), (86, 0, 86, 86))
        pieces[NineMenMorris.indice(Player.WHITE)]['Marcado'].blit(sprite_sheet, (0, 0), (2 * 86, 0, 86, 86))
        pieces[NineMenMorris.indice(Player.BLACK)]['Marcado'].blit(sprite_sheet, (0, 0), (3 * 86, 0, 86, 86))

        for player in range(0, 2):
            for name in pieces[player]:
                pieces[player][name] = pygame.transform.scale(pieces[player][name], (48, 48))
        return pieces


def check_mouse_position(mouse_position):
    for position in range(0, 24):
        if quadrature(mouse_position, tile_positions[position]) <= 25**2:
            return True, position
    return False, -1


def quadrature(p, q):
    return (p[0]-q[0])**2+(p[1]-q[1])**2
