import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error

from database import connection
from error_reporter import send_email
from server.classes import circuito

TABLE = "TEFT.circuito"

def creat_circuito(circuito):
    comando = """INSERT INTO {} (nome, tempo_deslocamento, KM, curvas, cones, n_setores ,local, data_criacao) VALUE(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')""".format(TABLE, circuito.nome, circuito.tempo_deslocamento, circuito.KM, circuito.curvas, circuito.cones, circuito.n_setores, circuito.local, circuito.data_criacao)
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

def get_circuitos():
    comando = "SELECT * FROM {}".format(TABLE)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            linhas = cursor.fetchall()
            saida = []
            for linha in linhas:
                saida.append(circuito.Circuito(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8]))
            var_login = saida
        except Error as e:
            verificador = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login
    else:
        return verificador, None

def get_circuito(id_circuito):
    comando = "SELECT * FROM {} WHERE ID_circuito = \'{}\'".format(TABLE, id_circuito)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            linhas = cursor.fetchall()
            saida = []
            for linha in linhas:
                saida.append(circuito.Circuito(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8]))
            var_login = saida
        except Error as e:
            verificador = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login[0]
    else:
        return verificador, None 

def modificar(circuito):
    comando = """UPDATE {} SET nome = \'{}\' ,tempo_deslocamento = \'{}\' ,KM = \'{}\' ,curvas = \'{}\' ,cones = \'{}\' ,local = \'{}\', n_setores = \'{}\' WHERE ID_circuito = \'{}\'""".format(TABLE, circuito.nome, circuito.tempo_deslocamento, circuito.KM, circuito.curvas, circuito.cones, circuito.local, circuito.n_setores, circuito.id_circuito)
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

def apagar(circuito):
    comando = """DELETE FROM {} WHERE ID_circuito = \'{}\'""".format(TABLE, circuito.id_circuito)
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

def get_id(data_criacao):
    comando = "SELECT * FROM {} WHERE data_criacao = \'{}\'".format(TABLE, data_criacao)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            linhas = cursor.fetchall()
            saida = []
            for linha in linhas:
                saida.append(circuito.Circuito(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8]))
            var_login = saida
        except Error as e :
            verificador = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login[0]
    else:
        return verificador, None
