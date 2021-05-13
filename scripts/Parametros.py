import os.path


class Parametros:
    def __init__(self):
        
        self.import_parameters()

    def import_parameters(self):

        pathfile = os.path.abspath(os.path.dirname(__file__))
        workfile = os.path.join(pathfile, '..', 'input', 'parametros.txt')

        with open(workfile) as arquivo:
            lines = arquivo.readlines()
        
        parametros = []

        for linha in lines:
            try:
                parametros.append(linha.split(sep=' = ')[1].split(sep='\n')[0].split())
            except:
                pass
            
   
        self.model_name = parametros[0][0]
        self.file_name = parametros[1][0]

        self.smooth = bool(parametros[2][0])

        self.Nz = int(parametros[3][0])
        self.Nx = int(parametros[4][0])
        self.Na = int(parametros[5][0])
        self.Wl = int(parametros[6][0])
    
        self.dt = float(parametros[7][0])
        self.h = int(parametros[8][0])
        self.fcorte = int(parametros[9][0])

        self.fat = float(parametros[10][0])
        self.ntotal = int(parametros[11][0])

        self.shot_z = int(parametros[12][0]) + self.Na
        self.shot_x = int(parametros[13][0]) + self.Na
        self.rec_shotz = int(parametros[14][0]) + self.Na
    
        self.remove_dw = bool(parametros[15][0])