# Application web pour gérer des livres d'une bibliothèque

Développement pour la bibliothèque de la société archéologique de Touraine.

Voir le [site de la société archéologique de Touraine](http://www.societearcheotouraine.eu/).


##  Pour le développeur

### Préparation du système

Le code a été testé sur Windows 10 ainsi que Debian Buster. Il est prévu de pouvoir faire tourner l'application sur Docker


Il a été décidé de coder le serveur à l'aide du framework web Flask et pour l'interface web, le choix s'est porté sur Vue JS v3 (build avec Vite).
Python 3.11 minimum.
Sur Debian:
```bash
apt-get install python3 python3-dev python3-pip 
apt-get install nodejs npm 
```

### Installation des paquets

Installation des paquets Python. Les dépendances sont déclarées dans `pyproject.toml`,
qui en est l'unique source de vérité ; `uv.lock` fige les versions exactes.
Python 3.11 minimum.

Avec [uv](https://docs.astral.sh/uv/) (versions verrouillées, identiques à celles de
l'image Docker) :
```bash
uv sync
```

Ou avec pip :
```bash
python3 -m venv venv-satbiblio
source venv-satbiblio/bin/activate
pip install -e .
```

Après toute modification des dépendances dans `pyproject.toml`, régénérer le lock
avec `uv lock` et le committer — sans quoi le build Docker échouera (`--locked`).

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
npm run serve
```

## Faire tourner avec Docker

`docker-compose.yml` monte la pile complète : l'API Flask (gunicorn) et l'interface
Vue 3 compilée, servie par nginx.

```bash
docker compose up -d --build
```

| Service | URL | Port hôte → conteneur |
| --- | --- | --- |
| `interface` | <http://localhost:8085> | 8085 → 8080 |
| `api` | <http://localhost:5000> | 5000 → 8080 |

L'interface attend que l'API soit *healthy* (`depends_on: condition: service_healthy`)
avant de démarrer ; la sonde interroge `/health`.

Commandes courantes :
```bash
docker compose logs -f api        # suivre les logs
docker compose ps                 # état et santé des services
docker compose down               # arrêter (les données sont conservées)
```

### ⚠️ L'URL de l'API est figée à la compilation

Vite intègre les variables `VITE_*` dans le bundle JavaScript au moment du build. Le
`docker-compose.yml` passe donc `VITE_APP_SITE_API_URL=http://localhost:5000/` en
**argument de build**, pas en variable d'exécution.

Conséquence : après avoir modifié cette valeur, un simple `restart` ne suffit pas, il
faut reconstruire l'image.

```bash
docker compose build interface && docker compose up -d
```

La variable doit être nommée `VITE_APP_SITE_API_URL`. L'ancienne convention Vue CLI
`VUE_APP_…` ne correspond à aucun `ARG` du Dockerfile : Docker l'ignore silencieusement
et le build retombe sur `.env.production`, c'est-à-dire l'API **de production**.

### `SERVER_NAME` et `CORS_ORIGINS`

Les conteneurs utilisent la configuration de production
(`sat_biblio_server/config/production.py`), qui restreint par défaut les requêtes à
l'en-tête `Host: api.satbiblio.clementbesnier.eu` — sinon Flask renvoie **404 sur
toutes les routes**.

Le compose neutralise ce filtrage pour l'usage local :

| Variable | Valeur dans le compose | Effet |
| --- | --- | --- |
| `SERVER_NAME` | vide | désactive le contrôle du `Host`, l'API répond sur `localhost` |
| `CORS_ORIGINS` | `http://localhost:8085` | autorise les appels du SPA |

En l'absence de ces variables, les valeurs de production s'appliquent. Si tu changes le
port publié de l'interface, `CORS_ORIGINS` doit suivre, faute de quoi le navigateur
bloquera tous les appels à l'API.

### Secrets

Les valeurs de `docker-compose.yml` (`SECRET_KEY`, `JWT_SECRET_KEY`, `MAIL_PASSWORD`…)
sont des **bouchons destinés au développement local**. Pour un déploiement réel, il
faut les remplacer, de préférence via un fichier `.env` non versionné plutôt qu'en dur
dans le compose.

À noter : les fichiers de secrets de `sat_biblio_server/config/` (cf. section
précédente) sont prioritaires sur ces variables d'environnement lorsqu'ils existent, et
le `COPY . .` du Dockerfile les embarque dans l'image s'ils sont présents dans le
contexte de build.

### Données persistantes

Deux volumes nommés survivent à `docker compose down` :

- `sat_biblio_data` → `/app/data` (base SQLite)
- `sat_biblio_uploads` → `/app/uploads` (fichiers téléversés)

```bash
docker compose down -v   # ⚠️ supprime les volumes, donc la base et les téléversements
```

### Documentation détaillée des images

- `DOCKERFILE.md` — l'image du backend Flask
- `sat-biblio-interface/DOCKERFILE.md` — l'image du frontend Vue 3 / nginx