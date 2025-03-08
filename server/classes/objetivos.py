class Objetivos:
    def __init__(self, id_metodologia, proposito, status, temporada ):
        self.id_metodologia = id_metodologia
        self.proposito = proposito
        self.status = status
        self.temporada = temporada
        self.saida = str(self.id_metodologia) + "|" + str(self.temporada)
