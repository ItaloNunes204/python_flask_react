import mysql.connector

def connect_to_db():
    try:
        con = mysql.connector.connect(host='localhost', database='TEFT', user='root', password='italo175933')
        cursor = con.cursor()
        verificador = True
    except:
        verificador = False
        cursor = None
        con = None
    return verificador, cursor, con

def close_connect_to_bd(cursor, con):
    cursor.close()
    con.close()
