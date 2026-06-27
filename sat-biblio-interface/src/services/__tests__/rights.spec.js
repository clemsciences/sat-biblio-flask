import { describe, it, expect } from 'vitest'
import { rights, canContribute, canEdit, canManage, isAdmin, getRightString } from '../rights.js'

describe('rights — indexs', () => {
  it('les droits sont ordonnés de 1 à 5', () => {
    expect(rights.lecteur.index).toBe(1)
    expect(rights.contributeur.index).toBe(2)
    expect(rights.editeur.index).toBe(3)
    expect(rights.gestionnaire.index).toBe(4)
    expect(rights.administrateur.index).toBe(5)
  })
})

describe('canContribute (index >= 2)', () => {
  it('lecteur ne peut pas contribuer', () => {
    expect(canContribute(rights.lecteur.index)).toBe(false)
  })
  it('contributeur peut contribuer', () => {
    expect(canContribute(rights.contributeur.index)).toBe(true)
  })
  it('administrateur peut contribuer', () => {
    expect(canContribute(rights.administrateur.index)).toBe(true)
  })
})

describe('canEdit (index >= 3)', () => {
  it('contributeur ne peut pas éditer', () => {
    expect(canEdit(rights.contributeur.index)).toBe(false)
  })
  it('éditeur peut éditer', () => {
    expect(canEdit(rights.editeur.index)).toBe(true)
  })
  it('administrateur peut éditer', () => {
    expect(canEdit(rights.administrateur.index)).toBe(true)
  })
})

describe('canManage (index >= 4)', () => {
  it('éditeur ne peut pas gérer', () => {
    expect(canManage(rights.editeur.index)).toBe(false)
  })
  it('gestionnaire peut gérer', () => {
    expect(canManage(rights.gestionnaire.index)).toBe(true)
  })
})

describe('isAdmin (index >= 5)', () => {
  it('gestionnaire n\'est pas admin', () => {
    expect(isAdmin(rights.gestionnaire.index)).toBe(false)
  })
  it('administrateur est admin', () => {
    expect(isAdmin(rights.administrateur.index)).toBe(true)
  })
})

describe('getRightString', () => {
  it('retourne la chaîne correspondant à l\'index', () => {
    expect(getRightString(rights.lecteur.index)).toBe('lecteur')
    expect(getRightString(rights.editeur.index)).toBe('éditeur')
    expect(getRightString(rights.administrateur.index)).toBe('administrateur')
  })
})
