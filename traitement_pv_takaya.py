#Script pour le traitement et la mise en forme des PV takaya
import os
import miseEnFormePv

									

chemin = ("//seratou/electronique/test/carte/takaya")
print ("Test")

#Création de list 
for client in os.listdir(chemin) :
	#print (client)
	if os.path.isdir (chemin + "/" + client) : #Vérification si c'est bien un dossier
		for carte in os.listdir(chemin + "/" + client) :
			#print (carte)
			if os.path.isdir (chemin + "/" + client + "/" + carte): #Vérification si dossier
					for dossierPv in os.listdir(chemin + "/" + client + "/" + carte):
						if dossierPv =="PV" :
							#print (dossierPv)
							if os.path.isdir (chemin + "/" + client + "/" + carte + "/" + dossierPv): #Vérification si dossier
								for dossierOF in os.listdir(chemin + "/" + client + "/" + carte + "/" + dossierPv):
									#print (dossierOF)
									if os.path.isdir (chemin + "/" + client + "/" + carte + "/" + dossierPv +"/" + dossierOF): #Vérification si dossier
										for element in os.listdir (chemin + "/" + client + "/" + carte + "/" + dossierPv +"/" + dossierOF) :
											if os.path.isfile (chemin + "/" + client + "/" + carte + "/" + dossierPv +"/" + dossierOF + "/" + element) :
												try :
													listElement = element.split ('.')
													#print (listElement[0])
													if listElement[1] == 'ATD' :
														print ("Log Trouvé")
														listOF = dossierOF.split("_")
														OF = listOF[0]
														try :
															listCarte = carte.split("_")
															refCarte = listCarte[1]
														except :
															refCarte = carte
														print ("Ref carte : {} ; OF : {}; Client {}".format(refCarte,OF, client))
														cheminLog = chemin + "/" + client + "/" + carte + "/" + dossierPv +"/" + dossierOF + "/" + element
														print ('cheminLog envoyé : {}'.format(cheminLog))
														miseEnFormePv.traitement(cheminLog,OF,refCarte,client = client)
												except :
													print ("Pas d'eclatement possible")
											
		