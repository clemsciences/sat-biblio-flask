import { test, expect } from '@playwright/test'

test.describe('Navigation publique (sans connexion)', () => {
  test('la page d\'accueil se charge', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/sat|biblio/i)
  })

  test('la liste des enregistrements est accessible', async ({ page }) => {
    await page.goto('/enregistrement/liste')
    // Au moins un tableau ou message de contenu doit être présent
    await expect(page.locator('table, [role="table"], .liste, main')).toBeVisible()
  })

  test('la liste des auteurs est accessible', async ({ page }) => {
    await page.goto('/auteur/liste')
    await expect(page.locator('table, [role="table"], .liste, main')).toBeVisible()
  })

  test('la page de connexion s\'affiche', async ({ page }) => {
    await page.goto('/utilisateur/connexion')
    await expect(page.locator('input[type="email"], input[type="text"]')).toBeVisible()
    await expect(page.locator('input[type="password"]')).toBeVisible()
  })

  test('une route protégée redirige vers la connexion', async ({ page }) => {
    await page.goto('/administrateur')
    await expect(page).toHaveURL(/connexion/)
  })
})

test.describe('Flux de connexion', () => {
  test('connexion avec des identifiants invalides affiche une erreur', async ({ page }) => {
    await page.goto('/utilisateur/connexion')
    await page.locator('input[type="email"], input[type="text"]').first().fill('inconnu@example.com')
    await page.locator('input[type="password"]').fill('mauvais-mot-de-passe')
    await page.locator('button[type="submit"], button:has-text("Connexion"), button:has-text("Se connecter")').click()
    // L'appli doit rester sur la page de connexion ou afficher une erreur
    await expect(page).toHaveURL(/connexion/)
  })
})
