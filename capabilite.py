'''
Generer une liste de figure au moment de la sauvegarde des objets 
Sauvegarder cette liste sous forme d'objet appeler listeFigure

Remarque : Attention revoir la façon de calculer le cpk
Attention si ecartType = 0 =>

'''

import os
import re #Pour les expressions régulières
import pickle #Pour la sauvegarde des objets
import graphique
import numpy

chLog = "" # variable pour l'import du log de test formaté
listLog = []
listDictObjet = [] # liste des dictionnaires d'objet
listDictObjetTraite = [] #Liste des dicitonnaires d'objet traité => avec les valeurs moyennes, ecart type et liste
chemin = "C:/Users/dgambie/Documents/15-PROGRAMMATION/PYTHON/traitement_PV_takaya/Log_out"

#Création de l'objet composant
class Composant :
	def __init__ (self):
		self.refValue = 0
		self.value = 0
		self.tolHaute = 0
		self.tolBasse = 0
		self.step = 0
		self.repere = "rep"
		self.unit = "unit"
		self.moyenne = 0
		self.ecartType = 0
		self.cpkInf = 0
		self.cpkSup = 0
		self.cpk = 0
		self.liste = []
		self.fonction = ""

		
def Variance(liste):

   m=Moyenne(liste)
   return Moyenne([(x-m)**2 for x in liste])
	
def Ecartype(liste):

	return Variance(liste)**0.5

def Moyenne (liste):

	somme = 0
	for i in liste:
		somme = somme + i
	if somme == 0:
		return 0
	return somme / len(liste)
	

	
def CpkInf (objComposant):
	'''
	Fonction pour le calcul du cpk par rapport à la limite basse
		Arg : Objet composant
'''
	#Récupération de la tolérance basse
	tolBasse = objComposant.tolBasse
	tolBasse = tolBasse.replace('-',"")
	tolBasse = tolBasse.replace('%',"")
	tolBasse = float (tolBasse)
	tol = tolBasse #pour le debug
	#Récupération de la value
	try :
		value = float(objComposant.value)
	except ValueError:
		print ("Convertion de la value en float impossible...Value à 99999999")
		value = 99999999
		
	#Récupération de la refValue	
	try :
		refValue = float(objComposant.refValue)
	except ValueError:
		print ("Convertion de la Refvalue en float impossible...Value à 99999999")
		refValue = 99999999	
	
	tolBasse = refValue - (refValue * tolBasse / 100)	
	cpk = ((objComposant.moyenne- tolBasse)/ (3*objComposant.ecartType))
	#print ("Repere : {} Tolbass = refValue - (refValue * tolBasse / 100 soit : {} - ({}*{}/100) = {} ".format(objComposant.repere,refValue,refValue,tol,tolBasse))
	#print ("Repere : {} cpk = (moyenne - tolBasse) / 3 * ecartType soit : ({} - {})/3 * {} = {} ".format(objComposant.repere,objComposant.moyenne,tolBasse,objComposant.ecartType,cpk))
	
	
	return cpk

def CpkSup (objComposant):
	'''
	Fonction pour le calcul du cpk par rapport à la limite haute
		Arg : Objet composant
'''
	#Récupération de la tolérance haute
	tolHaute = objComposant.tolHaute
	tolHaute = tolHaute.replace('+',"")
	tolHaute = tolHaute.replace('%',"")
	tolHaute = float (tolHaute)
	
	#Récupération de la value
	try :
		value = float(objComposant.value)
	except ValueError:
		print ("Convertion de la value en float impossible...Value à 99999999")
		value = 99999999
		
	#Récupération de la refValue	
	try :
		refValue = float(objComposant.refValue)
	except ValueError:
		print ("Convertion de la Refvalue en float impossible...Value à 99999999")
		refValue = 99999999	
	
	tolHaute = refValue - (refValue * tolHaute / 100)
	
	
	cpk = ((objComposant.moyenne- tolHaute)/ (3*objComposant.ecartType))
	return cpk
	
def Cpk (cpkInf,cpkSup):
	'''
	Fonction pour déterminer le cpk min
	Arg : Cpk par rapport à la limite basse et haute
'''
	if abs(cpkInf) < abs(cpkSup):
		return abs(cpkInf)
	else :
		return abs(cpkSup)
	
def Mise_en_forme (listDictObjet,fichier):
	'''
	Fonction pour la mise en forme de la liste des objets
'''
	#Ouverture, traitement et fermeture :
	log = open(fichier, "r") #Ouverture du fichier	
	chLog = log.read() #Contenu du log dans la chaine de caractère chLog
	log.close()

	listLog = chLog.split("\n")
	del listLog[0]
	del listLog[-1]

	for element in listLog:
		dictObjet = {} #dictionnaire d'objet avec le repere comme clé
		listElement = element.split("\t")
		cmp = Composant()
		#print (listElement)
		#os.system("Pause")
		cmp.repere = listElement[1]
		
		#Suppression des espaces dans les reperes
		listRepere = []
		listRepere = cmp.repere.split(" ")
		cmp.repere = listRepere[0]
		
		cmp.step = listElement[0]
		cmp.refValue = listElement[3]
		cmp.value = listElement[4]
		cmp.tolHaute = listElement[7]
		cmp.tolBasse = listElement[6]
		cmp.unit = listElement[5]
		cmp.fonction = listElement[9]
		dictObjet[cmp.step] = cmp
		listDictObjet.append(dictObjet)

	return listDictObjet

def Sav_Objet (chemin,objet, type = 'monComposant'):
	'''
	Permet la sauvegarde des objets
'''

	listChemin = chemin.split("/")
	cheminObjet = ""
	
	for element in listChemin:
		if element == 'Log_out':
			element = 'Objet'
			
		cheminObjet = cheminObjet + element + "/"
		
	if type == "monComposant" :
		step = int(objet.step)#Pour avoir des objet 0 ; 1 et non pas 0000 et 0001
		cheminObjet = cheminObjet + str(step)
		
	if type == "listFigure" :
		cheminObjet = cheminObjet + "listFigure"
		
	with open (cheminObjet,'wb') as fichier:
		mon_pickler = pickle.Pickler(fichier)
		mon_pickler.dump(objet)
				
def Moyenne_ecartType (listDictObjet,nbLog):

	nbStepTot = len(listDictObjet) #récupération du nombre de step total
	nbStepParLog = int (nbStepTot/nbLog) # calcul du nombre de step par log

	for step in range (nbStepParLog): #création d'une liste du nombre de step par log pour parcourir chaque step
		listeValue = []# pour effectuer des moyennes sur une liste
		
		for log in range(nbLog): #pour chaque LOG
			index = nbStepParLog*log+step #on récupère l'index qui nous intéresse en focntion du nombre de LOG et du nombre de pas par LOG

			for key,value in listDictObjet[index].items():
				monComposant = Composant()
				monComposant = value #on récupère l'objet
				
				try : #On tente une Conversion
					valeur = float(monComposant.value)
					
				except ValueError:
					print ("Conversion en Float impossible... mise à 99999999 de valeur")
					valeur = 99999999
					
				listeValue.append(valeur)#Ajout à la liste des valeurs pour avoir la moyenne (permettra d'avoir l'ecart type égalemet)
				#print ("Pas de test : {} ; Composant  : {} index : {}".format(monComposant.step, monComposant.repere,index))
		moyenne = Moyenne(listeValue)
		ecartType = numpy.std(listeValue)
		
		#Modification du premiere objet de chaque step dans listDictObjet => index-((nbLog-1)*nbStepParLog) )avec nbLog-1 pour retourner au premier LOG 
		for key,value in listDictObjet[index-((nbLog-1)*nbStepParLog)].items():
			#print (index)
			monComposant = value
			monComposant.moyenne = moyenne
			monComposant.ecartType = ecartType
			monComposant.cpkInf = CpkInf(monComposant)
			monComposant.cpkSup = CpkSup (monComposant)
			monComposant.cpk = Cpk(monComposant.cpkInf,monComposant.cpkSup)
			monComposant.liste = listeValue
			#print ("step : {}\trepere : {}\ttolBasse : {}\ttolHaute : {}\tcpk : {}".format(monComposant.step,monComposant.repere,monComposant.tolBasse,monComposant.tolHaute,monComposant.cpk))
 

def Generation_liste_traite (listDictObjet, nbLog):
	nbStepTot = len(listDictObjet) #récupération du nombre de step total
	nbStepParLog = int (nbStepTot/nbLog) # calcul du nombre de step par log

	for step in range (nbStepParLog): #création d'une liste du nombre de step par log pour parcourir chaque step
		listDictObjetTraite.append(listDictObjet[step])
		
	#return listDictObjetTraite
	#print (len(listDictObjetTraite))
	
def Capabilite(chemin, nomProjet = 'Projet') :
	#Ouverture des PV pour traitement
	for log in os.listdir(chemin) :
		Mise_en_forme(listDictObjet,chemin +"/"+ log)
		
	Moyenne_ecartType(listDictObjet,len(os.listdir(chemin)))	
	Generation_liste_traite(listDictObjet,len(os.listdir(chemin)))
	
	#Préparation du fichier pour création d'un rapport de capabilité
	listChemin = chemin.split("/")
	#print (listChemin)
	cheminRapport = ""
	for element in listChemin:
		if element == 'Log_out':
			element = 'Rapport'
		cheminRapport = cheminRapport + element + "/" #Création du chemin rapport
	rapport = open(cheminRapport + nomProjet + ".rap",'w')
	rapport.write("Step\tRepere\tUnité\tTolBasse\tTolHaute\tCpk\tFonction\n")
	
	listFigure = []#Pour la génération de la liste des figures => a sauver en objet
	for element in listDictObjetTraite :
		for key,value in element.items():
			monComposant = Composant()
			monComposant = value
			
			#Ajouter la generation de la liste des figures
			#graphique.Generation_liste_figure_par_objet(monComposant,listFigure)
						
			Sav_Objet(chemin,monComposant)#Sauvegarde de l'objet
			print ("Sav " + monComposant.repere)
			#print ("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(monComposant.step,monComposant.repere,monComposant.unit,
				#monComposant.tolBasse,monComposant.tolHaute,monComposant.cpk,monComposant.fonction))
			rapport.write(str (monComposant.step) + '\t' + str (monComposant.repere) + "\t" + str (monComposant.unit) + '\t' + str (monComposant.tolBasse) + "\t" + str (monComposant.tolHaute) + '\t' + str (monComposant.cpk) + "\t"+ str (monComposant.fonction) + '\n')
	#Sav_Objet(chemin,listFigure, type = "listFigure")
	rapport.close()
	
		