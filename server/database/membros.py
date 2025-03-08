import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from mysql.connector import Error

from database import connection
from error_reporter import send_email
from server.classes import membros
TABLE = "TEFT.membro"

def login(email, senha):
    comando = ("SELECT * FROM {} WHERE email = '{}' and senha = '{}'".format(TABLE, email, senha)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linha = cursor.fetchall()
            # verifica a informação 
            if len(linha) == 0:
                var_login = False
            else:
                var_login = True
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def get_membros():
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
                saida.append(membros.Membros(linha[0],None,linha[2],linha[3]))
            var_login = saida
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def get_membro(email):
    comando = ("SELECT * FROM {} WHERE email = '{}'".format(TABLE, email)) # comando sql 
    verificador, cursor, con = connection.connect_to_db() # coleta as informações para a conexão com o banco 
    if verificador == True:
        try:
            # tenta executar o comando 
            cursor.execute(comando) 
            linhas = cursor.fetchall()
            # verifica a informação
            saida = [] 
            for linha in linhas:
                saida.append(membros.Membros(linha[0],None,linha[2],linha[3]))
            var_login = saida[0]
        except Error as e: # 
            verificador = False
            send_email(e)
        # finaliza a conexão com o banco 
        connection.close_connect_to_bd(cursor,con)
        return verificador, var_login
    else:
        return verificador, None

def modifica(membro):
    if membro.senha != None:
        comando = ("UPDATE {} SET nome = \'{}\', subgrupo = \'{}\', senha = \'{}\'  WHERE email = \'{}\'".format(TABLE, membro.nome, membro.subgrupo, membro.senha, membro.email))
    else:
        comando = ("UPDATE {} SET nome = \'{}\', subgrupo = \'{}\'  WHERE email = \'{}\'".format(TABLE, membro.nome, membro.subgrupo, membro.email))
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

def creat_membro(membro):
    comando = """INSERT INTO {} (nome, email, subgrupo, senha) VALUE (\'{}\', \'{}\',\'{}\',\'{}\')""".format(TABLE, membro.nome, membro.email, membro.subgrupo, membro.senha )
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

def apagar(membro):
    comando = """DELETE FROM {} WHERE email = \'{}\'""".format(TABLE, membro.email)
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
