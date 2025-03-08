import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error

from database import connection
from error_reporter import send_email
from server.classes import piloto
TABLE = "TEFT.piloto"

def get_pilotos():
    comando = ("SELECT * FROM {} ".format(TABLE)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(piloto.Pilotos(linha[0],linha[1],linha[2],linha[3],linha[4]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def get_pilotos_temporada(temporada):
    comando = ("SELECT * FROM {} WHERE temporada = '{}' ".format(TABLE, temporada)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(piloto.Pilotos(linha[0],linha[1],linha[2],linha[3],linha[4]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None


def get_piloto(id_piloto):
    comando = ("SELECT * FROM {} WHERE id_piloto = '{}'".format(TABLE, id_piloto)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(piloto.Pilotos(linha[0],linha[1],linha[2],linha[3],linha[4]))
            var_login = saida[0]
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def modifica(piloto):
    comando = ("UPDATE {} SET temporada = \'{}\', n_testes = \'{}\', email = \'{}\', kms = \'{}\'  WHERE id_piloto = \'{}\'".format(TABLE, piloto.temporada, piloto.n_testes, piloto.email, piloto.kms, piloto.id_piloto))
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

def creat_piloto(piloto):
    comando = """INSERT INTO {} (temporada, n_testes, email, kms) VALUE (\'{}\', \'{}\',\'{}\',\'{}\')""".format(TABLE, piloto.temporada, piloto.n_testes, piloto.email, piloto.kms)
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

def apagar(piloto):
    comando = """DELETE FROM {} WHERE id_piloto = \'{}\'""".format(TABLE, piloto.id_piloto)
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
