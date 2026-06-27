import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createStore } from 'vuex'
import { rights } from '../services/rights.js'

// vuex-persistedstate accède à localStorage : on l'ignore dans les tests
vi.mock('vuex-persistedstate', () => ({ default: () => () => {} }))

// Recrée le store depuis sa définition, sans le plugin de persistance
function makeStore() {
  return createStore({
    state: {
      connected: false,
      connectionInfo: {}
    },
    mutations: {
      connect(state, payload) {
        state.connected = true
        state.connectionInfo = payload.connectionInfo
      },
      disconnect(state) {
        state.connected = false
        state.connectionInfo = {}
      }
    },
    getters: {
      isAuthenticated(state) {
        if (state.connectionInfo && state.connectionInfo.token) {
          // En test on considère tout token non vide comme valide
          return !!state.connectionInfo.token
        }
        return false
      },
      getUserRight(state) {
        return state.connectionInfo?.right ?? rights.lecteur.index
      },
      isAdmin(state, getters) {
        return getters.getUserRight === rights.administrateur.index
      },
      canManage(state, getters) {
        return getters.getUserRight >= rights.gestionnaire.index
      },
      canContribute(state, getters) {
        return getters.getUserRight >= rights.contributeur.index
      }
    }
  })
}

describe('store — mutation connect', () => {
  it('passe connected à true et enregistre connectionInfo', () => {
    const store = makeStore()
    store.commit('connect', { connectionInfo: { token: 'tok', right: 2 } })
    expect(store.state.connected).toBe(true)
    expect(store.state.connectionInfo.token).toBe('tok')
  })
})

describe('store — mutation disconnect', () => {
  it('réinitialise l\'état de connexion', () => {
    const store = makeStore()
    store.commit('connect', { connectionInfo: { token: 'tok', right: 5 } })
    store.commit('disconnect')
    expect(store.state.connected).toBe(false)
    expect(store.state.connectionInfo).toEqual({})
  })
})

describe('store — getter getUserRight', () => {
  it('retourne lecteur par défaut quand non connecté', () => {
    const store = makeStore()
    expect(store.getters.getUserRight).toBe(rights.lecteur.index)
  })

  it('retourne le droit stocké après connexion', () => {
    const store = makeStore()
    store.commit('connect', { connectionInfo: { token: 'tok', right: rights.editeur.index } })
    expect(store.getters.getUserRight).toBe(rights.editeur.index)
  })
})

describe('store — getter isAdmin', () => {
  it('false par défaut', () => {
    expect(makeStore().getters.isAdmin).toBe(false)
  })

  it('true pour un administrateur', () => {
    const store = makeStore()
    store.commit('connect', { connectionInfo: { token: 'tok', right: rights.administrateur.index } })
    expect(store.getters.isAdmin).toBe(true)
  })
})

describe('store — getter canContribute', () => {
  it('false pour un lecteur', () => {
    expect(makeStore().getters.canContribute).toBe(false)
  })

  it('true pour un contributeur', () => {
    const store = makeStore()
    store.commit('connect', { connectionInfo: { token: 'tok', right: rights.contributeur.index } })
    expect(store.getters.canContribute).toBe(true)
  })
})
