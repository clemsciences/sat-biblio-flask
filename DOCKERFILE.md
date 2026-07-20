# Le Dockerfile expliqué

Ce document décrit ligne par ligne le `Dockerfile` qui construit l'image du backend
Flask de sat-biblio.

L'image utilise une **construction multi-étapes** (*multi-stage build*) : une première
étape installe les dépendances (avec les outils de compilation), une seconde ne récupère
que le résultat. Les compilateurs, les en-têtes C et le cache de `git` restent dans
l'étape de build et n'alourdissent pas l'image finale.

---

## En-tête

```dockerfile
# syntax=docker/dockerfile:1
```

Active le *frontend* Dockerfile v1 de BuildKit, qui apporte la syntaxe moderne
(`COPY --chown`, `RUN --mount`, etc.).

---

## Étape 1 — `builder`

```dockerfile
FROM python:3.11-slim-bookworm AS builder
SHELL ["/bin/bash", "-c"]
WORKDIR /app
```

Base Python 3.11 en variante `slim` (Debian Bookworm sans les paquets superflus).
Le shell est passé à `bash` — plus permissif que le `/bin/sh` par défaut pour les
constructions un peu élaborées. `WORKDIR` crée et se place dans `/app`.

```dockerfile
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PATH="/opt/venv/bin:$PATH"
```

| Variable | Rôle |
| --- | --- |
| `PIP_NO_CACHE_DIR` | pip n'écrit pas son cache de roues : couche plus légère |
| `PIP_DISABLE_PIP_VERSION_CHECK` | supprime l'avertissement « a new release of pip is available » |
| `PIP_ROOT_USER_ACTION=ignore` | supprime l'avertissement d'installation en root |
| `PATH` | place le venv en tête du `PATH`, ce qui évite d'avoir à l'« activer » |

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
```

`git` est **indispensable** : `pyproject.toml` déclare deux dépendances installées
depuis un dépôt Git (`… @ git+https://…`), à savoir `sat-biblio-referencement` et un
fork épinglé de `flask-login`. `build-essential` fournit gcc & co. pour les paquets
qui devraient compiler des extensions C. La suppression des listes APT dans le
**même** `RUN` évite de les figer dans la couche.

```dockerfile
RUN pip install uv==0.9.21
```

### Pourquoi `uv` et pas `pip` ?

`pyproject.toml` est l'unique source de vérité des dépendances : il n'y a
volontairement **pas** de `requirements.txt` dans le dépôt, pour éviter d'entretenir
deux listes qui divergent.

Or `pip` ne sait pas « installer seulement les dépendances » d'un projet. Un
`pip install .` construit le paquet, et exige donc `version.txt` (la version est
`dynamic`), `README.md`, `LICENSE` **et le répertoire `sat_biblio_server/` lui-même**
(`packages` est explicite dans `[tool.setuptools]`). Il faudrait copier le code avant
d'installer — et alors **chaque modification d'une ligne de Python invaliderait le
cache** et relancerait l'installation complète.

`uv sync` lit directement la table `dependencies`. Comme celle-ci est statique et que
`--no-install-project` évite de construire l'application elle-même, les seuls fichiers
requis sont `pyproject.toml` et `uv.lock`.

```dockerfile
COPY pyproject.toml uv.lock ./
```

Seuls les manifestes sont copiés à ce stade — c'est le point clé du cache Docker :
tant qu'ils ne changent pas, l'étape d'installation qui suit est réutilisée telle
quelle, même si le code applicatif a été modifié.

```dockerfile
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN uv sync --locked --no-install-project
```

`UV_PROJECT_ENVIRONMENT` indique à `uv` où créer le virtualenv ; par défaut il
choisirait `.venv` dans le répertoire du projet. C'est `/opt/venv`, et lui seul, qui
sera transféré à l'étape suivante — d'où l'intérêt d'y concentrer toutes les
dépendances.

### `--locked` et non `--frozen`

Les deux flags se ressemblent mais ne font pas du tout la même chose :

| Flag | Comportement si `uv.lock` ne correspond plus à `pyproject.toml` |
| --- | --- |
| `--frozen` | installe le lock **sans le vérifier** — une dépendance ajoutée à `pyproject.toml` est silencieusement ignorée |
| `--locked` | **échoue** (code 2) |

C'est `--locked` qu'il faut ici : ajouter une dépendance sans relancer `uv lock`
produit une erreur de build franche, au lieu d'une image à laquelle il manque un
paquet et qui ne cassera qu'à l'exécution.

### Le verrouillage des versions

`uv.lock` fige les **42 paquets** de l'arbre de dépendances, y compris les transitifs
que `pyproject.toml` ne nomme pas (`sqlalchemy`, `werkzeug`, `jinja2`…). Sans lui,
deux builds à quinze jours d'écart pouvaient produire des images différentes, puisque
`lxml`, `rdflib`, `requests` et `gunicorn` ne sont pas épinglés dans `pyproject.toml`.

Il épingle aussi **`sat-biblio-referencement` à un commit précis** (`0c29ee2`), là où
la référence `git+https://…` sans `@rev` suivait le HEAD de la branche par défaut :
un push sur ce dépôt modifiait l'image sans que rien ne change ici.

Les deux dépendances Git sont des références directes PEP 508, **non éditables** :
elles atterrissent normalement dans `site-packages` et suivent donc le venv sans
manipulation particulière.

### Mettre à jour les dépendances

```bash
uv lock              # après avoir modifié pyproject.toml
uv lock --upgrade    # remonter les versions dans les bornes de pyproject.toml
```

`uv.lock` est committé : c'est lui qui rend les builds reproductibles.

---

## Étape 2 — exécution

```dockerfile
FROM python:3.11-slim-bookworm
```

On repart d'une base propre : rien de l'étape `builder` n'est présent, sauf ce que
l'on copie explicitement.

```dockerfile
LABEL org.opencontainers.image.authors="Clément Besnier" \
      org.opencontainers.image.title="sat-biblio-server" \
      org.opencontainers.image.description="Flask backend for the Société Archéologique de Touraine library"
```

Métadonnées standard OCI, visibles via `docker inspect`.

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*
```

`curl` est présent uniquement pour le `HEALTHCHECK` défini plus bas.

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app" \
    FLASK_ENV=production \
    DATA_DIR="/app/data" \
    UPLOAD_DIR="/app/uploads" \
    PATH="/opt/venv/bin:$PATH"
```

| Variable | Rôle |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE` | pas de `.pyc` — inutiles et non inscriptibles pour l'utilisateur non-root |
| `PYTHONUNBUFFERED` | sorties non tamponnées, pour que les logs arrivent en temps réel dans `docker logs` |
| `PYTHONPATH=/app` | rend le paquet `sat_biblio_server` importable depuis la racine |
| `FLASK_ENV=production` | sélectionne la configuration de production |
| `DATA_DIR` / `UPLOAD_DIR` | emplacements des données persistantes (cf. `VOLUME`) |
| `PATH` | à nouveau le venv en tête : `gunicorn`, `flask`, `python` viennent de `/opt/venv` |

```dockerfile
WORKDIR /app

RUN useradd -m -u 1000 satbiblio && \
    mkdir -p /app/data /app/uploads && \
    chown -R satbiblio:satbiblio /app/data /app/uploads
```

Création d'un utilisateur non privilégié (UID 1000, celui du premier utilisateur sur
la plupart des hôtes Linux — pratique pour les droits sur les volumes montés) et des
deux répertoires persistants, dont il devient propriétaire.

```dockerfile
COPY --from=builder --chown=satbiblio:satbiblio /opt/venv /opt/venv
COPY --chown=satbiblio:satbiblio . .
```

Le venv complet est récupéré depuis l'étape `builder`, puis le code applicatif est
copié. Le `--chown` au moment de la copie évite un
`RUN chown -R` supplémentaire, qui dupliquerait tous les fichiers dans une nouvelle
couche.

```dockerfile
USER satbiblio
```

Tout ce qui suit — et surtout le processus applicatif — s'exécute sans les droits root.

```dockerfile
EXPOSE 8080
VOLUME ["/app/data", "/app/uploads"]
```

`EXPOSE` est purement documentaire (il faut toujours un `-p` au `docker run`).
`VOLUME` déclare les deux répertoires comme persistants : bases SQLite et fichiers
téléversés survivent ainsi au remplacement du conteneur.

```dockerfile
CMD ["gunicorn", "--conf", "sat_biblio_server/gunicorn_conf.py", \
     "--bind", "0.0.0.0:8080", "app_server:app"]
```

Le serveur d'application est Gunicorn (et non le serveur de développement Flask).
La configuration `sat_biblio_server/gunicorn_conf.py` envoie les logs d'accès sur
stdout et les erreurs sur stderr — la convention attendue par Docker — et fixe
3 threads, un timeout de 120 s et `worker_tmp_dir = /dev/shm`. L'écoute sur
`0.0.0.0` (et non `127.0.0.1`) est nécessaire pour que le port soit joignable depuis
l'extérieur du conteneur.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD curl -f -H "Host: api.satbiblio.clementbesnier.eu" http://localhost:8080/health || exit 1
```

Vérification de vivacité toutes les 30 s, avec 20 s de grâce au démarrage et 3 échecs
consécutifs avant de marquer le conteneur `unhealthy`.

⚠️ **L'en-tête `Host` n'est pas décoratif.** La configuration de production définit
`SERVER_NAME` ; Flask ne fait alors correspondre que les requêtes dont l'en-tête `Host`
lui est égal. Une sonde vers `localhost` sans ce `-H` recevrait un 404 sur toutes les
routes et le conteneur serait déclaré en échec alors qu'il fonctionne. La même
précaution s'applique à tout `curl` de diagnostic lancé contre l'instance de
production.

`SERVER_NAME` est surchargeable par variable d'environnement, avec la valeur de
production par défaut. Passer `SERVER_NAME=` (vide) donne `None` et désactive ce
filtrage — c'est ce que fait `docker-compose.yml` pour rendre l'API joignable sur
`http://localhost:5000/`. `CORS_ORIGINS` fonctionne de la même manière.

---

## Construire et lancer

```bash
docker build -t sat-biblio-server .

docker run -d --name sat-biblio \
  -p 8080:8080 \
  -v sat-biblio-data:/app/data \
  -v sat-biblio-uploads:/app/uploads \
  sat-biblio-server
```

Les fichiers de secrets (`email_address`, `mail_password`, `secret_key`,
`jwt_secret_key`) sont lus dans `sat_biblio_server/config/` à l'import. Ils sont donc
inclus par le `COPY . .` s'ils sont présents dans le contexte de build — à monter
plutôt qu'à embarquer dans l'image si celle-ci doit être publiée.
