from Parametros import Parametros
import matplotlib.pyplot as plt
import numpy as np
import os.path


class Ricker(Parametros):
    def __init__(self):
        
        Parametros.__init__(self)

        self.fonte, self.t = self.ricker_wavelet()

    def ricker_wavelet(self):
        self.Nf = int(4 * np.sqrt(np.pi) / (self.fcorte * self.dt))   
        TF = 2 * np.sqrt(np.pi) / self.fcorte     # Período da função Gaussiana
        fc = self.fcorte / (3. * np.sqrt(np.pi))        # Frequência central
        
        source = np.zeros(self.Nf)
        t = np.zeros(self.Nf)

        for n in range(self.Nf):
            t[n] = n * self.dt - TF
            source[n] = (-np.exp(-np.pi * (np.pi * fc * t[n]) ** 2) * (1 - 2 * np.pi * (np.pi * fc * t[n]) * (np.pi * fc * t[n])))
  
        return source, t

    def ricker_plot(self):

        pathfile = os.path.abspath(os.path.dirname(__file__))
        workfile = os.path.join(pathfile, '..', 'output', f'Ricker_Wavelet_{self.fcorte}Hz.png')

        fig = plt.figure(figsize=(8,6))
        eixo = fig.add_axes([0,0,1,1])
        eixo.plot(self.t,-self.fonte)
        eixo.set_title('Ricker Wavelet', fontsize=18)
        eixo.set_xlabel('Tempo (s)', fontsize=15)
        eixo.set_ylabel('Amplitude (Hz)', fontsize=15)
        eixo.grid(True)
        fig.savefig(workfile, dpi=1000, bbox_inches='tight', transparent=True)