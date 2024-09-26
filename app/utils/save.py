import os

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

from app.config import PASTA_OUTPUT_BINARIOS, PASTA_OUTPUT_PLOTS
from app.models.ricker import RickerWavelet
from app.models.secao import Secao


def salvar_plot_secao(secao: Secao, cmap="cividis"):
    print("Salvando plots da seção...")

    for tipo in ("original", "extended"):
        if tipo == "original":
            modelo = secao.array
            nome = "Marmousi"
            xmax = secao.Nx * secao.dx
            zmax = secao.Nz * secao.dx

        elif tipo == "extended":
            modelo = secao.extended_array
            nome = "Marmousi Extendido"
            xmax = secao.Nxx * secao.dx
            zmax = secao.Nzz * secao.dx

        caminho_arquivo = os.path.join(PASTA_OUTPUT_PLOTS, f"{nome}.png")

        ## Eixo horizontal no topo da figura
        plt.rcParams["xtick.bottom"] = False
        plt.rcParams["xtick.labelbottom"] = False
        plt.rcParams["xtick.top"] = True
        plt.rcParams["xtick.labeltop"] = True

        plt.rc("xtick", labelsize=12)
        plt.rc("ytick", labelsize=12)
        plt.rcParams.update({"font.size": 12})

        ## Formatação do plot
        fig, ax = plt.subplots(figsize=(10, 15))
        ax.xaxis.set_label_position("top")
        im = ax.imshow(
            modelo, cmap=cmap, extent=[0, xmax, zmax, 0], interpolation="bicubic"
        )
        plt.title(nome)
        plt.xlabel("Distance (m)", fontsize=12)
        plt.ylabel("Profundidade (m)", fontsize=12)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        plt.savefig(caminho_arquivo, dpi=500, bbox_inches="tight")  # , transparent=True

    print("Plots da seção salvo com sucesso\n")


def salvar_plot_ricker_wavelet(ricker_wavelet: RickerWavelet):
    print("Salvando plot da Ricker Wavelet...")
    caminho_arquivo = os.path.join(
        PASTA_OUTPUT_PLOTS, f"Ricker_Wavelet_{ricker_wavelet.fcorte}Hz.png"
    )

    fig = plt.figure(figsize=(8, 6))
    eixo = fig.add_axes([0, 0, 1, 1])
    eixo.plot(ricker_wavelet.t, -ricker_wavelet.fonte)
    eixo.set_title("Ricker Wavelet", fontsize=18)
    eixo.set_xlabel("Tempo (s)", fontsize=15)
    eixo.set_ylabel("Amplitude (Hz)", fontsize=15)
    eixo.grid(True)
    fig.savefig(caminho_arquivo, dpi=500, bbox_inches="tight")  # , transparent=True)

    print("Plot da Ricker Wavelet salvo com sucesso\n")


def salvar_plot_sismograma(
    secao: Secao,
    ricker_wavelet: RickerWavelet,
    matriz_sismograma: np.ndarray,
    cmap="gray",
):
    print("Salvando plot do sismograma...")

    caminho_arquivo = os.path.join(PASTA_OUTPUT_PLOTS, "Sismograma.png")

    ## Eixos em dimensões reais
    scaleX = 1.0 / 1000
    scaleZ = 1

    Xmin = (0 * secao.dx) * scaleX
    Xmax = (secao.Nx * secao.dx) * scaleX
    Zmin = (0 * ricker_wavelet.dt) * scaleZ
    Zmax = (secao.ntotal * ricker_wavelet.dt) * scaleZ

    ## Eixo horizontal no topo da figura
    plt.rcParams["xtick.bottom"] = False
    plt.rcParams["xtick.labelbottom"] = False
    plt.rcParams["xtick.top"] = True
    plt.rcParams["xtick.labeltop"] = True

    plt.rc("xtick", labelsize=13)
    plt.rc("ytick", labelsize=13)
    plt.rcParams.update({"font.size": 13})

    ## Formatação do plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.xaxis.set_label_position("top")
    im = ax.imshow(
        matriz_sismograma,
        cmap="gray",
        vmin=-0.01,
        vmax=0.01,
        extent=[Xmin, Xmax, Zmax, Zmin],
        interpolation="bicubic",
        aspect=2,
    )
    plt.title("Sismograma", fontsize=18)
    plt.xlabel("Position (Km)", fontsize=13)
    plt.ylabel("Time (s)", fontsize=13)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)

    plt.savefig(caminho_arquivo, dpi=1000, bbox_inches="tight")

    print("Plot do sismograma salvo com sucesso\n")


def salvar_plot_secao_migrada(
    secao: Secao, numero: int, array: np.ndarray, cmap="gray"
):
    print(f"Salvando plot da seção migrada {numero}...")

    array_normalizado_fora_bordas = (
        array[secao.Na + secao.Wl : -secao.Na, secao.Na : -secao.Na]
        / array[secao.Na + secao.Wl : -secao.Na, secao.Na : -secao.Na].min()
    )

    nome = f"Seção Migrada {numero}"

    caminho_arquivo = os.path.join(PASTA_OUTPUT_PLOTS, f"{nome}.png")

    fig, ax = plt.subplots(figsize=(10, 15))
    ax.xaxis.set_label_position("top")
    im = ax.imshow(array_normalizado_fora_bordas, cmap=cmap, interpolation="bicubic")
    plt.title(nome)
    plt.xlabel("Distance (m)", fontsize=12)
    plt.ylabel("Profundidade (m)", fontsize=12)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
    plt.savefig(caminho_arquivo, dpi=500, bbox_inches="tight")  # , transparent=True

    print(f"Plot da seção migrada {numero} salvo com sucesso\n")


def salvar_plot_secao_generica(nome: str, array: np.ndarray):
    print(f"Salvando plot da seção {nome}...")

    caminho_arquivo = os.path.join(PASTA_OUTPUT_PLOTS, f"{nome}.png")

    fig, ax = plt.subplots(figsize=(10, 15))
    ax.xaxis.set_label_position("top")
    im = ax.imshow(array, interpolation="bicubic")
    plt.title(nome)
    plt.xlabel("Distance (m)", fontsize=12)
    plt.ylabel("Profundidade (m)", fontsize=12)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
    plt.savefig(caminho_arquivo, dpi=500, bbox_inches="tight")  # , transparent=True

    print(f"Plot da seção {nome} salvo com sucesso\n")


def salvar_binarios(
    extended_model: np.ndarray,
    fonte: np.ndarray,
    matriz_sismograma: np.ndarray,
    aux: np.ndarray,
    aux2: np.ndarray,
    aux3: np.ndarray,
) -> None:
    print("Salvando binários...")

    lista_arrays = [
        extended_model,
        fonte,
        matriz_sismograma,
        aux,
        aux2,
        aux3,
    ]
    lista_nomes = [
        "Extended_Model",
        "Ricker_Wavelet",
        "Seismogram",
        "1st_Migrated_Section",
        "2nd_Migrated_Section",
        "3rd_Migrated_Section",
    ]

    for i in range(len(lista_arrays)):
        if len(lista_arrays[i].shape) == 1:
            arquivo = f"{lista_nomes[i]}_{lista_arrays[i].shape[0]}.bin"

        elif len(lista_arrays[i].shape) == 2:
            arquivo = f"{lista_nomes[i]}_{lista_arrays[i].shape[0]}x{lista_arrays[i].shape[1]}.bin"

        elif len(lista_arrays[i].shape) == 3:
            arquivo = f"{lista_nomes[i]}_{lista_arrays[i].shape[2]}x{lista_arrays[i].shape[0]}x{lista_arrays[i].shape[1]}.bin"

        caminho_arquivo = os.path.join(PASTA_OUTPUT_BINARIOS, arquivo)

        with open(caminho_arquivo, "wb") as archieve:
            lista_arrays[i].tofile(archieve)

    print("Binários salvos com sucesso\n")
