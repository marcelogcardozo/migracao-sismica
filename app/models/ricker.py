import numpy as np


class RickerWavelet:
    def __init__(self, parametros: dict) -> None:
        self.get_atributos(parametros)

        self.fonte, self.t = self.get_ricker_wavelet()

    def get_atributos(self, parametros: dict):
        Na = parametros["grid"]["Na"]

        self.fcorte = parametros["fonte"]["fcorte"]
        self.dt = parametros["parameters"]["dt"]
        self.shot_z = parametros["fonte"]["shot_z"] + Na
        self.shot_x = parametros["fonte"]["shot_x"] + Na
        self.rec_shotz = parametros["fonte"]["rec_shotz"] + Na

        self.Nf = int(4 * np.sqrt(np.pi) / (self.fcorte * self.dt))

    def get_ricker_wavelet(self):
        TF = 2 * np.sqrt(np.pi) / self.fcorte  # Período da função Gaussiana
        fc = self.fcorte / (3.0 * np.sqrt(np.pi))  # Frequência central

        source = np.zeros(self.Nf)
        t = np.zeros(self.Nf)

        for n in range(self.Nf):
            t[n] = n * self.dt - TF
            source[n] = -np.exp(-np.pi * (np.pi * fc * t[n]) ** 2) * (
                1 - 2 * np.pi * (np.pi * fc * t[n]) * (np.pi * fc * t[n])
            )

        return source, t
