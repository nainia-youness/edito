import xmlrpc.client
import json


def save_as_json(element, file_name):
    j_data = json.dumps(element)
    with open(file_name, "w") as outfile:
        outfile.write(j_data)


url = 'http://13.37.208.5'
db = 'SLM_PROD_30_07'
username = 'n.youness'
password = 'youness123'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()

uid = common.authenticate(db, username, password, {})
print("uid= "+str(uid))

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

########Liste les ids des destinataires (seulement les clients)########
id_destinataires = models.execute_kw(
    db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])
# print(id_destinataires)

########get un client qui est une entreprise (pas un particulier)########
id_client = models.execute_kw(db, uid, password,
                              'res.partner', 'search', [
                                  [['is_company', '=', True]]],
                              {'limit': 1})
# print(id_client)

[record] = models.execute_kw(
    db, uid, password, 'res.partner', 'read', [id_client])

# print(record)
#save_as_json(record, 'client.json')

########Rechercher et lire les clients########

clients = models.execute_kw(db, uid, password,
                            'res.partner', 'search_read',
                            [[['is_company', '=', True]]],
                            {'fields': ['name', 'country_id', 'comment'], 'limit': 5})

# print(clients)

########Créer un client:########

# id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
#    'name': "Client test cree par API",
# }])

########get tout les colis avec etape nouveau########

id = models.execute_kw(
    db, uid, password, "sochepress.customer.request", "get_list_colis", ["new"])

print(id)

########create destination########

dict_destinator = {"nom_destinataire": "destinateur Test creer par API", "rue": "Rue 2 BV AIT WAKRIM",
                   "rue2": "Poste 24 Hay Addakhla", "ville": "Agadir",
                   "pays": "Maroc",
                   "region": "Tanger-Tetouan", "zip": "23003",
                   "destination": "Tanger", "phone": "0654653489",
                   "mobile": "0654653489",
                   "email": "mohamedelkbir@gmail.com"
                   }

# id = models.execute_kw(db,
#                       uid, password, "sochepress.customer.request",
#                       "create_destinator", [dict_destinator])

# print(id)

########create demand########

# methode 1
colis1 = {
    "ref_externe": "0000001",
    "type_colis": "normal",
    "expediteur": "PLF NORD SLM",
    "destinataire": "A070707",
    "source": "Adresse warakpress",
    "destination": "Kénitra",
    "poids_colis": 213,
    "methode_contre_remboursement": "Espèces",
    "montant_contre_remboursement": 198.23
}
colis2 = {
    "ref_externe": "0000002",
    "type_colis": "normal",
    "expediteur": "PLF NORD SLM",
    "destinataire": "A070706",
    "source": "Adresse warakpress",
    "destination": "Kénitra",
    "poids_colis": 213,
    "methode_contre_remboursement": "Espèces",
    "montant_contre_remboursement": 198.23
}

commande = {
    "customer_id": 28113,
    "type": "normal",
    "colis": [colis1, colis2]
}

# id = models.execute_kw(
#    db, uid, password, 'sochepress.customer.request', 'create_demand', [commande])
# print(id)

# methode 2

id_colis_1 = models.execute_kw(db, uid, password, "sochepress.customer.request.line", "create", [
                               {"name": "colis1", "expeditor_id": 1315, "type_colis_id": 1}])
id_colis_2 = models.execute_kw(db, uid, password, "sochepress.customer.request.line", "create", [
                               {"name": "colis2", "expeditor_id": 1315, "type_colis_id": 1}])

id_demand = models.execute_kw(db, uid, password, "sochepress.customer.request", "create", [
                              {"name": "DEMAND", "customer_id": 1315, "request_line_ids": [id_colis_1, id_colis_2]}])
print(id_demand)

########get colis########

dict_infos = {
    "ref": "MAR",
    "colis_name": 'XFJTYNAG',
    "request_id": 3000,
}

# p = models.execute_kw(db, uid,
#                      password, "sochepress.customer.request", "get_colis", [dict_infos])

# print(p)
