# NoSQL
Date de rendu : 18 janvier
**Commenter le code réalisé !**

## 1. Redis

### 1.1 Objectifs:

Simulation d'un **call center** avec le stockage de données (appels) à instant donné et la gestion des opérateurs.

### 1.2  Explications

#### 1.2.1 Structure

La manipulation des données de la base Redis est implémenté en **Python** . Nous proposons de plus une interface graphique, réalisée sous **Qt5**.

Le projet Redis est composé de deux fichiers :

- `call_center.py` qui représente toute la gestion de la base Redis, de la connection à la création d'appels et d'opérateurs.

- `UI.py` qui compose l'interface graphique. **Ce fichier est du génie logiciel, il n'est pas très interessant de le regarder**

#### 1.2.2 Utilisation

Nous avons 3 onglets dans l'interface graphique : 

- **Gestion des appels** 

	<img src="https://i.ibb.co/hgZv8ZS/appels.jpg" alt="appels" style="zoom:67%;" />

	Cette interface permet :

	- La visualisation de tous les appels

	- La création d'un appel avec la spécification d'une descrition, d'un numéro, d'une heure, d'une durée et la sélection du statut avec l'affectation de l'opérateur. La création d'un appel utilise diverses fonctionnalités Redis décrites dans le script `call_management`.

		Tous les champs doivent être inscrits avant d'ajouter un appel. Cependant, l'interface ne possède pas de sécurité qui vérifie le bon type de donnée.

- **Gestion des opérateurs**

	<img src="https://i.ibb.co/gyvwbKV/operateurs.jpg" alt="appels" style="zoom:67%;" />

	Cette interface permet :

	- La visualisation de tous les opérateurs

	- La création d'un opérateur avec la spécification d'un prenom, d'un nom, d'une date de naissance , d'une date d'arrivée. La création d'un opérateur rend celui-ci disponible sur la page gestion des appels. La création utilise diverses fonctionnalités Redis décrites dans le script `call_management`.

		Tous les champs doivent être inscrits avant d'ajouter un opérateur. Cependant, l'interface ne possède pas de sécurité qui vérifie le bon type de donnée.

- **Filtrage des opérateurs**

	<img src="https://i.ibb.co/kH87Q21/filtre.jpg" alt="appels" style="zoom:67%;" />

	Cette interface permet :

	- La visualisation de tous les appels et le filtrage de ceux-ci. Il est possible de rechercher un appel suivant son était (fini, en cours, …) et suivant l'opérateur en charge.
 
 
## 2. Mongodb
### 2.1 Objectifs:
Modéliser dans Mongodb des équipes, joueurs et matchs.

### 2.2 Explications:
Le Script de définition et manipulation des données de la base MongoDB est implémenté en **NodeJS**.  
Il réalise les fonctions suivantes :
 - Création d'un client mongo
 - Création de la base `football` si elle n'existe pas
 - Connexion à la base `football`
 - Création des collections : `Equipes`, `Joueurs`, `Matchs` et `JoueursStats` (stockant les joueurs ayant joué au moins X match) si elles n'existent pas
 - Insertion des joueurs (méthode `insertPlayer()`)
 - Insertion des équipes (méthode `insertTeam()` avec une liste d'id de joueur)
 - Optimisation des requêtes de joueurs par nom
 - Optimisation des requêtes d'équipes par nom
 - Insertion des matchs (méthode `insertMatch()` avec un dictionnaire associant une note à un id de joueur)
 - Affichage des statistiques d'un match donné (méthode `displayPlayerMarksForAMatch()`)
 - Affichage des joueurs attaquants de moins de 29 ans (méthode `displayPlayersListByPositionAndAge()`)
 - Mise à jour des statistiques de la collection `JoueursStats` à la suite des modifications des collections
 - Affichage des joueurs ayant joué au moins X match et leurs moyennes 

### 2.3 Lancement:
 - Installation et configuration de mongodb
 - Installation des dépendances mongodb pour NodeJS : `npm install mongodb`
 - Aller dans le dossier *mongodb* et lancer le script NodeJS : `node project.js`
 
 
## 3. Neo4j
### 3.1 Objectifs:
Modéliser dans Neo4j un "LinkedIn-like" constitué d'entreprises et d'utilisateurs.

### 3.2 Explications:
Le Script de définition et manipulation des données de la base Neo4j est implémenté en **Python** et utilise la bibliothèque `neo4j`.  
Les fonctions suivantes y sont décrites:
 - Création d'un driver neo4j pour la connexion à la base (La version community offre la possibilité de travailler avec une seule base : `neo4j`. La connexion se fait donc à cette base)
 - Création du label entreprise et insertion des données correspondantes
 - Création d'un index sur le nom du label entreprise
 - Recherche d'une entreprise par nom et affichage
 - Création du label utilisateur et insertion des données correspondantes
 - Création de deux indexes sur le nom et le prénom du label utilisateur
 - Recherche des utilisateurs par nom, prénom ou nom-prénom et affichage
 - Création de la relation de type Utilisateur-Entreprise : "A travaillé pour" avec les propriétés "Du...au..." et "En tant que ..."
 - Création de la relation de type Utilisateur-Utilisateur : "A travaillé avec"
 - Création de la relation de type Utilisateur-Utilisateur : "Connait"
 - Implémentation de la requête "Utilisateurs ayant travaillé en même temps qu’un utilisateur donné dans une entreprise donnée" et affichage des résultats
 - Implémentation de la requête "Utilisateurs connus par les connaissances d’un utilisateur donné" et affichage des résultats

### 3.3 Lancement:
 - Installation et configuration de neo4j
 - Création d'un utilisateur ainsi que son mot de passe dans la base (ici `tpuser` et `tpuser`)
 - Installation du module Python `neo4j` : `pip install neo4j`
 - Aller dans le dossier *neo4j* et lancer le script Python : `linkedin-like.py`
