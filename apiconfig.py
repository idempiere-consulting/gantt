user={
        'username': 'demo@ciao.com',
        'password': 'DEMOAdmin'
    }
options_token = {
        'host': '5.189.165.60',
        'port': '4081',
        'path': '/services/api/auth/login'
        }

options_tasks = {
        'host': '5.189.165.60',
        'port': '4081',
        'path': '/services/api/idempierepara/web/search/getGantt'
         }   


''' nella bash se creo un fike json devo usare le dooppie virgolette e  poi  usare curl -d "@data.json"

il  json  è case sensitive, il nome della chiave è quello che si vede su idempiere
l'id fa eccezione ed è sempre minuscolo ed è sempre id, senza il nome della tabella
'''