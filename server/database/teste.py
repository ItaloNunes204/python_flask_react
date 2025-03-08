import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error

from database import connection
from error_reporter import send_email
from server.classes import teste

TABLE = "TEFT.testes"

def get_testes():
    comando = """SELECT * FROM {} """.format(TABLE)
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(teste.Teste(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8],linha[9],linha[11],linha[12],linha[13]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def get_teste(id):
    comando = """SELECT * FROM {} WHERE id = \'{}\'""".format(TABLE, id)
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(teste.Teste(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8],linha[9],linha[10],linha[11],linha[12]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login[0]
    else:
        return verificador, None

def get_teste_prototipo(id_prototipo):
    comando = """SELECT * FROM {} WHERE id_prototipo = \'{}\'""".format(TABLE, id_prototipo)
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(teste.Teste(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8],linha[9],linha[10],linha[11],linha[12]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def creat_teste(teste):
    comando = """INSERT INTO {} (nome, pilotos, id_objetivos, N_voltas, inicio, fim, almoco, data, id_prototipo, id_circuito, status, observacao) VALUE(\'{}\',\'{}\',\'{}\',0,\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')""".format(TABLE, teste.nome, teste.pilotos, teste.id_objetivos, teste.inicio, teste.fim, teste.almoco, teste.data, teste.id_prototipo, teste.id_circuito, teste.status, teste.observacao)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            con.commit()
            var_login = True
        except Error as e:
            var_login = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login
    else:
        return verificador, None

def apagar(teste):
    comando = """DELETE FROM {} WHERE id = \'{}\'""".format(TABLE, teste.id)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            con.commit()
            var_login = True
        except Error as e:
            var_login = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login
    else:
        return verificador, None

def modificar(teste):
    comando = ("UPDATE {} SET pilotos = \'{}\', id_objetivos = \'{}\', N_voltas = \'{}\', inicio = \'{}\', fim = \'{}\', almoco = \'{}\', data = \'{}\', id_prototipo = \'{}\', id_circuito = \'{}\'  WHERE id = \'{}\'".format(TABLE,teste.pilotos, teste.id_objetivos, teste.N_voltas, teste.inicio, teste.fim, teste.almoco, teste.data, teste.id_prototipo, teste.id_circuito, teste.id))
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            cursor.execute(comando)
            con.commit()
            var_login = True
        except Error as e:
            var_login = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login
    else:
        return verificador, None

def get_max_teste():
    pass
