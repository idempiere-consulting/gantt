import datetime

def format_date2(epoch):
    return datetime.datetime.fromtimestamp(int( epoch)/1000).strftime('%Y-%m-%d %H:%M:%S')

class switcher(object):
    def __init__(self, token,data,str_in,api):
        self.data = data[0]
        figlio=0
        if str_in=='':
            str_in=self.data['parent']
            figlio=1
        str_id=str_in
        self.token = token
        self.method=data[1]
        self.number= int(str_id[0])+figlio
        self.iDempiere=str_id[1:]
        self.api=api
        print('iniziaizzo lo switcher, ecco i valori in ingresso:')
        print('figlio di ',self.data['parent'],' idcorrente ',str_in)
        print('quindi è di tipo ',self.number, 'con id ',self.iDempiere)
        print('infine tutto:\n',self.data)

    def num2type(self):
        
        print('ricevuto: ','tipo ',self.number,'id ',self.iDempiere)
         
        types={
            1:'project',
            2:'projectphase',
            3:'projecttask',
            4:'projectline'
        }
        method_name= self.method + '_'+types[self.number]   
        print(method_name)
        method = getattr(self,method_name, lambda: 'invalide choise')
        return method()

    def DELETE_project(self):
        print('switcher_method\nid: ',self.number)
        self.api.put_project(self.token,self.data,self.iDempiere)
        return 'project'

    def POST_project(self)        :
        print('switcher_method\nid: ',self.number)
        r=self.data
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
        return self.api.post_project(self.token,data)
    def PUT_project(self):
        print('switcher_method\nid: ',self.number)
        self.api.put_project(self.token,self.data,self.iDempiere)
        return 'project'
    def POST_projectphase(self):
        print('switcher_method\nid: ',self.number)
        data_in=self.data

        data={  
            'C_Project_ID'  : data_in['parent'][1:],
            'Name'          : data_in['text'],
            'StartDate'     : format_date2( data_in['start_date']),
            'EndDate'       : format_date2( data_in['end_date']),
            'S_Resource_ID' : int(data_in['owner_id']),
            'Type'          : data_in['type'],
            'progress'      : data_in['progress'],
            'SeqNo'         : '10'
           }  
        print('sparo \n:',data) 
        return self.api.post_project_phase(self.token,data)    
    def PUT_projectphase(self):
        print('switcher_method\nid: ',self.number)
        data_in=self.data
    

        data={  'id'            : int(self.iDempiere),
                'StartDate'     : format_date2( data_in['start_date']),
                'Type'          : data_in['Type'],
                'EndDate'       : format_date2( data_in['end_date']),
                'progress'      : data_in['progress'],
                'sortorder'     : '0',
                'Name'          : data_in['text'],
                'S_Resource_ID' : int(data_in['S_Resource_ID']),

           
           } 
        self.api.put_project_phase(self.token,data,self.iDempiere)
        return 'phase'
    def PUT_projecttask(self):
        print('switcher_method\nid: ',self.number)
        self.api.put_project_task(self.token,self.data,self.iDempiere)

        return 'task'
    def PUT_projectline(self):
        self.api.put_project_line(self.token,self.data,self.iDempiere)

        print('switcher_method\nid: ',self.number)
        return 'line'        

