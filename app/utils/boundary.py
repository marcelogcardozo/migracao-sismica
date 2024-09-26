import numpy as np

from app.models.ricker import RickerWavelet
from app.models.secao import Secao


def calcula_matrizes_auxiliares_A_C(
    secao: Secao, ricker_wavelet: RickerWavelet
) -> list[np.ndarray, np.ndarray]:
    print("-- MATRIZES AUXILIARES A e C --\n")

    print("Gerando matrizes...")

    C = np.zeros(
        (secao.Nzz, secao.Nxx)
    )  # Matriz para simplificação da equação da onda discretizada
    A = np.zeros(
        (secao.Nzz, secao.Nxx)
    )  # Matriz para simplificação da equação de bordas não reflexivas

    A[:, :] = secao.extended_array[:, :] * (ricker_wavelet.dt / secao.dx)
    C[:, :] = -(A[:, :] ** 2) / 12

    print("Matrizes geradas com sucesso\n")

    return A, C


def calcula_matrizes_com_fatores_absorcao(
    secao: Secao,
) -> list[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    print("-- MATRIZES ABSORÇÃO --\n")

    print("Calculando matrizes com fatores de absorção...")

    fat_s = np.ones(
        (secao.Nzz, secao.Nxx)
    )  # Fator de absorção da borda superior, inferior, esquerda e direita
    fat_d = np.ones((secao.Nzz, secao.Nxx))
    fat_i = np.ones((secao.Nzz, secao.Nxx))
    fat_e = np.ones((secao.Nzz, secao.Nxx))

    for i in range(secao.Na):
        fat_s[i, :] = np.exp(-((secao.fat * (secao.Na - i)) ** 2))
        fat_e[:, i] = np.exp(-((secao.fat * (secao.Na - i)) ** 2))

    for i in range(secao.Nzz - secao.Na, secao.Nzz):
        fat_i[i, :] = np.exp(-((secao.fat * (secao.Nzz - secao.Na - i)) ** 2))

    for i in range(secao.Nxx - secao.Na, secao.Nxx):
        fat_d[:, i] = np.exp(-((secao.fat * (secao.Nxx - secao.Na - i)) ** 2))

    print("Matrizes calculadas com sucesso\n")

    return fat_s, fat_d, fat_i, fat_e


def aplica_absorcao_nas_bordas(
    secao: Secao,
    P1: np.ndarray,
    P2: np.ndarray,
    P3: np.ndarray,
    A: np.ndarray,
    fat_s: np.ndarray,
    fat_d: np.ndarray,
    fat_i: np.ndarray,
    fat_e: np.ndarray,
):
    # --------------- Cerjan Boundary ---------------
    # sup
    P2[: secao.Na, 2 : secao.Nxx - 2] = (
        P2[: secao.Na, 2 : secao.Nxx - 2] * fat_s[: secao.Na, 2 : secao.Nxx - 2]
    )
    P3[: secao.Na, 2 : secao.Nxx - 2] = (
        P3[: secao.Na, 2 : secao.Nxx - 2] * fat_s[: secao.Na, 2 : secao.Nxx - 2]
    )

    # inf
    P2[secao.Nzz - secao.Na : secao.Nzz, 2 : secao.Nxx - 2] = (
        P2[secao.Nzz - secao.Na : secao.Nzz, 2 : secao.Nxx - 2]
        * fat_i[secao.Nzz - secao.Na : secao.Nzz, 2 : secao.Nxx - 2]
    )
    P3[secao.Nzz - secao.Na : secao.Nzz, 2 : secao.Nxx - 2] = (
        P3[secao.Nzz - secao.Na : secao.Nzz, 2 : secao.Nxx - 2]
        * fat_i[secao.Nzz - secao.Na : secao.Nzz, 2 : secao.Nxx - 2]
    )

    # esq
    P2[:, : secao.Na] = P2[:, : secao.Na] * fat_e[:, : secao.Na]
    P3[:, : secao.Na] = P3[:, : secao.Na] * fat_e[:, : secao.Na]

    # dir
    P2[:, secao.Nxx - secao.Na : secao.Nxx] = (
        P2[:, secao.Nxx - secao.Na : secao.Nxx]
        * fat_d[:, secao.Nxx - secao.Na : secao.Nxx]
    )
    P3[:, secao.Nxx - secao.Na : secao.Nxx] = (
        P3[:, secao.Nxx - secao.Na : secao.Nxx]
        * fat_d[:, secao.Nxx - secao.Na : secao.Nxx]
    )

    # --------------- Reynolds Boundary ---------------
    # sup
    P3[:2, :] = P2[:2, :] + A[:2, :] * (P2[1:3, :] - P2[:2, :])

    # inf
    P3[secao.Nzz - 2 : secao.Nzz, :] = P2[secao.Nzz - 2 : secao.Nzz, :] - A[
        secao.Nzz - 2 : secao.Nzz, :
    ] * (P2[secao.Nzz - 2 : secao.Nzz, :] - P2[secao.Nzz - 3 : secao.Nzz - 1, :])

    # esq
    P3[:, :2] = P2[:, :2] + A[:, :2] * (P2[:, 1:3] - P2[:, :2])

    # dir
    P3[:, secao.Nxx - 2 : secao.Nxx] = P2[:, secao.Nxx - 2 : secao.Nxx] - A[
        :, secao.Nxx - 2 : secao.Nxx
    ] * (P2[:, secao.Nxx - 2 : secao.Nxx] - P2[:, secao.Nxx - 3 : secao.Nxx - 1])

    return P1, P2, P3
