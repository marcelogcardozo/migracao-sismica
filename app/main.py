from app.utils import criar_secao, gerar_fonte_ricker, get_parametros
from app.utils.boundary import (
    calcula_matrizes_auxiliares_A_C,
    calcula_matrizes_com_fatores_absorcao,
)
from app.utils.operator import migrar_secao, modelar_secao
from app.utils.save import (
    salvar_binarios,
    salvar_plot_ricker_wavelet,
    salvar_plot_secao,
    salvar_plot_secao_migrada,
    salvar_plot_sismograma,
)


def main() -> None:
    print("\n---------- PROGRAMA INICIADO ----------\n")

    parametros = get_parametros()

    ricker_wavelet = gerar_fonte_ricker(parametros)

    secao = criar_secao(parametros, homogeneo=False, otimizar=False)

    A, C = calcula_matrizes_auxiliares_A_C(secao, ricker_wavelet)

    fat_s, fat_d, fat_i, fat_e = calcula_matrizes_com_fatores_absorcao(secao)

    matriz_sismograma, matriz_ascendente = modelar_secao(
        secao, ricker_wavelet, A, C, fat_s, fat_d, fat_i, fat_e
    )

    P1, P2, P3 = migrar_secao(
        secao,
        ricker_wavelet,
        A,
        C,
        fat_s,
        fat_d,
        fat_i,
        fat_e,
        matriz_sismograma,
        matriz_ascendente,
    )

    print("-- SALVANDO PLOTS E BINÁRIOS --\n")

    salvar_plot_ricker_wavelet(ricker_wavelet)
    salvar_plot_secao(secao)
    salvar_plot_sismograma(secao, ricker_wavelet, matriz_sismograma)
    salvar_plot_secao_migrada(secao, 1, P1)
    salvar_plot_secao_migrada(secao, 2, P2)
    salvar_plot_secao_migrada(secao, 3, P3)

    salvar_binarios(
        secao.extended_array, ricker_wavelet.fonte, matriz_sismograma, P1, P2, P3
    )

    print("\n---------- PROGRAMA FINALIZADO ----------\n")


if __name__ == "__main__":
    main()
