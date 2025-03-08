import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error

from database import connection
from error_reporter import send_email
from server.classes import metodologia

TABLE = "TEFT.metodologia"

def creat_metodologia(metodologia):
    comando = """INSERT INTO {} (objetivo, N_pessoas, subgrupo, procedimento, N_voltas, temporada, status) VALUE(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')""".format(TABLE, metodologia.objetivo, metodologia.N_pessoas, metodologia.subgrupo, metodologia.procedimento, metodologia.N_voltas, metodologia.temporada, metodologia.status)
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

def apagar(metodologia):
    comando = """DELETE FROM {} WHERE id_metodologia = \'{}\'""".format(TABLE, metodologia.id_metodologia)
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

def modificar(metodologia):
    comando = ("UPDATE {} SET objetivo = \'{}\', N_pessoas = \'{}\', subgrupo = \'{}\', procedimento = \'{}\', N_voltas = \'{}\',temporada = \'{}\', status = \'{}\' WHERE id_metodologia = \'{}\'".format(TABLE,metodologia.objetivo, metodologia.N_pessoas, metodologia.subgrupo, metodologia.procedimento, metodologia.N_voltas, metodologia.temporada, metodologia.status, metodologia.id_metodologia))
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

def get_metodologias():
    comando = "SELECT * FROM {} ".format(TABLE) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(metodologia.Metodologia(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[7]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def get_metodologias_temporada(temporada):
    comando = "SELECT * FROM {} WHERE temporada = \'{}\'".format(TABLE, temporada) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(metodologia.Metodologia(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[7]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def get_metodologia(id_metodologia):
    comando = "SELECT * FROM {} WHERE id_metodologia = \'{}\'".format(TABLE,id_metodologia) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(metodologia.Metodologia(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[7]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login[0]
    else:
        return verificador, None

def get_metodologia_max_id():
    comando = ("SELECT * FROM {} WHERE id_metodologia = (SELECT MAX(id_metodologia) FROM {});".format(TABLE, TABLE))# comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(metodologia.Metodologia(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[7]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login[0]
    else:
        return verificador, None