# Tests — sat-biblio-interface

## Prérequis

- Node.js installé, dépendances à jour (`npm install`)
- Pour les tests E2E : le backend Flask doit tourner sur `http://localhost:5000`

---

## Tests unitaires (Vitest)

Couvrent les services purs et le store Vuex, sans navigateur ni backend.

| Fichier | Ce qui est testé |
|---|---|
| `src/services/__tests__/authentication.spec.js` | `isValidJwt` — validité et expiration du JWT |
| `src/services/__tests__/rights.spec.js` | `canContribute`, `canEdit`, `canManage`, `isAdmin`, `getRightString` |
| `src/__tests__/store.spec.js` | Mutations `connect`/`disconnect`, getters `getUserRight`, `isAdmin`, `canContribute` |

### Commandes

```bash
# Mode watch (relance à chaque sauvegarde)
npm run test

# Exécution unique
npm run test:run

# Rapport de couverture
npm run test:coverage
```

---

## Tests E2E (Playwright)

Pilotent un vrai navigateur Chromium contre l'application. Le serveur Vite est démarré automatiquement par Playwright si aucune instance ne tourne déjà.

Les tests sont dans `e2e/navigation.spec.js` et vérifient :
- Chargement de la page d'accueil
- Accessibilité des listes publiques (enregistrements, auteurs)
- Affichage de la page de connexion
- Redirection vers `/connexion` depuis une route protégée
- Comportement à la connexion avec des identifiants invalides

### Commandes

```bash
# Lancer tous les tests E2E
npm run test:e2e

# Un seul fichier
npx playwright test e2e/navigation.spec.js

# Mode UI — timeline, snapshots DOM, logs réseau
npx playwright test --ui

# Voir le navigateur s'exécuter
npx playwright test --headed

# Déboguer pas à pas (Playwright Inspector)
npx playwright test e2e/navigation.spec.js --debug

# Générer un test depuis le navigateur
npx playwright codegen http://localhost:5173
```

### Artefacts en cas d'échec

Playwright enregistre automatiquement une capture d'écran et une vidéo dans `test-results/` quand un test échoue.
