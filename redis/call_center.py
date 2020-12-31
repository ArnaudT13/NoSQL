#!/usr/bin/python3.7

#sudo apt-get install python-pip
#sudo pip3 install redis

import redis
import datetime
import ast
import re

# Connexion avec la base redis
r = redis.Redis(host='localhost', port=6379, db=1)

# Etat des appels
call_state_list = ['inprogress','finished', 'ignored','unaffected']

# Noms des structures hash
operator_list_name   = "operators"
call_list_name		 = "calls"
call_state_list_name = "callstates"


""" 
Permet d'ajouter un opérateur dans la DB redis. L'ID de l'operateur est généré automatiquement.  

:param lastname: Nom de l'operateur
:param firstname: Prénom de l'operateur
:param birthdate: Date de naissance de l'operateur
:param income_date: Date d'arrivée de l'operateur

:return: returns nothing 
""" 
def add_operator(lastname, firstname, birthdate, income_date):

	# Permets d'obenir le dernier ID des opérateurs et attribue l'id+1 au nouvel opérateur
	id_operator= get_last_id_of_table('operators') + 1

	# Spécifie la hash et l'id de l'opérateur
	key = operator_list_name + ":" + str(id_operator)
	r.hset(key, "lastname", lastname)
	r.hset(key, "firstname", firstname)
	r.hset(key, "birthdate", birthdate)
	r.hset(key, "incomeDate", income_date)


""" 
Permet d'obtenir la liste de tous les opérateurs enregistrés dans la DB. 

:return: une liste de tous les opérateurs 
""" 
def get_all_operators():
	# On recupere toutes les clés des operateurs
	keys_operators = ["operators:"+str(ids) for ids in get_all_id_of_table('operators') ] 

	all_operators = []
	for operator in keys_operators:
		# On recupere les infos d'un opérateur suivant la clé 'operator'
		all_operators.append([call_id.decode("utf-8") for call_id in list( r.hgetall(operator).values() ) ])
	
	return all_operators


""" 
Permet d'obtenir la liste de tous les noms et prénoms des opérateurs enregistrés. La fonctions suivante réutilise la fonciton get_all_operators().

:return: une liste de tous les noms, prénom des opérateurs 
""" 
def get_all_operators_names():
	all_operators = get_all_operators()
	all_operators_names = []
	for operator in all_operators:
		all_operators_names.append(str(operator[0] + " " + operator[1]))
	
	return all_operators_names


""" 
Permet d'obtenir la liste de tous les prénoms des opérateurs enregistrés

:return: une liste de tous les prénom des opérateurs 
""" 
def get_name_of_operator_id(id = 0):
	key = operator_list_name + ":" + id
	keys_operators = [call_id.decode("utf-8") for call_id in list( r.keys(key) ) ]

	all_operators_names = []
	for operator in keys_operators:
		all_operators_names.append(
			#r.hget(operator, "id").decode('utf-8') + " " + 
			r.hget(operator, "firstname").decode('utf-8') + " " +
			r.hget(operator, "lastname").decode('utf-8'))

	print(all_operators_names)
	return all_operators_names


""" 
Permet d'ajouter un appel dans la base redis. L'ID de l'appel est généré automatiquement.

:param call_hour: Heure d'appel
:param origin_phone_number: Numéro de l'appel
:param call_duration: Durée de l'appel
:param operator_id: Id de l'opérateur en charge de l'appel
:param description: Description (string) de l'appel

:return: returns nothing 
""" 
def add_call(call_hour, origin_phone_number, call_duration, operator_id, state_id, description = "Appel SAV"):
	# Get last id in calls
	id_call= get_last_id_of_table('calls') + 1

	key = call_list_name + ":" + str(id_call)
	r.hset(key, "callHour", call_hour)
	r.hset(key, "originPhoneNumber", origin_phone_number)
	r.hset(key, "callDuration", call_duration)
	r.hset(key, "operatorId", operator_id)
	r.hset(key, "description", description)

	set_call_state(call_state_list[state_id], id_call)


""" 
Permet de definir l'état d'un appel à partir de l'ID de l'appel

:param state: état
:param call_id: id de l'appel
""" 
def set_call_state(state, call_id):
	key = call_state_list_name + ":" + state
	
	# Si l'appel existe
	if r.exists(call_list_name + ":" + str(call_id)):
		r.sadd(key, call_id)
	else:
		print("Call doesn't exist. Operation aborted")
	
	
""" 
Permet de changer l'état d"un appel suivant un ID d'appel donné en parametre

:param state: nouvel état 
:param call_id: id de l'appel

:return: returns nothing 
""" 
def change_call_state(state, call_id):
	key = call_state_list_name + ":" + state
		
	# Si l'appel existe
	if r.exists(call_list_name + ":" + str(call_id)):
		# Suppression de l'appel d'un état (si c'est le cas)
		for i_state in call_state_list:
			if state != i_state:
				r.srem(call_state_list_name + ":" + i_state, call_id)
			
		# Ajout de l'appel dans le bon état		
		r.sadd(key, call_id)
	else:
		print("Call doesn't exist. Operation aborted")

		
""" 
Permet d'obtenir la liste des IDs des appels en fonction de l'état en parametre

:param state: état 

:return: liste d'appels
""" 
def get_calls_id_with_state(state):
	key = call_state_list_name + ":" + state
	return [call_id.decode("utf-8") for call_id in list(r.smembers(key))] 


""" 
Permet d'obtenir la liste de tous les appels dans la base

ORDRE QUERIES :
1. KEYS *
2. HGETALL

:return: liste d'appels
""" 
def get_all_calls():
	#all_keys.sort(key=lambda x: x.split(':')[1])
	all_keys = ["calls:"+str(ids) for ids in get_all_id_of_table('calls') ] 

	all_calls = []
	for call in all_keys:
		all_calls.append([call_id.decode("utf-8") for call_id in list( r.hgetall(call).values() ) ])
	
	return all_calls


""" 
Permet d'obtenir les clés de tous les operateurs, i.e. "ID"," Nom", ... 

:return: liste de cles
""" 
def get_operators_keys():
	key = operator_list_name + ":" + "1"

	return [call_id.decode("utf-8") for call_id in list( r.hkeys(key) ) ]


""" 
Permet d'obtenir les clés de tous les appels, i.e. "ID"," Duree", ... 

:return: liste de cles
""" 
def get_calls_keys():
	key = call_list_name + ":" + "1"

	return [call_id.decode("utf-8") for call_id in list( r.hkeys(key) ) ]

""" 
Permet d'obtenir la liste de tous les appels suivant des critères de recherche

:param operator: tous les appels concernant cet opérateur. Par défault, '0' signifie tous les opérateurs
:param state: état de recherche. Par défault, '0' signifie tous les états
:param mapping: correspondance entre l'index d'un élément du combobox au l'ID de l'operateur

:return: liste d'appels
""" 	
def filter(state_id, operator_id_combo, mapping):
	all_calls_with_members = []

	## ETAPE 1 : ETATS DES APPELS
	if(state_id != 0):
		# On recupere les appels des etats à partir de state_id
		all_keys_state = [call_id.decode("utf-8") for call_id in list( r.keys("callstates:" + call_state_list[state_id - 1]) ) ]

		# On récupère les clés pour chaque appel
		all_calls_with_state = []
		for call in all_keys_state:
			all_calls_with_state.append(["calls:" + call_id.decode("utf-8") for call_id in list( r.smembers(call)) ]) 
		
		# Convertion de listes multiples en une seule, i.e. [ [], [ [], [], [] ], ... ] => [ [], [], ... , [] ]
		all_calls_with_state = [item for sublist in all_calls_with_state for item in sublist]

		# Liste filtreé
		for call in all_calls_with_state:
			all_calls_with_members.append([call_id.decode("utf-8") for call_id in list( r.hgetall(call).values() ) ])
	else:
		all_calls_with_members = get_all_calls()


	## ETAPE 2 : OPERATEURS
	# On filtre de nouveau la liste obtenu suivant les opérateurs (avec en plus mapping suivant combobox)
	all_calls_filtered = []
	if(operator_id_combo != 0):
		if operator_id_combo in mapping.keys():
			operator_id = mapping[operator_id_combo]
			for call in all_calls_with_members:
				if(int(call[3]) == operator_id):
					all_calls_filtered.append(call)
	else:
		all_calls_filtered = all_calls_with_members

	return (all_calls_filtered if len(all_calls_filtered)>0 else [[]])


""" 
Permet d'obtenir toutes les clés d'une table

:return: liste d'ids en int orodonnés dans l'ordre coirssant
""" 
def get_all_keys_of_table(table = 'calls'):
	key = table + ":" + "*"
	return [call_id.decode("utf-8") for call_id in list( r.keys(key) ) ]

def get_all_id_of_table(table = 'calls', asc = True):
	all_keys_of_table = get_all_keys_of_table(table)
	
	all_ids_of_table = []
	for k in all_keys_of_table:	
		matches = re.search(r'[^a-zA-Z_](\d+)', k)
		all_ids_of_table.append(int(matches.group(1))) if matches else None

	# Sorting id 
	all_ids_of_table.sort() if asc else all_ids_of_table.sort(reverse=True)

	return all_ids_of_table

def get_last_id_of_table(table = 'calls'):
	return (max(get_all_id_of_table(table)) if len(get_all_id_of_table(table)) != 0 else 0)

# Test 	

TEST = False
if(TEST):
	print("Adding operators")
	add_operator("Bourgin", "Lionnel", "15/03/1978", "10/12/2019")
	add_operator("Etienne", "Léo", "12/03/1993", "20/12/2020")
	add_operator("Rene", "Melville", "02/04/1953", "20/04/2004")

	print("Adding operators")
	add_call("12:00:01", "0410121314", "12m", 1, 0, "Appel SAV")
	add_call("18:30:34", "0685121311", "03:00", 2, 0,"Appel SAV")
	add_call("20:41:56", "0710126515", "10:50", 3, 0,"Appel SAV")
	add_call("09:11:00", "0110621389", "23:11", 1, 0,"Appel SAV")
	add_call("12:40:10", "0212671329", "00:40", 1, 0, "Rdv Client")

	print("Setting calls state")
	set_call_state("finished", 1)
	set_call_state("unaffected", 2)
	set_call_state("ignored", 3)
	set_call_state("inprogress", 4)
