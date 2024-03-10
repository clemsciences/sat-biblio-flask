<template>
  <b-container>
    <b-navbar toggleable="md" class="navbar-default fixed-top navbar-dark sat-color-nav" pills>
      <b-navbar-brand to="/" id="accueil-tooltip">
        <h1>SAT - Biblio</h1>
        <b-tooltip target="accueil-tooltip" triggers="hover" class="my-tooltip">
              Accueil
        </b-tooltip>
      </b-navbar-brand>
      <b-navbar-toggle target="navbarSupportedContent"></b-navbar-toggle>
      <b-collapse is-nav style="height: 1px;" id="navbarSupportedContent">
        <b-navbar-nav>
<!--          <b-nav-item to="/" class="nav-link space-around titre-nav-item">Accueil</b-nav-item>-->
          <b-nav-item v-if="connected && isContributor">
            <b-nav-item-dropdown text="Créer" class="titre-nav-item">
              <b-dropdown-item to="/auteur/creer">Auteur</b-dropdown-item>
              <b-dropdown-item to="/reference-livre/creer">Référence bibliographique</b-dropdown-item>
              <b-dropdown-item to="/enregistrement/creer">Enregistrement dans le catalogue</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-nav-item>
          <b-nav-item class="active" active>
            <b-nav-item-dropdown text="Consulter" class="titre-nav-item">
              <b-dropdown-item to="/auteur/liste">Auteurs</b-dropdown-item>
              <b-dropdown-item to="/reference-livre/liste">Références bibliographiques</b-dropdown-item>
              <b-dropdown-item to="/enregistrement/liste">Catalogue</b-dropdown-item>
<!--                    <router-link class="nav-link" to="/enregistrement/liste">Catalogue</router-link>-->
            </b-nav-item-dropdown>
          </b-nav-item>
<!--          <b-nav-item class="active nav-link space-around titre-nav-item" to="/rechercher">Rechercher</b-nav-item>-->
          <b-nav-item v-if="isManager">
            <b-nav-item-dropdown text="Autres" class="titre-nav-item">
              <b-dropdown-group v-if="isManager" id="group-borrowing" header="Emprunter" class="my-nav-group">
                <b-dropdown-item to="/emprunt/livre">Nouvel emprunt</b-dropdown-item>
                <b-dropdown-item to="/emprunt/liste">Livres empruntés</b-dropdown-item>
                <b-dropdown-item to="/gestionnaire">Gestionnaire</b-dropdown-item>
                <b-dropdown-item v-if="isAdmin" to="/evenements">Logs</b-dropdown-item>
                <b-dropdown-item v-if="isAdmin" to="/dublin-core">Dublin Core</b-dropdown-item>
              </b-dropdown-group>
              <b-dropdown-group v-if="isEditor" id="group-editor" header="Editeur">
                <b-dropdown-item to="/exporter">Exporter</b-dropdown-item>
                <b-dropdown-item to="/rechercher/bulletins">Recherche bulletin</b-dropdown-item>
              </b-dropdown-group>
              <b-dropdown-group v-if="isAdmin" id="group-admin" header="Admin" class="my-nav-group">
                <b-dropdown-item to="/administrateur">Admin</b-dropdown-item>
<!--                <b-dropdown-item to="/gestionnaire-importation">Gestionnaire d'importation</b-dropdown-item>-->
              </b-dropdown-group>
            </b-nav-item-dropdown>
          </b-nav-item>

          <b-nav-item to="/contact" class="nav-link space-around titre-nav-item">Contact</b-nav-item>

          <b-nav-item class="active" active>
            <b-nav-item-dropdown text="Liens" class="titre-nav-item">
              <b-dropdown-item @click="goToMainSite" id="sat-website-tooltip">
                Le site de la SAT
                <b-tooltip target="sat-website-tooltip" triggers="hover" class="my-tooltip">
                  Allez sur le site internet de la Société Archéologique de Touraine
                </b-tooltip>
              </b-dropdown-item>
              <b-dropdown-item @click="goToGallicaSAT" id="sat-gallica-tooltip">
                Les bulletins de la SAT sur Gallica
                <b-tooltip target="sat-gallica-tooltip" triggers="hover" class="my-tooltip">
                  Allez sur Gallica pour voir les bulletins de la Société Archéologique de Touraine
                </b-tooltip>
              </b-dropdown-item>
              <b-dropdown-item @click="getSatBiblioDoc" id="doc-sat-biblio-tooltip">
                La documentation de SAT-Biblio
                <b-tooltip target="doc-sat-biblio-tooltip" triggers="hover" class="my-tooltip">La documentation de ce site internet</b-tooltip>
              </b-dropdown-item>
            </b-nav-item-dropdown>
          </b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item id="connection-tooltip" class="nav-link space-around titre-nav-item ml-auto">
            <!-- v-b-tooltip.hover.bottomleft="connectionTooltipHints" -->
            <b-nav-item-dropdown v-if="connected" text="Mon profil" class="titre-nav-item">
              <b-dropdown-item to="/utilisateur/reinitialiser-mot-de-passe">
                Changer <br/> de mot de passe
              </b-dropdown-item>
              <b-dropdown-item to="/utilisateur/deconnexion">Se déconnecter</b-dropdown-item>
            </b-nav-item-dropdown>
            <b-nav-item-dropdown v-else text="Connexion" class="titre-nav-item">
              <b-dropdown-item :to="{name: 'utilisateur-connexion'}">
                Se connecter
              </b-dropdown-item>
              <b-dropdown-item to="/utilisateur/creer">
                Nouveau compte
              </b-dropdown-item>
            </b-nav-item-dropdown>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </b-container>

</template>

<script>

import {mapState} from "vuex";
import {canContribute, canEdit, canManage, getRightString, isAdmin} from "@/services/rights";

export default {
  name: "NavBar",
  computed: {
    ...mapState(["connected", "connectionInfo"]),
    isAdmin: function () {
      return isAdmin(this.connectionInfo.right);
    },
    isManager: function () {
      return canManage(this.connectionInfo.right);
    },
    isEditor: function () {
      return canEdit(this.connectionInfo.right);
    },
    isContributor: function () {
      return canContribute(this.connectionInfo.right);
    },
    connectionTooltipHints: function () {
      return `${this.connectionInfo.first_name} ${this.connectionInfo.family_name} - ${this.connectionInfo.email}
      ${getRightString(this.connectionInfo.right)}`
    },
    connectionLabel: function() {
      if(!this.connected) {
        return "Se connecter";
      } else {
        return "Se déconnecter";
      }
    },
  },
  methods: {
    goToGallicaSAT: function() {
      window.open('https://gallica.bnf.fr/ark:/12148/cb34429572f/date.item','_blank');
    },
    goToMainSite() {
      window.open('https://www.societearcheotouraine.eu/','_blank');
    },
    getSatBiblioDoc() {
      window.open(`${process.env.VUE_APP_SITE_API_URL}/static/sat_biblio_documentation-1.pdf`, '_blank');
    }
  }

}
</script>

<style scoped>

h1 {
  font-size: 2rem;

}
.sat-color-nav {
  background-color: #6cb0f3;
}
/*b-nav-item-dropdown
{
  background-color: #6cb0f3;
}*/

.titre-nav-item {
  font-size: 1.5rem;
}

.my-nav-group {
  background-color: white;
}

.my-tooltip {
  text-justify: auto;
}



</style>