<template>
  <b-container>
    <b-row>
      <h2>Accueil</h2>
    </b-row>
    <b-row><h3>Connexion</h3></b-row>
    <b-row v-if="connected">
      <b-col>
        <b-row>
          <p>Vous êtes connecté en tant que <b>{{ connectionInfo.first_name }} {{ connectionInfo.family_name }}</b> ù(<i>{{ connectionInfo.email }}</i>).
            Vous êtes <b>{{ rightString }}</b>.</p>
        </b-row>
        <b-row>
          <b-col cols="2">
            <p><b-button to="/utilisateur/deconnexion">Se déconnecter</b-button></p>
          </b-col>
          <b-col cols="2">
            <p><b-button to="/utilisateur/reinitialiser-mot-de-passe">Changer de mot de passe</b-button></p>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
    <b-row v-else>
      <b-col cols="2">
        <p><b-button to="/utilisateur/connexion">Se connecter</b-button></p>
      </b-col>
      <b-col cols="2">
        <p><b-button to="/utilisateur/creer">Créer un nouveau compte utilisateur</b-button></p>
      </b-col>
    </b-row>
    <b-row><h3>Description</h3></b-row>
    <b-row>
<!--      <b-col cols="9">-->
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
<!--      </b-col>-->
    </b-row>

  </b-container>

</template>

<script>

import {mapState} from "vuex";
import {getRightString} from "@/services/rights";
export default {
name: "Accueil",
  components: {},
  computed: {
    ...mapState(["connected", "connectionInfo"]),
    rightString: function () {
      return getRightString(this.connectionInfo.right);
    }
  }

}
</script>

<style scoped>


</style>