from flask import Flask, jsonify, request, session
from flask_cors import CORS
from datetime import datetime, datetime

from database import aerodinamica as bd_aerodinamica
from database import chassi as bd_chassi
from database import circuito as bd_circuito
from database import comentario as bd_comentario
from database import dinamica as bd_dinamica
from database import fator_externo as bd_fator_externo
from database import freio as bd_freio
from database import grafico as bd_grafico
from database import log as bd_log
from database import marcacao as bd_marcacao
from database import membros as bd_membros
from database import metodologia as bd_metodologia
from database import motor as bd_motor
from database import piloto as bd_piloto
from database import presenca as bd_presenca
from database import prototipo as bd_prototipo
from database import sensores as bd_sensores
from database import teste as bd_teste
from database import transmissao as bd_transmissao

from server.classes import aerodinamica as cl_aerodinamica
from server.classes import chassi as cl_chassi
from server.classes import circuito as cl_circuito
from server.classes import comentario as cl_comentario
from server.classes import dinamica as cl_dinamica
from server.classes import fator_externo as cl_fator_externo
from server.classes import freio as cl_freio
from server.classes import grafico as cl_grafico
from server.classes import log as cl_log
from server.classes import marcacao as cl_marcacao
from server.classes import membros as cl_membros
from server.classes import metodologia as cl_metodologia
from server.classes import motor as cl_motor
from server.classes import piloto as cl_piloto
from server.classes import presenca as cl_presenca
from server.classes import prototipo as cl_prototipo
from server.classes import sensores as cl_sensores
from server.classes import teste as cl_teste
from server.classes import transmissao as cl_transmissao
from server.classes import objetivos as cl_objetivos 
from server.classes import prototipos_saida as cl_prototipo_saida

import formatter

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Troque em produção!

# Configuração básica do CORS
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# Iniciar uma classe com as informações ja salvas
dados = {
    "nome": "Usuário Teste",
    "ultimo_login": "2023-10-20 14:30",
    "tarefas_concluidas": 5,
    "mensagem": "Bem-vindo de volta!"
}

# ------------ ROTAS DA API SISTEMA------------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    senha = formatter.encode_password(password)
    verificador, var_login = bd_membros.login(email,senha)
    if verificador == True and var_login == True:
        session['user'] = email
        return jsonify({"success": True, "name": email}),200
    elif verificador == True and var_login == False:
        return jsonify({"success": False, "error": "Usuario ou senha incorretos "}), 200
    else:
        return jsonify({"success": False, "error": "Erro na conexão com o banco de dados"}), 500

@app.route('/api/check-auth')
def check_auth():
    user = session.get('user')  # Obtém o email da sessão
    if user:
        return jsonify({
            "loggedIn": True,
            "email": user  # Adiciona o email na resposta
        })
    else:
        return jsonify({"loggedIn": False})

@app.route('/api/inicio_data')
def inicio_data():
    return jsonify(dados)

@app.route('/api/logout', methods=['POST'])
def logout():
    formatter.deleta_endereco_log(session['user'])
    session.pop('user', None)
    return jsonify({"success": True}), 200

@app.route("/api/anexo", methods=['POST'])
def anexo():
    data = request.get_json()
    arquivo = data.get("content")
    verificador_envio = formatter.adiciona_cred(arquivo)
    if verificador_envio == True:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Erro ao modificar o anexo"})
# ------------ ROTAS DA API MEMBROS------------
@app.route("/api/members")
def members():
    verificador, membros = bd_membros.get_membros()
    verificador_adm, usuario = bd_membros.get_membro(session.get('user'))
    if verificador == True and verificador_adm == True:
        if usuario.subgrupo == "Data Analysis" or usuario.subgrupo == "Gestão" or usuario.subgrupo == "Capitania":
            subgrupo = True
        else:
            subgrupo = False
        lista_dicionarios = formatter.formata_classe_dicionario(membros)
        data = {
            "success": True,
            "members": lista_dicionarios,
            "adm": subgrupo
        }
        return jsonify(data), 200
    else:
        return jsonify({"success": False,"error": "Erro na conexão com o banco de dados"}), 401

@app.route("/api/set_piloto", methods=['POST'])
def set_piloto():
    data = request.get_json()
    email = data.get('email')
    temporada = formatter.get_temporada()
    piloto = cl_piloto.Pilotos(None, temporada, 0, email, 0)
    verificador, var_piloto = bd_piloto.creat_piloto(piloto)
    if verificador == True and var_piloto == True:
        return jsonify({"success": True}), 200
    elif verificador == True and var_piloto == False:
        return jsonify({"success": False, "error": "Erro no cadastro"}), 200
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"}), 401

@app.route("/api/data_members", methods=['POST'])
def data_members():
    verificador, membro = bd_membros.get_membro(session.get('user'))
    if verificador == True:
        dado = {
            "success": True,
            "usuario":membro.to_dict()
        }
        return jsonify(dado)
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"}),401

@app.route("/api/modify_members", methods=['POST'])
def modify_members():
    data = request.get_json()
    nome = data.get("nome")
    subgrupo = data.get("subgrupo")
    email = data.get("email")
    senha = data.get("senha")
    if senha != None:
        senha_conf = data.get("senha_conf")
        if senha == "" and senha_conf == "":
            senha = None
        elif senha != senha_conf:
            return jsonify({"success": False, "error": "senhas diferentes"}), 200
        else:
            senha = formatter.encode_password(str(senha))
    else:
        verificador, membro = bd_membros.get_membro(email)
        if verificador == True:
            membro.modifica(nome, subgrupo, senha)
            verificador_modificador, var_modificador = bd_membros.modifica(membro)
            if verificador_modificador == True and var_modificador == True:
                return jsonify({
                    "success": True,
                    "message": "Membro atualizado com sucesso.",
                    "nome": membro.nome,
                    "email": membro.email,
                    "subgrupo": membro.subgrupo
                    }), 200
            elif verificador_modificador == True and var_modificador == False:
                erro = "Erro ao atualizar o membro. Tente novamente."
            else:
                erro = "Erro na integração"
            return jsonify({"success": False, "message": erro}), 200
        else:
            return jsonify({"success": False, "message": "Membro não encontrado."})

@app.route("/api/modify_user", methods=['POST'])
def modify_user():
    data = request.get_json()
    nome = data.get("nome")
    subgrupo = data.get("subgrupo")
    email = data.get("email")
    senha = data.get("senha")
    senha_conf = data.get("senha_conf")
    if senha == "" and senha_conf == "":
        senha = None
    elif senha != senha_conf:
        return jsonify({"success": False, "error": "senhas diferentes"}), 200
    else:
        senha = formatter.encode_password(str(senha))
        verificador, membro = bd_membros.get_membro(email)
        if verificador == True:
            membro.modifica(nome, subgrupo, senha)
            verificador_modificador, var_modificador = bd_membros.modifica(membro)
            if verificador_modificador == True and var_modificador == True:
                return jsonify({
                    "success": True,
                    "message": "Membro atualizado com sucesso.",
                    "nome": membro.nome,
                    "email": membro.email,
                    "subgrupo": membro.subgrupo
                    }), 200
            elif verificador_modificador == True and var_modificador == False:
                erro = "Erro ao atualizar o membro. Tente novamente."
            else:
                erro = "Erro na integração"
            return jsonify({"success": False, "message": erro}), 200
        else:
            return jsonify({"success": False, "message": "Membro não encontrado."})

@app.route("/api/delete_members", methods=['POST'])
def delete_members():
    data = request.get_json()
    email = data.get("email")
    usuario = session.get('user')
    if email == usuario:
        return jsonify({"success": False, "error": "Apagar a conta em uso"})
    else:
        verificador, membro = bd_membros.get_membro(email)
        if verificador == True:
            verificador_apagar, var_apagar = bd_membros.apagar(membro)
            if verificador_apagar == True and var_apagar == True:
                return jsonify({
                        "success": True,
                        "message": "Membro atualizado com sucesso.",
                        "nome": membro.nome,
                        "email": membro.email,
                        "subgrupo": membro.subgrupo
                        }), 200
            else:
                return jsonify({"success": False, "error": "Erro ao apagar os dados"})
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/create_members", methods=['POST'])
def create_members():
    data = request.get_json()
    nome = data.get("nome")
    subgrupo = data.get("subgrupo")
    email = data.get("email")
    senha = formatter.gen_senha(subgrupo)
    senha = formatter.encode_password(senha)
    membro = cl_membros.Membros(email, senha, nome, subgrupo)
    verificador, var_membro = bd_membros.creat_membro(membro)
    if verificador == True and var_membro == True:
        return jsonify({"success": True}), 200
    elif verificador == True and var_membro == False:
        return jsonify({"success": False, "error": "Erro no cadastro"}), 200
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

# ------------ ROTAS DA API PROTOTIPO------------
@app.route("/api/prototypes")
def prototypes():
    verificador_prototipos, prototipos = bd_prototipo.get_prototipos()
    verificador_membro, usuario = bd_membros.get_membro(session.get('user'))
    if verificador_prototipos == True and verificador_membro == True:
        if usuario.subgrupo == "Data Analysis" or usuario.subgrupo == "Gestão" or usuario.subgrupo == "Capitania":
            subgrupo = True
        else:
            subgrupo = False
        lista_dicionarios = formatter.formata_classe_dicionario(prototipos)
        data = {
            "success": True,
            "prototypes": lista_dicionarios,
            "adm": subgrupo
        }
        return jsonify(data), 200
    else:
        return jsonify({"success": False,"error": "Erro na conexão com o banco de dados"}), 401

@app.route("/api/modify_prototypes", methods=["POST"])
def modify_prototypes():
    data = request.get_json()
    id = data.get("id")
    nome = data.get("nome")
    ano_fabricacao = data.get("ano_fabricacao")
    status = data.get("status")
    peso = data.get("peso")
    temporada = data.get("temporada")
    if formatter.verifica_formatacao_temporada(temporada) == False:
        return jsonify({"success": False, "error": "Erro na formatação da temporada"}), 200
    else:
        verificador_prototipo, prototipo = bd_prototipo.get_prototipo(id)
        if verificador_prototipo == True:
            prototipo.modificar(nome, ano_fabricacao, status, peso, temporada, None)
            verificador_modifica, var_prototipo = bd_prototipo.modifica(prototipo)
            if verificador_modifica == True and var_prototipo == True:
                data = prototipo.to_dict()
                data["success"] = True
                data["message"] = "Prototipo atualizado com sucesso."
                return jsonify(data), 200
            elif verificador_modifica == True and var_prototipo == False:
                erro = "Erro ao atualizar o prototipo. Tente novamente."
            else:
                erro = "Erro na integração"
            return jsonify({"success": False, "message": erro}), 200
        else:
            return jsonify({"success": False,"error": "Erro na conexão com o banco de dados"}), 401

@app.route("/api/delete_prototypes",  methods=["POST"])
def delete_prototypes():
    data = request.get_json()
    id_prototipo = data.get("id")
    verificador_prototipo, prototipo = bd_prototipo.get_prototipo(id_prototipo)
    if verificador_prototipo == True:
        verificador_apagar, var_prototipo = bd_prototipo.apagar(prototipo)
        if verificador_apagar == True and var_prototipo == True:
            data = prototipo.to_dict()
            data["success"] = True
            data["message"] = "Prototipo atualizado com sucesso."
            return jsonify(data), 200
        else:
            return jsonify({"success": False, "error": "Erro ao apagar os dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/create_prototypes", methods=["POST"])
def create_prototypes():
    data = request.get_json()
    nome = data.get("nome")
    ano_fabricacao = data.get("ano_fabricacao")
    status = data.get("status")
    peso = data.get("peso")
    temporada = data.get("temporada")
    if formatter.verifica_formatacao_temporada(temporada) == False:
        return jsonify({"success": False, "error": "Erro na formatação da temporada"}), 200
    else:
        prototipo = cl_prototipo.Prototipo(None, nome, ano_fabricacao, status, peso, temporada, 0)
        verificador, var_prototipo = bd_prototipo.creat_prototipo(prototipo)
        if verificador == True and var_prototipo == True:
            verificador_busca, entidade = bd_prototipo.get_prototipo_max_id()
            if verificador_busca == True:
                dados =  entidade.to_dict()
                dados['success'] = True
                return jsonify(dados), 200
            else:
                return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
        elif verificador == True and var_prototipo == False:
            return jsonify({"success": False, "error": "Erro no cadastro"}), 200
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

# ------------ ROTAS DA API SENSORES------------
@app.route("/api/sensors")
def sensors():
    verificador_prototipos, entidade_prototipos = bd_prototipo.get_prototipos()
    if verificador_prototipos == True:
        data = {}
        data['success'] = True
        data["prototypes"] = formatter.formata_classe_dicionario(entidade_prototipos)
        return jsonify(data)
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/sensors/prototypes", methods=["POST"])
def processar_prototipo_sensores():
    data = request.get_json()
    prototipo_id = data.get('id')
    verificador, entidade_sensores = bd_sensores.get_sensor_prototipo(prototipo_id)
    if verificador == True:
        data['success'] = True
        data = formatter.formata_classe_dicionario(entidade_sensores)
        return jsonify(data)
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/create_sensors", methods=["POST"])
def create_sensors():
    data = request.get_json()
    nome = data.get('nome')
    id_prototipo = data.get('id_prototipo')
    informacao = data.get('informacao')
    sensor = cl_sensores.Sensores(None, nome, id_prototipo, informacao)
    verificador_sensores, var_sensores = bd_sensores.creat_sensores(sensor)
    if verificador_sensores == True and var_sensores == True:
        verificador_entidade, entidade = bd_sensores.get_sensor_max_id()
        if verificador_entidade == True:
            data = entidade.to_dict()
            data['success'] = True
            return jsonify(data)
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    elif verificador_sensores == True and var_sensores == False:
        return jsonify({"success": False, "error": "Erro na criação da entidade"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/modify_sensors", methods=["POST"])
def modify_sensors():
    data = request.get_json()
    nome = data.get('nome')
    informacao = data.get('informacao')
    id_sensores = data.get('id_sensor')
    verificador_sensor, entidade_sensor = bd_sensores.get_sensor(id_sensores)
    if verificador_sensor == True:
        entidade_sensor.modificar(nome, informacao)
        verificador_modificador, var_sensor = bd_sensores.modificar(entidade_sensor)
        if verificador_modificador == True and var_sensor == True:
            data = entidade_sensor.to_dict()
            data['success'] = True
            return jsonify(data)
        elif verificador_modificador == True and var_sensor == False:
            return jsonify({"success": False, "error": "Erro ao modificar as informações do sensor"})
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/delete_sensors", methods=["POST"])
def delete_sensors():
    data = request.get_json()
    id_sensores = data.get('id_sensor')
    verificador_sensor, entidade_sensor = bd_sensores.get_sensor(id_sensores)
    if verificador_sensor == True:
        verificador_apagar, var_sensor = bd_sensores.apagar(entidade_sensor)
        if verificador_apagar == True and var_sensor == True:
            data = entidade_sensor.to_dict()
            data['success'] = True
            return jsonify(data)
        elif verificador_apagar == True and var_sensor == False:
            return jsonify({"success": False, "error": "Erro ao apagar as informações do sensor"})
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

# ------------ ROTAS DA API TESTES------------
@app.route("/api/test")
def test():
    verificador_prototipos, entidade_prototipos = bd_prototipo.get_prototipos()
    if verificador_prototipos == True:
        data = {}
        data['success'] = True
        data["prototypes"] = formatter.formata_classe_dicionario(entidade_prototipos)
        return jsonify(data)
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/test/prototypes", methods=["POST"])
def processar_prototipo_teste():
    data = request.get_json()
    prototipo_id = data.get('id')
    verificaddor_teste, entidade_teste = bd_teste.get_teste_prototipo(prototipo_id)
    if verificaddor_teste == True:
        entidade_teste = formatter.formatar_informacoes_teste(entidade_teste)
        if entidade_teste == False:
            return jsonify({"success": False, "error": "Erro na Formatação das imagens"})
        else:
            data = {}
            data["success"] = True
            data["teste"] = formatter.formata_classe_dicionario(entidade_teste)
            return jsonify(data)
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/teste/get_objetivos", methods=["POST"])
def get_objetivos():
    data = request.get_json()
    prototipo_id = data.get('id')
    verificador_prototipo, entidade_prototipo = bd_prototipo.get_prototipo(prototipo_id)
    if verificador_prototipo == True:
        verificador_metodologia, entidade_metodologia = bd_metodologia.get_metodologias_temporada(entidade_prototipo.temporada)
        verificador_pilotos, entidade_piloto = bd_piloto.get_pilotos_temporada(entidade_prototipo.temporada)
        verificador_circuito, entidade_circuito = bd_circuito.get_circuitos()
        if verificador_metodologia == True and verificador_pilotos == True and verificador_circuito == True:
            entidade_piloto = formatter.formata_lista_classe_piloto(entidade_piloto)
            if entidade_piloto == False:
                return jsonify({"success": False, "error": "Erro na formatação das informações"})
            else:
                data = {}
                data["objetivos"] = formatter.formata_classe_dicionario(entidade_metodologia)
                data["piloto"] = formatter.formata_classe_dicionario(entidade_piloto)
                data["circuito"] = formatter.formata_classe_dicionario(entidade_circuito)
                return jsonify(data)
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/create_test", methods=["POST"])
def create_test():
    data = request.get_json()
    nome = data.get('nome')
    prototipo = data.get('prototipo')
    lista_objetivos = data.get('objetivos')
    lista_pilotos = data.get('pilotos')
    circuito = data.get('circuito')
    horaInicio = data.get('horaInicio')
    horaInicio = formatter.string_to_datetime(horaInicio)
    horaFim = data.get('horaFim')
    horaFim = formatter.string_to_datetime(horaFim)
    almoco = data.get('almoco')
    if almoco == True:
        almoco = 1
    else:
        almoco = 0
    dataTeste = data.get('dataTeste')
    dataTeste = datetime.strptime(dataTeste, "%Y-%m-%d").date()
    pilotos = formatter.concatenar_vetor(lista_pilotos)
    objetivos = formatter.concatenar_vetor(lista_objetivos)
    entidade_teste = cl_teste.Teste(None,nome,pilotos,objetivos,0,horaInicio,horaFim,almoco,dataTeste,prototipo,circuito,"Agendado",None)
    verificador_teste, var_teste = bd_teste.creat_teste(entidade_teste)
    if verificador_teste == True and var_teste == True:
        return jsonify({"success": True})
    elif verificador_teste == True and var_teste == False:
        return jsonify({"success": False, "error": "Erro no cadastro das informações"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/delete_test", methods=["POST"])
def delete_test():
    data = request.get_json()
    id = data.get('id')
    verificador_teste, entidade_teste = bd_teste.get_teste(id)
    if verificador_teste == True:
        verificador_apagar, var_apagar = bd_teste.apagar(entidade_teste)
        if verificador_apagar == True and var_apagar == True:
            return jsonify({"success": True})
        elif verificador_apagar == True and var_apagar == False:
            return jsonify({"success": False, "error": "Erro ao apagar as informações"})
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/modify_test", methods=["POST"])
def modify_test():
    data = request.get_json()
    id_teste = data.get('id')
    nome = data.get('nome')
    prototipo = data.get('prototipo')
    lista_objetivos = data.get('objetivos')
    lista_pilotos = data.get('pilotos')
    circuito = data.get('circuito')
    horaInicio = data.get('horaInicio')
    horaInicio = formatter.string_to_datetime(horaInicio)
    horaFim = data.get('horaFim')
    horaFim = formatter.string_to_datetime(horaFim)
    almoco = data.get('almoco')
    if almoco == True:
        almoco = 1
    else:
        almoco = 0
    dataTeste = data.get('dataTeste')
    dataTeste = datetime.strptime(dataTeste, "%Y-%m-%d").date()
    pilotos = formatter.concatenar_vetor(lista_pilotos)
    objetivos = formatter.concatenar_vetor(lista_objetivos)
    verificador_teste, entidade_teste = bd_teste.get_teste(id_teste)
    if verificador_teste == True:
        entidade_teste.modificar(nome, pilotos, objetivos, horaInicio, horaFim, almoco, data, prototipo, circuito)
        verificador_modificar, var_modificar = bd_teste.modificar(entidade_teste)
        if verificador_modificar == True and var_modificar == True:
            return jsonify({"success": True})
        elif verificador_modificar == True and var_modificar == False:
            return jsonify({"success": False, "error": "Erro ao modificar as informações"})
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    
# ------------ ROTAS DA API METODOLOGIAS------------
@app.route("/api/methodology")
def methodology():
    verificador_prototipos, entidade_prototipos = bd_prototipo.get_prototipos()
    if verificador_prototipos == True:
        data = {}
        data['success'] = True
        data["prototypes"] = formatter.formata_classe_dicionario(entidade_prototipos)
        return jsonify(data)
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/methodology/prototypes", methods=["POST"])
def processar_prototipo_metodologia():
    data = request.get_json()
    prototipo_id = data.get('id')
    verificador_prototipo, entidade_prototipo = bd_prototipo.get_prototipo(prototipo_id)
    if verificador_prototipo == True:
        verificador_metodologia, entidade_metodologia = bd_metodologia.get_metodologias_temporada(entidade_prototipo.temporada)
        if verificador_metodologia == True:
            data = {}
            data["success"] = True
            data = formatter.formata_classe_dicionario(entidade_metodologia)
            return jsonify(data)
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/create_methodology", methods=["POST"])
def create_methodology():
    data = request.get_json()
    objetivo = data.get('objetivo')
    N_pessoas = data.get('N_pessoas')
    subgrupo = data.get('subgrupo')
    procedimento = data.get('procedimento')
    N_voltas = data.get('N_voltas')
    temporada = data.get('temporada')
    status = data.get('status')
    if formatter.verifica_formatacao_temporada(temporada) == False:
        return jsonify({"success": False, "error": "Erro na formatação da temporada"}), 200
    else:
        metodologia = cl_metodologia.Metodologia(None, objetivo, N_pessoas, subgrupo, procedimento, N_voltas, temporada, status)
        verificador_metodologia, var_metodoloogia = bd_metodologia.creat_metodologia(metodologia)
        if verificador_metodologia == True and var_metodoloogia == True:
            verificador, metodologia = bd_metodologia.get_metodologia_max_id()
            if verificador == True:
                data = metodologia.to_dict()
                data["success"] = True
                return jsonify(data)
            else:
                return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
        elif verificador_metodologia == True and var_metodoloogia == False:
            return jsonify({"success": False, "error": "Erro na criação da metodologia"})
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/modify_methodology", methods=["POST"])
def modify_methodology():
    data = request.get_json()
    objetivo = data.get('objetivo')
    N_pessoas = data.get('N_pessoas')
    subgrupo = data.get('subgrupo')
    procedimento = data.get('procedimento')
    N_voltas = data.get('N_voltas')
    status = data.get('status')
    id_metodologia = data.get('id_metodologia')
    verificador_metodologia, metodologia = bd_metodologia.get_metodologia(id_metodologia)
    if verificador_metodologia == True:
        metodologia.modificar(objetivo, N_pessoas, subgrupo, procedimento, N_voltas, status)
        verificador_modificador, var_modificador = bd_metodologia.modificar(metodologia)
        if verificador_modificador == True and var_modificador == True:
            data = metodologia.to_dict()
            data["success"] = True
            return jsonify(data)
        elif verificador_modificador == True and var_modificador == False:
            return jsonify({"success": False, "error": "Erro ao modificar os dados"})
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/delete_methodology", methods=["POST"])
def delete_methodology():
    data = request.get_json()
    id_metodologia = data.get('id_metodologia')
    verificador_metodologia, entidade_metodologia = bd_metodologia.get_metodologia(id_metodologia)
    if verificador_metodologia == True:
        verificador_apagar, var_apagar = bd_metodologia.apagar(entidade_metodologia)
        if verificador_apagar == True and var_apagar == True:
            data = entidade_metodologia.to_dict()
            data["success"] = True
            return jsonify(data)
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

# ------------ ROTAS DA API PILOTOS------------
@app.route("/api/pilots", methods=["POST"])
def pilots():
    verificador_prototipos, entidade_prototipos = bd_prototipo.get_prototipos()
    if verificador_prototipos == True:
        data = {}
        data['success'] = True
        data["prototypes"] = formatter.formata_classe_dicionario(entidade_prototipos)
        return jsonify(data)
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/pilots/prototype", methods=["POST"])
def processar_prototipo_pilot():
    data = request.get_json()
    prototipo_id = data.get('prototipoId')
    verificador_prototipo, entidade_prototipo = bd_prototipo.get_prototipo(prototipo_id)
    if verificador_prototipo == True:
        verificador_pilotos, lista_pilotos = bd_piloto.get_pilotos_temporada(entidade_prototipo.temporada)
        if verificador_pilotos == True:
            lista_pilotos = formatter.formata_lista_pilotos(lista_pilotos)
            if lista_pilotos == False:
                return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
            else:
                data = {}
                data["success"] = False
                data["pilotos"] = formatter.formata_classe_dicionario(lista_pilotos)
                return jsonify(data)
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/delete_pilot", methods=["POST"])
def delete_pilot():
    data = request.get_json()
    id_piloto = data.get('id')
    verificador_piloto, entidade_piloto = bd_piloto.get_piloto(id_piloto)
    if verificador_piloto == True:
        verificador_apagar, var_apagar = bd_piloto.apagar(entidade_piloto)
        if verificador_apagar == True and var_apagar == True:
            if formatter.formata_dados_piloto(entidade_piloto) == False:
                return jsonify({"success": False, "error": "Erro na Formatação das informações"})
            else:
                data = entidade_piloto.to_dict()
                data["success"] = True
                return jsonify(data)
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

# ------------ ROTAS DA API CIRCUITOS------------
@app.route("/api/circuits")
def circuits():
    verificador_circuito, entidade_circuito = bd_circuito.get_circuitos()
    if verificador_circuito == True:
        data = {}
        data["success"] = True
        data["circuits"] = formatter.formata_classe_dicionario(entidade_circuito)
        return jsonify(data)
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/create_circuit", methods=["POST"])
def create_circuit():
    data = request.get_json()
    nome = data.get("nome")
    tempo_deslocamento = data.get("tempo_deslocamento")
    KM = data.get("KM")
    curvas = data.get("curvas")
    cones = data.get("cones")
    setor = data.get("n_setores")
    local = data.get("local")
    data_criacao = datetime.today().replace(microsecond=0)
    circuito = cl_circuito.Circuito(None, nome, tempo_deslocamento, KM, curvas, cones, setor,local,data_criacao)
    verificador_circuito, var_circuito = bd_circuito.creat_circuito(circuito)
    if verificador_circuito == True and var_circuito == True:
        verificador_entidade, entidade = bd_circuito.get_id(data_criacao)
        if verificador_entidade == True:
            verificador_imagem, mensagem = formatter.salva_imagem_circuito(data, entidade)
            return jsonify({"success": verificador_imagem, "message": mensagem})
        else:
            return jsonify({"success": False, "error": "Erro na coleta das informações"})
    elif verificador_circuito == True and var_circuito == False:
        return jsonify({"success": False, "error": "Erro criação do circuito"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/delete_circuit", methods=["POST"])
def delete_circuit():
    data = request.get_json()
    id = data.get("id_circuito")
    verificador_entidade, entidade_circuito = bd_circuito.get_circuito(id)
    if verificador_entidade == True:
        verificador_apagar, var_apagar = bd_circuito.apagar(entidade_circuito)
        if verificador_apagar == True and var_apagar == True:
            verificador_imagem = formatter.apagar_imagem_circuito(entidade_circuito)
            data = {}
            data["success"] = True
            data["circuit"] = entidade_circuito.to_dict()
            data["delete_image"] = verificador_imagem
            return jsonify(data)
        elif verificador_apagar == True and var_apagar == False:
            return jsonify({"success": False, "error": "Erro ao apgar as informações"})
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

@app.route("/api/modify_circuit", methods=["POST"])
def modify_circuit():
    # Coleta as informações a serem modificadas
    data = request.get_json()
    nome = data.get("nome")
    tempo_deslocamento = data.get("tempo_deslocamento")
    KM = data.get("KM")
    curvas = data.get("curvas")
    cones = data.get("cones")
    local = data.get("local")
    setor = data.get("n_setores")
    id_circuito = data.get("id_circuito")
    # coleta a entidade que esta no banco
    verificador_entidade, entidade = bd_circuito.get_circuito(id_circuito)
    if verificador_entidade == True:
        # modifica as informações
        entidade.modificar(nome, tempo_deslocamento, KM, curvas, cones, setor , local)
        verificador_modifica, var_modifica = bd_circuito.modificar(entidade)
        if verificador_modifica == True and var_modifica == True:
            # Cria as mensagens 
            dados = {}
            dados["success"] = True
            dados["circuit"] = entidade.to_dict()
            # Verifica se existe uma chave imagem nos dados enviados
            if "imagem" in data:
                # Chama a função de modificar imagem e adiciona as informações que vão ser retornadas ao dicionario de retorno
                verificador_imagem, mensagem = formatter.modificar_imagem_circuito(data, entidade)
                dados["modify_image"] = verificador_imagem
                dados["message"] = mensagem
            return jsonify(dados)
        elif verificador_modifica == True and var_modifica == False:
            return jsonify({"success": False, "error": "Erro ao modificar as informações do banco"})
        else:
            return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})
    else:
        return jsonify({"success": False, "error": "Erro na interação com o banco de dados"})

# ------------ ROTAS DA API LOG------------
#@app.route("/api/")
#def 
# ------------ ROTAS DA API MEMBROS------------
#@app.route("/api/")
#def 


if __name__ == '__main__':
    app.run(debug=True, port=5000)
