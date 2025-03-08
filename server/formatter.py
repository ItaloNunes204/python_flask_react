import hashlib
from datetime import datetime, date, timedelta
import base64
from io import BytesIO
from PIL import Image

import path_manager
import error_reporter

from database import metodologia as bd_metodologia
from database import piloto as bd_piloto
from database import membros as bd_membros
from database import metodologia as bd_metodologia
from database import circuito as bd_circuito
from database import prototipo as bd_prototipo
from server.classes import objetivos

def encode_password(password: str) -> str:
    result = hashlib.md5()
    result.update(password.encode('utf-8'))
    return result.hexdigest()

def get_temporada() -> str:
    data = date.today()
    if data.month >= 1 and data.month <= 8:
        return str(data.year - 1) + "/" + str(data.year)
    elif data.month > 8:
        return str(data.year) + "/" + str(data.year + 1)

def gen_senha(subgrupo):
    senha = "FormulaUFMG" + str(subgrupo) + "12"
    return senha

def verifica_formatacao_temporada(temporada):
    anos = temporada.split("/")
    if len(anos) != 2:
        return False
    else:
        if len(anos[0]) == 4 and len(anos[1]) == 4:
            return True
        else:
            return False

def formata_classe_dicionario(lista_classes):
    return [classe.to_dict() for classe in lista_classes]

def formata_informacoes_piloto(piloto, membro):
    piloto.add_nome(membro.nome)
    return piloto

def formata_dados_piloto(piloto):
    verificador, entidade_membro = bd_membros.get_membro(piloto.email)
    if verificador == True:
        piloto = formata_informacoes_piloto(piloto, entidade_membro)
    else: 
        return False

def formata_lista_pilotos(lista):
    for piloto in lista:
        verificador, entidade_membro = bd_membros.get_membro(piloto.email)
        if verificador == True:
            piloto = formata_informacoes_piloto(piloto, entidade_membro)
        else: 
            return False
    return lista

def salva_imagem_circuito(dados, entidade):
    if "imagem" in dados:
        try:
            imagem = dados["imagem"]
            # Remove o prefixo "data:image/png;base64," da string
            string_base64 = imagem.split(",")[1]
            # Adiciona padding manualmente
            while len(string_base64) % 4 != 0:
                string_base64 += "="
            imagem_decodificada = base64.b64decode(string_base64)
            # Abre a imagem a partir dos bytes decodificados
            imagem = Image.open(BytesIO(imagem_decodificada))
            # salva imagem 
            imagem.save(entidade.caminho)
            return True, "imagem salva no servidor"
        except:
            return False, "Erro ao salvar a imagem"
    else:
        return False, "A imagem não foi enviada"

def modificar_imagem_circuito(dados, entidade):
    # Verifica se existe a imagem
    if path_manager.file_exists(entidade.caminho) == True:
        # Tenta apagar a imagem
        if path_manager.delete_file(entidade.caminho) == True:
            # Salva a imagem
            verificador_imagem, mensagem = salva_imagem_circuito(dados, entidade)
        else:
            # Cria a mensagem de erro
            verificador_imagem = False
            mensagem = "Erro ao apagar a imagem sa salva"
            error_reporter.erro_imagem(entidade.camminho )
        return verificador_imagem, mensagem
    else:
        # Caso não exista a imagem, salvar a imagem
        verificador_imagem, mensagem = salva_imagem_circuito(dados, entidade)
        return verificador_imagem, mensagem

def apagar_imagem_circuito(entidade):
    if path_manager.file_exists(entidade.caminho) == True:
        if path_manager.delete_file(entidade.caminho) == True:
            return True
        else:
            error_reporter.erro_deletar_arquivo(entidade.caminho)
            return False
    else:
        return True

def concatenar_vetor(vetor: list) -> str:
    saida = ""
    contador = 1
    for elemento in vetor:
        if contador == 1:
            saida = str(elemento)
        else:
            saida += ";" + str(elemento)
        contador += 1
    return saida

def string_int(vetor: list) -> list:
    saida = []
    for elemento in vetor:
        saida.append(int(elemento))
    return saida

def string_float(vetor: list) -> list:
    saida = []
    for elemento in vetor:
        saida.append(float(elemento))
    return saida

def deserializacao(entrada: str,tipo: str) -> list:
    entrada = str(entrada)
    saida = entrada.split(";")
    match tipo:
        case "int":
            return string_int(saida)
        case _:
            return string_float(saida)

def coleta_nome_piloto(piloto):
    verificador_membro, entidade_membro = bd_membros.get_membro(piloto.email)
    if verificador_membro == True:
        piloto.add_nome(entidade_membro.nome)
        return piloto
    else:
        return False

def converte_lista_pilotos(pilotos):
    lista_saida = []
    for piloto in pilotos:
        verificar_piloto, entidade_piloto = bd_piloto.get_piloto(piloto)
        if verificar_piloto == True:
            entidade_piloto = coleta_nome_piloto(entidade_piloto)
            if entidade_piloto == False:
                return False
            else:
                lista_saida.append(entidade_piloto.nome)
        else:
            return False
    return lista_saida

def converte_lista_objetico(objetivos):
    saida_objetivos = []
    for objetivo in objetivos:
        verificador_objetivo, entidade_objetivo = bd_metodologia.get_metodologia(objetivo)
        if verificador_objetivo == True:
            saida_objetivos.append(entidade_objetivo.objetivo)
        else:
            return False
    return saida_objetivos

def formatar_informacoes_teste(testes):
    for teste in testes:

        # Formata informação do almoço
        if teste.almoco == 1:
            teste.almoco = "Nesse teste é necessario um intervalo para almoço"
        else:
            teste.almoco = "Nesse teste não é necessario um intervalo de almoço"

        # formata informações do briefing e do debriefing
        if path_manager.file_exists(teste.briefing) == True:
            teste.briefing = True
        else:
            teste.briefing = False
        if path_manager.file_exists(teste.debriefing) == True:
            teste.debriefing = True
        else:
            teste.debriefing = False

        # formata circuito
        verificador_circuito, entidade_circuito = bd_circuito.get_circuito(teste.id_circuito)
        if verificador_circuito == True:
            teste.id_circuito = entidade_circuito.caminho
        else:
            return False
        
        # formata prototipo
        verificador_prototipo, entidade_prototipo = bd_prototipo.get_prototipo(teste.id_prototipo)
        if verificador_prototipo == True:
            teste.id_prototipo = entidade_prototipo.nome
        else:
            return False
        
        # formata pilotos
        pilotos = deserializacao(teste.pilotos,"int")
        pilotos = converte_lista_pilotos(pilotos)
        if pilotos == False:
            return False
        else:
            pilotos = concatenar_vetor(pilotos)
            teste.pilotos = pilotos

        # formata objetivos
        objetivos = deserializacao(teste.id_objetivos, "int")
        objetivos = converte_lista_objetico(objetivos)
        if objetivos == False:
            return False
        else:
            objetivos = concatenar_vetor(objetivos)
            teste.id_objetivos = objetivos
            
    return testes

def formata_lista_classe_piloto(pilotos):
    for piloto in pilotos:
        piloto = coleta_nome_piloto(piloto)
        if piloto == False:
            return False
    return pilotos

def string_to_datetime(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M").time()
    return time_obj

def salva_cred(arquivo, caminho):
    try:
        if arquivo:
            while len(arquivo) % 4 != 0:
                arquivo += "="
            file_content = base64.b64decode(arquivo)
            with open(caminho, 'wb') as f:
                    f.write(file_content)
            return True
        else:
            return False
    except:
        return False

def adiciona_cred(arquivo):
    caminho = path_manager.get_creds()
    if path_manager.file_exists(caminho) == True:
        verificador_apagar = path_manager.delete_file(caminho)
        if verificador_apagar == True:
            verificador_cadastro = salva_cred(arquivo, caminho)
            return verificador_cadastro
        else:
            return False
    else:
        verificador_cadastro = salva_cred(arquivo, caminho)
        return verificador_cadastro






def verificador_arquivos(testes):
    saida = []
    for teste in testes:
        confirma = path_manager.file_exists(teste.documento)
        if confirma == True:
            saida.append(teste)
    return saida

def cria_objetivo(id):
    verificador, metodologia = bd_metodologia.get_metodologia(id)
    if verificador == True:
        saida = objetivos.Objetivos(metodologia.id_metodologia, metodologia.objetivo, metodologia.status, metodologia.temporada) 
    else:
        saida = None
    return saida

def get_objetivos(lista_testes):
    for teste in lista_testes:
        teste.id_objetivos = deserializacao(teste.id_objetivos, "int")
        objetivos = []
        for objetivo in teste.id_objetivos:
            objetivos.append(cria_objetivo(objetivo))
        teste.id_objetivos = objetivos
    return lista_testes

def coleta_informacao(entrada):
    saida = entrada.split("|")
    return saida[0]

def formatação_graficos(entrada):# criar uma lista de objetos para ser plotado nos grafico
    pass

def formatacao_piloto(entrada: list):
    lista_pilotos = []
    for piloto in entrada:
        verificador_piloto, entidade_piloto = bd_piloto.get_piloto(piloto)
        if verificador_piloto == True:
            verificador_membro, entidade_membro = bd_membros.get_membro(entidade_piloto.email)
            if verificador_membro == True:
                entidade_piloto.add_nome(entidade_membro.nome)
                dic = {
                    "id": entidade_piloto.id_piloto,
                    "nome": entidade_piloto.nome
                }
                lista_pilotos.append(dic)
            else:
                return "Erro ao realizar a busca"
        else:
            return "Erro ao realizar a busca"
    return lista_pilotos

def formatar_select_log(log):
    entidade = {
        "id": log.id_logs,
        "nome": "log: " + str(log.id_logs)
    }
    return entidade

def formatar_descricao(log):
    entidade = {
        "descricao": log.descricao
    }
    return entidade

def formata_coodenadas(entrada):# coleta o ponto inicial de converte em 2 saidas(x e y)
    pass

def id_piloto_nome(lista):
    nova_lista = deserializacao(lista, 'int')
    saida = []
    for piloto in nova_lista:
        verificador, entidade = bd_piloto.get_piloto(piloto)
        if verificador == True:
            verificador_membro, entidade_membro = bd_membros.get_membro(entidade.email)
            if verificador_membro == True:
                saida.append(entidade_membro.nome)
            else:
                return False
        else:
            return False
    return saida

def id_objetivo_objetivo(lista):
    nova_lista = deserializacao(lista, "int")
    saida = []
    for id in nova_lista:
        verificador, entidade_metodologia = bd_metodologia.get_metodologia(id)
        if verificador == True:
            saida.append(entidade_metodologia.objetivo)
        else:
            return False
    return saida

def formatar_lista_testes(lista):
    for teste in lista:
        teste.pilotos = id_piloto_nome(teste.pilotos)
    return lista

def deleta_endereco_log(email):
    pass

def formata_imformacoes_objetivos(lista):
    saida = []
    for objetivo in lista:
        saida.append({"id": objetivo.id_metodologia ,"nome": objetivo.objetivo})
    return saida

def timedelta_to_string(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

def formata_informacoes_teste(lista):
    for teste in lista:
        teste.pilotos = id_piloto_nome(teste.pilotos)
        teste.pilotos = concatenar_vetor(teste.pilotos)
        teste.id_objetivos = id_objetivo_objetivo(teste.id_objetivos)
        teste.id_objetivos = concatenar_vetor(teste.id_objetivos)
        teste.inicio = timedelta_to_string(teste.inicio)
        teste.fim = timedelta_to_string(teste.fim)
        teste.data = teste.data.strftime('%d/%m/%Y')
        if teste.almoco == 1:
            teste.almoco = "Para esse teste é necessario reserva um horario para o almoço"
        else:
            teste.almoco = "Para esse teste não é necessario reserva um horario para o almoço"
    return lista
