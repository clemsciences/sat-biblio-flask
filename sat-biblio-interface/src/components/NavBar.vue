<template>
  <BContainer>
    <BNavbar toggleable="md" class="navbar-default fixed-top navbar-dark sat-color-nav" pills>
      <BNavbarBrand to="/" id="accueil-tooltip">
        <h1 class="navbar-brand-title titre-nav-item" style="margin: 0; font-weight: normal; display: inline;">SAT -
          Biblio</h1>
<!--        <h1 class="navbar-brand-title titre-nav-item">SAT - Biblio</h1>-->
        <BTooltip target="accueil-tooltip" triggers="hover" class="my-tooltip">
              Accueil
        </BTooltip>
      </BNavbarBrand>
      <BNavbarToggle target="navbarSupportedContent"></BNavbarToggle>
      <BCollapse is-nav style="height: 1px;" id="navbarSupportedContent">
        <BNavbarNav>
<!--          <BNavItem to="/" class="nav-link space-around titre-nav-item">Accueil</BNavItem>-->
          <BNavItem v-if="connected && isContributor">
            <BNavItemDropdown text="Créer" class="titre-nav-item">
              <BDropdownItem to="/catalogue/creer">Nouvelle entrée</BDropdownItem>
              <BDropdownItem to="/auteur/creer" v-if="isAdmin">Auteur</BDropdownItem>
              <BDropdownItem to="/reference-livre/creer" v-if="isAdmin">Référence bibliographique</BDropdownItem>
              <BDropdownItem to="/enregistrement/creer" v-if="isAdmin">Enregistrement dans le catalogue</BDropdownItem>
            </BNavItemDropdown>
          </BNavItem>
          <BNavItem class="active" active>
            <BNavItemDropdown text="Consulter" class="titre-nav-item">
              <BDropdownItem to="/catalogue">Catalogue</BDropdownItem>
<!--              <BDropdownItem to="/cotes">Cotes</BDropdownItem>-->
              <BDropdownItem to="/mots-clefs">Mots clef</BDropdownItem>
              <BDropdownItem to="/enregistrement/liste" v-if="isAdmin">Liste des enregistrements</BDropdownItem>
              <BDropdownItem to="/auteur/liste">Auteurs</BDropdownItem>
              <BDropdownItem to="/reference-livre/liste" v-if="isAdmin">Références bibliographiques</BDropdownItem>
              <BDropdownItem to="/enregistrement/liste" v-if="isAdmin">Catalogue</BDropdownItem>
<!--                    <router-link class="nav-link" to="/enregistrement/liste">Catalogue</router-link>-->
            </BNavItemDropdown>
          </BNavItem>
<!--          <BNavItem class="active nav-link space-around titre-nav-item" to="/rechercher">Rechercher</BNavItem>-->
          <BNavItem v-if="isManager">
            <BNavItemDropdown text="Autres" class="titre-nav-item">
              <BDropdownGroup v-if="isManager" id="group-borrowing" header="Emprunter" class="my-nav-group">
                <BDropdownItem to="/emprunt/livre">Nouvel emprunt</BDropdownItem>
                <BDropdownItem to="/emprunt/liste">Livres empruntés</BDropdownItem>
                <BDropdownItem to="/gestionnaire">Gestionnaire</BDropdownItem>
                <BDropdownItem v-if="isAdmin" to="/evenements">Logs</BDropdownItem>
                <BDropdownItem v-if="isAdmin" to="/dublin-core">Dublin Core</BDropdownItem>
              </BDropdownGroup>
              <BDropdownGroup v-if="isEditor" id="group-editor" header="Editeur">
                <BDropdownItem to="/exporter">Exporter</BDropdownItem>
                <BDropdownItem to="/rechercher/bulletins">Recherche bulletin</BDropdownItem>
                <BDropdownItem to="/administrateur/fusionner-auteurs">Fusionner des auteurs</BDropdownItem>
              </BDropdownGroup>
              <BDropdownGroup v-if="isEditor" id="group-admin" header="Admin" class="my-nav-group">
                <BDropdownItem to="/administrateur">Admin</BDropdownItem>
<!--                <BDropdownItem to="/gestionnaire-importation">Gestionnaire d'importation</BDropdownItem>-->
              </BDropdownGroup>
            </BNavItemDropdown>
          </BNavItem>

          <BNavItem to="/contact" class="nav-link space-around titre-nav-item">Contact</BNavItem>

          <BNavItem class="active" active>
            <BNavItemDropdown text="Divers" class="titre-nav-item">
              <BDropdownItem to="/liens">Liens utiles</BDropdownItem>
              <BDropdownItem to="/conception">Conception</BDropdownItem>
              <BDropdownItem to="/notes-de-version">Notes de version</BDropdownItem>
            </BNavItemDropdown>
          </BNavItem>
        </BNavbarNav>
        <BNavbarNav class="ms-auto">
          <BNavItem id="connection-tooltip" class="nav-link space-around titre-nav-item ms-auto">
            <template v-if="connected">
              <BTooltip target="connection-tooltip" triggers="hover" class="my-tooltip">
                {{ connectionTooltipHints }}
              </BTooltip>
            </template>
            <BNavItemDropdown v-if="connected" text="Mon profil" class="titre-nav-item">
              <BDropdownItem to="/utilisateur/reinitialiser-mot-de-passe">
                Changer <br/> de mot de passe
              </BDropdownItem>
              <BDropdownItem to="/utilisateur/deconnexion">Se déconnecter</BDropdownItem>
            </BNavItemDropdown>
            <BNavItemDropdown v-else text="Connexion" class="titre-nav-item">
              <BDropdownItem :to="{name: 'utilisateur-connexion'}">
                Se connecter
              </BDropdownItem>
              <BDropdownItem to="/utilisateur/creer">
                Nouveau compte
              </BDropdownItem>
            </BNavItemDropdown>
          </BNavItem>
        </BNavbarNav>
      </BCollapse>
    </BNavbar>
  </BContainer>

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
      window.open(`${import.meta.env.VITE_APP_SITE_API_URL}/static/sat_biblio_documentation-1.pdf`, '_blank');
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