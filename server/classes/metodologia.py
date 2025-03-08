class Metodologia:
    def __init__(self, id_metodologia, objetivo, N_pessoas, subgrupo, procedimento, N_voltas, temporada, status):
        self.id_metodologia = id_metodologia
        self.objetivo = objetivo
        self.N_pessoas = N_pessoas
        self.subgrupo = subgrupo
        self.procedimento = procedimento
        self.N_voltas = N_voltas
        self.temporada = temporada
        self.status = status  
    
    def modificar(self, objetivo, N_pessoas, subgrupo, procedimento, N_voltas, status):
        self.objetivo = objetivo
        self.N_pessoas = N_pessoas
        self.subgrupo = subgrupo
        self.procedimento = procedimento
        self.N_voltas = N_voltas
        if status != None:
            self.status = status
    
    def to_dict(self):
        return {
            "id_metodologia": self.id_metodologia,
            "objetivo": self.objetivo,
            "N_pessoas": self.N_pessoas,
            "subgrupo": self.subgrupo,
            "procedimento": self.procedimento,
            "N_voltas": self.N_voltas,
            "temporada": self.temporada,
            "status": self.status
        }
