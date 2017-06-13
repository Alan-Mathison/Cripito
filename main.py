#!/usr/bin/python

# -*- coding: utf-8 -*-



intro_cripito = """
########################################################
########################################################
#
#			Cripito1.3.10
#
########################################################
########################################################

########################################################
Programme de cryptage/décryptage  il s'appuie sur  un cryptage flottant aléatoire
 symétrique double, sur une base d'une table alphanumérqiue de 83 octects.
cryptage de bon niveau, NON vulnérable aux attaques par fréquences.

Il fonctionne desormais sur l'ensemble des fichiers, dans le répertoire courant
 et dans les sous répetoires relatifs.

En dehors de ca, par rapport à v1.3.10 : 
* On a simplifié et factorise le code
* Il faut supprime le choix automatique des fichiers et mots de passe etc etc 
* Il faut supprimer les prints de confort
* On teste un passage en mode readline

Pour la v1.3.10:
* probleme il travaille sur une chaine de caractere mais pas sur le code source 
du programme il faudrait pouvoir travailler sur le code source du fichier...

* On simplifie le code pour accelerer la prod en moinee à 120ko/s
* Il faudrait mettre en place un systeme de hashage
* et un double criptage
* il faut rajouter tous les "x" caracteres un caractere aléatoire
* passer en mode classe  + modules
* GUI :)
crypte en moyenne à 127,7 ko/s
decrypte en moyenne à 125.3 ko/s

########################################################

########################################################
# Auteur	Alexandre GAZAGNES
# Version	1.3.10
# Date		19/02/2017
########################################################
\n"""



########################################################
# 	Import
########################################################


import os

import time



########################################################
# 	Variables et constantes
########################################################


# Chaine de caracteres pour criptage aléatoire, le code de repoduction de cette chaine est script2.py
TABLE_CRYPT = ''' s7GNC3ieIzOTP8l6EoKYvhqtB0kuJUHQcRDjmy49FXxZfrgdb2anwV5SMWLA1péèàùêâîôç()=.:;*&?!,-_ÉÈÀËÄÏÖûÜ°¨£$€^%µ/"'~#{[|`\^@]}¤'''

# il nous faut une ANTI_TABLE_CRYPT en mode "inverse" pour le décryptage de certaines clés (sup à len(TABLE_CRYPT))
ANTI_TABLE_CRYPT = str()
for i in (reversed(TABLE_CRYPT)) : ANTI_TABLE_CRYPT += str(i)

# variables déclarées, à supprimer...
volume_donnees = 0
time_stop_algo = 0
time_start_algo = 0
liste_fichiers = ""
liste_dossiers = ""



########################################################
# 	Fonctions
########################################################


def introduction():
	"""Fonction d'affichage des informations de lancement du programme
	il s'agit plus d'une routine/procedure que d'une vraie fonction

	Entree : -, Sortie : -"""

	rep = input("Afficher l'introduction? \n<Entrée> pour non, autre touche pour oui, ou <Crtl> + Z ou X pour arréter.\n")
	if rep : print(intro_cripito)



def formater_volume_donnees(vol_don):
	"""COMMENTAIRE
	"""

	for i in [(1, "o"), (1000, "Ko"), (1000000,"Mo"), (1000000000, "Go"), (1000000000000, "To"),(1000000000000000, "Po")] : 
		if (vol_don // i[0]) >0 : couple_multiple_unite = i
	return couple_multiple_unite



def formater_avancement_algo(nb, base=25):
	nb = int(nb/4)
	chaine = "[" + (nb * "I") + ((base-nb) * ".") + "]"
	return chaine



def conclusion():
	"""Fonction d'affichage des informations de cloture du programme
	il s'agit plus d'une routine/procedure que d'une vraie fonction

	Entree : -, Sortie : -"""

	print("durée du programme :\t {} secondes".format(round(temps_execution_programme,2)))	
	print("durée de l'algorithme :\t {} secondes".format(round(temps_execution_algo,2)))
	print("nombre de fichiers :\t {}".format(len(liste_fichiers)))
	print("nombre de dossiers :\t {}".format(len(liste_dossiers)))
	print("nombre d'éléments :\t {}".format(len(liste_fichiers)+len(liste_dossiers)))
	print("volume des données :\t {} {}".format(round(volume_donnees/div_nb_oct,2), type_oc))
	donnees_vitesse = (volume_donnees / temps_execution_algo)
	div_nb_oct2, type_oc2 = formater_volume_donnees(donnees_vitesse)
	print("vitesse estimée : \t {} {}/sec".format(round((donnees_vitesse/div_nb_oct2),2), type_oc2))



def choisir_action():
	"""Choisir action de cryptage ou de décryptage
	
	Entree : - 
	Sortie: True pour cryptage, False pour décryptage"""

	action_est_crypter = True
	action = input("Quelle est l'action, crypter ou décrypter ? \n<Entrée> pour crypter, autre touche pour decrypter, ou <Crtl> + Z ou X pour arréter.\n")
	if action : action_est_crypter = False

	return action_est_crypter



def lister_fichiers_dossiers():
	"""Choisir le repertoire de travail, le repertoire proposé de base est le repertoire courant
	Cela peut etre changé en fonction du choix de user
	
	Entree : -
	Sortie: un tuple : chemin global, la liste des dossiers et la liste des fichiers """

	# on identifie le repertoire parent

	repertoire_global = os.getcwd()
	rep_valide = False
	reponse = input("\nLe repertoire courant est {} est-ce le bon? \n<Entrée> pour oui, autre touche pour non ou <Crtl> + Z ou X pour arréter.\n".format(repertoire_global))
	while not rep_valide:
		if reponse : repertoire_global = input("\nEntrez le repertoire de votre choix:\n")
		try : 
			os.chdir(repertoire_global)
			rep_valide = True
		except:
			print("\nRepertoire non conforme, essayez encore, ou <Crtl> + Z ou X pour arréter.")

	# on reconstitue l'arborésence du dossier
	liste_fichiers,liste_dossiers =list(), list()
	for dossier, sous_dossiers, fichiers in os.walk(repertoire_global):
		for fichier in fichiers:
				liste_fichiers.append(os.path.join(dossier, fichier))
		for sous_dossier in sous_dossiers: 
				liste_dossiers.append(os.path.join(dossier,sous_dossier))

	liste_dossiers = list(reversed(liste_dossiers))

	return repertoire_global, liste_fichiers, liste_dossiers



def calculer_taille_dossiers_fichiers(): 
	""" renvoie la taille globale d'un répertoire

	Entree :  Chemin Dossier sous forme chaine
	Sortie : ?"""

	taille = 0  
	for dossier, sous_dossiers, liste_fichiers in os.walk(repertoire):  
		for fichier in liste_fichiers:  
			taille += os.path.getsize(os.path.join(dossier, fichier)) 
	return taille



def choisir_traduire_cle():
	"""choisir de la clé de criptage

	Entree : - 
	Sortie : la clé sous forme de nombre"""

	# 1/ On iput la Bonne Clé
	cle_valide = False
	cle_brute = input("Clé alphanumérique ?, entre 12 et 24 caracteres, pas d'espace en 1er caractere\n")

	while not cle_valide :

		# 1/ On input la Bonne Clé
		if not cle_brute : cle_brute = "abcdefghijklmn"

		cle_brute = str(cle_brute)

		if len(cle_brute)<12 : print("\nClé trop courte, pas assez de sécurité, il faut au moins 12 caracteres")
		if len(cle_brute)> 24 : print("\nClé trop longue, il faut au maximum 24 caracteres")
		if cle_brute[0] == " ": print("\nPas d'espace en 1er caractere!")
		if (cle_brute[0] != " ") and (25>len(cle_brute)>= 12) : 
			cle_valide = True
			# 2/ On la traduit en chiffre
			cle_int = str()
			for i in cle_brute : 
					for j,k in enumerate(TABLE_CRYPT): 
						if i == k : cle_int += str(j)
			cle_int = int(cle_int)
			if cle_int % len(TABLE_CRYPT) == 0 : 
				print("Clé non valide, cryptage impossible")
				cle_valide = False
		if not cle_valide : cle_brute = input("Essayez encore ou <Crtl> + Z ou X pour arréter:\n")

	return cle_brute, cle_int



def extraire_fichier():
	"""importer, extraire et traiter le fichier source
	le fichier est exporté dans une chaine qui est renvoyée

	Entree : un fichier
	Sortie : une chaine contenant l'information du fichier"""

	try: # traitement du fichier source
		obj_fichier = open(fichier, "r")  # le triptique classique :)
		texte_fichier = obj_fichier.read() # c'est texte_fichier que nous allons manipuler
		obj_fichier.close() # on pourrait meme des maintenant supprimer le fichier mais c'est un peu risqué...
	except:
		input("Problème import fichier, essayez encore, ou <Crtl> + Z ou X pour arréter\n")

	return texte_fichier



def crypter(texte, action, cle):
	"""crypter/décrypter 

	Entree : le texte  sous forme de chaine, l'action True pour crypter, False pour décrypter, la clé choisie par l'utilisateur
	Sortie : le texte du fichier,  crypté ou décrypté	"""

	# Travail sur la clé
	# --------------------------------------------------
	# quelque soit la clé brute elle a été transcripte en une suite de chiffres de 0 à 9 :274057291.
	# idéalement il faudrait avoir une liste ou  un tuple de type (12, 34, 6, 0, 1,89), ca rajouterai à la sécurité 
	# pour l'heure et pour éviter les attaques par fréquence, la transcription ne se fera pas de facon fixe (+12 par exemple)
	# cela va dépendre de la clé
	# si la clé est 123, le 1er car sera décalé de 1, puis le 2e de 2 puis le 3e de 3 puis le 4e de 1 puis le 5e de 2 etc etc
	# ainsi la lettre "a" dans le fichier d'origine ne sera pas transcrite toujours de la meme facon rendant les attaques par 
	# fréquences impossibles
	# pour rajouter de la sécurité on pourrait Inverser la chaine principale...
	cle = str(cle) # cle devient une chaine pour etre parcourue 
	long_cle = len(cle)
	count_cle = 0


	# process de cryptage /decryptage
	# ---------------------------------------

	# on créé la nouvelle chaine "traduite"
	texte_traduit = str()

	if int(cle) % len(TABLE_CRYPT) != 0: # si clé = len(chain_char), ou 0 ou multiple de len(chain_char) erreur ca n'est pas traduit!
		if action: 	# ON CRYPTE	
			for i in texte: # on analse les caracteres du ficier source 1 à 1
				if i in TABLE_CRYPT: # on ne va pas tout crypter, seulement les carateres "principaux", pas les É ou les À etc etc osef
					for j,k in enumerate(TABLE_CRYPT): # pour chaque caratere de la chaine on parours notre liste de caractere TABLE_CRYPT
						if i == k: #si concordance....
							nb_new_char = j+int(cle[count_cle]) # on décale de la valeur "clé"" la référence du caractere du fichier source
							while nb_new_char >= len(TABLE_CRYPT): # si le décalage est trop grand on "dépasse" de la chaine, ex nb_new char = 200
								nb_new_char = nb_new_char%(len(TABLE_CRYPT)) # ... on revient au debut de la chaine 
							texte_traduit += TABLE_CRYPT[nb_new_char] # notre texte "crypté" est donc "cle_brut carateres" "plus loin"
					count_cle += 1
					if count_cle == len(cle) : count_cle = 0
				else : texte_traduit+= i # si caractere spécial É À etc etc osef, on change rien

		else : 	# ON DECRYPTE
			for i in texte: # cf commentaire ci dessus
				if i in TABLE_CRYPT: # cf commentaire ci dessus
					for j,k in enumerate(TABLE_CRYPT): # cf commentaire ci dessus
						if i == k: # cf commentaire ci dessus
							nb_new_char = j-int(cle[count_cle]) # on décrypte donc on décale dans l'autre sens
							if int(cle) > len(TABLE_CRYPT): # ATTENTION du coup on peut passer en négatif !!! # il faut corriger ca!
								nb_new_char = len(TABLE_CRYPT) - nb_new_char -1 # on "inverse" nb_new_char par rapport à notre TABLE_CRYPT , -1 = 89, -2 =88 etc etc
								while nb_new_char >= len(TABLE_CRYPT): # cf commentaire ci dessus
									nb_new_char = nb_new_char%(len(TABLE_CRYPT)) # cf commentaire ci dessus
								texte_traduit+= ANTI_TABLE_CRYPT[nb_new_char] # ATTENTION on est en mode "inverse", c'est donc anti_chaine char qui entre en jeu!!!
							else: #sinon décriptage normal....
								while nb_new_char >= len(TABLE_CRYPT):
									nb_new_char = nb_new_char%(len(TABLE_CRYPT))
								texte_traduit+= TABLE_CRYPT[nb_new_char]
					count_cle += 1
					if count_cle == len(cle) : count_cle = 0
				else : texte_traduit+= i  # cf commentaire ci dessus

	return texte_traduit



def spliter_chemin(chemin, reverse=False):
	"""si reverse=False : dissocier un chemin sous forme de chaine et en faire une liste splité par "/"
	si reverse =True, action inverse ressocier une liste sous forme de chaine en ajoutant "/" en séparateur

	Entree : un chemin qui peut etre une liste ou une chaine + reverse False pour spliter, True pour ressocier
	Sortie : un chemin slité ou ressoicé qui peut etre une liste ou une chainen"""

	if not reverse: chemin = chemin.split("/")
	else: chemin = "/".join(chemin)

	return chemin



def dissocier_chemin_fichier(element):
	element = str(element)
	element = spliter_chemin(element)
	chemin = element[0:-1]
	fichier = element[-1]

	return chemin, fichier

	

########################################################
# 	MAIN
########################################################


# Introduction
########################################################

time_start_programme = time.time()
introduction()


# Receuil des données de lancement
########################################################


# Choix action
action = choisir_action()
print("action cripter = {}".format(action), end = "; ")
if action : print("On crypte.")
else : print("On décrypte.")


# Extraction des fichiers et dossiers
repertoire, liste_fichiers, liste_dossiers = lister_fichiers_dossiers()
print("\nrepertoire = {}\n".format(repertoire))
print("liste_fichiers = {}\n".format(liste_fichiers))
print("liste_dossiers = {}\n".format(liste_dossiers))
print("nombre liste_fichiers = {}".format(len(liste_fichiers)))
print("nombre liste_dossiers = {}".format(len(liste_dossiers)))

nombre_dossiers_fichiers = len(liste_fichiers)+len(liste_dossiers)

print("nombre d'éléments = {}".format(nombre_dossiers_fichiers))


# Calcul et mise en forme du volume des fichiers et dossiers
volume_donnees = calculer_taille_dossiers_fichiers()
div_nb_oct, type_oc = formater_volume_donnees(volume_donnees)
print("volume_donnees = {} {}\n".format(round(volume_donnees/div_nb_oct,2), type_oc))


# Choix et traduction de la clé de cryptage
cle_originale, cle_traduite = choisir_traduire_cle()
print("\nclé originale = {}".format(cle_originale))
print("clé traduite = {}".format(cle_traduite))


# Lancement de l'algorithme principal
########################################################

time_start_algo = time.time()
count_avancement = 0
count_donnees_traitees = 0
nombre_actions = 2 * (len(liste_fichiers)) + len(liste_dossiers)


# traitement du contenu des fichiers
for fichier in liste_fichiers:
	count_avancement+=1
	count_donnees_traitees += os.path.getsize(fichier)
	
	# splitage du chemin et traduction nom du element
	try :
		chemin, ancien_fichier = dissocier_chemin_fichier(fichier)
		nouveau_fichier = crypter(ancien_fichier, action, cle_traduite)
	except : 
		input("\nprobleme dans le splitage du chemin et traduction nom du {} pour {}\n"
			.format("fichier", ancien_fichier))

	# créer nouveau fichier
	try : 
		os.chdir("/".join(chemin))
		nouveau_fichier = crypter(ancien_fichier, action, cle_traduite)
		objet_nouveau_fichier = open(nouveau_fichier, "w")
	except :
		input("\nprobleme dans la creation du nouveau {} dans le répertoire {} : {}\n"
			.format("fichier", chemin, nouveau_fichier))

	objet_ancien_fichier = open(ancien_fichier, "r")

	# cryptage ligne par ligne
	continuer = True
	while continuer : 
		ligne_brute = objet_ancien_fichier.readline()
		ligne_traduite = crypter(ligne_brute, action, cle_traduite)
		objet_nouveau_fichier.write(ligne_traduite)
		if ligne_brute == "" : 
			continuer = False 

	objet_ancien_fichier.close()
	objet_nouveau_fichier.close()
	os.remove(ancien_fichier)

	p_100_avancement = (count_avancement/nombre_actions)*100
	p_100_donnees = (count_donnees_traitees/volume_donnees)*100
	print(formater_avancement_algo(p_100_avancement), round(p_100_avancement), 
		"%","du nombre total de fichiers")
	print(formater_avancement_algo(p_100_donnees), round(p_100_donnees), 
		"%", "du volume total de données\n")

print("\non a traité l'ensemble des contenus des fichiers, on va passer à leur nom\n")



# traitement du nom des fichiers, puis des dossiers (meme algorritme) 
chaine_element = "dossier"
liste_elements = liste_dossiers
for element in liste_elements:

	count_avancement+=1
		
	# splitage du chemin et traduction nom du element
	try :
		chemin, ancien_element = dissocier_chemin_fichier(element)
		nouveau_element = crypter(ancien_element, action, cle_traduite)
	except : 
		input("\nprobleme dans le splitage du chemin et traduction nom du {} pour {}\n"
			.format(chaine_element, element))
	
	# changement de nom du element
	try : 
		chemin = spliter_chemin(chemin, reverse=True)
		os.chdir(chemin)
		os.rename(ancien_element, nouveau_element)
	except: 
		input("\nProbleme dans le changement de nom pour {} \n"
			.format(element))
	p_100_avancement = (count_avancement/nombre_actions)*100
	p_100_donnees = (count_donnees_traitees/volume_donnees)*100
	print(formater_avancement_algo(p_100_avancement), round(p_100_avancement), 
		"%","du nombre total de fichiers")
	print(formater_avancement_algo(p_100_donnees), round(p_100_donnees), 
		"%", "du volume total de données\n")

if chaine_element == "fichier" : print("\non a traité l'ensemble des noms des fichiers, on va passer à leur dossiers\n")
else : print("\non a traité l'ensemble des noms des dossiers, on va passer à la conclusion\n")

time_stop_algo = time.time()


# Conclusion
########################################################

time_stop_programme = time.time()

temps_execution_algo = time_stop_algo - time_start_algo
temps_execution_programme = time_stop_programme - time_start_programme

conclusion()

