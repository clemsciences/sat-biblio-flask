# Application web pour gérer des livres d'une bibliothèque

Développement pour la bibliothèque de la société archéologique de Touraine.

Voir le [site de la société archéologique de Touraine](http://www.societearcheotouraine.eu/).


##  Pour le développeur

### Préparation du système

Le code a été testé sur Windows 10 ainsi que Debian Buster. Il est prévu de pouvoir faire tourner l'application sur Docker


Il a été décidé de coder le serveur à l'aide du framework web Flask et pour l'interface web, le choix s'est porté sur Vue JS v2.
Python 3.7 à 3.10 supporté.
Sur Debian:
```bash
apt-get install python3 python3-dev python3-pip 
apt-get install nodejs npm 
```

### Installation des paquets

Installation des paquets Python
```bash
cd sat_biblio_server
python3 -m venv venv-satbiblio
source venv-satbiblio/bin/activate
pip install -r requirements.txt
```

Installation des paquets NPM
```bash
cd sat-biblio-interface
npm install
```

### Installer les secrets

Ajouter les fichiers suivants dans le dossier sat_biblio_server/config/ : 
- email_address (adresse email utilisée pour faire tourner l'envoi d'email)
- mail_password (mot de passe pour envoyer des emails)
- (jwt_secret_key (clé pour chiffrer les JWT))
- (key.txt (clé))
- secret_key (phrase de passe pour le serveur Python)

### Faire tourner

Faire tourner le côté Python.
```bash
cd sat_biblio_server
python3 app.py
```
Et faire tourner le côté Vue JS.
```bash
cd sat-biblio-interface
npm run server
```