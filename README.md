# NoSQL
Date de rendu : 18 janvier
**Commenter le code réalisé !**

## 1. Redis
### Objectifs:
Simuler un **call center** --> simuler le stockage des données à instant donné.

### Structures:
 - Appels
 - Opérateurs
 
### Exemples:
 - Quels sont les appels (suivant l'état) à un instant donné ?
 - Quels sont les opérateurs effectuant un appel à un instant donné ?
 
 
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
