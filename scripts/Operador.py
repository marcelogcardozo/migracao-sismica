from Boundary import Boundary
from Ricker import Ricker
import numpy as np


class Operador(Boundary, Ricker):
    def __init__(self):

        Boundary.__init__(self)
        Ricker.__init__(self)

    def interpolate(self, boundary=True):
        
        P1 = np.zeros((self.Nzz, self.Nxx))               # Matriz no tempo passado
        P2 = np.zeros((self.Nzz, self.Nxx))               # Matriz no tempo presente
        P3 = np.zeros((self.Nzz, self.Nxx))               # Matriz no tempo futuro

        self.Asc = np.empty((self.Nzz, self.Nxx, self.ntotal))

        print("\nModelando...\n")
        for n in range(0,self.ntotal,1):
            
            # Termo fonte
            if n < self.Nf:
                P2[self.shot_z,self.shot_x] += (self.fonte[n] * (self.A[self.shot_z, self.shot_x] ** 2))
        
            P3[2:self.Nzz-2, 2:self.Nxx-2] = self.C[2:self.Nzz-2, 2:self.Nxx-2] * (P2[2:self.Nzz-2, 4:self.Nxx] + P2[2:self.Nzz-2, :self.Nxx-4] + P2[4:self.Nzz, 2:self.Nxx-2] + P2[:self.Nzz-4, 2:self.Nxx-2] - 16 * (P2[2:self.Nzz-2, 3:self.Nxx-1] + P2[2:self.Nzz-2, 1:self.Nxx-3] + P2[3:self.Nzz-1, 2:self.Nxx-2] + P2[1:self.Nzz-3, 2:self.Nxx-2]) + 60 * (P2[2:self.Nzz-2, 2:self.Nxx-2])) + 2 * (P2[2:self.Nzz-2, 2:self.Nxx-2]) - P1[2:self.Nzz-2, 2:self.Nxx-2]

            if boundary:

                P1, P2, P3 = self.apply_boundary(P1, P2, P3)

            # Atualização do campo de onda
            P1 = np.copy(P2)
            P2 = np.copy(P3)
            
            self.Asc[:,:,n] = P3[:,:]
            
            if n % 1000 == 0: print('Passo: ', n)