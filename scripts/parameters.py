# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 21:44:18 2020

@author: mcard
"""

model_name = 'marmousi_suave_383x151'



Nx = 383                  # Dimensão X do modelo 
Nz = 151                  # Dimensão Z do modelo
Na = 60                   # Número de pontos para borda de absorção

dt = 0.0006               # Variação temporal (eixo Z)
h = 10                    # Variação espacial (eixo X)
fcorte = 30                   # Frequência de corte da fonte

init_recz = 5             # Linha da matriz que será gravada no sismograma
init_shotz = 5            # Tiro inicial da fonte no eixo Z
init_shotx = 1            # Tiro inicial da fonte no eixo X

boundary = '1'            # Utilizar bordas de absorção (0 - Não, 1 - Sim)

Nxx = Nx + 2 * Na         # Dimensão X com as bordas de absorção
Nzz = Nz + 2 * Na         # Dimensão Z com as bordas de absorção

ntotal = 10000             # Quantidade total de passos de tempo do programa

fat = 0.0025              # Fator de absorção das bordas

dx_shot = 10              # Variação espacial dos tiros da fonte
num_shot = 38             # Número de tiros da fonte

camada_de_agua = 35

rec_shotz = init_recz + Na
init_shot_z = init_shotz + Na      
init_shot_x = init_shotx + Na