<template>
  <b-container class="text-center my-5">
    <h2 class="mb-4">Catalogue en ligne de la Bibliothèque d'Histoire de la Touraine - BHT</h2>

    <!-- Connection Info -->
    <div v-if="connected">
      <h3>Connexion</h3>
      <p>
        Vous êtes connecté en tant que
        <b>{{ connectionInfo.first_name }} {{ connectionInfo.family_name }}</b>
        (<i>{{ connectionInfo.email }}</i>). Vous êtes
        <b>{{ rightString }}</b>.
      </p>
    </div>

    <!-- Description -->
    <p class="lead mt-4">
      Bienvenue sur SatBiblio, une application web qui permet de consulter et de gérer
      le catalogue de la bibliothèque de la Société Archéologique de Touraine.
    </p>

    <!-- Bouton central -->
    <b-button
      variant="primary"
      size="lg"
      href="/catalogue"
      class="my-4"
    >
      <b-icon icon="book"></b-icon>
      Consulter le catalogue
    </b-button>

    <div>
      <a href="#new-tool" class="mx-2">Raisons de ce nouvel outil</a>
      <!--<a href="#video-introduction" class="mx-2">Vidéo d'introduction</a>-->
      <a href="/conception" class="mx-2">Conception</a>
      <a href="/liens" class="mx-2">Liens utiles</a>
    </div>

    <div class="d-flex flex-wrap justify-content-center align-items-center mt-5" id="book-images">
      <b-img src="bht_livres_1.jpg" class="m-3 img-fluid" style="max-width: 200px" alt="Livres sur étagère"/>
      <b-img src="bht_livres_2.jpg" class="m-3 img-fluid" style="max-width: 200px" alt="Livres sur étagère"/>
      <b-img src="bht_livres_3.jpg" class="m-3 img-fluid" style="max-width: 200px" alt="Livres sur étagère"/>
      <b-img src="bht_livres_4.jpg" class="m-3 img-fluid" style="max-width: 200px" alt="Livres sur étagère"/>
    </div>

    <!-- Bouton toggle et collapsible (placé plus bas à gauche) -->
    <div class="text-start mt-5" id="new-tool">
<!--      <b-button v-b-toggle.collapse-why variant="info" size="sm">-->
        <h5>Pourquoi passer à ce nouvel outil ?</h5>
<!--      </b-button>-->
<!--      <b-collapse id="collapse-why" class="mt-3">-->
        <b-list-group>
          <b-list-group-item>
            Le catalogue est <b>centralisé</b>.<br/> <span class="detail">Si quelqu'un fait une modification, celle-ci sera directement accessible par les autres,
            ce qui évite d'avoir différentes versions.</span>
          </b-list-group-item>
          <b-list-group-item>
            Le catalogue est <b>accessible</b> par tous selon.<br/> <span class="detail">Des droits spécifiques permettentde gérer et de modifier le catalogue.</span>
          </b-list-group-item>
          <b-list-group-item>
            Le catalogue ne dépend plus d'un format particulier.<br/> <span class="detail">On peut exporter les fichiers sous le format souhaité.</span>
          </b-list-group-item>
          <b-list-group-item>
            On peut <b>gérer les emprunts</b> des livres et envoyer des emails aux retardataires.
          </b-list-group-item>
        </b-list-group>
<!--      </b-collapse>-->
    </div>

    <div class="d-flex flex-wrap justify-content-center align-items-center mt-5" id="book-images">
      <b-img src="bht_rdc_1.jpg" class="m-auto img-fluid" style="max-width: 1000px" alt="Photo du rez-de-chaussée de la bibliothèque."/>
    </div>

    <div id="video-introduction">
      <b-embed
        type="iframe"
        aspect="16by9"
        src=""
        allowfullscreen
      ></b-embed>
    </div>
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