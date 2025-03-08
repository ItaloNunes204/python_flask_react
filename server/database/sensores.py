import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error

from database import connection
from error_reporter import send_email
from server.classes import sensores
TABLE = "TEFT.sensores"

def creat_sensores(sensor):
    comando = """INSERT INTO {} (nome, id_prototipo, informacao) VALUE (\'{}\', \'{}\',\'{}\')""".format(TABLE,sensor.nome, sensor.id_prototipo, sensor.informacao)
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

def get_sensores():
    comando = ("SELECT * FROM {} ORDER BY nome ASC".format(TABLE)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(sensores.Sensores(linha[0],linha[2],linha[1],linha[3]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def get_sensor(id_sensor):
    comando = ("SELECT * FROM {} WHERE id_sensor = '{}'".format(TABLE, id_sensor)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(sensores.Sensores(linha[0],linha[2],linha[1],linha[3]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login[0]
    else:
        return verificador, None

def get_sensor_prototipo(id_prototipo):
    comando = ("SELECT * FROM {} WHERE id_prototipo = '{}'".format(TABLE, id_prototipo)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(sensores.Sensores(linha[0],linha[2],linha[1],linha[3]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def modificar(sensor):
    comando = ("UPDATE {} SET nome = \'{}\', id_prototipo = \'{}\', informacao = \'{}\'  WHERE id_sensor = \'{}\'".format(TABLE, sensor.nome, sensor.id_prototipo, sensor.informacao, sensor.id_sensor))
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

def apagar(sensor):
    comando = """DELETE FROM {} WHERE id_sensor = \'{}\'""".format(TABLE, sensor.id_sensor)
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

def get_sensor_max_id():
    comando = ("SELECT * FROM {} WHERE id_sensor = (SELECT MAX(id_sensor) FROM {});".format(TABLE, TABLE)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(sensores.Sensores(linha[0],linha[2],linha[1],linha[3]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login[0]
    else:
        return verificador, None
