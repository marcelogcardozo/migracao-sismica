from Secao_Migrada import Secao_Migrada
import matplotlib.pyplot as plt
import time


def main():

    # Criação do objeto Seção Migrada
    secao = Secao_Migrada()

    # Modelagem
    secao.build('modelar')
    #secao.sis_plot()

    # Migração
    secao.build('migrar')
    secao.section_plot('3') # 1 - 3 ( Condições de Imagem )

    # Salvar arquivos binários
    secao.save_bins()


if __name__ == '__main__':

    inicio = time.time()
    main()
    fim = time.time()
    print('%.2f segundos' % (fim - inicio))