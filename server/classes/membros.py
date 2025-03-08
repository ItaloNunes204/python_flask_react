class Membros:
    def __init__(self, email, senha, nome, subgrupo) ->None:
        self.email = email
        self.senha = senha
        self.nome = nome
        self.subgrupo = subgrupo

    def modifica(self, nome, subgrupo, senha) -> None:
        self.nome = nome
        self.subgrupo = subgrupo
        if senha != None:
            self.senha = senha
    
    def to_dict(self):
        return {
            "email": self.email,
            "senha": self.senha,
            "nome": self.nome,
            "subgrupo": self.subgrupo
        }
