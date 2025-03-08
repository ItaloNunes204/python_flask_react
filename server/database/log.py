import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error
from database import connection
from error_reporter import send_email
from server.classes import log

TABLE = "TEFT.logs"

def get_logs():
    comando = f"SELECT * FROM {TABLE}"  # comando SQL
    verificador, cursor, con = connection.connect_to_db()  # Conexão com o banco
    if verificador:
        try:
            cursor.execute(comando)  # Executa o comando
            linhas = cursor.fetchall()
            saida = []
            for linha in linhas:
                # Cria objetos Log com os valores retornados
                saida.append(log.Log(
                    linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6],
                    linha[7], linha[8], linha[9], linha[10], linha[11], linha[12],
                    linha[13], linha[14], linha[15], linha[16], linha[17], linha[18],
                    linha[19], linha[20], linha[21], linha[22], linha[23], linha[24], linha[25],linha[26],linha[27],linha[28]
                ))
            var_login = saida
        except Error as e:
            verificador = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)  # Fecha a conexão
        return verificador, var_login
    else:
        return verificador, None

def get_log(id_log):
    comando = f"SELECT * FROM {TABLE} WHERE id_logs = '{id_log}'"  # comando SQL
    verificador, cursor, con = connection.connect_to_db()  # Conexão com o banco
    if verificador:
        try:
            cursor.execute(comando)  # Executa o comando
            linhas = cursor.fetchall()
            saida = []
            for linha in linhas:
                saida.append(log.Log(
                    linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6],
                    linha[7], linha[8], linha[9], linha[10], linha[11], linha[12],
                    linha[13], linha[14], linha[15], linha[16], linha[17], linha[18],
                    linha[19], linha[20], linha[21], linha[22], linha[23], linha[24], linha[25],linha[26],linha[27],linha[28]
                ))
            var_login = saida[0]
        except Error as e:
            verificador = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)  # Fecha a conexão
        return verificador, var_login
    else:
        return verificador, None

def get_log_piloto_teste(id_piloto, id_teste):
    comando = f"SELECT * FROM {TABLE} WHERE id_piloto = '{id_piloto}' and id_teste = '{id_teste}'"  # comando SQL
    verificador, cursor, con = connection.connect_to_db()  # Conexão com o banco
    if verificador:
        try:
            cursor.execute(comando)  # Executa o comando
            linhas = cursor.fetchall()
            saida = []
            for linha in linhas:
                saida.append(log.Log(
                    linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6],
                    linha[7], linha[8], linha[9], linha[10], linha[11], linha[12],
                    linha[13], linha[14], linha[15], linha[16], linha[17], linha[18],
                    linha[19], linha[20], linha[21], linha[22], linha[23], linha[24], linha[25],linha[26],linha[27],linha[28]
                ))
            var_login = saida
        except Error as e:
            verificador = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)  # Fecha a conexão
        return verificador, var_login
    else:
        return verificador, None

def modifica(log_obj):
    comando = f"""
        UPDATE {TABLE} 
        SET vazao_de_bancada_a = '{log_obj.vazao_de_bancada_a}', wps = '{log_obj.wps}', 
            temperatura_oleo = '{log_obj.temperatura_oleo}', pressao_embreagem = '{log_obj.pressao_embreagem}', 
            id_teste = '{log_obj.id_teste}', tps = '{log_obj.tps}', time = '{log_obj.time}', 
            velo_rte = '{log_obj.velo_rte}', amortecedor_te = '{log_obj.amortecedor_te}', 
            forca_g_long = '{log_obj.forca_g_long}', amortecedor_de = '{log_obj.amortecedor_de}', 
            tensao_bateria = '{log_obj.tensao_bateria}', velo_rtd = '{log_obj.velo_rtd}', 
            pressao_oleo = '{log_obj.pressao_oleo}', temperatura_ar = '{log_obj.temperatura_ar}', 
            temperatura_motor = '{log_obj.temperatura_motor}', pressao_diferencial_combustivel = '{log_obj.pressao_diferencial_combustivel}', 
            sonda_geral = '{log_obj.sonda_geral}', pressao_freio = '{log_obj.pressao_freio}', 
            rpm = '{log_obj.rpm}', marcha = '{log_obj.marcha}', velo_rfe = '{log_obj.velo_rfe}', 
            link = '{log_obj.link}', descricao = '{log_obj.descricao}', 
            forca_g_lateral = '{log_obj.forca_g_lateral}' 
        WHERE id_logs = '{log_obj.id_logs}'
    """
    verificador, cursor, con = connection.connect_to_db()  # Conexão com o banco
    if verificador:
        try:
            cursor.execute(comando)  # Executa o comando
            con.commit()
            var_login = True
        except Error as e:
            var_login = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)  # Fecha a conexão
        return verificador, var_login
    else:
        return verificador, None

def cria_log(log_obj):
    comando = f"""
        INSERT INTO {TABLE} (link, descricao, id_piloto, data, id_teste, passada) 
        VALUES ('{log_obj.link}', '{log_obj.descricao}', 
        '{log_obj.id_piloto}', '{log_obj.data}', '{log_obj.id_teste}', '{log_obj.passada}')
    """
    verificador, cursor, con = connection.connect_to_db()
    if verificador:
        try:
            cursor.execute(comando)  # Executa o comando
            con.commit()
            var_login = True
        except Error as e:
            var_login = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)  # Fecha a conexão
        return verificador, var_login
    else:
        return verificador, None

def apagar_log(id_log):
    comando = f"DELETE FROM {TABLE} WHERE id_logs = '{id_log}'"
    verificador, cursor, con = connection.connect_to_db()
    if verificador:
        try:
            cursor.execute(comando)  # Executa o comando
            con.commit()
            var_login = True
        except Error as e:
            var_login = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)  # Fecha a conexão
        return verificador, var_login
    else:
        return verificador, None

def get_log_data(data):
    comando = f"SELECT * FROM {TABLE} WHERE data = '{data}'"  # comando SQL
    verificador, cursor, con = connection.connect_to_db()  # Conexão com o banco
    if verificador:
        try:
            cursor.execute(comando)  # Executa o comando
            linhas = cursor.fetchall()
            saida = []
            for linha in linhas:
                saida.append(log.Log(
                    linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6],
                    linha[7], linha[8], linha[9], linha[10], linha[11], linha[12],
                    linha[13], linha[14], linha[15], linha[16], linha[17], linha[18],
                    linha[19], linha[20], linha[21], linha[22], linha[23], linha[24], linha[25],linha[26],linha[27],linha[28]
                ))
            var_login = saida[0]
        except Error as e:
            verificador = False
            send_email(e)
        connection.close_connect_to_bd(cursor, con)  # Fecha a conexão
        return verificador, var_login
    else:
        return verificador, None
