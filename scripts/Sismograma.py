from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import numpy as np
import os.path

class Sismograma:

    def __init__(self, operador):

        self.op = operador

    def build(self):
  
        self.op.sis = np.empty((self.op.ntotal, self.op.Nx))

        for i in range(self.op.ntotal):
            self.op.sis[i,:] = self.op.Asc[self.op.rec_shotz,self.op.Na:-self.op.Na, i]
    
    def plot(self, cmap='gray'):

        ## Eixos em dimensões reais
        scaleX = 1.0 / 1000
        scaleZ = 1

        Xmin = (0 * self.op.h) * scaleX
        Xmax = (self.op.Nx * self.op.h) * scaleX
        Zmin = (0 * self.op.dt) * scaleZ
        Zmax = (self.op.ntotal * self.op.dt) * scaleZ

        pathfile = os.path.abspath(os.path.dirname(__file__))
        workfile = os.path.join(pathfile, '..', 'output', 'Sismograma.png')


        ## Eixo horizontal no topo da figura
        plt.rcParams['xtick.bottom'] = False
        plt.rcParams['xtick.labelbottom'] = False
        plt.rcParams['xtick.top'] = True
        plt.rcParams['xtick.labeltop'] = True

        plt.rc('xtick', labelsize=16)    
        plt.rc('ytick', labelsize=16)
        plt.rcParams.update({'font.size':16})

        ## Formatação do plot
        fig, ax = plt.subplots(figsize=(12,6))
        ax.xaxis.set_label_position('top')
        im = ax.imshow(self.op.sis, cmap='gray', vmin=-0.01, vmax=0.01 , extent=[Xmin,Xmax,Zmax,Zmin], interpolation='bicubic', aspect=2)
        plt.title('Sismograma', fontsize=18)
        plt.xlabel('Position (Km)', fontsize=16)
        plt.ylabel('Time (s)', fontsize=16)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)

        plt.savefig(workfile, dpi=500,bbox_inches='tight')