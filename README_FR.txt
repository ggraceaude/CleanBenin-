CLEANBENIN — VERSION CORRIGÉE

IMPORTANT
- Le ZIP contient le code du site, pas un site déjà publié sur Internet.
- Il faut un hébergement compatible Python/Flask pour que les réservations soient reçues à distance.
- Ouvrir directement templates/login.html dans un navigateur ne fonctionne pas : les fichiers HTML utilisent le moteur de modèles Flask.
- Aucun numéro de téléphone de l'entreprise n'est affiché publiquement.
- Les clients fournissent leurs propres coordonnées dans le formulaire.
- Les réservations sont enregistrées dans une base SQLite sur le serveur.
- Le tableau de bord ne prévient pas automatiquement l'administratrice : il faut consulter /admin/reservations.

IDENTIFIANT ADMINISTRATEUR
Nom d'utilisateur par défaut : CleanBenin

MOT DE PASSE
Aucun mot de passe par défaut n'est fourni. Configure-le dans les variables d'environnement de l'hébergement :
CLEANBENIN_ADMIN_PASSWORD = un mot de passe fort choisi par toi
CLEANBENIN_SECRET_KEY = une longue clé secrète aléatoire
CLEANBENIN_ADMIN_USERNAME = CleanBenin (facultatif, déjà la valeur par défaut)

LANCEMENT LOCAL SUR UN ORDINATEUR
1. Installer Python 3.
2. Ouvrir un terminal dans ce dossier.
3. Installer les dépendances : pip install -r requirements.txt
4. Définir CLEANBENIN_ADMIN_PASSWORD et CLEANBENIN_SECRET_KEY.
5. Lancer : python app.py
6. Ouvrir http://127.0.0.1:5000

Pour utiliser le site avec des clients, il faut le déployer sur un hébergeur Python/Flask et configurer les variables ci-dessus. Ne partage jamais ton mot de passe dans une conversation.
