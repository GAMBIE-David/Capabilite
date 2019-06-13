''' PROGRAMME	: Application pour la capabilite
	BUT			: Permet de d'analyser les capabilite des PV importés
	PAR			: D.GAMBIE
	LE			: 26/04/2019
	VERSION		:1.0
	COMMENTAIRE	: 
	
	### HISTORIQUE : ############################################################
	#1.0 	: Création.															#
	#																			#
	#############################################################################
	
	Remarque :
	Prévoir l'installation
'''	
import os
from tkinter import * #import pour l'interface graphique
from tkinter.messagebox import * #pour les fenetres de dialog
from tkinter import filedialog # pour l'explorateur
import generation_projet
import shutil
import capabilite
from tkinter import ttk
import miseEnFormePv
import graphique
import pickle #Pour la sauvegarde des objets



def Init_chemin_projet () :
	with open('chemin.conf', 'r') as mon_fichier:
		cheminInitDir = mon_fichier.read()

	return cheminInitDir

def Quitter () : #Fonction pour quitter le programme
	'''
	Fonction pour Quitter l'application
'''
	fenetre.destroy()

def About():
	'''
	Fonction pour le à propos
'''
	showinfo("À propos", "Appli d'analyse de capabilite\nVersion 1.0\nLaudren Electronique - DG - 2019") #Fonction pour le APROPOS
	
def Nouveau_Projet (frmSuivant,frmPrecedent, monGraphique, lblInfoComposant, fenetre):
	'''
		Fonction pour la création d'un nouveau projet
		Demande à l'utilisateur l'endroit de sauvegrade du projet => création des répertoires et du fichier	
			par la generation_projet.Init_folder
		Demande à l'utilisateur la localisation des PV a traiter
		Copie les PV dans le repertoire de travail
		Mouline les PV pour garder ce qui est intéressant (permet de définir un PV d'entrée)
		Calcul les capabilite et enregistre un fichier rapport
'''
	print ("***Nouveau projet***")
	chemin = filedialog.asksaveasfilename(initialdir = Init_chemin_projet(),defaultextension='.cap',filetypes =[("Projet Capabilite","*.cap")], initialfile = "Nommer_projet",title = "Nouveau Projet")
	#Mise en forme du chemin et  récupération du nom de projet
	listChemin = chemin.split("/")
	nomProjet = listChemin[-1]
	listNomProjet = nomProjet.split(".")
	nomProjet = listNomProjet[0]
	del listChemin[-1]
	chemin = ""
	for element in listChemin:
		chemin = chemin + element + "/"

	try :
		generation_projet.Init_folder(chemin,nomProjet)
	except :
		print ("Erreur lors de la création du projet")
		showerror("Erreur","Erreur lors du la création du projet")
		return("erreur création projet")
	#Migration des Pv
	Recuperation_Pv(chemin,nomProjet)
	
	#Traitement Utiliser le scripte miseEnForme
	for log in os.listdir (chemin + '/' + nomProjet + '/Log_in/'):
		print ("le log {} est en cours de traitement".format(log))
		miseEnFormePv.traitement (chemin + '/' + nomProjet + '/Log_in/' + log,cheminSav = chemin + nomProjet +'/' + 'Log_out/')
	
	showinfo("Traitement des PV", "Conversion des PV terminées")
	#Traitement pour la capabilite Utiliser le script capabilite
	print ("***Calcul des capabilites***")
	capabilite.Capabilite(chemin + '/' + nomProjet + '/Log_out/')
	showinfo("Calcul Capabilite","Calcul des capabilites terminé")
	cheminObjet = chemin  + nomProjet + "/Objet/"
	Boutons(frmSuivant,frmPrecedent,monGraphique,lblInfoComposant,cheminObjet)
	lblInfoComposant.config(text = "Cliquer sur suivant pour commencer l'analyse")
	return (chemin)

def Boutons (frmSuivant, frmPrecedent, monGraphique,lblInfoComposant,cheminObjet) :
	'''
	Création des boutons après la génération du projet
'''
	#Création des boutons Suivant et précedent :
	btnSuivant = Button(frmSuivant,text="Suivant",command = lambda : graphique.Suivant(monGraphique,frmGraphique,monGraphique.canvas,lblInfoComposant,cheminObjet,varCpkmin.get(), varCpkmax.get (), varMontrer ) )
	btnSuivant.grid(column = 2, row = 0)

	btnPrecedent = Button(frmPrecedent,text="Precedent",command = lambda : graphique.Precedent(monGraphique,frmGraphique,monGraphique.canvas,lblInfoComposant,cheminObjet,varCpkmin.get(), varCpkmax.get(), varMontrer))
	btnPrecedent.grid(column = 0, row = 0)
	
	#Création des labels pour les cpk
	lblCpkmin = Label (frmSpin,text='Cpk minimum : ')
	lblCpkmin.grid(column = 0, row = 0)
	lblCpkmax = Label (frmSpin, text = 'Cpk maximum : ')
	lblCpkmax.grid (column = 0, row = 2)
	
	#Création des spinBox
	spinCpkmin = Spinbox(frmSpin, textvariable = varCpkmin, from_=0, to = 10, increment=0.1,width = 3)
	spinCpkmin.grid(column = 0, row = 1)
	
	spinCpkmax = Spinbox(frmSpin, textvariable = varCpkmax, from_=0, to = 10, increment=0.1,width = 3)
	spinCpkmax.grid(column = 0, row = 3)
	
	#Création de spin pour montrer le graphique
	spinMontrerGraph = Spinbox(frmShowGraph, textvariable = varMontrer, from_=0, to = 100000000000, increment=1,width = 5)
	spinMontrerGraph.grid(column = 0,row = 0)
	
	#Cration du bouton show graphique
	step = varMontrer.get()
	step = str (step)
	btnShowGraph = Button (frmShowGraph, text = 'Graphique', command = lambda : Montrer_graphique(str(varMontrer.get()),cheminObjet) )
	btnShowGraph.grid(column = 0, row = 1)

def Montrer_graphique (step, cheminObjet) :
	'''
	Fonction pour montrer le graphique en fonction du step
'''

	#Récupération du composant :
	cheminComposant = cheminObjet  + step
	print (cheminComposant)
	#print (step)
	try :
		with open (cheminComposant,'rb') as fichier:
			mon_depickler = pickle.Unpickler(fichier)
			monComposant = capabilite.Composant ()
			monComposant = mon_depickler.load() #Récupéation de l'objet monComposant
	except FileNotFoundError:
		print ("Pas de numéro de step associé")
		showerror("Pas de step", "Pas de pas de test numéro :" + str (varMontrer.get()))
	print (monComposant.repere)
	graphique.Show_graph (monComposant)
	
def Recuperation_Pv (cheminProjet,nomProjet):
	'''
	Fonction pour récupérer les PV sur le réseau
		argument = chemin projet => chemin de sav ou se situe le projet
				 = nomProjet => nom du projet définie par l'utilisateur
'''
	i = 0
	print ("***Recupération des Pv de test dans Log_in***")
	cheminPv = filedialog.askdirectory(initialdir ="Z:\Test\CARTE\TAKAYA")
	cheminLog_in = cheminProjet + nomProjet + "/Log_in/" 
	print ("Répertoire de récupération : {}".format(cheminPv))
	print ("Répertoire de destination : {}".format(cheminLog_in))
	#Copie des fichier
	try : #On essai d'acceder au chemin des PV pointer par l'utilisateur
		for log in os.listdir(cheminPv) :
			if os.path.isfile(cheminPv + "/" + log) :
				listLog = log.split('.')
				#print (listLog)
				if listLog[-1] == "ATD": #Vérification de l'extension avant import
					print ("Copie du log {}".format(log))
					shutil.copy(cheminPv + "/" + log,cheminLog_in) #Copie des log
					i = i+1
	
	except FileNotFoundError:
		print("Erreur dand le nom du chemin")
		showerror("Erreur","Import des fichiers impossibles")
		return ("Erreur import")
	showinfo("Import des PV", str (i) + " PV(s) importé(s)\nDispo dans Log_in")
	return(cheminLog_in)
	
#################################################################################################	

#Création de la fenetre
fenetre = Tk()
#fenetre.geometry("805x400")
fenetre.title("Analyse de Capabilite")

#Instance de graphique
monGraphique = graphique.Graphique(graphique.Generation_figure([0,0],-1,1),fenetre)


	

#Création d'un menu
menu_principal = Menu(fenetre)  ## Barre de menu 
sous_menu = Menu(fenetre)
menu_principal.add_command(label = "Nouveau Projet",command = lambda :  Nouveau_Projet(frmSuivant,frmPrecedent,monGraphique,lblInfoComposant,fenetre))
menu_principal.add_command(label = "A propos",command = About)
menu_principal.add_command (label = "Quitter", command = Quitter)
fenetre.config(menu = menu_principal)

#Création des frames
frmSuivant = Frame(fenetre,borderwidth = 2)
frmSuivant.grid(column = 2, row = 1)
frmSuivant.columnconfigure(2,minsize = 100)

frmPrecedent = Frame(fenetre,borderwidth = 2)
frmPrecedent.grid (column = 0, row = 1)
frmPrecedent.columnconfigure(0,minsize = 100)

frmInfoComposant = Frame(fenetre,borderwidth = 2, relief = GROOVE)
frmInfoComposant.grid(column = 1, row = 0)
#frmInfoComposant.columnconfigure(1,minsize = 800)
frmInfoComposant.rowconfigure(0,minsize = 100)

frmGraphique = Frame(fenetre,borderwidth = 2,relief = GROOVE)
frmGraphique.grid(column = 1, row = 2)
frmGraphique.rowconfigure(1,minsize = 400)

frmSpin = Frame(fenetre,borderwidth = 2,relief = GROOVE)
frmSpin.grid(column = 2, row = 2)

frmShowGraph = Frame (fenetre,borderwidth = 2,relief = GROOVE)
frmShowGraph.grid(column = 0, row = 2)

#frmLogo = Frame (fenetre,borderwidth = 2,relief = GROOVE)
#frmLogo.grid(column = 0, row = 0)

#canLogo = Canvas (fenetre)
logo = PhotoImage (file = 'logo.gif')
Label(image=logo).grid(column = 0, row = 0)



#Variable pour les spin
varCpkmin = DoubleVar ()
varCpkmax = DoubleVar ()
varMontrer = IntVar ()

varCpkmin.set (0)
varCpkmax.set (1.6)
varMontrer.set (1)


#Création du Label
varInfoComposant = StringVar ()#String var pour affichage des infos selon le composants
varInfoComposant = 'Cliquer sur nouveau projet pour lancer une analyse'
lblInfoComposant = Label (frmInfoComposant, text = varInfoComposant,justify = 'left')
lblInfoComposant.grid(column = 1, row = 0)


fenetre.mainloop()

