from flask import Flask, request, render_template
from flask_cors import CORS
from flask_restful import Resource, Api
from json import dumps,loads
from flask_jsonpify import jsonify
import idempiereAPI as idapi
import apiconfig as cfg
from switcher import switcher
import datetime


def format_date2(epoch):
    return datetime.datetime.fromtimestamp(int( epoch)/1000).strftime('%Y-%m-%d %H:%M:%S')


#db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__,
            #static_url_path='', 
            #static_folder='/static',
            template_folder='templates')
#api = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)
token=''


class Data(Resource):
    def get(self):
        print('quantomeno ce provo')
        global token
        if token == '':
            token=idapi.get_token(cfg.options_token,cfg.user)
        #print(token)
        tasks=idapi.get_data(cfg.options_tasks,token)
        tasks_json=loads(tasks)
        links=idapi.get_links(cfg.options_tasks,token)
        links_json=loads(links)
        links_tr1=[dict(('target' if k=='lit_target' else k,v) for k,v in item.items()) for item in links_json]
        links_json=[dict(('type' if k=='lit_type' else k,v) for k,v in item.items()) for item in links_tr1]

        #print(tasks_json)
        result= {'tasks': tasks_json,"links": links_json}
        #print(result)
        return  result


class Risorse(Resource):
    def get(self):
        global token
        if token == '':
            token=idapi.get_token(cfg.options_token,cfg.user)
        #print(token)
        tasks=idapi.get_risorse(cfg.options_tasks,token)
        tasks_json=loads(tasks)
        #print(tasks_json)
        result= {'tasks': tasks_json}
        return  result

class TASK_change(Resource):
    def put(self,myid):
        global token
        ''' attenzione parent su altra api
        '''
        ''' id è una stringa'''
        print('tipo id \n',myid)
        print('\n*********************\nprogetto..',myid[0])
        r=request.values.to_dict()
        print('change task\n',request.values.to_dict())
        sw=switcher(token,(r,request.method),myid,idapi)
        rr=sw.num2type()
        print('si è scelto: ',rr)
        #idapi.put_project_phase(token,request.values.to_dict(),id)
        print('finished change',myid,'\n-------------------\n')


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
                'Type'          : r['type'],
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
api.add_resource(Risorse, '/risorse') # Route_4
api.add_resource(TASK_change,'/api/task/<myid>')
api.add_resource(LINK_change,'/api/link/<id>')
api.add_resource(LINK_add,'/api/link')
api.add_resource(TASK_add,'/api/task')


@app.route('/')
#@app.route('/<task>')

def home_gantt(task=''):
        print(request.method,' si parte')
        #return render_template('gantt copy.html')
        #return render_template('gantt.html')
        #html=render_template('gantt.html',task=task)
        html=render_template('constraints.html')

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
