<template>
  <div>
    <h2>Nouvelle référence bibliographique - livre</h2>
    <b-form @submit="saveReference">
      <b-form-group label="Auteurs">
        <b-form-input></b-form-input> <!-- pour chercher l'auteur -->
      </b-form-group>
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
        <b-form-input v-model="nb_pages"/>
      </b-form-group>
      <b-button type="submit">Enregistrer</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ReferenceLivre",
  data: function () {
    return {
      titre: "",
      lieu_edition: "",
      editeur: "",
      annee: "",
      nb_pages: ""
    }
  },
  methods: {
    saveReference: function () {
      const formData = {
        titre: this.titre,
        lieu_edition: this.lieu_edition,
        editeur: this.editeur,
        annee: this.annee,
        nb_pages: this.nb_pages
      }
      axios.post("/api/reference-livre/creer", formData)
          .then(
              (response) => {
                if(response.data.success) {
                  console.log("créer une référence livresque");
                }
              }
          )
    }
  }
}
</script>

<style scoped>

</style>