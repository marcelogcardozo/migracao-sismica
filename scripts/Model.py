from mpl_toolkits.axes_grid1 import make_axes_locatable
from Parametros import Parametros
import matplotlib.pyplot as plt
import numpy as np
import os.path


class Model(Parametros):
    def __init__(self, homo=False, smooth=False, optimize=False):

        Parametros.__init__(self)

        self.Nxx = self.Nx + 2 * self.Na
        self.Nzz = self.Nz + self.Wl + 2 * self.Na

        if homo:
            self.model = np.empty((self.Nz + self.Wl, self.Nx))
            self.extended_model = np.empty((self.Nzz,self.Nxx))

            self.model[:,:] = 1500
            self.extended_model[:,:] = 1500
        else:
            self.model, self.extended_model = self.get_models()
       

    def get_models(self):
    
        def add_boundary(model):
        
            extended_model = np.empty((self.Nzz, self.Nxx))

            # Criando bordas
            extended_model[self.Na:-self.Na,self.Na:-self.Na] = model[:,:]
            
            for i in range(self.Na):
                # Borda superior
                extended_model[i, self.Na:-self.Na] = extended_model[self.Na + 20, self.Na:-self.Na]     
                #Borda inferior     
                extended_model[self.Nz + self.Na + i, self.Na:-self.Na] = extended_model[self.Na + self.Nz - 1, self.Na:-self.Na]     
                # Borda lateral esquerda
                extended_model[self.Na:-self.Na, i] = extended_model[self.Na:-self.Na, self.Na + 1]
                # Borda lateral direita
                extended_model[self.Na:-self.Na, self.Na + self.Nx + i] = extended_model[self.Na:-self.Na, self.Na + self.Nx - 1]
                # Borda quina superior esquerda
                extended_model[:self.Na, :self.Na] = extended_model[self.Na + 1, self.Na + 1]
                # Borda quina superior direita
                extended_model[:self.Na, self.Na + self.Nx:] = extended_model[self.Na + 1, self.Na + self.Nx - 1]
                
                # Borda quina inferior esquerda
                extended_model[-self.Na:, :self.Na] = extended_model[self.Nz + self.Na - 1, self.Na + 1]
                # Borda quina inferior direita
                extended_model[-self.Na:, self.Na + self.Nx:] = extended_model[self.Na + self.Nz - 1, self.Na + self.Nx - 1]

            return extended_model
        
        pathfile = os.path.abspath(os.path.dirname(__file__))
        workfile = os.path.join(pathfile, '..', 'models', self.file_name)
        
        model = np.fromfile(workfile, dtype=np.float32).reshape(self.Nx, self.Nz).T
            
        # Adicionando camada de água 
        self.Nz += self.Wl

        model_camada_de_agua = np.empty((self.Nz, self.Nx))
        model_camada_de_agua[:self.Wl,:] = model.min()
        model_camada_de_agua[self.Wl:,:] = model[:,:]

        extended_model = add_boundary(model_camada_de_agua)


        return model_camada_de_agua, extended_model
        
    def normalize(self, P):
        P[:,:] /= P.min()
        return P
    
    def model_plot(self, type='original', cmap='cividis'):      

        if type.lower() == 'original':
            modelo = self.model
            nome = 'Marmousi'
            xmax = self.Nx * self.h
            zmax = self.Nz * self.h
            escala = 1/1000

        elif type.lower() == 'extended':
            modelo = self.extended_model
            nome = 'Marmousi Extendido'
            xmax = self.Nxx * self.h
            zmax = self.Nzz * self.h
            escala = 1/1000

        elif type.lower() != 'original':
            raise ValueError ('Parâmetro Incorreto.')

        pathfile = os.path.abspath(os.path.dirname(__file__))
        workfile = os.path.join(pathfile, '..', 'output', nome + '.png')


        ## Eixo horizontal no topo da figura
        plt.rcParams['xtick.bottom'] = False
        plt.rcParams['xtick.labelbottom'] = False
        plt.rcParams['xtick.top'] = True
        plt.rcParams['xtick.labeltop'] = True

        plt.rc('xtick', labelsize=12)    
        plt.rc('ytick', labelsize=12)
        plt.rcParams.update({'font.size':12})

        ## Formatação do plot
        fig, ax = plt.subplots(figsize=(10,15))
        ax.xaxis.set_label_position('top')
        im = ax.imshow(modelo, cmap = cmap, extent=[0,xmax,zmax,0], interpolation='bicubic')
        plt.title(nome)
        plt.xlabel('Distance (m)', fontsize=12)
        plt.ylabel('Profundidade (m)', fontsize=12)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        plt.savefig(workfile, dpi=1000, bbox_inches='tight', transparent=True)
        plt.grid(True)
        plt.show()
        