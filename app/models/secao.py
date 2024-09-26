import os

import numpy as np

from app.config import PASTA_BINARIOS


class Secao:
    def __init__(self, parametros: dict) -> None:
        self.get_atributos(parametros)

    def get_atributos(self, parametros: dict):
        self.Nx = parametros["grid"]["Nx"]
        self.Nz = parametros["grid"]["Nz"]
        self.Na = parametros["grid"]["Na"]
        self.Wl = parametros["grid"]["Wl"]
        self.Nxx = self.Nx + 2 * self.Na
        self.Nzz = self.Nz + self.Wl + 2 * self.Na

        self.dx = parametros["parameters"]["dx"]
        self.fat = parametros["parameters"]["fat"]
        self.ntotal = parametros["parameters"]["ntotal"]

        self.nome_arquivo = parametros["model"]["arquivo_binario"]

        self.array = np.empty((self.Nz, self.Nx))
        self.extended_array = np.empty((self.Nzz, self.Nxx))

    def criar_matriz_modelo(self, homogeneo: bool) -> None:
        if homogeneo:
            self.array[:, :] = 1500.0
            return

        caminho_arquivo = os.path.join(PASTA_BINARIOS, self.nome_arquivo)

        model = (
            np.fromfile(caminho_arquivo, dtype=np.float32).reshape(self.Nx, self.Nz).T
        )

        # Adicionando camada de água
        self.Nz += self.Wl

        model_camada_de_agua = np.empty((self.Nz, self.Nx))
        model_camada_de_agua[: self.Wl, :] = model.min()
        model_camada_de_agua[self.Wl :, :] = model[:, :]

        self.array = model_camada_de_agua

    def adicionar_bordas_absorcao(self) -> None:
        extended_model = np.empty((self.Nzz, self.Nxx))

        # Criando bordas
        extended_model[self.Na : -self.Na, self.Na : -self.Na] = self.array[:, :]

        for i in range(self.Na):
            # Borda superior
            extended_model[i, self.Na : -self.Na] = extended_model[
                self.Na + 20, self.Na : -self.Na
            ]
            # Borda inferior
            extended_model[self.Nz + self.Na + i, self.Na : -self.Na] = extended_model[
                self.Na + self.Nz - 1, self.Na : -self.Na
            ]
            # Borda lateral esquerda
            extended_model[self.Na : -self.Na, i] = extended_model[
                self.Na : -self.Na, self.Na + 1
            ]
            # Borda lateral direita
            extended_model[self.Na : -self.Na, self.Na + self.Nx + i] = extended_model[
                self.Na : -self.Na, self.Na + self.Nx - 1
            ]
            # Borda quina superior esquerda
            extended_model[: self.Na, : self.Na] = extended_model[
                self.Na + 1, self.Na + 1
            ]
            # Borda quina superior direita
            extended_model[: self.Na, self.Na + self.Nx :] = extended_model[
                self.Na + 1, self.Na + self.Nx - 1
            ]

            # Borda quina inferior esquerda
            extended_model[-self.Na :, : self.Na] = extended_model[
                self.Nz + self.Na - 1, self.Na + 1
            ]
            # Borda quina inferior direita
            extended_model[-self.Na :, self.Na + self.Nx :] = extended_model[
                self.Na + self.Nz - 1, self.Na + self.Nx - 1
            ]

        self.extended_array = extended_model
