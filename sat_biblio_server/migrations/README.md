Generic single-database configuration.


À la racine du projet :
```bash
$ python -m flask db migrate
```
Il faut ensuite modifier le fichier généré.
(Il faut commenter les commandes associées à sqlite_sequence)
Puis lancer la commande de mise à jour de la base
```bash
$ python -m flask db upgrade
```