from Boundary import Boundary
from Ricker import Ricker
import numpy as np


class Operador(Boundary, Ricker):
    def __init__(self):

        Boundary.__init__(self)
        Ricker.__init__(self)

    def interpolate(self, type, boundary=True):
        
        type = type.lower()

        if type == 'modelar':

            P1 = np.empty((self.Nzz, self.Nxx))               # Matriz no tempo passado
            P2 = np.empty((self.Nzz, self.Nxx))               # Matriz no tempo presente
            P3 = np.empty((self.Nzz, self.Nxx))               # Matriz no tempo futuro

            self.sis = np.empty((self.ntotal, self.Nx))
            self.Asc = np.empty((self.Nzz, self.Nxx, self.ntotal))

            inicio = 0
            fim = self.ntotal
            passo = 1
            print("\nModelando...\n")

        elif type == 'migrar':

            P1 = np.zeros((self.Nzz, self.Nxx))               # Matriz no tempo passado
            P2 = np.zeros((self.Nzz, self.Nxx))               # Matriz no tempo presente
            P3 = np.zeros((self.Nzz, self.Nxx))               # Matriz no tempo futuro

            self.aux = np.zeros((self.Nzz, self.Nxx))        
            self.aux2 = np.zeros((self.Nzz, self.Nxx))
            self.aux3 = np.zeros((self.Nzz, self.Nxx))

            inicio = self.ntotal - 1
            fim = - 1
            passo = - 1
            print("Migrando...\n")

        else:
            raise ValueError('Tipo incorreto de operador.')


        for n in range(inicio,fim,passo):
            
            if type == 'modelar':
                # Termo fonte
                if n < self.Nf:
                    P2[self.shot_z,self.shot_x] += (self.fonte[n] * (self.A[self.shot_z, self.shot_x] ** 2))

            elif type == 'migrar':
                
                P2[self.rec_shotz,self.Na:-self.Na] += self.sis[n,:]

            P3[2:self.Nzz-2, 2:self.Nxx-2] = self.C[2:self.Nzz-2, 2:self.Nxx-2] * (P2[2:self.Nzz-2, 4:self.Nxx] + P2[2:self.Nzz-2, :self.Nxx-4] + P2[4:self.Nzz, 2:self.Nxx-2] + P2[:self.Nzz-4, 2:self.Nxx-2] - 16 * (P2[2:self.Nzz-2, 3:self.Nxx-1] + P2[2:self.Nzz-2, 1:self.Nxx-3] + P2[3:self.Nzz-1, 2:self.Nxx-2] + P2[1:self.Nzz-3, 2:self.Nxx-2]) + 60 * (P2[2:self.Nzz-2, 2:self.Nxx-2])) + 2 * (P2[2:self.Nzz-2, 2:self.Nxx-2]) - P1[2:self.Nzz-2, 2:self.Nxx-2]

            if boundary:

                P1, P2, P3 = self.apply_boundary(P1, P2, P3)

            # Atualização do campo de onda
            P1 = np.copy(P2)
            P2 = np.copy(P3)
            
            if type == 'modelar':
                self.Asc[:,:,n] = P3[:,:]
                self.sis[n,:] = self.Asc[self.rec_shotz,self.Na:-self.Na, n]

            elif type == 'migrar':

                self.aux[:,:] += P3[:,:] * self.Asc[:,:,n]
                self.aux2[:,:] += self.aux[:,:] / (P3[:,:] ** 2 + 0.00000000000000000000000000000000000000000000000000001)
                self.aux3[:,:] += self.aux[:,:] / (self.Asc[:,:,n] ** 2 + 0.00000000000000000000000000000000000000000000000000001)

            if n % 1000 == 0: print('Passo: ', n)

        print("\n")