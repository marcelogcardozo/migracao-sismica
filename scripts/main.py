from Sismograma import Sismograma
from Operador import Operador

import time

def main():

    Op = Operador()
    Op.interpolate()
    sis = Sismograma(Op)
    sis.build()
    sis.plot()


if __name__ == '__main__':

    inicio = time.time()
    main()
    fim = time.time()
    print(f'{fim - inicio} segundos')