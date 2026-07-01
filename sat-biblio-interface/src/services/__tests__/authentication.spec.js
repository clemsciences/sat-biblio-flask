import { describe, it, expect } from 'vitest'
import { isValidJwt } from '../authentication.js'

function makeJwt(expOffsetSeconds) {
  const exp = Math.floor(Date.now() / 1000) + expOffsetSeconds
  const payload = btoa(JSON.stringify({ exp }))
  return `header.${payload}.signature`
}

describe('isValidJwt', () => {
  it('retourne false pour une valeur null', () => {
    expect(isValidJwt(null)).toBe(false)
  })

  it('retourne false pour une chaîne vide', () => {
    expect(isValidJwt('')).toBe(false)
  })

  it('retourne false si le JWT a moins de 3 segments', () => {
    expect(isValidJwt('header.payload')).toBe(false)
  })

  it('retourne false pour un JWT expiré', () => {
    const expired = makeJwt(-3600) // expiré il y a 1h
    expect(isValidJwt(expired)).toBe(false)
  })

  it('retourne true pour un JWT valide non expiré', () => {
    const valid = makeJwt(3600) // expire dans 1h
    expect(isValidJwt(valid)).toBe(true)
  })

  it('retourne false pour un JWT expirant exactement maintenant', () => {
    // exp = now → now < exp est false
    const almostExpired = makeJwt(0)
    expect(isValidJwt(almostExpired)).toBe(false)
  })
})
