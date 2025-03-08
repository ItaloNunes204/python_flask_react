import os

def join_path(path,folder_file):
    return os.path.join(path,folder_file)

def get_path():
    return os.getcwd()

def get_circuitos_path():
    raiz_projeto = get_path()
    server = join_path(raiz_projeto, "server")
    upload = join_path(server, "upload")
    circuito = join_path(upload, "circuito")
    return circuito

def file_exists(path):
    return os.path.isfile(path)

def delete_file(path):
    if file_exists(path) == True:
        try:
            os.remove(path)
            return True
        except:
            return False
    else:
        return True

def get_creds():
    raiz_projeto = get_path()
    server = join_path(raiz_projeto, "server")
    creds = join_path(server, "creds")
    creds = join_path(creds,"creds.json")
    return creds







def get_documentos_path():
    raiz_projeto = get_path()
    server = join_path(raiz_projeto, "server")
    static = join_path(server, "static")
    upload = join_path(static, "upload")
    documentos = join_path(upload, "documentos")
    return documentos

def get_log():
    raiz_projeto = get_path()
    server = join_path(raiz_projeto, "server")
    logs = join_path(server, "logs")
    return logs

def get_briefing_path():
    documentos = get_documentos_path()
    briefing = join_path(documentos,"briefing")
    return briefing

def get_debriefing_path():
    documentos = get_documentos_path()
    debriefing = join_path(documentos, "debriefing")
    return debriefing

def get_templates_path():
    raiz_projeto = get_path()
    server = join_path(raiz_projeto, "server")
    templates = join_path(server, "templates")
    return templates

def get_json():
    raiz_projeto = get_path()
    server = join_path(raiz_projeto, "server")
    logs = join_path(server, "logs")
    return logs

def lista_diretorio(caminho):
    return os.listdir(caminho)