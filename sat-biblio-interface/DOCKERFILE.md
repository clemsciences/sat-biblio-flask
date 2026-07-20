# Le Dockerfile du frontend expliqué

Ce document décrit le `Dockerfile` qui construit l'image du frontend Vue 3 de
sat-biblio. Pour le backend Flask, voir `../DOCKERFILE.md`.

Comme celui du backend, il s'agit d'une **construction multi-étapes** — mais la
logique est différente : ici la première étape produit des **fichiers statiques**, et
l'image finale ne contient pas du tout Node. C'est un serveur nginx qui sert un
répertoire de HTML/JS/CSS. Node, npm et les ~700 Mo de `node_modules` restent dans
l'étape de build.

---

## Étape 1 — `build-stage`

```dockerfile
FROM node:20-alpine AS build-stage
WORKDIR /app
```

Node 20 sur base Alpine (image de quelques dizaines de Mo au lieu de ~1 Go pour la
variante Debian complète).

```dockerfile
COPY package*.json ./
RUN npm ci
```

Le motif `package*.json` capture **`package.json` et `package-lock.json`**. Les deux
sont nécessaires : `npm ci` (contrairement à `npm install`) exige le *lockfile*, échoue
s'il est absent ou désynchronisé, et installe exactement les versions qui y figurent.
C'est ce qui rend le build reproductible.

À noter : le `.dockerignore` **ne masque volontairement pas** `package-lock.json` — un
commentaire y rappelle explicitement pourquoi. L'ignorer casserait `npm ci`.

Comme pour le backend, ne copier que les manifestes à ce stade préserve le cache
Docker : tant que les dépendances ne bougent pas, l'installation n'est pas rejouée,
même si le code source a changé.

```dockerfile
COPY . .

ARG VITE_APP_SITE_API_URL

RUN npm run build
```

Le code est copié, puis `vite build --outDir satbiblio-dist` (cf. `package.json`)
produit le bundle de production.

### L'URL de l'API : `ARG` nu, et surtout pas `ENV`

Vite **fige** les variables `VITE_*` dans le bundle au moment du build — ce ne sont pas
des variables lues à l'exécution. L'URL de l'API est donc gravée dans le JavaScript
livré, et la changer impose de reconstruire l'image.

Deux sources possibles pour cette valeur :

1. le fichier `.env.production` du dépôt, qui contient
   `VITE_APP_SITE_API_URL="https://api.satbiblio.clementbesnier.eu"` (il est copié dans
   l'image par le `COPY . .`, le `.dockerignore` ne l'exclut pas) ;
2. un `--build-arg`, qui l'emporte sur le premier.

| Build | URL gravée dans le bundle |
| --- | --- |
| `docker build .` | `https://api.satbiblio.clementbesnier.eu` (depuis `.env.production`) |
| `docker build --build-arg VITE_APP_SITE_API_URL=https://recette.exemple.fr .` | `https://recette.exemple.fr` |

⚠️ **Ne jamais rajouter `ENV VITE_APP_SITE_API_URL=$VITE_APP_SITE_API_URL`**, comme
c'était le cas auparavant. Un `ARG` sans valeur par défaut vaut la chaîne vide, et
`ENV` définit alors bel et bien la variable — **à vide**. Or Vite donne priorité aux
variables d'environnement réelles sur les fichiers `.env` : un build sans
`--build-arg` gravait donc une URL d'API vide, et `.env.production` était ignoré.

Le symptôme n'était pas une erreur réseau franche : le frontend émettait ses appels
vers des chemins relatifs, donc vers nginx lui-même, qui renvoie `index.html` pour
toute route inconnue (cf. `try_files`). On recevait du HTML là où du JSON était
attendu.

Un `ARG` **nu** est simplement absent de l'environnement quand il n'est pas passé,
ce qui laisse le repli sur `.env.production` fonctionner.

---

## Étape 2 — `production-stage`

```dockerfile
FROM nginx:stable-alpine AS production-stage
RUN apk add --no-cache curl
```

`curl` sert uniquement au `HEALTHCHECK`. `--no-cache` évite d'écrire l'index des
paquets APK dans la couche (l'équivalent Alpine du `rm -rf /var/lib/apt/lists/*` côté
Debian).

```dockerfile
RUN addgroup -S satbiblio && adduser -S satbiblio -G satbiblio
```

Utilisateur et groupe **système** (`-S`, syntaxe BusyBox), sans mot de passe ni home.
Contrairement au backend, aucun UID n'est imposé : l'image ne monte pas de volume, la
correspondance d'UID avec l'hôte n'a donc pas d'importance ici.

```dockerfile
COPY --from=build-stage /app/satbiblio-dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

Seul le résultat du build traverse la frontière entre les deux étapes. Le nom
`satbiblio-dist` n'est pas celui par défaut de Vite (`dist`) : il vient du
`--outDir satbiblio-dist` du script `build`. Les deux doivent rester cohérents — c'est
l'objet du commentaire dans le Dockerfile.

```dockerfile
RUN chown -R satbiblio:satbiblio /usr/share/nginx/html /var/cache/nginx /var/log/nginx
RUN sed -i 's|^pid .*;|pid /tmp/nginx.pid;|' /etc/nginx/nginx.conf && \
    grep -q '^pid /tmp/nginx.pid;' /etc/nginx/nginx.conf
USER satbiblio
```

Ces trois lignes forment un tout : faire tourner nginx **sans les droits root**.
L'image officielle suppose un démarrage en root (le master écrit son PID, ouvre les
logs, gère le cache). Il faut donc céder les répertoires concernés à l'utilisateur,
**et** déplacer le fichier PID vers `/tmp`, seul endroit sûrement inscriptible.

Deux pièges, tous deux rencontrés pour de vrai — l'image ne démarrait pas du tout
avant correction :

- **La substitution doit viser la directive `pid`, pas un chemin en dur.** L'image
  `nginx:stable-alpine` déclare `pid /run/nginx.pid;`. Un `sed` sur
  `/var/run/nginx.pid` ne correspond à rien, ne signale aucune erreur, et nginx meurt
  au démarrage sur `[emerg] open() "/run/nginx.pid" failed (13: Permission denied)`.
  Le `grep -q` qui suit sert de garde-fou : si l'image amont change encore la
  directive, le build échoue bruyamment au lieu de produire une image cassée.
- **`/var/run` ne doit pas figurer dans le `chown`.** C'est un lien symbolique vers
  `../run` ; `chown -R` modifie le lien lui-même sans descendre dedans, `/run` reste
  donc la propriété de root. Le déplacement du PID vers `/tmp` rend de toute façon ce
  `chown` inutile.

```dockerfile
EXPOSE 8080
```

Le port 8080 — et non 80 — n'est pas un détail esthétique : un processus non-root ne
peut pas se lier à un port privilégié (< 1024). `nginx.conf` écoute donc bien sur 8080.

⚠️ Le backend expose **également** 8080. Les deux conteneurs ne peuvent pas être
publiés sur le même port de l'hôte ; il faut décaler l'un des deux
(`-p 8081:8080`) ou les placer derrière un reverse proxy.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/ || exit 1
```

Bien plus simple que celui du backend : nginx sert des fichiers statiques et n'a pas de
`SERVER_NAME` qui filtrerait sur l'en-tête `Host`, donc aucun `-H "Host: …"` n'est
nécessaire. Il n'y a pas non plus de `--start-period` : nginx démarre en quelques
dizaines de millisecondes.

```dockerfile
CMD ["nginx", "-g", "daemon off;"]
```

`daemon off;` maintient nginx au premier plan. Un conteneur s'arrête dès que son
processus principal se termine ; si nginx se plaçait en arrière-plan, le conteneur
sortirait immédiatement.

---

## Ce que fait `nginx.conf`

- **`try_files $uri $uri/ /index.html`** — indispensable à une SPA. Vue Router gère les
  URL côté client ; sans cette directive, un accès direct à `/catalogue` ou un simple
  F5 renverrait 404, puisqu'aucun fichier ne porte ce nom sur le disque.
- **`expires 1y`** sur les fichiers statiques — sans danger parce que Vite ajoute une
  empreinte au nom des fichiers générés : un nouveau build produit de nouveaux noms.
  `index.html` n'est délibérément pas concerné par la règle, c'est lui qui référence les
  bundles à jour.
- **En-têtes de sécurité** — `X-Frame-Options`, `X-Content-Type-Options`, etc.

À signaler : la `Content-Security-Policy` y est très permissive
(`'unsafe-inline' 'unsafe-eval'`, et `http:` autorisé). Elle n'apporte à peu près
aucune protection contre le XSS en l'état. La resserrer est possible mais demande de
vérifier ce dont BootstrapVueNext et Leaflet ont besoin — ce n'est pas un simple
ajustement de configuration.

---

## Construire et lancer

Pour la production, `.env.production` fait foi — aucun argument n'est nécessaire :

```bash
cd sat-biblio-interface

docker build -t sat-biblio-interface .
docker run -d --name sat-biblio-front -p 8081:8080 sat-biblio-interface
```

Pour pointer vers une autre API (recette, instance locale) :

```bash
docker build -t sat-biblio-interface:recette \
  --build-arg VITE_APP_SITE_API_URL=https://recette.exemple.fr .
```

Le port de l'hôte est décalé à 8081 parce que le backend expose lui aussi 8080.

Rappel : l'URL de l'API étant compilée dans le bundle, une même image ne peut pas
servir à la fois la recette et la production. Il faut une image par environnement.
