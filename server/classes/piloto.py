class Pilotos:
    def __init__(self, id_piloto, temporada, n_testes, email, kms):
        self.id_piloto = id_piloto
        self.temporada = temporada
        self.n_testes = n_testes
        self.email = email
        self.kms = kms
        self.nome = None
    
    def add_nome(self, nome):
        self.nome = nome

    def formato_saida(self, nome):
        self.saida = str(self.id_piloto) + "|" + str(self.temporada)
        self.nome = nome

    def to_dict(self):
        return {
            "id": self.id_piloto,
            "temporada": self.temporada,
            "n_testes": self.n_testes,
            "email": self.email,
            "kms": self.kms,
            "nome": self.nome,
        }
