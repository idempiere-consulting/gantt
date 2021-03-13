
# questa struttura indica i campi delle api 
# definite su iDempiere (case sensitive, tbd retrive automatico via postgres/psycopg2) 
# e la loro traduzione sui campi del gantt.
# se presente un secondo elemento questo è il nome della funzione di "traduzione" per ripristinare il 
# valore "originale" presente come metodo statico della classe in coda alla struttura: vedasi il campo id per esempio banale
# il campo "api" indica l'endpoint da contattare.

mapping={
"c_project" : {
    "id":["id","strip_id"],
    "DateContract":["start_date","format_date"],
    "DateFinish":["end_date","format_date"],
    "Name":"text",
    "ProjectLineLevel":["type","get_first"],     
    "progress":"progress",
    "sortorder":"sortorder",
    "S_Resource_ID": ["s_resource_id","intero"],
    "LIT_gantt_constraint_date":["constraint_date","format_date"],
    "LIT_gantt_constraint_type":["constraint_type","not_null"],
    "api":"Project"
},
"c_projectphase" : {
    "id":["id","strip_id"],
    "StartDate":["start_date","format_date"],
    "EndDate":["end_date","format_date"],
    "Name": "text",
    "Type": "type",
    "progress": "progress",
    "SeqNo": "sortorder",
    "S_Resource_ID": ["s_resource_id","intero"],
    "LIT_gantt_constraint_date":["constraint_date","format_date"],
    "LIT_gantt_constraint_type":["constraint_type","not_null"],
    "api":"ProjectPhase"
},

"c_projecttask" :{ 
    "id":["id","strip_id"],
    "AssignDateFrom":["start_date","format_date"],
    "AssignDateTo":["end_date","format_date"],
    "Name": "text",
    "Type": "type",
    "progress": "progress",
    "SeqNo": "sortorder",
    "S_Resource_ID": ["s_resource_id","intero"],
    "LIT_gantt_constraint_date":["constraint_date","format_date"],
    "LIT_gantt_constraint_type":["constraint_type","not_null"],
    "api":"ProjectTask"
},
"c_projectline" : {
    "id":["id","strip_id"],
    "AssignDateFrom":["start_date","format_date"],
    "AssignDateTo":["end_date","format_date"],
    "Description": "text",
    "Type": "type",
    "progress": "progress",
    "Line": "sortorder",
    "S_Resource_ID": ["S_Resource_ID","intero"],
    "LIT_gantt_constraint_date":["constraint_date","format_date"],
    "LIT_gantt_constraint_type":["constraint_type","not_null"],
    "api":"ProjectLine"
},
"lit_gantt_links" : {
    "id":["id","strip_id"],
    "lit_target":["target","intero"],
    "source":["source","intero"],
    "lit_type":["type","intero"],
    "Name": ["new","new"],
    "api":"Link"

}

}
import datetime
class translator(object):
    @staticmethod
    def strip_id(id):
        return int(id[1:])
    @staticmethod
    def get_first(type):
        # FIXME solo perchè il caso è semplice faccio così
        # altrimenti dovrei fare un array....
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
    @staticmethod
    def new(string):
        return "progetto"
