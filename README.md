# Cripito
Easy, fast, free and handable Crypto!

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
