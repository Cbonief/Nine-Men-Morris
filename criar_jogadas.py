from Assets import *
from minimax import *
from mills import *
import copy
import os
import json

# # Estrutura das primeiras jogadas:
# # primeiro valor é o player,
# # o segundo a profundidade,
# # e o terceiro a jogada do outro jogador.
# # Por fim retorna o hash da melhor jogada.
# primeira_jogada = []
#
# # Calculo do preto.
trilha = Mills()
# primeira_jogada.append([])
# for profundidade in range(1, 2):
#     primeira_jogada[trilha.indice(Jogador.PRETO)].append({})
#     print("--------------------------------------")
#     print("-----------PROFUNDIDADE {}-------------".format(profundidade))
#     for jogada in trilha.jogadas_validas(Jogador.BRANCO):
#         trilha_filha = copy.deepcopy(trilha)
#         trilha_filha.executar_jogada(jogada)
#         melhor_jogada = calcular_movimento(trilha_filha, profundidade, Jogador.PRETO)
#         primeira_jogada[trilha.indice(Jogador.PRETO)][profundidade-1][hash(trilha_filha)] = hash(melhor_jogada)
#
# print(primeira_jogada[trilha.indice(Jogador.PRETO)])
# for i in range(2, 8):
#     primeira_jogada[trilha.indice(Jogador.PRETO)].append(primeira_jogada[trilha.indice(Jogador.PRETO)][profundidade-2])
#     print(primeira_jogada[trilha.indice(Jogador.PRETO)])
# print(primeira_jogada[trilha.indice(Jogador.PRETO)])
# print("BRANCO")
#
# primeira_jogada.append([])
# for profundidade in range(1, 8):
#     print("--------------------------------------")
#     print("-----------PROFUNDIDADE {}-------------".format(profundidade))
#     melhor_jogada = calcular_movimento(trilha, profundidade, Jogador.BRANCO)
#     primeira_jogada[trilha.indice(Jogador.BRANCO)].append(hash(melhor_jogada))
#     print(primeira_jogada[trilha.indice(Jogador.BRANCO)][profundidade-1])
# #
# with open(os.path.join("Assets", "primeiras_jogadas.json"), "w") as write_file:
#     json.dump(primeira_jogada, write_file, indent=4)


print(hash(trilha))

