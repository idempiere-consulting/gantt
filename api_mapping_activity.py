
# questa struttura indica i campi delle api 
# definite su iDempiere (case sensitive, tbd retrive automatico via postgres/psycopg2) 
# e la loro traduzione sui campi del gantt.
# se presente un secondo elemento questo è il nome della funzione di "traduzione" per ripristinare il 
# valore "originale" presente come metodo statico della classe in coda alla struttura: vedasi il campo id per esempio banale
# il campo "api" indica l'endpoint da contattare.
# Fare attenzione al campo tab nella maschera delle api, serve a simulare il comportamento di gestione 
# tramite questa finestra, quindi aprire tale maschera e controllare quali sono i campi obbligatori, quelli con 
# asterisco, oppure fare nuovo record e inserire tutti i campi rossi
# Quindi questa struttura serve nel "viaggio" dei dati DAL gantt AD idempiere
# mnemonicamente uso la tabella rispondendo a questa domanda:
# Per scrivere sulla colonna di IDEMPIERE(SX)    quale campo cerco sul GANTT(DX) e COME lo devo trattare?
#                             "DateContract" :   ["start_date"     ,                   "format_date"],
# la chiave (a sx) è il     il valore a dx è in arrivo
#    nome su IDEMPIERE          DAL GANTT
mapping={
"1"    : "s_resourceassignment",
"9"     : "s_resourceassignment",
"0"     : "c_contactactivity",
"s_resourceassignment" : {
    "id":["id","strip_id"],
    "AssignDateFrom":["start_date","format_date"],
    #"DateFinish":["end_date","format_date"],
    "Qty":"duration",
    "Name":"text",
    "Description":"Description",
    #"ProjectLineLevel":["Type","get_first"],     
    #"isConfirmed":"progress",
    "sortorder":"sortorder",
    # "S_Resource_ID": ["S_Resource_ID","intero"],    NOT UPDATABLE
    #"LIT_gantt_constraint_date":["constraint_date","format_date"],
    #"LIT_gantt_constraint_type":["constraint_type","not_null"],
    "api":"putHourDettaglio",
    "apipost":"postHourDettaglio"
},
"c_contactactivity" : {
    "id":["id","strip_id"],
    "Description":"Description",
    "StartDate":["start_date","format_date"],
    "SalesRep_ID":["S_Resource_ID","intero"],
    "ContactActivityType":"ctype",
    "C_Activity_ID":["C_Activity_ID","intero"],
    "api":"putActivity",
    "apipost":"postContactActivity"
},
"lit_gantt_links" : {
    "id":["id","strip_id"],
    "lit_target":["target","intero"],
    "source":["source","intero"],
    "lit_type":["type","intero"],
    "Name": ["new","new"],
    "api":"Link"
    "apipost":"postLink"

}


# quindi la procedura corretta da seguiere è:
# (disclaimer: non dimenticarsi dell'azzeramento cache se qualcosa non torna)
# - ANDATA
# analizzare le tabelle di interese e PRENDERE NOTA dei campi obbligatori con la select sotto
# creare la vista  su Postgres avendo cura di inswerire anche i campi sopra
# importante creare un campo id che sia uguale all'  ..._id della tabella
# creare la vista su idempiere ed importare i campi 
# creare la API getGantt (esempio ma può essere qualsiasi cosa)
# indicare sul file di configurazione il nome della API appena creata
# procedere così per tutti gli insiemi di dati che mi interessano (Links, resources....)
# - RITORNO
# creare la API verso la tabella di riferimento 
# nella tab field out inserire 
# - come PRIMO campo l'id della tabella 
# - i campi obbligatori 
# - i campi che ci interessa salvare 
# creare la voce di dizionario nel file mapping con lo stesso nome della tabella
# creare le chiavi con lo stesso nome indicato nella API (case sensitive)
# impostare i valori come 
#   - valore secco se il tipo ed i valori passati sono corretti
#   - lista di due valori:
#     * il primo è il nome del campo che arriva dal dhtmlx
#     * il secondo è il nome della funzione di "traduzione"
# aggiungere la chiave "api" che indicherà quale endpoint contattare su idempiere
}
""" 
query per elencare tutti i campi obbligatori (meno i 4 che le API gestiscono di default)
select column_name from information_schema.columns 
where table_name='INSERISCI' 
    and is_nullable='NO' 
    and column_default is  null 
    and column_name not in ('ad_client_id','ad_org_id','createdby','updatedby');
 """

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
        data= datetime.datetime.fromtimestamp(int( epoch)/1000).strftime('%Y-%m-%d %H:%M:%S')
        print('la data modificata:',data,type(data))
        return(data)
        
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

