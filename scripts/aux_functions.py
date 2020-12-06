# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 21:42:58 2020

@author: mcard
"""

import numpy as np
from parameters import *
from math import exp, sqrt, pi
from numba import jit
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import ndimage

def read_model():
    model = np.fromfile('../models/{}.bin'.format(model_name), dtype=np.float32).reshape((Nx, Nz)).T
    return model

def add_boundary(extended_model, model):

    for k in range(Nx):
        for i in range(Nz):
            extended_model[i + Na, k + Na] = model[i, k]

    # Borda superior
    for k in range(Na, Nx + Na):
        for i in range(Na):
            extended_model[i,k] = extended_model[Na + 1, k]

    #Borda inferior
    for k in range(Na, Nx + Na):
        for i in range(Nz + Na, Nzz):
            extended_model[i,k] = extended_model[Na + Nz - 1, k]
                
    # Borda lateral esquerda
    for k in range(Na):
        for i in range(Na, Nz + Na):
            extended_model[i,k] = extended_model[i, Na + 1]
                
   # Borda lateral direita
    for k in range(Nx + Na, Nxx):
        for i in range(Na, Nz + Na):
            extended_model[i,k] = extended_model[i, Nx + Na - 1]
            
    # Borda quina superior esquerda
    for k in range(Na):
        for i in range(Na):
            extended_model[i,k] = extended_model[Na + 1, Na + 1]
            
    # Borda quina superior direita
    for k in range(Nx + Na, Nxx):
        for i in range(Na):
            extended_model[i,k] = extended_model[Na, Nx + Na - 1]
            
    # Borda quina inferior esquerda
    for k in range(Na):
        for i in range(Nz + Na, Nzz):
            extended_model[i,k] = extended_model[Nz + Na - 1, Na + 1]
                
    # Borda quina inferior direita
    for k in range(Nx + Na, Nxx):
        for i in range(Nz + Na, Nzz):
            extended_model[i,k] = extended_model[Nz + Na - 1, Nx + Na]
            
    return extended_model

def ricker_wavelet():

    # Derivada segunda da gaussiana
    Nf = int(4 * sqrt(pi) / (fcorte * dt))
    fonte = np.zeros(Nf)
    TF = 2 * sqrt(pi) / fcorte       # Período da função Gaussiana
    fc = fcorte / (3. * sqrt(pi))    # Frequência central
    
    t=[]

    for n in range(Nf):
        t.append((n) * dt - TF)
        fonte[n] = (-exp(-pi * (pi * fc * t[n]) ** 2) * (1 - 2 * pi * (pi * fc * t[n]) * (pi * fc * t[n])))
    
    return fonte, t, Nf

def calc_A_C(extended_model,A,C):
  for i in range(Nzz):
      for k in range(Nxx):
          A[i, k] = extended_model[i, k] * (dt/h)
          C[i, k] = - (A[i, k] ** 2) / 12
  return A, C

def calc_fat(fat_s,fat_i,fat_e,fat_d):
  for k in range(Nxx):
      if Na != 0:
          for i in range(Na):
              fat_s[i, k] = exp(-((fat * (Na - i)) ** 2))
                
          for i in range(Nzz - Na, Nzz):
              fat_i[i, k] = exp(-((fat * (Nzz - Na - i)) ** 2))
                  
  if Na != 0:
      for k in range(Na):
          for i in range(Nzz):
              fat_e[i, k] = exp(-((fat * (Na - k)) ** 2))

      for k in range(Nxx - Na, Nxx):
          for i in range(Nzz):
              fat_d[i, k] = exp(-(((fat) * (Nxx - Na - k)) ** 2))
  return fat_s,fat_i,fat_e,fat_d

@jit
def modelagem(fat_d, fat_e, fat_s, fat_i, P1, P2, P3, C, A, Asc, sis, fonte, Nf, shot_x, shot_z):
    
    print("\nModelando...\n")
    for n in range(0,ntotal,1):
        
        # Termo fonte
        if n < Nf:
            v = A[shot_z, shot_x]
            P2[shot_z, shot_x] = P2[shot_z, shot_x] + (fonte[n] * v*v)
    
        # Cálculo do Campo no interior do modelo
        for i in range(2, Nzz-2):
            for k in range(2, Nxx-2):

                P3[i, k] = C[i, k] * (P2[i, k + 2] + P2[i, k - 2] + P2[i + 2, k] + P2[i - 2, k] - 16 * (P2[i, k + 1] + P2[i, k - 1] + P2[i + 1, k] + P2[i - 1, k]) + 60 * (P2[i, k])) + 2 * (P2[i, k]) - P1[i, k]
        
        if boundary == "1":

            # --------------- Cerjan Boundary ---------------

            for k in range(2, Nxx - 2):
        
                if Na != 0:

                    # Borda superior
                    for i in range(Na):
                        P2[i,k] = fat_s[i,k] * P2[i,k]
                        P3[i,k] = fat_s[i,k] * P3[i,k]
                if Na != 0:

                    # Borda inferior
                    for i in range(Nzz - Na, Nzz):
                        P2[i,k] = fat_i[i,k] * P2[i,k]
                        P3[i,k] = fat_i[i,k] * P3[i,k]

            if Na != 0:

                # Borda lateral esquerda
                for k in range (Na):
                    for i in range(Nzz):
                        P2[i,k] = fat_e[i,k] * P2[i,k]
                        P3[i,k] = fat_e[i,k] * P3[i,k]

                # Borda Lateral Direita
                for k in range(Nxx - Na, Nxx):
                    for i in range(Nzz ):
                        P2[i,k] = fat_d[i,k] * P2[i,k]
                        P3[i,k] = fat_d[i,k] * P3[i,k]

            # --------------- Reynolds Boundary ---------------

            for k in range(Nxx):
                # Borda superior
                for i in range(2):
                    P3[i,k] = P2[i,k] + A[i,k] * (P2[i+1, k] - P2[i,k])

                # Borda inferior
                for i in range(Nzz-2, Nzz):
                    P3[i,k] = P2[i,k] - A[i,k] * (P2[i, k] - P2[i-1,k])

            for i in range(Nzz):
                # Borda esquerda
                for k in range(2):
                    P3[i,k] = P2[i,k] + A[i,k] * (P2[i, k+1] - P2[i,k])
                # Borda direita
                for k in range(Nxx-2, Nxx):
                    P3[i,k] = P2[i,k] - A[i,k] * (P2[i, k] - P2[i,k-1])
                  

        # Atualização do campo de onda
        P1 = np.copy(P2)
        P2 = np.copy(P3)
    
        for k in range (Nx):
            sis[n, k] = P3[rec_shotz,k + Na]

        for k in range(Nxx):
            for i in range(Nzz):
                Asc[i,k,n] = P3[i,k]

        if n % 1000 == 0:
            print(n)

    return sis

@jit
def migracao(P1_mig, P2_mig, P3_mig, sis, A, C, Asc, Im, Im2, Im3, fat_s, fat_d, fat_e, fat_i):

    print("\nMigrando...\n")
    ## Computação do campo de pressão reverso no tempo
    for n in range(ntotal-1,-1,-1):
        # Termo fonte
        for k in range(Nx):
            P2_mig[rec_shotz, Na + k] = P2_mig[rec_shotz, Na + k] + sis[n,k]
    
        # Cálculo do Campo no interior do modelo
        for i in range(2, Nzz-2):
            for k in range(2, Nxx-2):

                P3_mig[i, k] = C[i, k] * (P2_mig[i, k + 2] + P2_mig[i, k - 2] + P2_mig[i + 2, k] + P2_mig[i - 2, k] - 16 * (P2_mig[i, k + 1] + P2_mig[i, k - 1] + P2_mig[i + 1, k] + P2_mig[i - 1, k]) + 60 * (P2_mig[i, k])) + 2 * (P2_mig[i, k]) - P1_mig[i, k]
    
        if boundary == "1":

            # --------------- Cerjan Boundary ---------------

            for k in range(2, Nxx - 2):
        
                if Na != 0:

                    # Borda superior
                    for i in range(Na):
                        P2_mig[i,k] = fat_s[i,k] * P2_mig[i,k]
                        P3_mig[i,k] = fat_s[i,k] * P3_mig[i,k]
                if Na != 0:

                    # Borda inferior
                    for i in range(Nzz - Na, Nzz):
                        P2_mig[i,k] = fat_i[i,k] * P2_mig[i,k]
                        P3_mig[i,k] = fat_i[i,k] * P3_mig[i,k]

            if Na != 0:

                # Borda lateral esquerda
                for k in range (Na):
                    for i in range(Nzz):
                        P2_mig[i,k] = fat_e[i,k] * P2_mig[i,k]
                        P3_mig[i,k] = fat_e[i,k] * P3_mig[i,k]

                # Borda Lateral Direita
                for k in range(Nxx - Na, Nxx):
                    for i in range(Nzz ):
                        P2_mig[i,k] = fat_d[i,k] * P2_mig[i,k]
                        P3_mig[i,k] = fat_d[i,k] * P3_mig[i,k]

            # --------------- Reynolds Boundary ---------------

            for k in range(Nxx):
                # Borda superior
                for i in range(2):
                    P3_mig[i,k] = P2_mig[i,k] + A[i,k] * (P2_mig[i+1, k] - P2_mig[i,k])

                # Borda inferior
                for i in range(Nzz-2, Nzz):
                    P3_mig[i,k] = P2_mig[i,k] - A[i,k] * (P2_mig[i, k] - P2_mig[i-1,k])

            for i in range(Nzz):
                # Borda esquerda
                for k in range(2):
                    P3_mig[i,k] = P2_mig[i,k] + A[i,k] * (P2_mig[i, k+1] - P2_mig[i,k])
                # Borda direita
                for k in range(Nxx-2, Nxx):
                    P3_mig[i,k] = P2_mig[i,k] - A[i,k] * (P2_mig[i, k] - P2_mig[i,k-1])
    
        for i in range(Nzz):
            for k in range(Nxx):
                Im[i,k] += P2_mig[i,k] * Asc[i,k,n]
                Im2[i,k] += Im[i,k] / ((P2_mig[i,k] ** 2) + 0.0000000001)
                Im3[i,k] += Im[i,k] / ((Asc[i,k,n] ** 2) + 0.0000000001)
        
        P1_mig = np.copy(P2_mig)
        P2_mig = np.copy(P3_mig)

        if n % 1000 == 0:
            print(n)
    
    return Im, Im2, Im3

def remove_water(Im_sem_agua, Im2_sem_agua, Im3_sem_agua, Im_soma, Im2_soma, Im3_soma):
    
    for i in range(Nz-camada_de_agua):
        for k in range(Nx):
            Im_sem_agua[i,k] = Im_soma[i+Na+camada_de_agua,k+Na]
            Im2_sem_agua[i,k] = Im2_soma[i+Na+camada_de_agua,k+Na]
            Im3_sem_agua[i,k] = Im3_soma[i+Na+camada_de_agua,k+Na]

    return Im_sem_agua, Im2_sem_agua, Im3_sem_agua

def calc_laplacian(Im_sem_agua, Im2_sem_agua, Im3_sem_agua):
    
    laplacian = ndimage.laplace(Im_sem_agua)
    laplacian2 = ndimage.laplace(Im2_sem_agua)
    laplacian3 = ndimage.laplace(Im3_sem_agua)
    
    return laplacian, laplacian2, laplacian3

def plot_model(model, name, dim1, dim2):
    
    xmax = dim2 * h
    zmax = dim1 * h
    
    ## Eixo horizontal no topo da figura
    plt.rcParams['xtick.bottom'] = False
    plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.top'] = True
    plt.rcParams['xtick.labeltop'] = True

    plt.rc('xtick', labelsize=16)    
    plt.rc('ytick', labelsize=16)
    plt.rcParams.update({'font.size':16})
    
    ## Formatação do plot
    fig, ax = plt.subplots(figsize=(8,16))
    ax.xaxis.set_label_position('top')
    im = ax.imshow(model, cmap='gray', extent=[0,xmax,zmax,0], interpolation='bicubic')
    plt.title(name)
    plt.xlabel('Distance (m)', fontsize=16)
    plt.ylabel('Profundidade (m)', fontsize=16)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
    plt.savefig('../output/images/'+name+".png", dpi=300, bbox_inches='tight')
    plt.show()

def plot_sis(data, name):

    ## Eixos em dimensões reais
    scaleX = 1.0 / 1000
    scaleZ = 1

    Xmin = (0 * h) * scaleX
    Xmax = (Nx * h) * scaleX
    Zmin = (0 * dt) * scaleZ
    Zmax = (ntotal * dt) * scaleZ


    ## Eixo horizontal no topo da figura
    plt.rcParams['xtick.bottom'] = False
    plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.top'] = True
    plt.rcParams['xtick.labeltop'] = True

    plt.rc('xtick', labelsize=16)    
    plt.rc('ytick', labelsize=16)
    plt.rcParams.update({'font.size':16})

    ## Formatação do plot
    fig, ax = plt.subplots(figsize=(12,12))
    ax.xaxis.set_label_position('top')
    im = ax.imshow(data, cmap='gray', vmin=-0.01, vmax=0.01 , extent=[Xmin,Xmax,Zmax,Zmin], interpolation='bicubic', aspect=1.5)
    plt.title(name)
    plt.xlabel('$Posição (Km)$', fontsize=16)
    plt.ylabel('Tempo (s)', fontsize=16)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
  
    plt.savefig('../output/images/'+name+'.png', dpi=300,bbox_inches='tight')

def binCreate(modelName, model):

    output_name = "../output/{}.bin".format(modelName)
    
    binFile = open(output_name, "wb")
    model.tofile(binFile)
    binFile.close()