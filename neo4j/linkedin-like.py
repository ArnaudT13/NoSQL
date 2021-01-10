#!/usr/bin/python3.7

# Création user
# CREATE USER tpuser SET PASSWORD "tpuser" CHANGE NOT REQUIRED;
# MATCH(n) RETURN(n)
# pip3 install neo4j

from neo4j import GraphDatabase
from datetime import date

# Paramètres de connexion
uri = 'neo4j://localhost:7687'
username = "tpuser"
password = "tpuser"

# Neo4j labels
company_label = "COMPANY"
user_label = "USER"

# Neo4j relations
work_for_relation = "HAS_WORKED_FOR"
work_with_relation = "HAS_WORKED_WITH"
knows_relation = "KNOWS"

# Liste de compétences
skills_list = ["Active listening", "Communication", "Computer skills", "Customer service", "Interpersonal skills", "Leadership",
    "Management skills", "Problem-solving", "Time management", "Transferable skills"]


def main():

	# Driver de la base neo4j
	driver = None

	# Création de la connexion à la base neo4j
	try:
		driver = GraphDatabase.driver(uri, auth=(username, password), max_connection_lifetime=10)
	except:
		print("Echec de connexion à la base neo4j")
		return

	# On crée la session neo4j
	with driver.session() as graphDB_Session:
		# On supprime tous les anciens noeuds
		deleteAll(graphDB_Session)

		# On crée les entreprises
		peugeot = create_company(graphDB_Session, "Peugeot", "Automobile", "Constructeur automobile", 100000)
		orange1 = create_company(graphDB_Session, "Orange", "Operateur", "Société de communication", 20000)
		orange2 = create_company(graphDB_Session, "Orange", "Informatique", "Société de conseil et services en informatique", 10000)
		sopra_steria = create_company(graphDB_Session, "Sopra Steria", "Informatique", "Société de conseil et services en informatique", 5000)

		# On crée un index sur le nom de l'entreprise
		createIndex(graphDB_Session, company_label, 'name')
		print("")

		# On cherche une entreprise par nom
		print("--> Recherche des entreprises nommée Orange")
		comp = searchCompanyByName(graphDB_Session, "Orange")
		displayCompanyObject(comp)

		# On crée les utilisateurs
		u_etienne_thomas = create_user(graphDB_Session, "Etienne", "Thomas", "Manager, 55 ans, marié, 3 enfants", [skills_list[5], skills_list[6], skills_list[7]])
		u_baumet_richard = create_user(graphDB_Session, "Baumet", "Richard", "Scrum master, 35 ans, marié, 2 enfants", [skills_list[0], skills_list[1], skills_list[2]])
		u_dominique_richard = create_user(graphDB_Session, "Dominique", "Richard", "Ingénieur RF, 30 ans", [skills_list[4], skills_list[7], skills_list[8]])
		u_marie_estelle = create_user(graphDB_Session, "Marie", "Estelle", "Ingénieur systèmes, 40 ans", [skills_list[0], skills_list[1], skills_list[2], skills_list[5], skills_list[6], skills_list[7]])
		u_fayet_cedric = create_user(graphDB_Session, "Fayet", "Cédric", "Développeur, 23 ans", [skills_list[0], skills_list[2], skills_list[7]])

		# On crée un index sur le nom ou prénom d'un utilisateur 
		createIndex(graphDB_Session, user_label, 'lastname')
		createIndex(graphDB_Session, user_label, 'firstname')
		print("")

		# On cherche les utilisateurs par nom ou prénom ou nom, prénom
		print("--> Recherche des utilisateurs")
		print("1. Recherche par nom 'Etienne': ")
		user1 = searchUserByLastname(graphDB_Session, "Etienne")
		displayUserObject(user1)
		print("2. Recherche par prénom 'Richard': ")
		user2 = searchUserByFirstname(graphDB_Session, "Richard")
		displayUserObject(user2)
		print("3. Recherche par nom 'Dominique' et prénom 'Richard': ")
		user3 = searchUserByLastnameAndFirstname(graphDB_Session, "Dominique", "Richard")
		displayUserObject(user3)

		# On crée les relations entre utilisateurs et entreprises
		createUserCompanyWorkForRelation(graphDB_Session, u_etienne_thomas, peugeot, [date(2000, 10, 15), date(2014, 7, 9)], "Salarié")
		createUserCompanyWorkForRelation(graphDB_Session, u_etienne_thomas, orange2, [date(2014, 9, 29), date.today()], "Salarié")
		createUserCompanyWorkForRelation(graphDB_Session, u_baumet_richard, orange2, [date(2010, 10, 2), date(2020, 12, 2)], "Salarié")
		createUserCompanyWorkForRelation(graphDB_Session, u_baumet_richard, sopra_steria, [date(2010, 10, 25), date.today()], "Salarié")
		createUserCompanyWorkForRelation(graphDB_Session, u_dominique_richard, orange1, [date(2019, 1, 2), date.today()], "Salarié")
		createUserCompanyWorkForRelation(graphDB_Session, u_marie_estelle, orange2, [date(2000, 1, 2), date(2014, 1, 2)], "Salarié")
		createUserCompanyWorkForRelation(graphDB_Session, u_marie_estelle, sopra_steria, [date(2014, 1, 2), date.today()], "Salarié")
		createUserCompanyWorkForRelation(graphDB_Session, u_fayet_cedric, orange2, [date(2020, 9, 20), date.today()], "Salarié")

		# On crée les relation entre utilisateurs
		# Work with
		createUserUserWorkWithRelation(graphDB_Session, u_etienne_thomas, u_baumet_richard)
		createUserUserWorkWithRelation(graphDB_Session, u_baumet_richard, u_etienne_thomas)
		createUserUserWorkWithRelation(graphDB_Session, u_fayet_cedric, u_etienne_thomas)
		createUserUserWorkWithRelation(graphDB_Session, u_etienne_thomas, u_fayet_cedric)
		createUserUserWorkWithRelation(graphDB_Session, u_baumet_richard, u_marie_estelle)
		createUserUserWorkWithRelation(graphDB_Session, u_marie_estelle, u_baumet_richard)

		# Knows
		createUserUserKnowsRelation(graphDB_Session, u_etienne_thomas, u_baumet_richard)
		createUserUserKnowsRelation(graphDB_Session, u_baumet_richard, u_etienne_thomas)
		createUserUserKnowsRelation(graphDB_Session, u_fayet_cedric, u_etienne_thomas)
		createUserUserKnowsRelation(graphDB_Session, u_etienne_thomas, u_fayet_cedric)
		createUserUserKnowsRelation(graphDB_Session, u_baumet_richard, u_marie_estelle)
		createUserUserKnowsRelation(graphDB_Session, u_marie_estelle, u_baumet_richard)
		createUserUserKnowsRelation(graphDB_Session, u_marie_estelle, u_fayet_cedric)
		createUserUserKnowsRelation(graphDB_Session, u_fayet_cedric, u_marie_estelle)
		createUserUserKnowsRelation(graphDB_Session, u_etienne_thomas, u_dominique_richard)
		createUserUserKnowsRelation(graphDB_Session, u_dominique_richard, u_etienne_thomas)

		# Requêtes complexes
		print("--> Requêtes complexes")
		print("- Utilisateur(s) ayant travaillé en même temps que Etienne Thomas à Orange: ")
		user_match = getUsersWorkWithSpecificUserInSpecificCompany(graphDB_Session, u_etienne_thomas, orange2)
		displayUserObject(user_match)

		print("- Utilisateur(s) connus par les connaissances de Baumet Richard: ")
		user_match = getUsersKnownByKnownUsers(graphDB_Session, u_baumet_richard)
		displayUserObject(user_match)

		print("- Utilisateur(s) connus par les connaissances de Dominique Richard: ")
		user_match = getUsersKnownByKnownUsers(graphDB_Session, u_dominique_richard)
		displayUserObject(user_match)


	# Fermeture du driver
	driver.close()



####################### Commun ########################

# Supprimer tous les noeuds de la base neo4j
def deleteAll(graphDB_Session):
	cql_search = 'MATCH (n) \
				  DETACH DELETE n'
	graphDB_Session.run(cql_search)


# On crée un index dans la base neo4j sur la propriété d'un label, tous deux passés en paramètres 
def createIndex(graphDB_Session, label, property):
	cql_create_idx = 'CREATE INDEX ON :' + label + '(' + property + ')'
	try:
		graphDB_Session.run(cql_create_idx)
		print("Création de l'index: label --> " + label + " property --> " + property)
	except:
		print("L'index existe déjà : aucune modification")
	
#######################################################




####################### Company #######################

 # Création d'une entreprise dans la base neo4j (propriétés passées en paramètres)
def create_company(graphDB_Session, name, business_line, description, size):
	cql_create = 'CREATE (comp:' + company_label + ' {name: $name, businessLine: $business_line, description: $description, size: $size}) \
				  RETURN comp'
	comp = graphDB_Session.run(cql_create, name=name, business_line=business_line, description=description, size=size)
	print("Company " + name + " created")
	return comp.values()


# Permet de récupérer un noeud company en fonction d'un nom donné en paramètre
def searchCompanyByName(graphDB_Session, name):
	cql_search = 'MATCH (comp:' + company_label + ' {name: $name}) \
				  RETURN comp'
	comp = graphDB_Session.run(cql_search, name=name)
	return comp.values()


# Permet d'afficher un ou plusieurs noeuds company
def displayCompanyObject(companies):
	count=1
	for comp in companies:
		print("Entreprise " + str(count)+ " : ")
		print("\tNom: " +  comp[0]['name'])
		print("\tSecteur d'activité: " + comp[0]['businessLine'])
		print("\tDescription: " + comp[0]['description'])
		print("\tTaille: " + str(comp[0]['size']))
		print("")
		count+=1

#######################################################




######################## User #########################

# Création d'un utilisateur dans la base neo4j (propriétés passées en paramètres)
def create_user(graphDB_Session, lastname, firstname, description, skills):
	cql_create = 'CREATE (u:' + user_label + ' {lastname: $lastname, firstname: $firstname, description: $description, skills: $skills}) \
				  RETURN u'
	u = graphDB_Session.run(cql_create, lastname=lastname, firstname=firstname, description=description, skills=skills)
	print("User " + firstname + " " + lastname + " created" )
	return u.values()


# Permet de récupérer un noeud user en fonction du nom donné en paramètre
def searchUserByLastname(graphDB_Session, lastname):
	cql_search = 'MATCH (u:' + user_label + ' {lastname: $lastname}) \
				  RETURN u'
	u = graphDB_Session.run(cql_search, lastname=lastname)
	return u.values()


# Permet de récupérer un noeud user en fonction du prénom donné en paramètre
def searchUserByFirstname(graphDB_Session, firstname):
	cql_search = 'MATCH (u:' + user_label + ' {firstname: $firstname}) \
				  RETURN u'
	u = graphDB_Session.run(cql_search, firstname=firstname)
	return u.values()


# Permet de récupérer un noeud user en fonction du nom et prénom donné en paramètre
def searchUserByLastnameAndFirstname(graphDB_Session, lastname, firstname):
	cql_search = 'MATCH (u:' + user_label + ' {lastname: $lastname, firstname: $firstname}) \
				  RETURN u'
	u = graphDB_Session.run(cql_search, lastname=lastname, firstname=firstname)
	return u.values()


# Permet d'afficher un ou plusieurs noeuds user
def displayUserObject(users):
	count=1
	for user in users:
		print("Utilisateur " + str(count)+ " : ")
		print("\tNom: " + user[0]['lastname'])
		print("\tPrénom: " + user[0]['firstname'])
		print("\tDescription: " + user[0]['description'])
		print("\tListe de compétences: " + str(user[0]['skills']))
		print("")
		count+=1

#######################################################




############### Relation User Company #################

# Creation de la relation "A travaillé pour" entre un noeud company et un noeud user (noeuds et propriétés passés en paramètres)
def createUserCompanyWorkForRelation(graphDB_Session, user_node, company_node, from_to_dates, job):
	# On récupère les id des nodes entreprise et utilisateur
	user_node_id = user_node[0][0].id
	company_node_id = company_node[0][0].id

	# On crée la requête
	cql_create_rel = 'MATCH (comp:' + company_label + ') WHERE id(comp)=$company_node_id \
					  MATCH (u:' + user_label + ') WHERE id(u)=$user_node_id \
					  CREATE (u)-[r:' + work_for_relation + ' {fromTo: $from_to_dates, job: $job}]->(comp) \
					  RETURN r'

	# On exécute la requête
	graphDB_Session.run(cql_create_rel, user_node_id=user_node_id, company_node_id=company_node_id, from_to_dates=from_to_dates, job=job)

#######################################################




################# Relation User User ##################

# Fonction générale permettant de créer une relation entre deux utilisateurs (noeuds et type de relation transmis en paramètres)
def createUserUserRelation(graphDB_Session, user_node1, user_node2, relation):
	# On récupère les id des nodes utilisateurs
	user_node_id1 = user_node1[0][0].id
	user_node_id2 = user_node2[0][0].id

	# On crée la requête
	cql_create_rel = 'MATCH (u1:' + user_label + ') WHERE id(u1)=$user_node_id1 \
					  MATCH (u2:' + user_label + ') WHERE id(u2)=$user_node_id2 \
					  CREATE (u1)-[r:' + relation + ']->(u2)'

	# On exécute la requête
	graphDB_Session.run(cql_create_rel, user_node_id1=user_node_id1, user_node_id2=user_node_id2)


# Creation de la relation "A travaillé avec" entre deux utilisateurs (noeuds transmis en paramètres)
def createUserUserWorkWithRelation(graphDB_Session, user_node1, user_node2):
	createUserUserRelation(graphDB_Session, user_node1, user_node2, work_with_relation)


# Creation de la relation "Connait" entre deux utilisateurs (noeuds transmis en paramètres)
def createUserUserKnowsRelation(graphDB_Session, user_node1, user_node2):
	createUserUserRelation(graphDB_Session, user_node1, user_node2, knows_relation)

#######################################################




################# Requêtes complexes ##################

# Permet d'obtenir les utilisateurs ayant travaillé en même temps qu'un utilisateur dans une entreprise (noeuds user et company passés en paramètres)
def getUsersWorkWithSpecificUserInSpecificCompany(graphDB_Session, user_node, company_node):
	# On récupère les id des nodes entreprise et utilisateur
	user_node_id = user_node[0][0].id
	company_node_id = company_node[0][0].id

	# On crée la requête
	cql_search = 'MATCH(u1:' + user_label + ')-[r1:' + work_for_relation + ']->(comp:' + company_label + ') \
				  MATCH(un:' + user_label + ')-[rn:' + work_for_relation + ']->(comp:' + company_label + ') \
				  WHERE id(comp) = $company_node_id  AND id(u1) = $user_node_id AND $user_node_id <> id(un) AND NOT(r1.fromTo[0] > rn.fromTo[1]) AND NOT(rn.fromTo[0] > r1.fromTo[1]) \
				  RETURN un'

	un = graphDB_Session.run(cql_search, user_node_id=user_node_id , company_node_id=company_node_id)

	return un.values()


# Permet d'obtenir les utilisateurs connus par les connaissances d'un utilisateur donné en paramètre
def getUsersKnownByKnownUsers(graphDB_Session, user_node):
	# On récupère l'id du node user
	user_node_id = user_node[0][0].id

	# On crée la requête
	cql_search = 'MATCH(u1:' + user_label + ')-[r1:' + knows_relation + ']->(u2:' + user_label + ') \
				  MATCH(u2)-[r2:' + knows_relation + ']->(u3:' + user_label + ') \
				  WHERE id(u1) = $user_node_id AND id(u3) <> $user_node_id \
				  RETURN DISTINCT u3'

	u3 = graphDB_Session.run(cql_search, user_node_id=user_node_id)

	return u3.values()

#######################################################


main()
