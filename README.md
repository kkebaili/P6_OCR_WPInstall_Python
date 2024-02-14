# OC-P6
Projet 6 de la formation AIC de OpenClassrooms

Ces scripts ont pour objectif d'automatiser l'installation d'un serveur WordPress sur un serveur Linux Ubuntu.
Il a été testé avec succès sur Ubuntu Server 20.04 LTS. 
Il devrait également fonctionner (mais n'a pas été testé) sur un serveur Debian.

Le script principl est : "P6_MainInstWP.py" qui appelle en cascade :
"P6_InstallWP.py"  puis "P6_InstallDependencies" puis "P6_UninstallWPython.py"

Dans la mesure où le programme modifie le système, il doit être exécuté en root (via un sudo sous Ubuntu).
Commande pour executer le script principal:  sudo python3 P6_MainInstWP.py

Commandes pour executer les scripts: 
sudo python3 P6_MainInstWP.py
sudo python3 P6_MainInstWP.py  > logs.txt 2>&1

sudo python3 P6_InstallWP.py 
sudo python3 P6_InstallWP.py > logs.txt 2>&1

sudo python3 P6_UninstallWPython.py
sudo python3 P6_UninstallWPython.py > logs.txt 2>&1

Liens pour tester wordPress
http://IP-VM-Ubuntu/wp-login.php  

Une description exhaustive de ce que font les programme est dans un document PDF en annexe.


Pré-requis : 
1.	Une VM ubuntu 20.04 ou supérieur avec un dossier partagé sur le PC local pointant sur le répertoitre des scripts
2.	Un repertoire de scripts Python pointant sur un dépôt GitHub 
3.	Un repo GitHub
Cinématique d’appel des scripts Pythons : 
1.	Le script Main (P6_MainInstWP.py) vérifie si WordPress est installé sur la VM ubuntu en vérifiant l'existence d'un répertoire spécifique (/var/www/html/wordpress). 
En fonction du résultat de cette vérification, il exécute soit : 
o	un processus de désinstallation propre de WordPress, 
o	soit un processus d'installation de WordPress.


2.	Le script d’installation (P6_InstallWP.py)  automatise le processus d'installation et de configuration de WordPress sur un serveur Ubuntu, en s'assurant que toutes les dépendances nécessaires sont installées et que WordPress est correctement configuré et prêt à être utilisé. Il effectue les actions suivantes :

•	Vérification et installation des dépendances : (bibliothèque Paramiko et curl).
•	Configuration du fichier de configuration Apache pour le virtual host.
•	Installation de WP-CLI pour gérer WordPress en ligne de commande.
•	Configuration de la base de données MySQL/MariaDB.
•	Installation d'Apache, PHP et autres dépendances nécessaires.
•	Téléchargement, extraction et configuration de WordPress.
•	Configuration des permissions sur les fichiers WordPress.
•	Configuration du fichier de configuration de WordPress avec les informations de base de données.
•	Installation de WordPress en utilisant WP-CLI avec les informations d'administrateur spécifiées.

3.	le script P6_InstallDependencies.py installe Python et la bibliothèque Paramiko, utilisée pour la communication SSH en Python. 
4.	Le script Python(P6_UninstallWPython.py)  assure une désinstallation complète de WordPress et de ses dépendances, y compris la suppression des fichiers, de la base de données et des utilisateurs associés, ainsi que la désinstallation propre des packages PHP et MySQL. Il effectue plusieurs actions pour désinstaller WordPress et ses dépendances sur un système Ubuntu :
•	Création d'un utilisateur MySQL :
o	Vérifie d'abord si l'utilisateur existe déjà dans la base de données MySQL. S'il n'existe pas, le script crée un nouvel utilisateur avec les privilèges appropriés.
•	Suppression de la base de données :
o	Vérifie si la base de données WordPress existe. Si c'est le cas, elle est supprimée.
•	Suppression des fichiers WordPress :
o	Supprime les fichiers téléchargés de WordPress ainsi que le répertoire WordPress s'il existe.
•	Suppression de la configuration Apache pour WordPress :
o	Supprime le fichier de configuration du virtual host Apache pour WordPress.
•	Désactivation du module rewrite Apache :
o	Désactive le module rewrite Apache.
•	Redémarrage d'Apache :
o	Redémarre le service Apache pour appliquer les changements.
•	Suppression de PHP :
o	Vérifie si PHP est installé. Si oui, le package PHP et ses dépendances sont supprimés.
•	Suppression de MySQL : 
o	Vérifie si MySQL est installé. Si oui, MySQL est supprimé, puis les commandes apt autoremove et apt autoclean sont exécutées pour nettoyer les dépendances inutilisées et les fichiers de cache.
