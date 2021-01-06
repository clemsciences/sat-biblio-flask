<template>
  <div>
    <h2>Nouvelle référence bibliographique - livre</h2>
    <b-form @submit.prevent="saveReference">
      <b-form-group label="Auteurs">
        <vue-typeahead-bootstrap
          v-model="author_query"
          :data="suggestedAuthors"
          :serializer="s => s.text"
          placeholder="Tapez le prénom ou le nom de l'auteur"
          @hit="addAuthor($event)"
        />
<!--        <b-form-input readonly v-if="selectedAuthor" v-model="selectedAuthor"/> &lt;!&ndash; pour chercher l'auteur &ndash;&gt;-->
      </b-form-group>
      <b-form-group :label="selectedAuthorsMessage">
        <b-form-select :options="selectedAuthors" :select-size="5" size="sm"></b-form-select>
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
        <b-form-input v-model="nb_page"/>
      </b-form-group>
      <b-button type="submit">Enregistrer</b-button>
      <span class="mx-3">{{ saveMessage }}</span>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ReferenceLivre",
  data: function () {
    return {
      author_query: '',
      suggestedAuthors: [],
      selectedAuthor: '',
      selectedAuthors: [],
      titre: "",
      lieu_edition: "",
      editeur: "",
      annee: "",
      nb_page: "",
      selectedAuthorsMessage: "Les auteurs sélectionnés vont s'afficher en dessous.",
      saveMessage: ""
    }
  },
  methods: {
    getSuggestedAuthors: function (query) {
      if (query.length >= 2) {
        axios.get("/api/auteur/chercher?auteur=:query".replace(":query", query))
            .then((response) => {
              if (response.data.success) {
                this.suggestedAuthors = response.data.suggestedAuthors;
              }
            }).catch();
      }
    },
    addAuthor: function(event) {
      this.selectedAuthor = event;
      this.selectedAuthors.push(event);
      this.author_query = "";
    },
    saveReference: function () {
      const formData = {
        auteurs: this.selectedAuthors,
        titre: this.titre,
        lieu_edition: this.lieu_edition,
        editeur: this.editeur,
        annee: this.annee,
        nb_page: this.nb_page
      };
      axios.post("/api/reference-livre/creer", formData)
          .then(
              (response) => {
                if(response.data.success) {
                  this.saveMessage = "La référence a été créée."
                  console.log("créer une référence livresque");
                } else {
                  this.saveMessage = "La création de la référence a échoué."
                }
              }
          )
    }
  },
  watch: {
    author_query: function (newValue) {
      this.getSuggestedAuthors(newValue);
    },
    selectedAuthors: function (newValue) {
      if(newValue.length > 1) {
        this.selectedAuthorsMessage = "Auteurs sélectionnés"
      } else {
        this.selectedAuthorsMessage = "Auteur sélectionné"
      }
    }
  }
}
</script>

<style scoped>

</style>