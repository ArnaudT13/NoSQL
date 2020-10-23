"use strict";
// On charge le module mongodb
const Mongo = require('mongodb');

// On crée l'object client mongo
const MongoClient = Mongo.MongoClient;

// L'uri de connexion à la base mongodb
const uri = 'mongodb://localhost:27017';

// Variables globales : le client mongo et l'objet base de données
var client = new MongoClient(uri, {useNewUrlParser: true, useUnifiedTopology: true});
var db;

// Le nom de la base de données
const dbName = 'football';

// Le nom des collections de la base Mongodb
const teamsCollectionName = 'Equipes';
const playersCollectionName = 'Joueurs';
const matchsCollectionName = 'Matchs';
const playerStatsCollectionName = 'PlayerStats';

// Limite à partir de laquelle la moyenne des joueurs est calculée
const averageCalculationLimit = 3;




async function main(){
 
    try {
        // Connection à la base de données
        await client.connect();
        db = await client.db(dbName);
 
        // Création des collections (dans le cas de la première création)
        await createCollections([teamsCollectionName, playersCollectionName, matchsCollectionName, playerStatsCollectionName]);
        
        // Insertion des joueurs
        await insertPlayer(1, "Mbappé", "Kylian", new Date("1998-12-20"), 1.78, 73, "Attaquant");
        await insertPlayer(2, "Neymar", "JR", new Date("1992-02-05"), 1.75, 68, "Attaquant");
        await insertPlayer(3, "Hamouma", "Romain", new Date("1987-03-29"), 1.78, 74, "Attaquant");
        await insertPlayer(4, "Moulin", "Jessy", new Date("1986-01-13"), 1.85, 80, "Gardien");
        await insertPlayer(5, "Mandanda", "Steve", new Date("1985-03-28"), 1.85, 82, "Gardien");
        await insertPlayer(6, "Sakai", "Hiroki", new Date("1990-04-12"), 1.83, 70, "Défenseur");
        
        // Insertion des équipes
        await insertTeam(1, "PSG", ["Bleu", "Blanc", "Rouge"], "Parc des Princes", [1, 2]);
        await insertTeam(2, "ASSE", ["Vert", "Blanc"], "Geoffroy Guichard", [3, 4]);
        await insertTeam(3, "OM", ["Bleu", "Blanc"], "Vélodrome", [5, 6]);
        
        // Optimiser la lecture par nom de joueur
        await db.collection(playersCollectionName).createIndexes({"lastname": 1});
        
        // Optimiser la lecture par nom d'équipe
        await db.collection(teamsCollectionName).createIndexes({"name": 1});      
        
        // Insertion des matchs
        await insertMatch(1, new Date("2020-10-10"), 1, 2, "Ligue 1", 1, 0, {1: 8, 2: 7}, {3: 5, 4: 6});
        await insertMatch(2, new Date("2020-10-03"), 1, 3, "Ligue 1", 5, 0, {1: 6, 2: 6}, {5: 2, 6: 2});
        await insertMatch(3, new Date("2020-10-17"), 2, 3, "Ligue 1", 2, 0, {3: 5, 4: 6}, {5: 3, 6: 1});
        await insertMatch(4, new Date("2020-10-17"), 3, 2, "Ligue 1", 0, 4, {5: 3, 6: 3}, {3: 6, 4: 8});
        console.log("");
        
      	// Affiche les statistiques d'un match
       	await displayPlayerMarksForAMatch(1);
       	console.log("");
       	await displayPlayerMarksForAMatch(2);
       	console.log("");
       	await displayPlayerMarksForAMatch(3);
       	console.log("");
       	
       	// Affiche les joueurs attaquants de moins de 29 ans
       	await displayPlayersListByPositionAndAge("Attaquant", 29);
       	console.log("");
       	
       	// Mise à jour de la collection stats des joueurs (moyennes)
       	await updatePlayersStats();
       	console.log("");

       	// Affiche les joueurs ainsi que leurs moyennes
       	await displayPlayerStatsCollection();

       	
 
    } catch (e) {
        console.error(e);
    } finally {
        await client.close();
    }
}


// Permet de créer les collections de données dans la base mongodb
async function createCollections(collections){
    // Pour toutes les collections
    collections.forEach(collection => {
        db.createCollection(collection);
        console.log("Collection ", collection, " created !");
        }); // On crée la collection
}


// Permet d'insérer un joueur dans la base mongodb
async function insertPlayer(id, lastname, firstname, birthDate, height, weight, position){ 
	let result = await db.collection(playersCollectionName).findOne({"_id": id});
	// Si le joueur existe déjà
	if (result){
		console.log("Player with id=", id, " already exists !");
	}
	else{
		let doc = {"_id": id, 
			   	   "lastname": lastname,
			   	   "firstname": firstname,
			   	   "birthDate": birthDate,
		       	   "height": height,
			   	   "weight": weight, 
			       "position": position
			      };
		// On insert les informations du joueur
		await db.collection(playersCollectionName).insertOne(doc);
		console.log("Player ", firstname, " ", lastname, " inserted !");
	}
}


// Permet d'insérer une équipe dans la base mongodb
async function insertTeam(id, name, colors, stadium, players){
	let result = await db.collection(teamsCollectionName).findOne({"_id": id});
	// Si l'équipe existe déjà
	if (result){
		console.log("Team with id=", id, " already exists !");
	}
	else{
		let doc = {"_id": id, 
			   	   "name": name,
			   	   "colors": colors,
			   	   "stadium": stadium,
		       	   "players": players
			  	  };
		// On insert les informations de l'équipe
		await db.collection(teamsCollectionName).insertOne(doc);
		console.log("Team ", name, " inserted !");
	}
}


// Permet d'insérer un match dans la base mongodb
async function insertMatch(id, date, homeTeam, outsideTeam, competitionName, homeScore, outsideScore, homePlayers, outsidePlayers){
	let result = await db.collection(matchsCollectionName).findOne({"_id": id});
	// Si le match existe déjà
	if (result){
		console.log("Match with id=", id, " already exists !");
	}
	else{
		let doc = {"_id": id,
				   "date": date, 
			   	   "homeTeam": homeTeam,
			   	   "outsideTeam": outsideTeam,
			   	   "competitionName": competitionName,
		       	   "homeScore": homeScore,
		       	   "outsideScore": outsideScore,
		       	   "homePlayers": homePlayers,
		       	   "outsidePlayers": outsidePlayers
			  	  };
		// On insert les informations du match
		await db.collection(matchsCollectionName).insertOne(doc);
		console.log("Match ", await getTeamNameFromTeamId(homeTeam), " - ", await getTeamNameFromTeamId(outsideTeam), " inserted !");
	}
}


// Permet d'obtenir le nom d'une équipe suivant son ID
async function getTeamNameFromTeamId(id){
	// On filtre par id et on récupère seulement les noms d'équipes
	let jsonTeam = await db.collection(teamsCollectionName).findOne({"_id": id}, {projection: {_id: 0, name: 1}});
	return jsonTeam.name;
}


// Permet d'obtenir la liste des joueurs en fonction de la position et de l'age
async function displayPlayersListByPositionAndAge(position, age){
	// On calcule la différence entre aujourd'hui et il y "age" ans
	let startDate = new Date(Date.now() - age*31536000000);
	// On filtre par poste et age et on récupère les informations nécessaires du joueur
	let playerMarksDict = await db.collection(playersCollectionName).find({$and: [{"position" : position}, {"birthDate": {$gte: startDate}}]}, {projection: {_id:0, firstname: 1, lastname: 1, position: 1, birthDate: 1}}).toArray(); // On récupère un tableau de dictionnaires de joueurs
	
	// On affiche ces informations
	console.log("Liste des joueurs: ");
	for(let player of playerMarksDict) {
		console.log(player.firstname, player.lastname, Math.floor((Date.now() - player.birthDate)/31536000000), "ans -->", player.position);
	}
}


// Permet d'obtenir le nom prénom d'un joueur suivant son ID
async function getPlayerLastnameAndFirstnameFromPlayerId(id){
	let jsonPlayer = await db.collection(playersCollectionName).findOne({"_id": id}, {projection: {_id: 0, lastname: 1, firstname: 1}});
	return jsonPlayer.firstname.concat(" ", jsonPlayer.lastname);
}


// Permet de retourner les noms des joueurs d'une équipe
async function getTeamPlayers(teamName){
	let playerNameArray = [];
	// On récupère les id des joueurs de l'équipe teamname
    let playersIdArray = await db.collection(teamsCollectionName).findOne({"name" : teamName}, {projection: {_id:0, players:1}});
   	console.log(playersIdArray.players);
	for(let playerId of playersIdArray.players) {
		playerNameArray.push(await getPlayerLastnameAndFirstnameFromPlayerId(playerId));
	}
	return playerNameArray;
}


// Permet d'afficher les notes des joueurs d'un match
async function displayPlayerMarksForAMatch(matchId){
	// On récupère l'ensemble des notes des joueurs (domicile et extérieur)
	let playerMarksDict = await db.collection(matchsCollectionName).findOne({"_id" : matchId}, {projection: {_id:0, homeTeam: 1, outsideTeam:1 , homeScore:1, outsideScore:1 ,homePlayers:1, outsidePlayers:1}});
	// On récupère le nom des équipes
	let homeTeamName = await getTeamNameFromTeamId(playerMarksDict.homeTeam);
	let outsideTeamName = await getTeamNameFromTeamId(playerMarksDict.outsideTeam);
	
	console.log("Match ", homeTeamName, " ", playerMarksDict.homeScore, " - ", playerMarksDict.outsideScore, " ", outsideTeamName);
	
	console.log("- Notes de l'équipe ", homeTeamName, " :");
	// Les scores sont stockés dans un dictionnaire, on itère donc sur l'ensemble des valeurs contenues dans celui-ci
	for (const [key, value] of Object.entries(playerMarksDict.homePlayers)) {
  		console.log("   ", await getPlayerLastnameAndFirstnameFromPlayerId(Number(key)), ": ", value, "/10");
	}
	
	console.log("- Notes de l'équipe ", outsideTeamName, " :");
	for (const [key, value] of Object.entries(playerMarksDict.outsidePlayers)) {
  		console.log("   ", await getPlayerLastnameAndFirstnameFromPlayerId(Number(key)), ": ", value, "/10");
	}
}


// Permet de gérer le stockage des moyennes des joueurs
async function updatePlayersStats(){
	// Stocke les joueurs et leurs notes 
	// Format {"id_joueur1" : [note1, note2], "id_joueur2" : [note1, note2], ...}
	let playersMarksDict = {};

	// On récupère les notes de l'ensemble des matches (équipe à domicile et extérieur)
	let playerMarksArray = await db.collection(matchsCollectionName).find({}, {projection: {_id:0, homePlayers:1, outsidePlayers:1}}).toArray();
	for (let i = 0; i < playerMarksArray.length; i++) {
		await insertPlayerMarks(playersMarksDict, playerMarksArray[i].homePlayers);
		await insertPlayerMarks(playersMarksDict, playerMarksArray[i].outsidePlayers);
	}

	// On calcule la moyenne des notes des matchs pour chaque joueur
	// Changement de format {"id_joueur1" : moyenne, "id_joueur2" : moyenne, ...}
	for (const [key, value] of Object.entries(playersMarksDict)) {
		if (value.length < averageCalculationLimit){
			delete playersMarksDict[key];
		}
		else{
			playersMarksDict[key] = await calculateAverage(value);
		}
	}

	// On stocke les moyennes dans la base mongodb
	for (const [key, value] of Object.entries(playersMarksDict)) {
		// Si le joueur est déjà présent dans la collection
		if (await db.collection(playerStatsCollectionName).findOne({"_id": key})){
			// On met à jour la moyenne
			await db.collection(playerStatsCollectionName).updateOne({"_id": key}, {$set: {average: value}});
		}
		else{
			// Sinon, on l'ajoute à la collection
			await db.collection(playerStatsCollectionName).insertOne({"_id": key, "average": value});
		}
	}
	console.log("Player stats updated");
	
}

// Permet de récupérer les notes contenues dans "playersMarksDictPerMatch" et de les stocker dans le dictionnaire "playersMarksDict" sous forme de tableau pour chaque joueur
async function insertPlayerMarks(playersMarksDict, playersMarksDictPerMatch){
	for (const [key, value] of Object.entries(playersMarksDictPerMatch)) {
		// Si le joueur n'est pas présent dans la collection
  		if (typeof playersMarksDict[key] === 'undefined'){
			playersMarksDict[key] = [value]; // On initialise le tableau de notes du joueur
		}
		else{
			playersMarksDict[key].push(value); // On ajoute la note au tableau de notes
		}
	}
}


// Retourne la moyenne des notes du tableau passé en paramètre
async function calculateAverage(markArray){
	let sum = 0;
	markArray.forEach(mark => {
        sum = sum + mark;
    });
    return sum/markArray.length;
}


// Affiche l'ensemble des joueurs dans la collection PlayerStats ainsi que leurs moyennes
async function displayPlayerStatsCollection(){
	console.log("Moyenne des joueurs: ");
	// On récupère l'ensemble des stats des joueurs (id et moyenne)
	let playersMarksArray = await db.collection(playerStatsCollectionName).find({}, {}).toArray();
	// On affiche la moyenne pour chaque joueur
    for(let player of playersMarksArray) {
		let playerName = await getPlayerLastnameAndFirstnameFromPlayerId(Number(player["_id"]));
        console.log("Le joueur ", playerName, "a la moyenne de ", player["average"], "/ 10");
	}
}


main();
