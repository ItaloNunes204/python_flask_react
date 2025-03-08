import smtplib
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(recipient, subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender = "dataanalysisformulaufmg2024@gmail.com"
    password = "skzv emrw adck mhny"

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(message,'plain'))

    try:
        server = smtplib.SMTP(smtp_server,smtp_port)
        server.starttls()
        server.login(sender, password)

        server.sendmail(sender, recipient, msg.as_string())
        print("email enviado")
    except Exception as e:
        print('erro ao enviar email:{}'.format(e))
    finally:
        server.quit()

def report_error(error):
    emails = ["dataanalysisformulaufmg2024@gmail.com","italonunespereiravieira@gmail.com","italonunca04@gmail.com"]
    for email in emails:
        send_email(email,"Erro no TEFT",error)

def incorrect_access(email):
    emails = ["dataanalysisformulaufmg2024@gmail.com","italonunespereiravieira@gmail.com","italonunca04@gmail.com"]
    for email in emails:
        send_email(email,"acesso incorreto","{} no dia e hora: {}".format(email,datetime.now()))

def erro_imagem(caminho): # envia um emal falando que n foi possivel apagar uma imagem e manda o caminho da imagem 
    pass

def erro_deletar_arquivo(caminho):
    pass