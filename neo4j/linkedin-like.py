#!/usr/bin/python3.7

# Création user
#CREATE USER tpuser SET PASSWORD "tpuser" CHANGE NOT REQUIRED;
#MATCH(n) RETURN(n)
#pip3 install neo4j

from neo4j import GraphDatabase

# Paramètres de connexion
uri = 'neo4j://localhost:7687'
username = "tpuser"
password = "tpuser"

# Création de la connexion à la base neo4j
driver = GraphDatabase.driver(uri, auth=(username, password), max_connection_lifetime=10)

# Neo4j labels
company_label = "COMPANY"


def main():
	# On crée la session neo4j
	with driver.session() as graphDB_Session:
		create_company(graphDB_Session, "Peugeot", "Automobile", "Constructeur automobile", 100000)
		create_company(graphDB_Session, "Orange", "Operateur", "Société de communication", 50000)

		comp = searchCompanyByName(graphDB_Session, "Peugeot")
		displayCompanyObject(comp)


# Création des entreprises dans la base neo4j
def create_company(graphDB_Session, name, business_line, description, size):
	cql_create = 'MERGE (comp:' + company_label + ' {name: "' + name + '", businessLine: "' + business_line + '", description: "' + description + '", size: ' + str(size) + '})'
	comp = graphDB_Session.run(cql_create)
	print("Company " + name + " created" )


# Permet d'afficher un noeud company
def displayCompanyObject(companies):
	count=1
	for comp in companies:
		print("Entreprise " + str(count)+ " : ")
		print("\tNom: " + comp['name'])
		print("\tSecteur d'activité: " + comp['businessLine'])
		print("\tDescription: " + comp['description'])
		print("\tTaille: " + str(comp['size']))
		print("")

# Permet de récupérer un noeud company en fonction d'un nom donné en paramètre
def searchCompanyByName(graphDB_Session, name):
	cql_search = 'MATCH (comp:' + company_label + ' {name: "' + name + '"}) \
				  RETURN comp.name AS name, comp.businessLine AS businessLine, comp.description AS description, comp.size AS size'
	comp = graphDB_Session.run(cql_search)
	return comp


main()

# fermeture du driver
driver.close()