from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Resource, Api
from json import dumps,loads
import datetime
#import user
#import json
# la classe che comunica con le API di iDempiere
from api_idempiere import api as idapi
configuration_file="api_config Demo.json"
#visualization_file="qtyduration.html"
visualization_file="risorse_e_vincoli.html"
# la struttura di mappatura tra i campi del gantt e le tabelle di iDempiere
from api_mapping_project import mapping,translator


""" import argparse
parser = argparse.ArgumentParser(description='Server GANTT configurabile verso idempiere.')
parser.add_argument('config_file',nargs='?',help='filename of configuration',default='api_config Consulting.json')
parser.add_argument('mapping_file',nargs='?',help='filename of mapping',default='api_mapping_activity')
args = parser.parse_args()
print(args)
 """#exit

# questa funzione è quella che si occupa "materialmente" di restituire il payload corretto 
# da spedire ad iDempiere traducendo quello in arrivo dal DHTMLX
# devo inserire come parametro l'id perchè non è dentro il payload
# piccola funzione di comodo per stampare chiaramente un json
def pretty_json(json_obj,message=None):
    if message:
        print(message)
    print(dumps(json_obj, sort_keys=False, indent=2))

def translate_data(data_from_gantt,gantt_id=None):
    # arriva qualcosa del tipo :
    #{'S_Resource_ID': '', 'constraint_date': '', 'constraint_type': '', 'end_date': '1598652000000', 'parent': '0', 'progress': '0.71538461', 
    # 'sortorder': '0', 'start_date': '1593554400000', 'table_from': 'c_project', 'text': 'Commessa XXX', 'type': 'Task', 'duration': '59'}
    # inizializzo il payload vuoto
    payload=dict()
    print('/////////////////')
    # ESTRAGGO dai dati che mi arrivano dal DHTMLX la TABELLA da modificare
    tbl=data_from_gantt.pop('table_from')
    # SOLE SE passata AGGIUNGO la chiave id indispensabile per le API PUT
    if gantt_id :
        data_from_gantt['id']=gantt_id
    print('devo modificare la tabella:  ',tbl)
    #mapping[tbl].pop('api')
    # questa è la LISTA delle chiavi che mi ARRIVANO da DHTMLX
    gantt_keys=data_from_gantt.keys()
    print(gantt_keys)
    # adesso ciclo i VALORI della struttura mapping 
    # (vedere mapping.py per la descrizione precisa ma:
    # chiave = nome campo su idempiere
    # valore = chiave in arrivo DAL DHTMLX)
    for k,v in mapping[tbl].items():
        # k è la chiave (--idempiere)
        # v è il valore (--DHTMLX)
        print(k,' <- campo in idempiere in cui scrivere il valore di->',v)
        # imposto un'etichetta in caso sia da ignorare, solo per debug
        api_value='chiave ignorata'
        # se è presente una funzione di traduzione la devo usare!
        #FIXME se è una post l'id non c'è, dovrei ignorarlo:
        # trasformo tutti i valori in liste e aggiungo come terzo valore il metodo
        # e filtro su quello? boh, ci penso....  CHE MOSTRO CHE STA DIVENTANDO!!
        if isinstance(v,list):
            
            # il primo elemento della lista è QUALE chiave contiene il valore che arriva... MALFORMATO per idempiere
            gantt_key=v[0]
            if gantt_key in gantt_keys:
                print('sto processando la chiave DHTMLX: ',gantt_key,' : ',data_from_gantt[gantt_key])

                # il secondo è il nome della funzione di traduzione
                key_tr_func=v[1]
                # cerco nella classe translator il metodo indicato e "me lo prendo come funzione"
                trl=getattr(translator,key_tr_func, lambda: 'invalide choice')
                # siccome è una lista sono sicuro che la chiave esiste da entrambe le parti (idempiere e DHTMLX)
                # quindi trasformo il dato tramite "la funzione presa sopra"
                api_value=trl(data_from_gantt[gantt_key])
                # e lo aggiungo al payload
                payload[k]=api_value
                print('\t',k,api_value)

        else:
            # è indicata una chiave secca, senza funzione di traduzione, va bene così com'è se esiste,
            # infatti qui potrebbe essere un campo di appoggio (api o table from)
            # solo per leggibilità "cambio nome alla variabile"
            gantt_key=v
            # quindi se la chiave è presente nella LISTA delle chiavi che mi ARRIVANO da DHTMLX
            if gantt_key in gantt_keys:
                # qui la chiave è valida, non è campo di appoggio
                # quindi prendo il valore in arrivo che mi interessa
                api_value=(data_from_gantt[gantt_key])
                # e aggiungo la chiave nel payload (data) aggiungo (in caso contrario resta l'etichetta di debug)
                payload[k]=api_value if api_value != '' else None
                print('\t',gantt_key,api_value)
        print('\t',k,api_value)

    print('payload:\n',payload)
    print('/////////////////')
    return payload

# inizializzo la app
app = Flask(__name__)#,
            #static_url_path='', 
            #static_folder='/static',
            #template_folder='templates')
# lo rendo RESTFUL COMPLIANT             
api = Api(app)
# inizializzo l'oggetto che comunicherà con iDempiere
gantt = idapi(config_file=configuration_file)
# FIXME ottengo subito il token di login, non so se è bene così concettualmente
#gantt.login()
#print('ecco il token: ',gantt.token)
#print(gantt.cfg['getTasks'])
# questa è la chiamata principale, quella di inizializzazione dei dati della pagina html
class Login(Resource):
    # una funzione per metodo, qui basta la GET, sto prendendo i dati da iDempiere

    def get(self):
        print('login class')
        pass
class Data(Resource):
    # una funzione per metodo, qui basta la GET, sto prendendo i dati da iDempiere

    def get(self):
        # prendo i dati separatamente e poi li assemblo
        #print(gantt)
        def minuscolizza(dict):
            newd={k.lower():v  for k,v in dict.items()}
            # newd['Name']='pippo'
            return newd
# minuscolizzo TUTTI i nomi che mi arrivano per il DHTMLX
        


        tasks=gantt.query('get',gantt.cfg['getTasks'])
        tasks_json=loads(tasks.text)
        tasks_json=list(map(minuscolizza ,tasks_json))
        pretty_json(tasks_json,'TASKS')
        
        links=gantt.query('get','getLinks')
        links_json=loads(links.text)
        links_json=list(map(minuscolizza ,links_json))
        pretty_json(links_json,'LINKS')        
        #links_dict=links_json.values.to_dict()
        #links_dict['target']=links_dict['Target']
        
        resources=gantt.query('get','getResources')
        resources_json=loads(resources.text)
        resources_json=list(map(minuscolizza ,resources_json))
        pretty_json(resources_json,'RISORSE')
        
        # qualsiasi altro dato che volessi far processare al gantt devo metterlo dentro a collections e poi importarlo dentro al javascript
        #links_json=[]
        #resources_json=[]
        # assemblamento finale
        result= {'tasks': tasks_json,"links": links_json ,'collections':{'my_resources':resources_json,'otherone':[]}}
        #print(result)
        pretty_json(result)
        return  result
        
# quando MODIFICO un "task" viene eseguita questa
class TASK_change(Resource):
    # ovviamente modifica generica (cancellazione più sotto)
    def put(self,myid):
        ''' myid è una stringa'''
        print('\n*********************\nNidificazione progetto..',myid[0])
        print('tipo id \n',myid)
        # request è definito da flask (riga 1), non confondere con libreria requests
        # estraggo il payload del gantt e lo trasformo nel tipo dizionario per manipolarlo
        r=request.values.to_dict()
        print('change task\n',r)
        # costruisco la parte finale della endPoint da contattare
        api= mapping[r['table_from']]['api']
        # trasformo il payload
        payload=translate_data(r,myid)
        # finalmente eseguo la PUT API
        r=gantt.query('put',api,payload)
        print(r.content,'\nfinished change',myid,'\n-------------------\n')
    # quando ELIMINO un task
    def  delete(self,myid):
        ''' myid è una stringa'''
        print('tipo id \n',myid)
        print('\n*********************\nNidificazione progetto..',myid[0])
        # questa chiamata è la più semplice, basta indicare l'id da cancellare e l'endpoint
        #idapi.delete(gantt.token,myid[1:])
        print('finished delete',myid,'\n-------------------\n')
# quando AGGIUNGO un task        
class TASK_add(Resource):
    # necessario metodo POST
    def post(self):
        # il payload in arrivo dal DHTMLX, comodamnete trasformato in dizionario
        r=request.values.to_dict()
        print('aggiungo task, ecco cosa mi arriva\n',r)
        #TODO TODO tutta da implementare, molto molto male!!!!!
        # prima di tutto si tratta di distinguere il livello, ricordo che l'unico modo a me noto
        # che DHTMLX usa è quello del 'parent', quindo credo che questo sia il fattore determinante
        # non mi torna infatti la table from a meno che non la inserisca a forza ma mi pare complicato
        # costruisco la parte finale della endPoint da contattare
        #api= mapping[r['table_from']]['apipost']
        first_char=r['parent'][0]
        print(mapping[first_char])  # devo prima cercare il n
        api= mapping[mapping[first_char]]['apipost']
        # trasformo il payload
        r['table_from']=mapping[first_char]
        payload=translate_data(r)
        # finalmente eseguo la POST API
        r=gantt.query('post',api,payload)
        print(r.content,'\nfinished POST, quasi implementato','\n-------------------\n')

class LINK_change(Resource):
    def put(self,id):
        r=request.values.to_dict()
        payload=r
        gantt.query('put',api,payload)

        print(id)
    def delete(self,id):
        print('cancello link: ',id)
        gantt.delete('deleteLink',id)
        rr=request.values.to_dict()
        r=(rr,request.method)
        print('delete link\n',r) 
        print('finished link change',id,'\n-------------------\n')

class LINK_add(Resource):

    def post(self):
        print('aggiungo link')
        r=request.values.to_dict()
        r['Name']='pippo'
        r['table_from']='lit_gantt_links'
        payload=translate_data(r)

        print('\n*********************\nadd link..',payload)
        response=gantt.query('post','postLink',payload)

        #idapi.post_links(self,payload=r)
        print('finished add link','\n-------------------\n',response.request.body)
        """ 
DEVO CAPIRE come fare a renderizzare il template jinja!!!
class home_ganttt(Resource):
    def get(self):
        print(request.method,' si parte')
        return render_template('gantt.html')
api.add_resource(home_ganttt,'/home')
 """
# qui indirizzo alle funzioni locali le API che mi arrivano dal DHTMLX, 
# il dato tra parentesi angolate è una variabile
api.add_resource(Data, '/data')
api.add_resource(TASK_change,'/api/task/<myid>')
api.add_resource(TASK_add,'/api/task')
api.add_resource(LINK_change,'/api/link/<id>')
api.add_resource(LINK_add,'/api/link')
#api.add_resource(LOGIN,'/api/login/')

@app.route('/')
def index():
    print('punto di ingresso')
    return render_template('index.html')

@app.route('/profile')
def profile():
    print('profile')

    return render_template('profile.html')

""" @app.route('/loginauth')
def loginauth():
    return render_template('loginauth.html')
 """
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email,password,gantt.cfg['login_user']['username'],gantt.cfg['login_user']['password'])
    remember = True if request.form.get('remember') else False
    print(gantt.cfg)
    if email == gantt.cfg['login_user']['username'] and password ==gantt.cfg['login_user']['password']:
        gantt.login()
        return redirect(url_for('home_gantt'))
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
#    if not user or not check_password_hash(user.password, password):
 #       flash('Please check your login details and try again.')
   #     return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('loginq'))
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    print('logout')
    return render_template('logout.html')
    
        # se user uguale a quello della configurazione allora faccio il 
    # gantt.login() così da prendere il token) e renderizzo il gantt


# decoratore per "interfacciare" la chiamata API con le funzioni interne alla classe
# API principale
@app.route('/gantt') 
# se volessi gestire un parametro potrei fare così
#@app.route('/<task>')
# essendo il parametro passato di default a ''
def home_gantt(task=''):
        print(request.method,' si parte')
        #return render_template('gantt copy.html')
        #html= render_template('gantt.html')
#        html= render_template('ganttRisorseNOTchange.html')
        #html=render_template('gantt.html',task=task)
        #html=render_template('constraints.html')
        #html=render_template('ganttRisorse.html')
        #html=render_template('child1.html')
        #html=render_template('04_resource.html')
        #html=render_template('risorse_test.html')
        #html= render_template('04_resource_usage_diagram.html')
        #html= render_template('05_resource_usage_templates copy.html')   # ok  funziona quasi tutto
        #html= render_template('risorse_e_vincoli.html')
        #html= render_template('attivita.html')
        #html = render_template('01_basic_init copy.html')
        #html = render_template('Cons_base.html')       # di base, solo task e bottoni scala 
#        html = render_template('qtyduration copy.html')
      #  html = render_template('qtyduration.html')
        html = render_template(visualization_file)
        #html = render_template('login.html')

        #html = render_template('V_test.html')
        #html= render_template('vincoli.html')   #esempio funzionante
        #html= render_template('25_click_drag_select_by_drag.html')
        # 19_constraints_scheduling copy  
        #html= render_template('19_constraints_scheduling copy.html')
        #html=render_template('samples/03_scales/09_skip_weekends.html')  # non mostra i  weekend, solo giorni lavorativi
        #html=render_template('18_linked_tasks.html') # interessante: evidenzia i collegamenti
        #html=render_temlate('samples/11_resources/11_resource_histogram_display_tasks.html')
        #print(html)
        return html
# per poter aprire all'esterno il server di sviluppo senza usare librerie esterne CORS
@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response        
# potrei lanciare lo script direttamente allora prenderebbe il parametro indicato
if __name__ == '__main__':
    print('giro')
    #app.run(host='127.0.0.1', port=8090, debug=True)



""" {'tasks': 
[{
    'id': 11006353, 
    'owner': 1000226, 
    'parent': 91003929, 
    'duration': 0, 
    'progress': '0', 
    'sortorder': '0', 
    'start_date': '2020-12-03 15:33:02', 
    'end_date': '2020-12-03 15:33:02', 
    'table_from': 'lit_hour', 
    'text': '999-testone'}, 
    {'duration': 1, 'end_date': None, 'id': 91003929, 'owner': None, 'parent': 0, 'progress': '0.5', 'sortorder': '0', 'start_date': '2020-12-03 15:34:46', 'table_from': 'c_contactactivity', 'text': '999 testone'}], 'links': '[]'}
12
 """
