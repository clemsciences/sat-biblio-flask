# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: navigation.spec.js >> Flux de connexion >> connexion avec des identifiants invalides affiche une erreur
- Location: e2e/navigation.spec.js:33:7

# Error details

```
Error: locator.click: Error: strict mode violation: locator('button[type="submit"], button:has-text("Connexion"), button:has-text("Se connecter")') resolved to 2 elements:
    1) <button type="button" aria-haspopup="menu" aria-expanded="false" id="BootstrapVueNext__ID__v-4__dropdown___" class="btn btn-md btn-link nav-link dropdown-toggle">Connexion</button> aka getByRole('button', { name: 'Connexion' })
    2) <button type="submit" class="btn btn-md btn-secondary">Se connecter</button> aka getByRole('button', { name: 'Se connecter' })

Call log:
  - waiting for locator('button[type="submit"], button:has-text("Connexion"), button:has-text("Se connecter")')

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - navigation [ref=e4]:
    - generic [ref=e5]:
      - link "SAT - Biblio" [ref=e6] [cursor=pointer]:
        - /url: /
        - heading "SAT - Biblio" [level=1] [ref=e7]
      - generic [ref=e8]:
        - list [ref=e9]:
          - listitem [ref=e10]:
            - link "Consulter" [ref=e11] [cursor=pointer]:
              - /url: "#"
              - listitem [ref=e12]:
                - button "Consulter" [ref=e14]
          - listitem [ref=e15]:
            - link "Contact" [ref=e16] [cursor=pointer]:
              - /url: /contact
          - listitem [ref=e17]:
            - link "Divers" [ref=e18] [cursor=pointer]:
              - /url: "#"
              - listitem [ref=e19]:
                - button "Divers" [ref=e21]
        - list [ref=e22]:
          - listitem [ref=e23]:
            - link "Connexion" [ref=e24] [cursor=pointer]:
              - /url: "#"
              - listitem [ref=e25]:
                - button "Connexion" [ref=e27]
  - generic [ref=e28]:
    - generic [ref=e29]:
      - heading "Se connecter" [level=2] [ref=e31]
      - button "Info" [ref=e34] [cursor=pointer]:
        - img [ref=e35]: 
        - text: Info
    - generic [ref=e38]:
      - group [ref=e39]:
        - generic [ref=e40]: Adresse email
        - textbox "Adresse email" [ref=e41]: inconnu@example.com
      - group [ref=e42]:
        - generic [ref=e43]: Mot de passe
        - generic [ref=e44]:
          - textbox "Mot de passe" [active] [ref=e46]: mauvais-mot-de-passe
          - button "Afficher le mot de passe" [ref=e48] [cursor=pointer]
      - button "Se connecter" [ref=e49] [cursor=pointer]
    - paragraph [ref=e50]:
      - button "Mot de passe oublié ?" [ref=e51] [cursor=pointer]
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test'
  2  | 
  3  | test.describe('Navigation publique (sans connexion)', () => {
  4  |   test('la page d\'accueil se charge', async ({ page }) => {
  5  |     await page.goto('/')
  6  |     await expect(page).toHaveTitle(/sat|biblio/i)
  7  |   })
  8  | 
  9  |   test('la liste des enregistrements est accessible', async ({ page }) => {
  10 |     await page.goto('/enregistrement/liste')
  11 |     // Au moins un tableau ou message de contenu doit être présent
  12 |     await expect(page.locator('table, [role="table"], .liste, main')).toBeVisible()
  13 |   })
  14 | 
  15 |   test('la liste des auteurs est accessible', async ({ page }) => {
  16 |     await page.goto('/auteur/liste')
  17 |     await expect(page.locator('table, [role="table"], .liste, main')).toBeVisible()
  18 |   })
  19 | 
  20 |   test('la page de connexion s\'affiche', async ({ page }) => {
  21 |     await page.goto('/utilisateur/connexion')
  22 |     await expect(page.locator('input[type="email"], input[type="text"]')).toBeVisible()
  23 |     await expect(page.locator('input[type="password"]')).toBeVisible()
  24 |   })
  25 | 
  26 |   test('une route protégée redirige vers la connexion', async ({ page }) => {
  27 |     await page.goto('/administrateur')
  28 |     await expect(page).toHaveURL(/connexion/)
  29 |   })
  30 | })
  31 | 
  32 | test.describe('Flux de connexion', () => {
  33 |   test('connexion avec des identifiants invalides affiche une erreur', async ({ page }) => {
  34 |     await page.goto('/utilisateur/connexion')
  35 |     await page.locator('input[type="email"], input[type="text"]').first().fill('inconnu@example.com')
  36 |     await page.locator('input[type="password"]').fill('mauvais-mot-de-passe')
> 37 |     await page.locator('button[type="submit"], button:has-text("Connexion"), button:has-text("Se connecter")').click()
     |                                                                                                                ^ Error: locator.click: Error: strict mode violation: locator('button[type="submit"], button:has-text("Connexion"), button:has-text("Se connecter")') resolved to 2 elements:
  38 |     // L'appli doit rester sur la page de connexion ou afficher une erreur
  39 |     await expect(page).toHaveURL(/connexion/)
  40 |   })
  41 | })
  42 | 
```