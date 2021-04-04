<template>
  <b-container>
    <Title title="Nouvelle référence bibliographique - livre"
           info="Une référence bibliographique désigne les informations propres à un livre"
           id="id-ref"/>

    <b-form @submit.prevent="saveReference">
      <SuggestionAuteur v-model="selectedAuthors" class="my-3"/>
      <b-form-group label="Titre">
        <b-form-input v-model="titre"></b-form-input>
      </b-form-group>
      <b-form-group label="Lieu d'édition">
        <b-form-input v-model="lieu_edition"></b-form-input>
      </b-form-group>
      <b-form-group label="Editeurs">
        <b-form-input v-model="editeur"/>
      </b-form-group>
      <b-form-group label="Année">
        <b-form-input v-model="annee"/>
      </b-form-group>
      <b-form-group label="Nombre de pages">
        <b-form-input v-model="nb_page"/>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect">Enregistrer</b-button>
      <span class="mx-3">{{ saveMessage }}</span>
    </b-form>
  </b-container>
</template>

<script>
import {createBookReference} from "../../services/api";
import SuggestionAuteur from "../auteur/SuggestionAuteur";
import Title from "../visuel/Title";

export default {
  name: "ReferenceLivre",
  components: {Title, SuggestionAuteur},
  data: function () {
    return {
      selectedAuthors: [],
      titre: "",
      lieu_edition: "",
      editeur: "",
      annee: "",
      nb_page: "",
      saveMessage: ""
    }
  },
  methods: {
    saveReference: function () {
      const formData = {
        auteurs: this.selectedAuthors,
        titre: this.titre,
        lieu_edition: this.lieu_edition,
        editeur: this.editeur,
        annee: this.annee,
        nb_page: this.nb_page
      };

      createBookReference(formData)
        .then(
            (response) => {
              if(response.data.success) {
                this.saveMessage = "La référence a été créée."
                console.log("créer une référence livresque");
                this.selectedAuthors = [];
                this.titre = "";
                this.lieu_edition = "";
                this.editeur = "";
                this.annee = "";
                this.nb_page = "";
              } else {
                this.saveMessage = "La création de la référence a échoué."
              }
            }
        )
    }
  },
  computed: {
    isIncorrect: function () {
      return this.selectedAuthors.length === 0 || this.titre.length === 0 || this.editeur.length === 0;
    }
  }
}
</script>

<style scoped>

</style>