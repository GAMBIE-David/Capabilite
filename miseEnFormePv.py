#Script pour le traitement et la mise en forme des PV takaya
import os
from datetime import datetime

def traitement (fichier, OF = "NC", refCarte = "NC", cheminSav = "C:/Users/dgambie/Documents/15-PROGRAMMATION/PYTHON/traitement_PV_takaya/Log_out/", client = "NC") :
	#Création des variables :
	chLog = "" # création de la varivale str du log
	chData = ""
	chEntete = "" # variable pour stocker les entetes du PV formaté
	chPvFormate = ""#variable pour stocker le PV formaté sous forme de chaine de caractères
	chNomPv = ""#va pour le nom du PV
	listLog=[] #Création de la liste du log 
	dictLog = {} #Dictionnaire du log

	dictNomCol = {} #Dictionnaier pour les noms de colonnes avec les clés = nom de colonne
	listNomCol = [] #Liste pour les noms de colonnes
	dictLigne = {}
	listLogFormate = []
	listEclatee = []

	#Liste des elements à sortier du PV - Dans l'ordre
	listElement = []
	listElement.append("Step_number")
	listElement.append("Parts")
	listElement.append("Value")
	listElement.append("Ref._Value_(Char)")
	listElement.append("Test_Value_1_(Char)")
	listElement.append("Unit")
	listElement.append("Tolerance_(-)%")
	listElement.append("Tolerance_(+)%")
	listElement.append("Judgement")
	listElement.append("Function")
	
	#Dictionnaire des elements a sortir dans le PV
	dictElementPv = {}
	dictElementPv["Step_number"] = 0
	dictElementPv["Parts"] = 1
	dictElementPv["Value"] = 2
	dictElementPv["Ref._Value_(Char)"] = 16
	dictElementPv["Test_Value_1_(Char)"] = 18
	dictElementPv["Tolerance_(-)%"] = 34
	dictElementPv["Tolerance_(+)%"] = 33
	dictElementPv["Judgement"] = 14
	dictElementPv["Function"] = 56
	dictElementPv["Unit"] = 17
	

	#Ouverture, traitement et fermeture :
	try :
		log = open(fichier, "r") #Ouverture du fichier	
		chLog = log.read() #Contenu du log dans la chaine de caractère chLog
		log.close()
	except FileNotFoundError:
		print ("Ouverture du fichier impossible - miseEnForme.traitement")
		return ("errur ouverture fichier module miseEnForme.traitement")

	#Eclatement de la chaine de caractère issue du LOG	
	listLog = chLog.split("@")

	#Attribution des listes dans le dictionnaire :
	dictLog["en-tete"] = listLog[1]
	dictLog["data"] = listLog[2]

	#Eclatement de la partie data 
	listData = dictLog["data"].split('\n')
	del listData[0] #Suppression des element inutiles
	del listData[-1]#idem
	listNomCol = listData[0].split('\t') #Nom des données
	del listData[0]	

	#Mise en forme des données
	i= 0
	for list in listData:
		listLogDictData = [] # liste intermédiaire avant listLogFormate
		listDataParLigne = list.split ('\t') #Eclatement des lignes
		i = i+1
		j = 0
		for data in listDataParLigne: #Parcours de chaque donnée de ligne
			dictData = {} #Création d'un dictionnaire 
			dictData[listNomCol[j]] = data #Récupération des data avec le noms associé
			j = j+1
			listLogDictData.append(dictData)

		listLogFormate.append(listLogDictData)	

	
	
	
	#Création d'un PV formaté
	for element in listElement:#Création de l'entete
		if element != "Test_Value_2_(Char)" :
			chEntete = chEntete + element + "\t"

	chPvFormate = chEntete + "\n"

	#Recherche des elements en fonctione de l'entete avec un try pour les doubles mesures
	for element in listLogFormate :

		try :
			chPvFormate = chPvFormate + "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(element[dictElementPv["Step_number"]]["Step_number"],element[dictElementPv["Parts"]]["Parts"],
							element[dictElementPv["Value"]]["Value"],element[dictElementPv["Ref._Value_(Char)"]]["Ref._Value_(Char)"],
							element[dictElementPv["Test_Value_1_(Char)"]]["Test_Value_1_(Char)"],element[dictElementPv["Unit"]]["Unit"],
							element[dictElementPv["Tolerance_(-)%"]]["Tolerance_(-)%"],element[dictElementPv["Tolerance_(+)%"]]["Tolerance_(+)%"],
							element[dictElementPv["Judgement"]]["Judgement"],element[dictElementPv["Function"]]["Function"])
		except KeyError :
			print ("erreur de clés")

	#Eclatement de la partie du log entete pour récupérer des info utiles		
	listEntete = dictLog["en-tete"].split ('\n')

	#Parcour de la liste de l'entet
	for element in listEntete :
		try :
			listElement = element.split (':')
			if listElement[0] == 'Model':
				chModel = listElement[1]
			if listElement[0] == 'Serial No.':
				chSn = listElement[1]
			if listElement[0] == 'Test time' :
				listTempsTest = listElement[1].split (' ')
				chTempsTest = listTempsTest[0]			
		except :
			print ('Pas de découpage possible')

			
	#print ('Le programme {} carte sn {} est testé en {} secondes pour {} pas de test '.format(chModel,chSn,chTempsTest,listLogFormate[-1][dictElementPv["Step_number"]]["Step_number"]))
	
	#Création des fichiers
	#Enregistrments des elements importants dans un fichier de données unique:
	ficDonnee = open ('donnee','a')
	chDonnee = "\n{};{};{};{};{};{};{}".format(chModel,chSn,chTempsTest,int (listLogFormate[-1][dictElementPv["Step_number"]]["Step_number"]),OF,refCarte,client)
	ficDonnee.write (chDonnee)
	ficDonnee.close()
	
	#Création du PV
	#Mise en forme du nom du PV
	now = datetime.now()
	#print (now.day)
	#print (cheminSav)
	chNomPv = cheminSav + chModel + "_" + chSn + "_" + str (now.day) + "-" + str (now.hour) + "-" + str (now.minute) + ".pv"
	
	PvFormate = open(chNomPv, "a")
	PvFormate.write(chPvFormate)
	PvFormate.close()

	
	
if __name__ == "__main__":	
	traitement("PVADENEO.ATD")

		
		
		
		
		