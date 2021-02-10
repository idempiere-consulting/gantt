# GANTT PROJECT

## Esigenza

Produrre un grafico GANTT utilizzando un prodotto già pronto per quanto riguarda la parte grafica ([DHTMLX](https://dhtmlx.com/docs/products/dhtmlxGantt/))  di tabelle a scelta su iDempiere, possibilmente in modo parametrico.
Nello specifico si vuole produrre il GANTT della tabella `Progetto` con tutte e tre le sue annidate.

## Soluzione

Utilizzando le API REST di iDempiere otteniamo la parametrizzazione voluta, il gestore della grafica verrà servito da un servizio web in python3:  [flask](https://flask.palletsprojects.com/en/1.1.x/) 

## Componenti
``` mermaid
graph LR
subgraph 'FLASK'

G[GANTT] 
A{{API}}
F[Server]
        subgraph 'conf Risorse'
            cf3[conf]
            mp3[mapping]
        end
        subgraph 'conf Progetto'
            cf1[conf]
            mp1[mapping]
        end
        subgraph 'conf Attività'
            cf2[conf]
            mp2[mapping]
        end

G --- A
A --- F
F -->cf1
F -->mp1
F -->cf2
F -->mp2
F -->cf3
F -->mp3
	subgraph 'iDempiere uno'
	id1[(Progetto)]
	api1{{API}}
    api1 -->id1
    cf1 --> api1
    mp1 -->api1
    end
 
 	subgraph 'iDempiere Due'
    id2[(Attività)]
	api2{{API}}
    api2 -->id2
    cf2 --> api2
    mp2 -->api2
    end
    subgraph 'iDempiere Tre'
    id3[(Risorse)]
	api3{{API}}
    api3 -->id3
    cf3 --> api3
    mp3 -->api3
    end

end    
```

## Software

Il server si occupa di fornire il file indicato nella riga:

​        html= render_template(`'risorse_e_vincoli.html'`)

file che si trova nela cartella  `templates`

`from api_idempiere import api as idapi`

questa è la classe che gestisce le api di iDempiere

`from api_mapping_project import mapping,translator`

qui importo la struttura che si occupa della trasformazione ed adattamento tra i nomi della tabella del gantt con i nomi e i tipi gestiti da iDempiere.





## Mapping

`

mapping={

"c_project" : {

​    "id":["id","strip_id"],

​    "DateContract":["start_date","format_date"],

​    

`

procedura:

il campo che mi arriva dal Gantt con nome id viene mappato, grazie al campo `table_from`  nella API della  tabella corrispondebìnte di idempieere con il nome che trovo dopo i due punti quindi n

