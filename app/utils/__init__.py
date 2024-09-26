import json

from app.models.ricker import RickerWavelet
from app.models.secao import Secao


def get_parametros() -> dict:
    print("-- PARÂMETROS --\n")
    print('Abrindo arquivo de configuração "app.config.json"')

    with open("app.config.json") as f:
        parametros = json.load(f)

    print("Parâmetros carregados com sucesso\n")
    return parametros


def gerar_fonte_ricker(parametros: dict) -> RickerWavelet:
    print("-- FONTE --\n")
    print("Gerando a Ricker Wavelet...")

    ricker_wavelet = RickerWavelet(parametros)

    print("Ricker Wavelet gerada com sucesso.\n")
    return ricker_wavelet


def criar_secao(parametros: dict, homogeneo: bool, otimizar: bool) -> Secao:
    print("-- SEÇÃO --\n")
    print("Criando modelo da seção sísmica...")

    secao = Secao(parametros)

    print("Modelo criado com sucesso.")
    print("Gerando array da seção...")

    secao.criar_matriz_modelo(homogeneo)

    print("Array gerado com sucesso.")
    print("Adicionando bordas de absorção...")

    secao.adicionar_bordas_absorcao()

    print("Bordas de absorção adicionadas com sucesso.\n")

    return secao
