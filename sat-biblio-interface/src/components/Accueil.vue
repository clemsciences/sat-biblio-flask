<template>
  <b-container>
    <b-row>
      <h2>Accueil</h2>
    </b-row>
    <b-row>
      <b-col cols="9">
        <p>Bienvenue sur SatBiblio, c'est une application web qui permet de gérer
        le catalogue de la bibliothèque de la Société Archéologique de Touraine.</p>
        <p>Pourquoi passer à ce nouvel outil ? </p>
        <b-list-group>
            <b-list-group-item>Le catalogue est centralisé : si quelqu'un fait une modification, celle-ci sera directement accessible par les autres, de plus, ça évite d'avoir différentes versions</b-list-group-item>
            <b-list-group-item>Le catalogue est accessible par tous selon des droits précis : tout le monde peut consulter le catalogue,
            mais seulement les contributeurs peuvent proposer des modifications, le gestionnaire peut en plus accepter les modifications.</b-list-group-item>
            <b-list-group-item>Le catalogue ne dépend plus d'un format particulier. On peut exporter les fichiers sous le format qu'on souhaite.</b-list-group-item>
            <b-list-group-item>On peut gérer les emprunts des livres par cet outil.</b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col cols="3">
        <h3>Connexion</h3>
        <div v-if="connectionInfo.connected">
          <p>Vous êtes connecté en tant que {{ connectionInfo.email }} {{ connectionInfo.first_name }} {{ connectionInfo.family_name }}.</p>
          <p><router-link to="/utilisateur/deconnexion">Se déconnecter</router-link></p>
        </div>
        <div v-else>
          <p><router-link to="/utilisateur/connexion">Se connecter</router-link></p>
          <p><router-link to="/utilisateur/mot-de-passe-oublie">Mot de passe oublié</router-link></p>
          <p><router-link to="/utilisateur/creer">Créer un nouveau compte utilisateur</router-link></p>
        </div>
      </b-col>
    </b-row>

  </b-container>

</template>

<script>

import localStorageManager from "@/services/localstorageManager";
export default {
name: "Accueil",
  components: {},
  data: function () {
    return {
      connectionInfo: {}
    }
  },
  mounted() {
  this.connectionInfo = localStorageManager.getSessionInfo();
    console.log("info de session");
    console.log(localStorageManager.getSessionInfo());
  }

}
</script>

<style scoped>


</style>