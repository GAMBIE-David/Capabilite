'''
Note = A voir pour changer de méthode de création des graphiques
Peut être le faire en dynamique

Clique sur suivant => ouverture de l'objet 1 
						Génération du graphique par l'objet 1
						Récupération des infos composant grace à l'objet 1

						
Pour le trie :
Lors de l'apuis sur suivant => on vérifie si le cpk est inférieur sinon numgraph + 1


'''
import os
from tkinter import * #import pour l'interface graphique
from tkinter.messagebox import * #pour les fenetres de dialog
from tkinter import filedialog # pour l'explorateur
import numpy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle #Pour la sauvegarde des objets
#from capabilite import * #Pour utiliser la class Composant dans la mise au point du script
import capabilite


chemin = "C:/Users/dgambie/Documents/Projet-capabilite/Potain-carte-gyro/Objet/"
nomProjet = "Test"
listData = [5,4,2,6,9,8,7,1,2,3,8,6,3,4,5,5,6,4,7,5,2]
numGraph = 0
minCpkVisu = 0
maxCpkVisu = 0.5

class Graphique ():
	'''
	Classe Graphique pour la génération des graphique
'''
	def __init__ (self,figure,fenetre):
		self.graph = FigureCanvasTkAgg(figure, master = fenetre)
		self.canvas = self.graph.get_tk_widget()
		self.composant = "Objet"
		self.figure = figure

	def actualiser (self,figure,fenetre):
		self.graph = FigureCanvasTkAgg(figure, master = fenetre)
		self.canvas = self.graph.get_tk_widget()
		
	def afficher (self,canvas) :
		canvas.grid(column = 1, row = 1)
		
	def effacer (self, canvas) :
		canvas.destroy()
		
	def savComposant (self,monComposant):
		self.composant = monComposant
		
##########################Copier coller du module Application #############################################	
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

	

def Generation_figure (listData,tolBasse,tolHaute,titre = "Titre", legendTolBasse = "Tolérance -", legendTolHaute = "Tolérance +", legendData = "Donnée"):
	'''
	Fonction pour la génération des figures
'''
	#Création des lignes pour les tolérances
	listTolBasse = []
	listTolHaute = []
	
	for element in range(len(listData)) :
		listTolBasse.append(tolBasse)

	for element in range(len(listData)):
		listTolHaute.append(tolHaute)

	#Création du graphique
	figure = Figure(figsize = (6,5), dpi = 96)
	ax = figure.add_subplot(111)
	ax.plot(range(len(listData)),listData,label = legendData) #Data
	ax.plot (range (len(listTolBasse)),listTolBasse, label = legendTolBasse)#TolBasse
	ax.plot (range (len(listTolHaute)),listTolHaute,label = legendTolHaute)#TolBasse
	figure.suptitle(titre)
	figure.align_labels()
	ax.legend()
	#ax.text(0.5,0.5,"Test")
	#Print des labels
	#xlabel('x label')
	
	#plt.show()
	return figure

def Conversion_tol (strTol):
	'''
	Fonction pour convertir la tolérance en float => +30.1% = 30.1
'''
	strTol = strTol.replace('-',"")
	strTol = strTol.replace('%',"")
	strTol = float (strTol)
	return strTol

def Show_graph (objComposant) :
	'''
	Fonction pour afficher un graphique
'''
	listData = objComposant.liste
	tolBasse = objComposant.tolBasse
	tolHaute = objComposant.tolHaute
	
	#Transformation des tol en float
	tolBasse = Conversion_tol(tolBasse)
	tolHaute = Conversion_tol(tolHaute)
	
	try :
		refValue = float(objComposant.refValue)
	except ValueError:
		print ("Convertion de la value en float impossible...Value à 99999999")
		refValue = 99999999
		
	tolBasse = refValue - (tolBasse/100*refValue)
	tolHaute = refValue + (tolHaute/100*refValue)
	
	#Création des lignes pour les tolérances
	listTolBasse = []
	listTolHaute = []
	
	for element in range(len(listData)) :
		listTolBasse.append(tolBasse)

	for element in range(len(listData)):
		listTolHaute.append(tolHaute)
		
	#Création du graphique
	'''
	figure = Figure(figsize = (6,5), dpi = 96)
	ax = figure.add_subplot(111)
	ax.plot(range(len(listData)),listData,label = "Data") #Data
	ax.plot (range (len(listTolBasse)),listTolBasse, label = objComposant.tolBasse)#TolBasse
	ax.plot (range (len(listTolHaute)),listTolHaute,label = objComposant.tolHaute)#TolBasse	
	'''
	#x = numpy.arange(0, 10, 0.2)
	#y = numpy.sin(x)
	fig, ax = plt.subplots()
	ax.plot(range(len(listData)),listData)
	ax.plot (range (len(listTolBasse)),listTolBasse, label = objComposant.tolBasse)#TolBasse
	ax.plot (range (len(listTolHaute)),listTolHaute,label = objComposant.tolHaute)#TolBasse
	fig.suptitle("Composant : " + objComposant.repere + " Step : " + objComposant.step + "\nCpk : " + str (objComposant.cpk) )
	#plt.title("Graphique " + objComposant.repere)
	fig.canvas.set_window_title('Graphique ' + objComposant.repere)
	fig.align_labels()
	ax.legend()
	plt.show()

	
def Suivant (objGraphique,fenetre,canvas, label, chemin, minCpkVisu,maxCpkVisu, varMontrer) :
	'''
	Fonction pour actualiser le graphique lors de l'appuis sur suivant
'''
	global numGraph
	#global lblInfoComposant
	
	numGraph = numGraph +1
	#print (numGraph)
	
	#Ouverture du premier objet :
	try :
		with open (chemin + str (numGraph),'rb') as fichier:
			mon_depickler = pickle.Unpickler(fichier)
			monComposant = capabilite.Composant()#Création de l'objet
			monComposant = mon_depickler.load() #Récupéation de l'objet monComposant
		
	#Récupération du cpk et de la fonction
		cpk = monComposant.cpk
		fonction = monComposant.fonction

		
	#Vérification du cpk pour afficher que ceux qui nous intéresse (filtre)
		while cpk > maxCpkVisu or cpk < minCpkVisu or fonction != "**" :
			numGraph = numGraph + 1
			with open (chemin + str (numGraph),'rb') as fichier:
				mon_depickler = pickle.Unpickler(fichier)
				monComposant = capabilite.Composant()#Création de l'objet
				monComposant = mon_depickler.load() #Récupéation de l'objet monComposant	
			cpk = monComposant.cpk
			fonction = monComposant.fonction
			#print (cpk)
		#print ("avant")	
		
	
	except FileNotFoundError:
		print ("Plus de composant a analyser")
		showinfo("Plus de graphique","Plus de composant à analyser")
		#Precedent(objGraphique,fenetre,canvas,label,chemin, minCpkVisu,maxCpkVisu)#Pour laisser le dernier graphique
		return 0
		
		
	#Généation de la figure :
	#Converton des tolérances
	tolBasse = Conversion_tol(monComposant.tolBasse)
	tolHaute = Conversion_tol(monComposant.tolHaute)
	
	try :
		refValue = float(monComposant.refValue)
	except ValueError:
		print ("Convertion de la value en float impossible...Value à 99999999")
		refValue = 99999999
		
	tolBasse = refValue - (tolBasse/100*refValue)
	tolHaute = refValue + (tolHaute/100*refValue)
	
	#print ("liste : {} , tolbasse : {} , tolHaute {} , moyenne : {} , ecartType : {} , cpkInf : {} , cpkSup : {}".format(monComposant.liste,tolBasse,tolHaute,monComposant.moyenne,
	#monComposant.ecartType, monComposant.cpkInf, monComposant.cpkSup))
	
	#Génération de la figure en fonction du composant actuel
	cpkFormat = str (monComposant.cpk)
	cpkFormat = cpkFormat[:4]
	valeur = str (monComposant.value)
	valeur = valeur[:4]
	moyenne = str(monComposant.moyenne)
	moyenne = moyenne [:4]
	toleranceBasse = str (tolBasse)
	toleranceBasse = toleranceBasse[:4]
	toleranceHaute = str (tolHaute)
	toleranceHaute = toleranceHaute[:4]
	
	figure = Generation_figure (monComposant.liste,tolBasse,tolHaute,
	titre = "Composant : " + monComposant.repere + " Step : " + monComposant.step + " Fonction :" + monComposant.fonction + "\ncpk : " + cpkFormat,
	legendTolBasse = monComposant.tolBasse, legendTolHaute = monComposant.tolHaute, legendData = "Données (" + monComposant.unit + ")")
	
	#Génération du graphique
	objGraphique.effacer(objGraphique.canvas)
	objGraphique.actualiser(figure,fenetre)
	objGraphique.afficher(objGraphique.canvas)
	
	#Mise a jour du label
	#Génération du texte pour le label
	txtlbl = "Composant : " + monComposant.repere + "\t\t\t\t\tUnite : " + monComposant.unit + "\nValeur : " + str (monComposant.refValue) + "\t\t\t\t\tMoyenne : " + moyenne + "\nTolérance basse : " + toleranceBasse + "\t\t\t\tTolérance haute : " + toleranceHaute
	label.config(text = txtlbl)
	varMontrer.set(int (monComposant.step))
	
def Mise_a_jour_label (text = 'Mise a jour') :
	#Création des labels pour les informations composant
	varInfoComposant = text
	
def Precedent (objGraphique,fenetre,canvas, label, chemin, minCpkVisu,maxCpkVisu, varMontrer) :
	'''
	Fonction pour actualiser le graphique lors de l'appuis sur Precedent
'''
	global numGraph
	#global lblInfoComposant
	numGraph = numGraph -1
	
	#Ouverture du premier objet :
	try :
		with open (chemin + str (numGraph),'rb') as fichier:
			mon_depickler = pickle.Unpickler(fichier)
			monComposant = capabilite.Composant()#Création de l'objet
			monComposant = mon_depickler.load() #Récupéation de l'objet monComposant
		
	#Récupération du cpk et de la fonction
		cpk = monComposant.cpk
		fonction = monComposant.fonction

		
	#Vérification du cpk pour afficher que ceux qui nous intéresse (filtre)
		while cpk > maxCpkVisu or cpk < minCpkVisu or fonction != "**" :
			numGraph = numGraph - 1
			with open (chemin + str (numGraph),'rb') as fichier:
				mon_depickler = pickle.Unpickler(fichier)
				monComposant = capabilite.Composant()#Création de l'objet
				monComposant = mon_depickler.load() #Récupéation de l'objet monComposant	
			cpk = monComposant.cpk
			fonction = monComposant.fonction
			#print (cpk)
			
	except FileNotFoundError:
		print ("Plus de composant a analyser")
		showinfo("Plus de graphique","Plus de composant à analyser")
		numGraph = numGraph +2
		#Suivant(objGraphique,fenetre,canvas,label,chemin, minCpkVisu,maxCpkVisu)#Pour laisser le dernier graphique
		return 0
			
	#Généation de la figure :
	#Converton des tolérances
	tolBasse = Conversion_tol(monComposant.tolBasse)
	tolHaute = Conversion_tol(monComposant.tolHaute)
	
	try :
		refValue = float(monComposant.refValue)
	except ValueError:
		print ("Convertion de la value en float impossible...Value à 99999999")
		refValue = 99999999
		
	tolBasse = refValue - (tolBasse/100*refValue)
	tolHaute = refValue + (tolHaute/100*refValue)
	
	#print ("liste : {} , tolbasse : {} , tolHaute {} , moyenne : {} , ecartType : {} , cpkInf : {} , cpkSup : {}".format(monComposant.liste,tolBasse,tolHaute,monComposant.moyenne,
	#monComposant.ecartType, monComposant.cpkInf, monComposant.cpkSup))
	
	#Génération de la figure en fonction du composant actuel
	cpkFormat = str (monComposant.cpk)
	cpkFormat = cpkFormat[:4]
	valeur = str (monComposant.value)
	valeur = valeur[:4]
	moyenne = str(monComposant.moyenne)
	moyenne = moyenne [:4]
	toleranceBasse = str (tolBasse)
	toleranceBasse = toleranceBasse[:4]
	toleranceHaute = str (tolHaute)
	toleranceHaute = toleranceHaute[:4]
	
	figure = Generation_figure (monComposant.liste,tolBasse,tolHaute,
	titre = "Composant : " + monComposant.repere + " Step : " + monComposant.step + " Fonction :" + monComposant.fonction + "\ncpk : " + cpkFormat,
	legendTolBasse = monComposant.tolBasse, legendTolHaute = monComposant.tolHaute, legendData = "Données (" + monComposant.unit + ")")
	
	#Génération du graphique
	objGraphique.effacer(objGraphique.canvas)
	objGraphique.actualiser(figure,fenetre)
	objGraphique.afficher(objGraphique.canvas)
	
	#Mise a jour du label
	#Génération du texte pour le label
	txtlbl = "Composant : " + monComposant.repere + "\t\t\t\t\tUnite : " + monComposant.unit + "\nValeur : " + str (monComposant.refValue) + "\t\t\t\t\tMoyenne : " + moyenne + "\nTolérance basse : " + toleranceBasse + "\t\t\t\tTolérance haute : " + toleranceHaute
	label.config(text = txtlbl)
	varMontrer.set(int (monComposant.step))
	
	
if __name__ == "__main__":	
	#Generation de la liste des figures
	#listFigure = []
	#listFigure = Ouverture_liste_figure(chemin,nomProjet)


		
	#Création de la fenetre
	fenetre = Tk()
	fenetre.geometry("640x480")
	fenetre.title("Analyse de Capabilite")

	#Instance de graphique
	monGraphique = Graphique(Generation_figure([0,0],-1,1),fenetre)

	#Création d'un menu
	menu_principal = Menu(fenetre)  ## Barre de menu 
	sous_menu = Menu(fenetre)
	menu_principal.add_command(label = "Nouveau Projet",command = Quitter)
	menu_principal.add_command(label = "A propos",command = About)
	menu_principal.add_command (label = "Quitter", command = Quitter)
	fenetre.config(menu = menu_principal)

	#Création du Label
	varInfoComposant = StringVar ()#String var pour affichage des infos selon le composants
	varInfoComposant = ''
	lblInfoComposant = Label (fenetre, text = varInfoComposant)
	lblInfoComposant.pack()
	
	
	
	#Création d'un bouton suivant et précédent
	btnSuivant = Button(fenetre,text="Suivant",command = lambda : Suivant(monGraphique,fenetre,monGraphique.canvas,lblInfoComposant))
	btnSuivant.pack()
	
	btnPrecedent = Button(fenetre,text="Precedent",command = lambda : Precedent(monGraphique,fenetre,monGraphique.canvas,lblInfoComposant))
	btnPrecedent.pack()
	


	fenetre.mainloop()