# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 21:37:20 2020

@author: marcelo cardozo
"""

import time
import numpy as np
from aux_functions import *
from parameters import *
import matplotlib.pyplot as plt

def main():

    ## Declaração de matrizes
    extended_model = np.zeros((Nzz, Nxx))
    
    fat_s = np.ones((Nzz, Nxx))            # Fator de absorção da borda superior, inferior, esquerda e direita
    fat_d = np.ones((Nzz, Nxx))            
    fat_i = np.ones((Nzz, Nxx))            
    fat_e = np.ones((Nzz, Nxx))
    
    C = np.zeros((Nzz, Nxx))                # Matriz para simplificação da equação da onda discretizada 
    A = np.zeros((Nzz, Nxx))                # Matriz para simplificação da equação de bordas não reflexivas
    
    P1 = np.zeros((Nzz, Nxx))               # Matriz no tempo passado
    P2 = np.zeros((Nzz, Nxx))               # Matriz no tempo presente
    P3 = np.zeros((Nzz, Nxx))               # Matriz no tempo futuro

    sis = np.zeros((ntotal, Nx))            # Matriz do sismograma
    
    Asc = np.zeros((Nzz, Nxx, ntotal))      # Matriz para gravar a matriz P3 em cada passo de tempo (n)

    P1_mig = np.zeros((Nzz, Nxx))           # Matriz no tempo passado (migração)
    P2_mig = np.zeros((Nzz, Nxx))           # Matriz no tempo presente (migração)
    P3_mig = np.zeros((Nzz, Nxx))           # Matriz no tempo futuro (migração)
    
    Im = np.zeros((Nzz, Nxx))               # Matriz da Imagem1 gerada pela migração
    Im2 = np.zeros((Nzz, Nxx))              # Matriz da Imagem1 gerada pela migração
    Im3 = np.zeros((Nzz, Nxx))              # Matriz da Imagem1 gerada pela migração

    Im_soma = np.zeros((Nzz, Nxx))
    Im2_soma = np.zeros((Nzz, Nxx))
    Im3_soma = np.zeros((Nzz, Nxx))
    
    Im_sem_agua = np.zeros((Nz-camada_de_agua, Nx))
    Im2_sem_agua = np.zeros((Nz-camada_de_agua, Nx))
    Im3_sem_agua = np.zeros((Nz-camada_de_agua, Nx))

    # Início do programa
    model = read_model()
    extended_model = add_boundary(extended_model, model)
    fonte, t, Nf = ricker_wavelet() 
    fat_s,fat_i,fat_e,fat_d = calc_fat(fat_s,fat_i,fat_e,fat_d)
    A,C = calc_A_C(extended_model,A,C)
    
    
    for tiro in range(num_shot):
        
        print('\nTiro {}'.format(tiro+1))
        
        shot_x = tiro * dx_shot + init_shot_x
        shot_z = init_shot_x
        
        sis = modelagem(fat_d, fat_e, fat_s, fat_i, P1, P2, P3, C, A, Asc, sis, fonte, Nf, shot_x, shot_z)
    
        Im, Im2, Im3 = migracao(P1_mig, P2_mig, P3_mig, sis, A, C, Asc, Im, Im2, Im3, fat_s, fat_d, fat_e, fat_i)
    
        for i in range(Nzz):
            for k in range(Nxx):
                Im_soma[i,k] += Im[i,k]
                Im2_soma[i,k] += Im2[i,k]
                Im3_soma[i,k] += Im3[i,k]
    
    # Remoção camada de água e cálculo do filtro laplaciano do modelo sem água
    Im_sem_agua, Im2_sem_agua, Im3_sem_agua = remove_water(Im_sem_agua, Im2_sem_agua, Im3_sem_agua, Im_soma, Im2_soma, Im3_soma)
    laplacian, laplacian2, laplacian3 = calc_laplacian(Im_sem_agua, Im2_sem_agua, Im3_sem_agua)
    
    # Plot dos modelos e criação dos binários
    plot_model(Im_soma, 'Im_soma', Nzz, Nxx)
    binCreate('Im_soma', Im_soma)
    plot_model(Im2_soma, 'Im2_soma', Nzz, Nxx)
    binCreate('Im2_soma', Im2_soma)
    plot_model(Im3_soma, 'Im3_soma', Nzz, Nxx)
    binCreate('Im3_soma', Im3_soma)
    
    plot_model(Im_sem_agua, 'Im_soma_sem_água', Nz-camada_de_agua, Nx)
    binCreate('Im_sem_agua', Im_sem_agua)
    plot_model(Im2_sem_agua, 'Im2_soma_sem_água', Nz-camada_de_agua, Nx)
    binCreate('Im2_sem_agua', Im2_sem_agua)
    plot_model(Im3_sem_agua, 'Im3_soma_sem_água', Nz-camada_de_agua, Nx)
    binCreate('Im3_sem_agua', Im3_sem_agua)
    
    plot_model(laplacian, 'Laplacian', Nz-camada_de_agua, Nx)
    binCreate('Laplacian', laplacian)
    plot_model(laplacian2, 'Laplacian 2', Nz-camada_de_agua, Nx)
    binCreate('Laplacian 2', laplacian2)
    plot_model(laplacian3, 'Laplacian 3', Nz-camada_de_agua, Nx)
    binCreate('Laplacian 3', laplacian3)
    
    plot_sis(sis, 'Seismogram Marmousi')
    binCreate('Seismogram Marmousi', sis)

    
if __name__ == '__main__':
    
    start_t = time.time()
    main()
    tempo = time.time() - start_t
    print("Tempo de execução: {:.2f} segundos".format(tempo))