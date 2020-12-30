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
 - Aller dans le dossier mongodb et lancer le script NodeJS : `node project.js`
