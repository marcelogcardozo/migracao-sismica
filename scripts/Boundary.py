import matplotlib.pyplot as plt
from Model import Model
import numpy as np


class Boundary(Model):
    def __init__(self):

        Model.__init__(self)

        # Cálculo das matrizes auxiliares A e C
        self.calc_A_C()

        # Cálculo dos fatores de absorção
        self.calc_fat()


    def calc_A_C(self):

        self.C = np.zeros((self.Nzz, self.Nxx))                # Matriz para simplificação da equação da onda discretizada 
        self.A = np.zeros((self.Nzz, self.Nxx))                # Matriz para simplificação da equação de bordas não reflexivas

        self.A[:,:] = self.extended_model[:,:] * (self.dt/self.h)
        self.C[:,:] = -(self.A[:,:] ** 2) / 12
 
    def calc_fat(self):

        self.fat_s = np.ones((self.Nzz, self.Nxx))            # Fator de absorção da borda superior, inferior, esquerda e direita
        self.fat_d = np.ones((self.Nzz, self.Nxx))            
        self.fat_i = np.ones((self.Nzz, self.Nxx))            
        self.fat_e = np.ones((self.Nzz, self.Nxx))

        for i in range(self.Na):
            self.fat_s[i, :] = np.exp(-((self.fat * (self.Na - i)) ** 2))
            self.fat_e[:, i] = np.exp(-((self.fat * (self.Na - i)) ** 2))
        
        for i in range(self.Nzz - self.Na, self.Nzz):
            self.fat_i[i, :] = np.exp(-((self.fat * (self.Nzz - self.Na - i)) ** 2))
        
        for i in range(self.Nxx - self.Na, self.Nxx):
            self.fat_d[:, i] = np.exp(-((self.fat * (self.Nxx - self.Na - i)) ** 2))


    def apply_boundary(self, P1, P2, P3):

         # --------------- Cerjan Boundary ---------------
        #sup
        P2[:self.Na, 2:self.Nxx - 2] = P2[:self.Na, 2:self.Nxx - 2] * self.fat_s[:self.Na, 2:self.Nxx - 2]
        P3[:self.Na, 2:self.Nxx - 2] = P3[:self.Na, 2:self.Nxx - 2] * self.fat_s[:self.Na, 2:self.Nxx - 2]

        #inf
        P2[self.Nzz-self.Na:self.Nzz,2:self.Nxx - 2] = P2[self.Nzz-self.Na:self.Nzz,2:self.Nxx - 2] * self.fat_i[self.Nzz-self.Na:self.Nzz,2:self.Nxx - 2]
        P3[self.Nzz-self.Na:self.Nzz,2:self.Nxx - 2] = P3[self.Nzz-self.Na:self.Nzz,2:self.Nxx - 2] * self.fat_i[self.Nzz-self.Na:self.Nzz,2:self.Nxx - 2]

        #esq
        P2[:,:self.Na] = P2[:,:self.Na] * self.fat_e[:,:self.Na]
        P3[:,:self.Na] = P3[:,:self.Na] * self.fat_e[:,:self.Na]

        #dir
        P2[:,self.Nxx-self.Na:self.Nxx] = P2[:,self.Nxx-self.Na:self.Nxx] * self.fat_d[:,self.Nxx-self.Na:self.Nxx]
        P3[:,self.Nxx-self.Na:self.Nxx] = P3[:,self.Nxx-self.Na:self.Nxx] * self.fat_d[:,self.Nxx-self.Na:self.Nxx]

        # --------------- Reynolds Boundary ---------------
        #sup
        P3[:2,:] = P2[:2,:] + self.A[:2,:] * (P2[1:3, :] - P2[:2,:])

        #inf
        P3[self.Nzz-2:self.Nzz,:] = P2[self.Nzz-2:self.Nzz,:] - self.A[self.Nzz-2:self.Nzz,:] * (P2[self.Nzz-2:self.Nzz,:] - P2[self.Nzz-3:self.Nzz-1,:])

        #esq
        P3[:,:2] = P2[:,:2] + self.A[:,:2] * (P2[:, 1:3] - P2[:,:2])
        
        #dir
        P3[:,self.Nxx-2:self.Nxx] = P2[:,self.Nxx-2:self.Nxx] - self.A[:,self.Nxx-2:self.Nxx] * (P2[:, self.Nxx-2:self.Nxx] - P2[:,self.Nxx-3:self.Nxx-1])

        return P1, P2, P3