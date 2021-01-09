<template>
  <div>
  <h2>Référence bibliographique</h2>
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
      <b-button type="submit">Valider</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>
    <b-button class="my-3" v-b-modal.suppression>Supprimer</b-button>
    <b-modal id="suppression" title="Suppression de la référence"
      cancel-title="Annuler" ok-title="Supprimer" @ok="deleteReference">
      <p>Êtes-vous sûr de supprimer cette référence ?</p>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";

export default {
name: "LireReferenceLivre",
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
      message: "",
      selectedAuthorsMessage: "Les auteurs sélectionnés vont s'afficher en dessous.",
    }
  },
  methods: {
    loadReference: function() {
        axios.get("/api/reference-livre/lire/"+this.$route.params.id)
          .then(
              (response) => {
                if(response.data.success) {
                  console.log("authors");
                  console.log(response.data.reference);
                  this.selectedAuthors = response.data.reference.authors,

                  this.titre = response.data.reference.titre,
                  this.lieu_edition = response.data.reference.lieu_edition,
                  this.editeur = response.data.reference.editeur,
                  this.annee = response.data.reference.annee,
                  this.nb_page = response.data.reference.nb_page,
                  this.message = ""
                } else {
                  this.message = "Impossible de récupérer la référence."
                }
              }
          )
    },
    saveReference: function() {
      const formData = {
        auteurs: this.selectedAuthors,
        titre: this.titre,
        lieu_edition: this.lieu_edition,
        editeur: this.editeur,
        annee: this.annee,
        nb_page: this.nb_page
      };
      axios.post("/api/reference-livre/modifier/"+this.$route.params.id, formData)
          .then(
              (response) => {
                if(response.data.success) {
                  this.saveMessage ="La référence a été mise à jour."
                  console.log("référence livresque mise à jour");
                } else {
                  this.saveMessage = "La référence n'a pas pu être mise à jour."
                }
              }
          )
    },
    deleteReference: function() {
        axios.get("/api/reference-livre/supprimer/"+this.$route.params.id)
          .then(
              (response) => {
                if(response.data.success) {
                  console.log("référence livresque supprimée");
                  this.$router.push("/auteur/liste")
                } else {
                  this.saveMessage = "La référence n'a pas pu être supprimée."
                }
              }
          )
    },
    // TODO store
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
    // TODO store
    addAuthor: function(event) {
      this.selectedAuthor = event;
      this.selectedAuthors.push(event);
      this.author_query = "";
    },
  },
  mounted() {
    this.loadReference();
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