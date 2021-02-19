
import json
import requests
import datetime

class api(object):
    """base class to manage iDempiere API REST"""
    def __init__(self,config_file="api_config Demo.json"):
        """initialize api class, bringing the config file explicitally 
           it manages parameters according to"""
        with open(config_file, "r") as read_file:
            self.cfg = json.load(read_file)
            #print(self.cfg)
        self.base_url=self.get_base_url()
        self.login_path=self.get_login_url()
        self.query_path=self.get_url()
        self.config_file=config_file
        self.login()
        self.method=""
        self.data = ""
    def get_base_url(self):
        """returns the url base to build former API call"""
        s="s" if self.cfg.get("ssl") else ""
        url ="http" + s + "://" + self.cfg.get("host") + ":" + self.cfg.get("port") + "/"
        return url
    def get_login_url(self):
        """ returns url to call for logging in"""
        path=self.cfg.get("path")["login"]
        url=self.base_url + path
        return url
    def get_url(self,path="query"):
        '''return the complete url for requests
        path tells if login-call or query-call (default one)'''
        path=self.cfg.get("path")[path]
        url=self.base_url + path
        return url
    def set_query_header(self):
        """build and set headers with autentication token pre-requested"""
        self.headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer "+self.token
        }
    def re_init(self,config_file=""):
        """ reinitialize api object with specific config file passed in"""
        cfg_file = self.config_file if config_file == "" else config_file
        self.__init__(cfg_file)
    def delete(self,endpoint,id):
        endpoint=endpoint + "_" + id
        method="delete"
        self.query(method,endpoint)
    def query(self,method_NaMe,endpoint,payload=None): #, *vartuple):
        """try to call the specific API passing all of parameters needed"""
        #for var in vartuple:
        #    print (var)
        print(method_NaMe,endpoint,payload)
        # mi assicuro che il case sia corretto: minuscolo
        method_name= method_NaMe.lower()
        #    print(method_name)
        # "mi prendo il metodo come funzione" della classe importata requests (non c'entra flask)
        method = getattr(requests,method_name, lambda: 'invalide choise')
        print(method)
        # costruisco l'url da contattare nella sua interezza
        url=self.get_url() + endpoint
        print(url)
        print('intestazioni',self.headers)
        try:
            # provo a chiamare la API
            response = method(url,json=payload,headers=self.headers)  
        except Exception as error:
            print(error)
        except AttributeError as error:
            print('ecco errore',error)
        # se ci riesco mostro la risposta (come id oggetto, TODO migliorare output)    
        #print(response.request.method)        
        print(response)
        return response
    def login(self):
        try:
            print("provo il login")
            """ restituisce una stringa contenente il token di autorizzazione\n
            impostandolo anche nelle proprietà della classe"""  
            print("cfg")  
            print(self.cfg)  
            print("path")  
            print(self.login_path)
            print("user")  
            print(self.cfg.get("login_user"))
            #print("token")  
            #print((self.cfg.get("login_user")).json())
            #     --------------------------------------------------------------
            #  questa  è la risposta busando alla login con l'utente specificato
            #                                                                   ----------------
            #                             sintassi per estrarre il campo con chiave "token"
            token=requests.post(self.login_path,json=self.cfg.get("login_user")).json()["token"]
            print(token)
        except Exception as error:
            print("ecco l'errore")
            print(error)
        except requests.exceptions.ConnectionError:
            print("eccolo il bastardo")

        except:
            print("eseguo per errrori sconosciuti")
        else:
            print("eseguo SOLO SE nessun problema")
            self.token = token
            self.set_query_header()
            return self.token
        finally:
            print("eseguo SEMPRE")
            pass


""" 
d.apparent_encoding      d.cookies                d.history                d.iter_lines(            d.ok                     d.request
d.close(                 d.elapsed                d.is_permanent_redirect  d.json(                  d.raise_for_status(      d.status_code
d.connection             d.encoding               d.is_redirect            d.links                  d.raw                    d.text
d.content                d.headers                d.iter_content(          d.next                   d.reason                 d.url
>>> d.request
d.request
>>> d.request.
d.request.body                     d.request.method                   d.request.prepare_content_length(  d.request.prepare_url(
d.request.copy(                    d.request.path_url                 d.request.prepare_cookies(         d.request.register_hook(
d.request.deregister_hook(         d.request.prepare(                 d.request.prepare_headers(         d.request.url
d.request.headers                  d.request.prepare_auth(            d.request.prepare_hooks(           
d.request.hooks                    d.request.prepare_body(            d.request.prepare_method(          
 """