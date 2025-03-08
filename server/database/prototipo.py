import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error

from database import connection
from error_reporter import send_email
from server.classes import prototipo

TABLE = "TEFT.prototipo"

def creat_prototipo(prototipo):
    comando = """INSERT INTO {} (nome, ano_fabricacao, status, peso, temporada, n_teste) VALUE (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')""".format(TABLE, prototipo.nome, prototipo.ano_fabricacao, prototipo.status, prototipo.peso, prototipo.temporada, prototipo.n_teste)
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

def get_prototipos():
    comando = "SELECT * FROM {} ORDER BY id_prototipo DESC ".format(TABLE)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            linhas = cursor.fetchall()
            saida = []
            for linha in linhas:
                saida.append(prototipo.Prototipo(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6]))
            var_login = saida
        except Error as e :
            verificador = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login
    else:
        return verificador, None

def get_prototipo(id_prototipos):
    comando = "SELECT * FROM {} WHERE id_prototipo = \'{}\'".format(TABLE, id_prototipos)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            linhas = cursor.fetchall()
            saida = []
            for linha in linhas:
                saida.append(prototipo.Prototipo(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6]))
            var_login = saida
        except Error as e :
            verificador = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login[0]
    else:
        return verificador, None

def modifica(prototipo):
    comando = """UPDATE {} SET nome = \'{}\', ano_fabricacao = \'{}\', status = \'{}\', peso = \'{}\', temporada = \'{}\', n_teste = \'{}\' WHERE id_prototipo = \'{}\'""".format(TABLE,prototipo.nome, prototipo.ano_fabricacao, prototipo.status, prototipo.peso, prototipo.temporada, prototipo.n_teste, prototipo.id)
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

def apagar(prototipo):
    comando = """DELETE FROM {} WHERE id_prototipo = \'{}\'""".format(TABLE, prototipo.id)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            con.commit()
            var_login = True
        except Error as e:
            var_login = False
            send_email(e)
            connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def get_prototipo_max_id():
    comando = "SELECT * FROM {} WHERE id_prototipo = (SELECT MAX(id_prototipo) FROM {});".format(TABLE, TABLE)
    verificador, cursor, con = connection.connect_to_db()
    if verificador == True:
        try:
            cursor.execute(comando)
            linhas = cursor.fetchall()
            saida = []
            for linha in linhas:
                saida.append(prototipo.Prototipo(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6]))
            var_login = saida
        except Error as e :
            verificador = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)
        return verificador, var_login[0]
    else:
        return verificador, None
