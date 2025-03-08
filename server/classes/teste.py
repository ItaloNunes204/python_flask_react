import sys
import os
from datetime import timedelta

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from path_manager import get_briefing_path, get_debriefing_path

class Teste:
    def __init__(self, id, nome, pilotos, id_objetivos, N_voltas, inicio, fim, almoco, data, id_prototipo, id_circuito, status, observacao):
        self.id = id
        self.nome = nome
        self.pilotos = pilotos
        self.id_objetivos = id_objetivos
        self.N_voltas = N_voltas
        self.inicio = inicio
        self.fim = fim
        self.almoco = almoco
        self.data = data
        self.id_prototipo = id_prototipo
        self.id_circuito = id_circuito
        self.status = status
        self.observacao = observacao
        if self.id is not None:
            self.briefing = get_briefing_path() + "briefing" + str(self.id) + ".pdf"
            self.debriefing = get_debriefing_path() + "debriefing" + str(self.id) + ".pdf"
        else:
            self.briefing = None
            self.debriefing = None

    def modificar(self, nome, pilotos, id_objetivos, inicio, fim, almoco, data, id_prototipo, id_circuito):
        self.nome = nome
        self.pilotos = pilotos
        self.id_objetivos = id_objetivos
        self.inicio = inicio
        self.fim = fim
        self.almoco = almoco
        self.data = data
        self.id_prototipo = id_prototipo
        self.id_circuito = id_circuito

    def serialize_timedelta(self, value):
        if isinstance(value, timedelta):
            # Retorna o número de segundos do timedelta
            return value.total_seconds()
        return value

    def to_dict(self):
        def timedelta_to_str(td):
            total_minutes = int(td.total_seconds() // 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"{hours:02}:{minutes:02}"

        return {
            "id": self.id,
            "nome": self.nome,
            "pilotos": self.pilotos,
            "id_objetivos": self.id_objetivos,
            "N_voltas": self.N_voltas,
            "inicio": timedelta_to_str(self.inicio),
            "fim": timedelta_to_str(self.fim),
            "almoco": self.almoco,
            "data": str(self.data.day) + "/" + str(self.data.month) + "/" + str(self.data.year),
            "id_prototipo": self.id_prototipo,
            "id_circuito": self.id_circuito,
            "status": self.status,
            "observacao": self.observacao,
            "briefing": self.briefing if hasattr(self, 'briefing') else None,
            "debriefing": self.debriefing if hasattr(self, 'debriefing') else None,
            "URL_briefing": get_briefing_path() + "briefing" + str(self.id) + ".pdf",
            "URL_debriefing": get_debriefing_path() + "debriefing" + str(self.id) + ".pdf"
        }
