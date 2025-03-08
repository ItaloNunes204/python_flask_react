import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

import path_manager 

class Circuito:
    def __init__(self, id_circuito, nome, tempo_deslocamento, KM, curvas, cones, n_setores , local, data_criacao):
        self.id_circuito = id_circuito
        self.nome = nome
        self.tempo_deslocamento = tempo_deslocamento
        self.KM = KM
        self.curvas = curvas
        self.cones = cones
        self.n_setores = n_setores
        self.local = local
        self.data_criacao = data_criacao
        if id_circuito != None:
            caminho = "circuito" + str(id_circuito) + ".png"
            self.caminho = path_manager.join_path(path_manager.get_circuitos_path(),caminho)

    def modificar(self, nome, tempo_deslocamento, KM, curvas, cones, n_setores , local):
        self.nome = nome
        self.tempo_deslocamento = float(tempo_deslocamento)
        self.KM = float(KM)
        self.curvas = int(curvas)
        self.n_setores = int(n_setores)
        self.cones = int(cones)
        self.local = local

    def to_dict(self):
        return {
            'id_circuito': self.id_circuito,
            'nome': self.nome,
            'tempo_deslocamento': self.tempo_deslocamento,
            'KM': self.KM,
            'curvas': self.curvas,
            'cones': self.cones,
            'n_setores': self.n_setores,
            'local': self.local,
            'data_criacao': self.data_criacao,
            'caminho': self.caminho
        }
