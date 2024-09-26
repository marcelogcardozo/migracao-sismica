import numpy as np

from app.models.ricker import RickerWavelet
from app.models.secao import Secao
from app.utils.boundary import aplica_absorcao_nas_bordas


def modelar_secao(
    secao: Secao,
    ricker_wavelet: RickerWavelet,
    A: np.ndarray,
    C: np.ndarray,
    fat_s: np.ndarray,
    fat_d: np.ndarray,
    fat_i: np.ndarray,
    fat_e: np.ndarray,
    boundary=True,
) -> list[np.ndarray, np.ndarray]:
    print("-- MODELAGEM --\n")

    P1 = np.empty((secao.Nzz, secao.Nxx))  # Matriz no tempo passado
    P2 = np.empty((secao.Nzz, secao.Nxx))  # Matriz no tempo presente
    P3 = np.empty((secao.Nzz, secao.Nxx))  # Matriz no tempo futuro

    matriz_sismograma = np.empty((secao.ntotal, secao.Nx))
    matriz_ascendente = np.empty((secao.Nzz, secao.Nxx, secao.ntotal))

    inicio = 0
    fim = secao.ntotal
    passo = 1

    print(f"N total: {secao.ntotal}")

    print("Modelando a seção sísmica...")

    for n in range(inicio, fim, passo):
        if (n + 1) % 1000 == 0 or (n + 1) == fim:
            print(f"\tProgresso: {n+1}")

        # Termo fonte
        if n < ricker_wavelet.Nf:
            P2[ricker_wavelet.shot_z, ricker_wavelet.shot_x] += (
                ricker_wavelet.fonte[n]
            ) * (A[ricker_wavelet.shot_z, ricker_wavelet.shot_x] ** 2)

        P3[2 : secao.Nzz - 2, 2 : secao.Nxx - 2] = (
            C[2 : secao.Nzz - 2, 2 : secao.Nxx - 2]
            * (
                P2[2 : secao.Nzz - 2, 4 : secao.Nxx]
                + P2[2 : secao.Nzz - 2, : secao.Nxx - 4]
                + P2[4 : secao.Nzz, 2 : secao.Nxx - 2]
                + P2[: secao.Nzz - 4, 2 : secao.Nxx - 2]
                - 16
                * (
                    P2[2 : secao.Nzz - 2, 3 : secao.Nxx - 1]
                    + P2[2 : secao.Nzz - 2, 1 : secao.Nxx - 3]
                    + P2[3 : secao.Nzz - 1, 2 : secao.Nxx - 2]
                    + P2[1 : secao.Nzz - 3, 2 : secao.Nxx - 2]
                )
                + 60 * (P2[2 : secao.Nzz - 2, 2 : secao.Nxx - 2])
            )
            + 2 * (P2[2 : secao.Nzz - 2, 2 : secao.Nxx - 2])
            - P1[2 : secao.Nzz - 2, 2 : secao.Nxx - 2]
        )

        if boundary:
            P1, P2, P3 = aplica_absorcao_nas_bordas(
                secao, P1, P2, P3, A, fat_s, fat_d, fat_i, fat_e
            )

        P1 = np.copy(P2)
        P2 = np.copy(P3)

        matriz_ascendente[:, :, n] = P3[:, :]
        matriz_sismograma[n, :] = matriz_ascendente[
            ricker_wavelet.rec_shotz, secao.Na : -secao.Na, n
        ]

    print("Modelagem concluída.")
    print("Sismograma gerado com sucesso\n")

    return matriz_sismograma, matriz_ascendente


def migrar_secao(
    secao: Secao,
    ricker_wavelet: RickerWavelet,
    A: np.ndarray,
    C: np.ndarray,
    fat_s: np.ndarray,
    fat_d: np.ndarray,
    fat_i: np.ndarray,
    fat_e: np.ndarray,
    matriz_sismograma: np.ndarray,
    matriz_ascendente: np.ndarray,
    boundary=True,
) -> list[np.ndarray, np.ndarray, np.ndarray]:
    print("-- MIGRAÇÃO --\n")

    P1 = np.zeros((secao.Nzz, secao.Nxx))  # Matriz no tempo passado
    P2 = np.zeros((secao.Nzz, secao.Nxx))  # Matriz no tempo presente
    P3 = np.zeros((secao.Nzz, secao.Nxx))  # Matriz no tempo futuro

    aux = np.zeros((secao.Nzz, secao.Nxx))
    aux2 = np.zeros((secao.Nzz, secao.Nxx))
    aux3 = np.zeros((secao.Nzz, secao.Nxx))

    inicio = secao.ntotal - 1
    fim = -1
    passo = -1

    print(f"N total: {secao.ntotal}")
    print("Migrando a seção sísmica...")

    for n in range(inicio, fim, passo):
        if (n + 1) % 1000 == 0 or (n + 1) == fim:
            print(f"\tProgresso: {n+1}")

        P2[ricker_wavelet.rec_shotz, secao.Na : -secao.Na] += matriz_sismograma[n, :]

        P3[2 : secao.Nzz - 2, 2 : secao.Nxx - 2] = (
            C[2 : secao.Nzz - 2, 2 : secao.Nxx - 2]
            * (
                P2[2 : secao.Nzz - 2, 4 : secao.Nxx]
                + P2[2 : secao.Nzz - 2, : secao.Nxx - 4]
                + P2[4 : secao.Nzz, 2 : secao.Nxx - 2]
                + P2[: secao.Nzz - 4, 2 : secao.Nxx - 2]
                - 16
                * (
                    P2[2 : secao.Nzz - 2, 3 : secao.Nxx - 1]
                    + P2[2 : secao.Nzz - 2, 1 : secao.Nxx - 3]
                    + P2[3 : secao.Nzz - 1, 2 : secao.Nxx - 2]
                    + P2[1 : secao.Nzz - 3, 2 : secao.Nxx - 2]
                )
                + 60 * (P2[2 : secao.Nzz - 2, 2 : secao.Nxx - 2])
            )
            + 2 * (P2[2 : secao.Nzz - 2, 2 : secao.Nxx - 2])
            - P1[2 : secao.Nzz - 2, 2 : secao.Nxx - 2]
        )

        if boundary:
            P1, P2, P3 = aplica_absorcao_nas_bordas(
                secao, P1, P2, P3, A, fat_s, fat_d, fat_i, fat_e
            )

        # Atualização do campo de onda
        P1 = np.copy(P2)
        P2 = np.copy(P3)

        aux[:, :] += P3[:, :] * matriz_ascendente[:, :, n]
        aux2[:, :] += aux[:, :] / (
            P3[:, :] ** 2 + 0.00000000000000000000000000000000000000000000000000001
        )
        aux3[:, :] += aux[:, :] / (
            matriz_ascendente[:, :, n] ** 2
            + 0.00000000000000000000000000000000000000000000000000001
        )

    print("Migração concluída.")
    print("Seção migrada gerada com sucesso\n")

    return aux, aux2, aux3
