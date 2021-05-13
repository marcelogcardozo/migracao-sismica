from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from Operador import Operador
import os.path


class Sismograma(Operador):

    def __init__(self):

        Operador.__init__(self)
 
    def sis_plot(self, cmap='gray'):

        ## Eixos em dimensões reais
        scaleX = 1.0 / 1000
        scaleZ = 1

        Xmin = (0 * self.h) * scaleX
        Xmax = (self.Nx * self.h) * scaleX
        Zmin = (0 * self.dt) * scaleZ
        Zmax = (self.ntotal * self.dt) * scaleZ

        # Diretório para salvar a imagem
        pathfile = os.path.abspath(os.path.dirname(__file__))
        workfile = os.path.join(pathfile, '..', 'output', 'Sismograma.png')

        ## Eixo horizontal no topo da figura
        plt.rcParams['xtick.bottom'] = False
        plt.rcParams['xtick.labelbottom'] = False
        plt.rcParams['xtick.top'] = True
        plt.rcParams['xtick.labeltop'] = True

        plt.rc('xtick', labelsize=13)    
        plt.rc('ytick', labelsize=13)
        plt.rcParams.update({'font.size':13})

        ## Formatação do plot
        fig, ax = plt.subplots(figsize=(10,5))
        ax.xaxis.set_label_position('top')
        im = ax.imshow(self.sis, cmap='gray', vmin=-0.01, vmax=0.01 , extent=[Xmin,Xmax,Zmax,Zmin], interpolation='bicubic', aspect=2)
        plt.title('Sismograma', fontsize=18)
        plt.xlabel('Position (Km)', fontsize=13)
        plt.ylabel('Time (s)', fontsize=13)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)

        plt.savefig(workfile, dpi=1000, bbox_inches='tight')