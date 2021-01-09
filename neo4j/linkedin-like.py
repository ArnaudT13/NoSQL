#!/usr/bin/python3.7

# Création user
#CREATE USER tpuser SET PASSWORD "tpuser" CHANGE NOT REQUIRED;
#MATCH(n) RETURN(n)
#pip3 install neo4j

from neo4j import GraphDatabase
from datetime import date

# Paramètres de connexion
uri = 'neo4j://localhost:7687'
username = "tpuser"
password = "tpuser"

# Création de la connexion à la base neo4j
driver = GraphDatabase.driver(uri, auth=(username, password), max_connection_lifetime=10)

# Neo4j labels
company_label = "COMPANY"
user_label = "USER"

# Neo4j relations
work_for_relation = "WORK_FOR"

# Liste de compétences
skills_list = ["Active listening", "Communication", "Computer skills", "Customer service", "Interpersonal skills", "Leadership",
    "Management skills", "Problem-solving", "Time management", "Transferable skills"]


def main():
	# On crée la session neo4j
	with driver.session() as graphDB_Session:
		# On supprime tous les anciens noeuds
		deleteAll(graphDB_Session)

		# On crée les entreprises
		peugeot = create_company(graphDB_Session, "Peugeot", "Automobile", "Constructeur automobile", 100000)
		orange1 = create_company(graphDB_Session, "Orange", "Operateur", "Société de communication", 20000)
		orange2 = create_company(graphDB_Session, "Orange", "Informatique", "Société de conseil et services en informatique", 10000)

		# On cherche une entreprise par nom
		comp = searchCompanyByName(graphDB_Session, "Orange")
		displayCompanyObject(comp)

		# On crée les utilisateurs
		u_etienne_thomas = create_user(graphDB_Session, "Etienne", "Thomas", "55 ans, marié, 3 enfants", [skills_list[5], skills_list[6], skills_list[7]])
		u_baumet_richard = create_user(graphDB_Session, "Baumet", "Richard", "35 ans, marié, 2 enfants", [skills_list[0], skills_list[1], skills_list[2]])
		u_dominique_richard = create_user(graphDB_Session, "Dominique", "Richard", "30 ans", [skills_list[4], skills_list[7], skills_list[8]])

		# On cherches les utilisateurs par nom ou prénom ou nom, prénom
		print("1. Recherche par nom : ")
		user1 = searchUserByLastname(graphDB_Session, "Etienne")
		displayUserObject(user1)
		print("2. Recherche par prénom : ")
		user2 = searchUserByFirstname(graphDB_Session, "Richard")
		displayUserObject(user2)
		print("3. Recherche par nom et prénom : ")
		user3 = searchUserByLastnameAndFirstname(graphDB_Session, "Dominique", "Richard")
		displayUserObject(user3)

		# On crée les relations entre utilisateurs et entreprise
		createUserCompanyWorkForRelation(graphDB_Session, u_etienne_thomas, peugeot, [date(2000, 10, 15), date(2014, 7, 9)], "Manager")
		createUserCompanyWorkForRelation(graphDB_Session, u_etienne_thomas, orange2, [date(2014, 9, 29), date.today()], "Manager senior")
		createUserCompanyWorkForRelation(graphDB_Session, u_baumet_richard, orange2, [date(2010, 10, 2), date(2020, 12, 2)], "Développeur")
		createUserCompanyWorkForRelation(graphDB_Session, u_dominique_richard, orange1, [date(2019, 1, 2), date.today()], "Ingénieur RF")



####################### Common ########################

# Supprimer tous les noeuds de la base neo4j
def deleteAll(graphDB_Session):
	cql_search = 'MATCH (n) \
				  DETACH DELETE n'
	graphDB_Session.run(cql_search)

#######################################################





####################### Company #######################

 # Création d'une entreprise dans la base neo4j
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


# Permet d'afficher une ou plusieurs entreprises
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

# Création d'un utilisateur dans la base neo4j
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

# Creation de la relation "A travaillé pour" entre une entreprise et un utilisateur
def createUserCompanyWorkForRelation(graphDB_Session, user_node, company_node, from_to_dates, job):
	# On récupère les id des nodes entreprise et utilisateur
	user_node_id = user_node[0][0].id
	company_node_id = company_node[0][0].id

	# On crée la requête
	cql_create_rel = 'MATCH (comp:COMPANY) WHERE id(comp)=$company_node_id \
					  MATCH (u:USER) WHERE id(u)=$user_node_id \
					  CREATE (u)-[r:' + work_for_relation + ' {fromTo: $from_to_dates, job: $job}]->(comp) \
					  RETURN r'

	# On exécute la requête
	graphDB_Session.run(cql_create_rel, user_node_id=user_node_id, company_node_id=company_node_id, from_to_dates=from_to_dates, job=job)

#######################################################

main()

# Fermeture du driver
driver.close()