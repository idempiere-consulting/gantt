
# questa struttura indica i campi delle api 
# definite su iDempiere (case sensitive, tbd retrive automatico via postgres/psycopg2) 
# e la loro traduzione sui campi del gantt.
# se presente un secondo elemento questo è il nome della funzione di "traduzione" per ripristinare il 
# valore "originale" presente come metodo statico della classe in coda alla struttura: vedasi il campo id per esempio banale
# il campo "api" indica l'endpoint da contattare.
# Quindi questa struttura serve nel "viaggio" dei dati DAL gantt AD idempiere
# mnemonicamente uso la tabella rispondendo a questa domanda:
# Per scrivere sulla colonna di IDEMPIERE(SX)    quale campo cerco sul GANTT(DX) e COME lo devo trattare?
#                             "DateContract" :   ["start_date"     ,                   "format_date"],
# la chiave (a sx) è il     il valore a dx è in arrivo
#    nome su IDEMPIERE          DAL GANTT
mapping={
"lit_hour" : {
    "id":["id","strip_id"],
    "DateWorkStart  ":["start_date","format_date"],
    "DateFinish":["end_date","format_date"],
    "Name":"text",
    "ProjectLineLevel":["Type","get_first"],     
    "isConfirmed":"progress",
    "sortorder":"sortorder",
    "S_Resource_ID": ["S_Resource_ID","intero"],
    #"LIT_gantt_constraint_date":["constraint_date","format_date"],
    #"LIT_gantt_constraint_type":["constraint_type","not_null"],
    "api":"putHour"
},
"c_contactactivity" : {
    "id":["id","strip_id"],
    "Name":"text",

    "api":"putActivity"
}

}
import datetime
class translator(object):
    @staticmethod
    def strip_id(id):
        return int(id[1:])
    @staticmethod
    def get_first(type):
        return type[0].upper()
    @staticmethod
    def format_date(epoch):
        if epoch == '':
            return None
        return datetime.datetime.fromtimestamp(int( epoch)/1000).strftime('%Y-%m-%d %H:%M:%S')
        
    @staticmethod
    def intero(string):
        if string== '' :
            return None
        return int(string)
    @staticmethod
    def not_null(string):
        # FIXME attenzione, non vuol dire che il campo sia vincolato not null
        # ma che se arriva stringa vuota passo un valore null

        if string== '' :
            return None
        return string

