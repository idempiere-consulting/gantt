import requests
import json
import datetime

def format_date(epoch):
    return datetime.datetime.fromtimestamp(int( epoch)/1000).strftime('%d-%m-%Y %H:%M')
def format_date2(epoch):
    return datetime.datetime.fromtimestamp(int( epoch)/1000).strftime('%Y-%m-%d %H:%M:%S')
# 02-04-2017 00:00


def get_url(options):
    '''restituisce una stringa contenente url da contattare \n
       dando in ingresso un dizionario con le informazioni particolari'''
    url = 'http://'    + options['host'] + ':'+ options['port'] + options['path']
    return url

def get_data(opt,token):
    ''' restituisce l'elenco dei task previa login \n
        corrispondente al token passato'''
    print('recupero i dati')
    myheaders= {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+token
        }
    r=requests.get(get_url(opt),headers=myheaders)
    #print(r.text)
    return r.text
    # anche questo funziona 
    # print(r.json())
def get_links(opt,token):
    ''' restituisce l'elenco dei task previa login \n
        corrispondente al token passato'''
    print('recupero i dati')
    myheaders= {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+token
        }
    url='http://5.189.165.60:4081/services/api/idempierepara/web/search/getLinks'
    r=requests.get(url,headers=myheaders)
    #print(r.text)
    return r.text
    # anche questo funziona 
    # print(r.json())

def post_links(token,data_in):
    ''' restituisce la stringa contenente il json dei dati da modificare\n
        \n
        \n
        '''    
    myheaders= {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    data={  
            "source": data_in['source'],                                                                                                                                                                                                               
            "lit_target": data_in['target'],                                                                                                                                                                                                           
            "lit_type": data_in['type'],                                                                                                                                                                                                                 
            "Name": "pippolino"                                                                                                                                                                                                                 

           }
    print('ecco cosa ricevo  datain\n',data_in)           

    print(type(data_in))
    print('\nricevuti dati:\n',data)
    print('\n adesso sparo la postlinks \n(token):',token)
    url='http://5.189.165.60:4081/services/api/idempierepara/web/search/postLinks'
    r=requests.post(url,json=data,headers=myheaders)
    print('ecco la risposta\n',r.text,'\n ti è piaciuta?')
    return r.json()


def get_risorse(opt,token):
    ''' restituisce l'elenco dei task previa login \n
        corrispondente al token passato'''
    myheaders= {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+token
        }
    url='http://5.189.165.60:4081/services/api/idempierepara/web/search/getRisorse'
    r=requests.get(url,headers=myheaders)
    print('le risorse?\n',r.text)
    return r.text
    # anche questo funziona 
    # print(r.json())



def delete_project(token,myid):
    url='http://5.189.165.60:4081/services/api/idempierepara/web/search/delProject_'+myid
    myheaders= {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+token
        }
    r=requests.delete(url,headers=myheaders)
    print('ecco la risposta\n',r.text,'\n ti è piaciuta?')
    return r.json()



        
def put_project(token,data_in,myid):
    ''' restituisce la stringa contenente il json dei dati da modificare\n
        \n
        \n
        '''    
    myheaders= {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    data={  'id'            : int(myid),
            'DateContract'  : format_date2( data_in['start_date']),
            'DateFinish'    : format_date2( data_in['end_date']),
            'progress'      : data_in['progress'],
            'sortorder'     : data_in['sortorder'],
            'Name'          : data_in['text'],
            'Type'          : data_in['Type'],
            'S_Resource_ID' : data_in['S_Resource_ID'],
            'parent'        : data_in['parent']
           }
    print('ecco cosa sparo\n',myid,' data\n',data)           

    print(type(data))
    print('\nricevute le modifiche:\n',data)
    print('\n adesso sparo la put \n(token):',token)
    url='http://5.189.165.60:4081/services/api/idempierepara/web/search/putProject'
    r=requests.put(url,json=data,headers=myheaders)
    print('ecco la risposta\n',r.text,'\n ti è piaciuta?')
    return r.json()

def post_project(token,data_in):
    ''' restituisce la stringa contenente il json dei dati da modificare\n
        \n
        \n
        '''    
    myheaders= {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }

    print('\necco cosa sparo:\n',data_in,'\n')           

    #print(type(data))  # deve essere dict
    url='http://5.189.165.60:4081/services/api/idempierepara/web/search/postProject'
    print('sparata')
    r=requests.post(url,json=data_in,headers=myheaders)
    print('ecco la risposta\n',r.json(),'\n ti è piaciuta?')
    return r.json()
def post_project_phase(token,data):
    myheaders= {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    url='http://5.189.165.60:4081/services/api/idempierepara/web/search/postProjectPhase'
    print('sparata')
    r=requests.post(url,json=data,headers=myheaders)
    print('ecco la risposta\n',r.json(),'\n ti è piaciuta?')
    return r.json()

def put_project_phase(token,data,myid):
    ''' restituisce la stringa contenente il json dei dati da modificare\n
        \n
        \n
        '''    
    myheaders= {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }

    #print(type(data))
    print('\nPUTto le modifiche:\n',data)
    #print('\n adesso sparo la put \n(token):',token)
    url='http://5.189.165.60:4081/services/api/idempierepara/web/search/putProjectPhase'
    r=requests.put(url,json=data,headers=myheaders)
    print('ecco la risposta\n',r.text,'\n ti è piaciuta?')
    return r.json()



def put_project_task(token,data_in,myid):
    ''' restituisce la stringa contenente il json dei dati da modificare\n
        \n
        \n
        '''    
    myheaders= {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    """{'Type': 'task', 'end_date': '1586815200000', 'parent': '11000001', 'progress': '1', 'sortorder': '10', 'start_date': '1585692000000', 'text': 'Progetto 3D', 'duration': '13'}"""
    '''UPDATE c_projectphase set startdate = '2020-02-18 00:00:00' where c_projectphase_id=1000006;
    '''
    
    data={  'id'            : int(myid),
            'AssignDateFrom'     : format_date( data_in['start_date']),
            'Type'          : data_in['Type'],
            'AssignDateTo'       : format_date( data_in['end_date']),
            'progress'      : data_in['progress'],
            'SeqNo'     : data_in['sortorder'],
            'Name'          : data_in['text'],

           
           }
    print('ecco cosa sparo\n',myid,' data\n',data)           
    print('\nricevute le modifiche:\n',data)
    print('\n adesso sparo la put \n(token):',token)
    url='http://5.189.165.60:4081/services/api/idempierepara/web/search/putProjecttask'
    r=requests.put(url,json=data,headers=myheaders)
    print('ecco la risposta\n',r.text,'\n ti è piaciuta?')
    return r.json()



def put_project_line(token,data_in,myid):
    ''' restituisce la stringa contenente il json dei dati da modificare\n
        \n
        \n
        '''    
    myheaders= {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    data={  'id'                : int(myid),
            'AssignDateFrom'    : format_date( data_in['start_date']),
            'Type'              : data_in['Type'],
            'AssignDateTo'      : format_date( data_in['end_date']),
            'Line'              : data_in['sortorder'],
            'Description'       : data_in['text'],
           }

    print('ecco cosa sparo\n',myid,' data\n',data)           
    print('\nricevute le modifiche:\n',data)
    print('\n adesso sparo la put \n(token):',token)
    url='http://5.189.165.60:4081/services/api/idempierepara/web/search/putProjectLine    '
    r=requests.put(url,json=data,headers=myheaders)
    print('ecco la risposta\n',r.text,'\n ti è piaciuta?')
    return r.json()



def get_token(options,user):
    ''' restituisce una stringa contenente il token di autorizzazione\n
        options   contiene le info per la richiesta API\n
        user è un dizionario contenente le due chiavi\n
        username e password'''    
    url=get_url(options)

    #print(url,'\n',user)
    #print(type(user))
    r=requests.post(url,json=user)
    #print('r     ',type(r))
    #print('r.json',type(r.json()['token']))
    
    return r.json()['token']
    # anche questo funziona 
    # print(r.json())
    # qui il gioco è fatto
def update_session(url,token):        
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer '+token})
    # FIXME TODO  verificare il metodo
    response = session.get('https://httpbin.org/headers')
    print(response.json())
