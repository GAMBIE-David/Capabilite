#Script pour la génération du projet
import os
import datetime

chemin = "C:/Users/dgambie/Documents/15-PROGRAMMATION/PYTHON/traitement_PV_takaya/TestProjet"
nomProjet = "Projet"

def Init_folder (chemin,nomProjet):
	date = datetime.datetime.today()

	
	#Création du répertoire Nom de projet et du fichier cap
	fichier = open(chemin + nomProjet + ".cap","w")
	fichier.write("[chemin:" + chemin + "]")
	fichier.write ("[date de création:" + str(date.day) + '/' + str (date.month) + '/' + str (date.year) + '_' + str (date.hour) + "h" + str(date.minute) + "]")
	fichier.close()
		
	os.makedirs(chemin + nomProjet, exist_ok=True)
	os.makedirs(chemin + nomProjet + "/Log_in", exist_ok=True)
	os.makedirs(chemin + nomProjet + "/Log_out", exist_ok=True)
	os.makedirs(chemin + nomProjet + "/Objet", exist_ok=True)
	os.makedirs(chemin + nomProjet + "/Rapport", exist_ok=True)
	
#Init_folder(chemin,nomProjet)