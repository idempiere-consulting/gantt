# GANTT
server  per fornire la funzionalità GANTT integrato ad iDempiere
si compone di un server python flask per fornire un file html "statico" ma creato dinamicamente all'avvio del progetto
nella cartella templates ci sono tutti i pezzi da assemblare per creare la pagina completa.
# Prerequisiti:
-  API funzionanti per interagire con le tabelle interessate dal gantt
-  python3 più flask e virtualenv..
-  il repository contiene già l'oggetto gantt ma volendo si può sovrascrivere con versione aggiornata

##  API funzionanti
abilitare su idempiere le API REST (maschera `Web Services Sicurezza`)
- GET     per recuperare i dati
- POST    per inserire un record nella tabella
- PUT     per modificare i dati di un record
- DELETE  per cancellare un record

utile la query SQL che mostra i campi obbligatori ma che non hanno un valore di default:
(per esempio tabella c_project)
```
select column_name from information_schema.columns 
where table_name='c_project' and is_nullable='NO' and column_default is  null 
    and column_name not in ('ad_client_id','ad_org_id','createdby','updatedby');
```
## python3 più flask e virtualenv
### virtual environment
```
apt install python3 python3-venv python3-pip
```
### debugging tools
```
apt install curl lynx
```
### attiviamo e installiamo le dipendenze
```
mkdir gantt
cd gantt/
python3 -m venv gantV 
. gantV/bin/activate  
python3 -m pip install Flask Flask-restful requests
```
### script di aiuto per avviare il server
```
cat > gantt_start.sh
python --version
cd /root/gantt
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_ENV=development
export FLASK_APP=ilserver-risorse.py
. /root/gantt/gantV/bin/activate
python --version
flask run --host=0.0.0.0 --port=8090
CTRL + D
```
per avviare il server lanciare lo script
```
bash gantt_start.sh
```
## Strumenti utili da riga di comando per eseguire test
(con riferimento alla macchina 140 su test1 ed utente demo@ciao.com, cambiare i dati in accordo )
#### creare user.json
```
cat >user.json
{
        "username": "demo@ciao.com",
        "password": "inserisci qui la password che tu conosci :-)"
}
CTRL + D
```
NOTE:
- le virgolette è importante che siano doppie.. nella bash, in python non creano problemi
- i campi di tipo NUMERICO non devono essere virgolettati, verificare il caso specifico del tipo sulla tabella
```
cat>> ~/.bashrc 
alias token='TOKEN=$(curl -d "@user.json" -H "Content-Type: application/json" -X "POST" http://192.168.0.40:8081/services/api/auth/login )'
alias tokeno='echo $TOKEN|sed s/^.*\":\"//|sed s/\",\".*$//'
alias mycurl='token && curl'
CTRL + D
. ~/.bashrc
```
in seguito per testare una API REQUEST basterà creare il payload json ( per esempio vogliamop inserire un link)
```
cat >links.json
{
        "source": "21000012",
        "lit_target": "21000013",
        "lit_type": "task",
        "Name": "pippotask"

}
```
e lanciare il comando
```
mycurl \
-d "@links.json" \
-H "Content-Type: application/json" -H "Authorization: Bearer  $(tokeno)" \
-X "POST" http://192.168.0.40:8081/services/api/idempierepara/web/search/postLinks && \
echo
```
NOTE: ipotizzo di lanciare il comando dalla stessa macchina che fornisce le API, se usassi localhost o 127.0.0.1 non funzionerebbe.
ovviamente per accedere da fuori bisogna conoscere il forward della porta su proxmox, in questo caso test1:4081

### otteremo qualcosa del tipo:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   233  100   160  100    73  24566  11208 --:--:-- --:--:-- --:--:-- 26666
{"message":"model inserito"}
root@db-id-Scheduler:~/gantt# 
```
## Controllare i log di idempiere
``` 
alias log_name='date +/opt/idempiere/idempiere-Test/log/idempiere.%Y-%m-%d_0.log'
tail -f $(log_name)
```
NOTE: l'alias sopra fa riferimento al file di log con indice 0, eventualmente verificare che il numero sia giusto




