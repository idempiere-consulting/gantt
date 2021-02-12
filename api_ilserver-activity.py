from flask import Flask, request, render_template
from flask_cors import CORS
from flask_restful import Resource, Api
from json import dumps,loads
import json
#from flask_jsonpify import jsonify
from api_idempiere import api as idapi
from api_mapping_activity import mapping,translator
#from api_payload_Demo import putProject,putProjectPhase,putProjectTask,putProjectLine  #,dagantt

import datetime

def translate_data(data_from_gantt,gantt_id):
    # arriva questo :
    #{'S_Resource_ID': '', 'constraint_date': '', 'constraint_type': '', 'end_date': '1598652000000', 'parent': '0', 'progress': '0.71538461', 
    # 'sortorder': '0', 'start_date': '1593554400000', 'table_from': 'c_project', 'text': 'Commessa XXX', 'type': 'Task', 'duration': '59'}
    # la mia mappa è fatta così:
    """ mapping= {
    "c_project" : {
            "id":               ["id","strip_id"],
            "DateContract":     "start_date",
            "DateFinish":       "end_date",
            "Name":             "text",
            "ProjectLineLevel": "type",     
            "progress":         "progress",
            "sortorder":        "sortorder",
            "S_Resource_ID":    "S_Resource_ID",
            "LIT_gantt_constraint_date":"constraint_date",
            "LIT_gantt_constraint_type":"constraint_type",
            "parent":"parent",
            "api":"Project"
    }, 
    "c_projectphase" : {
    ......
    }
    """
    # inizializzo il payload vuoto
    data=dict()
    print('/////////////////')
    # ESTRAGGO dai dati che mi arrivano dal gantt la tabella da modificare
    tbl=data_from_gantt.pop('table_from')
    data_from_gantt['id']=gantt_id
    print('devo modificare la tabella:  ',tbl)
    #mapping[tbl].pop('api')
    gantt_keys=data_from_gantt.keys()
    for k,v in mapping[tbl].items():
        print(k,v)
        # se è presente una funzione di traduzione la devo usare!
        if isinstance(v,list):
            # il primo elemento della lista è il valore che arriva... malformato per idempiere
            gantt_key=v[0]
            # il secondo è il nome della funzione di traduzione
            key_tr=v[1]
            trl=getattr(translator,key_tr, lambda: 'invalide choise')
            # siccome è una lista sono sicuro che la chiave esiste da entrambe le parti
            # quindi trasformo il dato 
            api_value=trl(data_from_gantt[gantt_key])
            # e lo aggiungo al payload
            data[k]=api_value
            print('\t',k,api_value)

        else:
            # qui potrebbe essere un campo di appoggio (api o table from)
            gantt_key=v
            if gantt_key in gantt_keys:
                # solo se la chiave è valida la aggiungo
                api_value=(data_from_gantt[gantt_key])
                data[k]=api_value if api_value != '' else None
    print('payload:\n',data)
    print('/////////////////')
    return data
#db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)#,
            #static_url_path='', 
            #static_folder='/static',
            #template_folder='templates')
#api = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)
gantt = idapi(config_file="api_config Consulting.json")
gantt.login()
print(gantt.token)

token=''
tasks=gantt.query('get','getTasks')


class Data(Resource):
    def get(self):
        
        tasks=gantt.query('get','getTasks')
        tasks_json=loads(tasks.text)
        """ links=gantt.query('get','getLinks')
        links_json=loads(links.text)
        resources=gantt.query('get','getResources')
        resources_json=loads(resources.text)
         """
        # qualsiasi altro dato che volessi far processare al gantt devo mettorlo dentro a collections e poi importarlo dentro al javascript
        links_json=[]
        resources_json=[]

        result= {'tasks': tasks_json,"links": links_json ,'collections':{'my_resources':resources_json,'otherone':[]}}
        print(result)
        return  result
        

class TASK_change(Resource):
    def put(self,myid):
        global token
        ''' attenzione parent su altra api???? non ricordo....
        '''
        ''' id è una stringa'''
        print('\n*********************\nprogetto..',myid[0])
        print('tipo id \n',myid)
        # request è definito da flask, non confondere con libreria reequests
        r=request.values.to_dict()
        print('change task\n',request.values.to_dict())
        api='put' + mapping[r['table_from']]['api']
        payload=translate_data(r,myid)
        gantt.query('put',api,payload)
        print('finished change',myid,'\n-------------------\n')
#{'S_Resource_ID': '', 'constraint_date': '', 'constraint_type': '', 'end_date': '1598652000000', 'parent': '0', 'progress': '0.71538461', 'sortorder': '0', 'start_date': '1593554400000', 'table_from': 'c_project', 'text': 'Commessa XXX', 'type': 'Task', 'duration': '59'}

    def  delete(self,myid):
        global token
        ''' attenzione parent su altra api
        '''
        ''' id è una stringa'''
        print('tipo id \n',myid)
        print('\n*********************\nprogetto..',myid[0])
        idapi.delete_project(token,myid[1:])
        rr=request.values.to_dict()
        r=(rr,request.method)
        print('change task\n',r) 
        #sw=switcher(token,r,myid,idapi)
        #rr=sw.num2type()
        #print('si è scelto: ',rr)
        #idapi.put_project_phase(token,request.values.to_dict(),id)
        print('finished change',myid,'\n-------------------\n')
        
class TASK_add(Resource):

    def post(self):
        r=request.values.to_dict()
        print('aggiungo task, ecco cosa mi arriva\n',r)
        print('\n*********************\nprogetto..',r['text'])
        data={  'C_Currency_ID' : '102',
            'Seq_No'      : r['progress'],
            'Name'          : r['text'],
            'Value'         : r['text']
           }
        
        data={  'C_Currency_ID' : '102',
                'DateContract'  : format_date2( r['start_date']),
                'DateFinish'    : format_date2( r['end_date']),
                'Seq_No'      : r['progress'],
                'Name'          : r['text'],
                'Value'         : r['text'],
                'Type'          : r['Type'],
                #'S_Resource_ID' : '1000004',
                'CopyFrom'        : r['parent']
           }
        #print('provo ad inserire \n',data)

        #idapi.post_project(token,data)
        sw=switcher(token,(r,request.method),'',idapi)
        rr=sw.num2type()
        print('si è scelto: ',rr)
        #idapi.put_project_phase(token,request.values.to_dict(),id)
        print('finished change',r['text'],'\n-------------------\n')




        pass
class LINK_change(Resource):
    def put(self,id):
        print(id)
    def delete(self,myid):
        global token
        ''' id è una stringa'''
        print('cancello link: ',myid)
        idapi.delete_link(token,myid[1:])
        rr=request.values.to_dict()
        r=(rr,request.method)
        print('delete link\n',r) 
        #sw=switcher(token,r,myid,idapi)
        #rr=sw.num2type()
        #print('si è scelto: ',rr)
        #idapi.put_project_phase(token,request.values.to_dict(),id)
        print('finished delete',myid,'\n-------------------\n')

class LINK_add(Resource):

    def post(self):
        print('aggiungo link')
        r=request.values.to_dict()
        print('\n*********************\link..',r)
        print('add link\n',r)
        idapi.post_links(token,r)
        print('finished add link','\n-------------------\n')
        """ 
DEVO CAPIRE come fare a renderizzare il template jinja!!!
class home_ganttt(Resource):
    def get(self):
        print(request.method,' si parte')
        return render_template('gantt.html')
api.add_resource(home_ganttt,'/home')
 """

api.add_resource(Data, '/data') # Route_4

api.add_resource(TASK_change,'/api/task/<myid>')
api.add_resource(TASK_add,'/api/task')
api.add_resource(LINK_change,'/api/link/<id>')
api.add_resource(LINK_add,'/api/link')


@app.route('/')
#@app.route('/<task>')

def home_gantt(task=''):
        print(request.method,' si parte')
        #return render_template('gantt copy.html')
        #html= render_template('gantt.html')
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
        html = render_template('Cons_base.html')       # di base, solo task e bottoni scala 
        #html= render_template('vincoli.html')   #esempio funzionante
        #html= render_template('25_click_drag_select_by_drag.html')
        # 19_constraints_scheduling copy  
        #html= render_template('19_constraints_scheduling copy.html')
        #html=render_template('samples/03_scales/09_skip_weekends.html')  # non mostra i  weekend, solo giorni lavorativi
        #html=render_template('18_linked_tasks.html') # interessante: evidenzia i collegamenti
        #html=render_temlate('samples/11_resources/11_resource_histogram_display_tasks.html')
        #print(html)
        return html
        






@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response        

if __name__ == '__main__':
     print('giro')
     app.run(port='5002')




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