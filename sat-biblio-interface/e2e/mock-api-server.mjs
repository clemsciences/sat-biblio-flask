// Serveur d'API factice pour les tests end-to-end.
//
// Il ne dépend d'aucun paquet (module `http` natif) et se contente de renvoyer
// des réponses au format attendu par le front (`json_result` côté Flask :
// { success, message, ...data }). Objectif : permettre à l'appli Vue de se
// charger et aux parcours publics de tourner en CI sans backend ni base de
// données réels.
//
// Playwright le démarre automatiquement (voir `playwright.config.js`).

import http from 'node:http'

const PORT = Number(process.env.MOCK_API_PORT || 5000)

// En-têtes CORS. Le front appelle l'API avec `withCredentials: true`, donc
// l'origine doit être renvoyée explicitement (jamais `*` avec des credentials)
// et `Access-Control-Allow-Credentials` doit valoir `true`.
function corsHeaders(req) {
  return {
    'Access-Control-Allow-Origin': req.headers.origin || 'http://localhost:5173',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
    'Access-Control-Allow-Headers':
      'Content-Type, Authorization, X-CSRF-TOKEN-ACCESS, X-CSRF-TOKEN-REFRESH',
  }
}

function send(res, req, status, body) {
  res.writeHead(status, {
    'Content-Type': 'application/json',
    ...corsHeaders(req),
  })
  res.end(JSON.stringify(body))
}

const server = http.createServer((req, res) => {
  const { method } = req
  const path = new URL(req.url, `http://localhost:${PORT}`).pathname

  // Préflight CORS.
  if (method === 'OPTIONS') {
    res.writeHead(204, corsHeaders(req))
    res.end()
    return
  }

  // Endpoint de santé : sert de sonde de disponibilité pour Playwright.
  if (path === '/' || path === '/health') {
    send(res, req, 200, { success: true, message: 'mock-api ok' })
    return
  }

  // Connexion / vérification de session : on refuse toujours, ce qui laisse
  // l'utilisateur sur la page de connexion (comportement testé en e2e).
  if (path === '/users/connect/' || path === '/users/check_login/') {
    send(res, req, 401, { success: false, message: 'Identifiants invalides' })
    return
  }

  // Endpoints de comptage : renvoient 0.
  if (path.includes('/count')) {
    send(res, req, 200, { success: true, message: '', count: 0, total: 0 })
    return
  }

  // Par défaut (listes GET, etc.) : réponse vide mais valide. On expose
  // plusieurs clés possibles pour couvrir les différents composants de liste.
  if (method === 'GET') {
    send(res, req, 200, {
      success: true,
      message: '',
      data: [],
      records: [],
      authors: [],
      references: [],
      total: 0,
      count: 0,
      pages: 0,
    })
    return
  }

  // Toute autre requête (POST/PUT/DELETE) : succès neutre.
  send(res, req, 200, { success: true, message: '' })
})

server.listen(PORT, () => {
  // eslint-disable-next-line no-console
  console.log(`Mock API server en écoute sur http://localhost:${PORT}`)
})
