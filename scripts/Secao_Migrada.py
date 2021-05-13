from Sismograma import Sismograma
import matplotlib.pyplot as plt
from os import path


class Secao_Migrada(Sismograma):
    
    def __init__(self):

        Sismograma.__init__(self)
    
    def build(self, operacao = 'modelar'):

        self.interpolate(operacao)

    def section_plot(self, number = '1'):

        if number == '1':
            array = self.aux
        elif number == '2':
            array = self.aux2
        elif number == '3':
            array = self.aux3
        else:
            raise ValueError ('Seção Incorreta.')

        array[:,:] = array[:,:] / array.min()

        print((array[:,:] / array.min()).min())
        print((array[:,:] / array.min()).max())

        plt.imshow(array[self.Na + self.Wl:-self.Na,self.Na:-self.Na] / array[self.Na + self.Wl:-self.Na,self.Na:-self.Na].min(), cmap='gray')

    def save_bins(self):
        
        lista_arrays = [self.extended_model, self.fonte, self.sis, self.aux, self.aux2, self.aux3]
        lista_nomes = ['Extended_Model', 'Ricker_Wavelet', 'Seismogram', '1st_Migrated_Section', '2nd_Migrated_Section', '3rd_Migrated_Section']

        for i in range(len(lista_arrays)):

            if len(lista_arrays[i].shape) == 1:
                arquivo = f'{lista_nomes[i]}_{lista_arrays[i].shape[0]}.bin'

            elif len(lista_arrays[i].shape) == 2:
                arquivo = f'{lista_nomes[i]}_{lista_arrays[i].shape[0]}x{lista_arrays[i].shape[1]}.bin'

            elif len(lista_arrays[i].shape) == 3:
                arquivo = f'{lista_nomes[i]}_{lista_arrays[i].shape[2]}x{lista_arrays[i].shape[0]}x{lista_arrays[i].shape[1]}.bin'

            pathfile = path.abspath(path.dirname(__file__))
            workfile = path.join(pathfile, '..', 'output', arquivo)

            with open(workfile, 'wb') as archieve:
                lista_arrays[i].tofile(archieve)



