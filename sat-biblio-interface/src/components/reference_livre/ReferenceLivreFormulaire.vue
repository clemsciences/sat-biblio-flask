<template>
  <b-form @submit.prevent="onSubmit">
    <SuggestionAuteur
        v-if="reference.selectedAuthors"
        v-model="reference.selectedAuthors" class="my-3"
        :disabled="disabled"/>
    <b-form-group label="Titre">
      <b-form-input v-model="reference.titre" :disabled="disabled"/>
      <BNFSearchBadge :title="reference.titre" labelPrefix=" - Titre"/>
    </b-form-group>
    <b-form-group label="Lieu d'édition">
      <b-form-input v-model="reference.lieu_edition" :disabled="disabled"/>
    </b-form-group>
    <b-form-group label="Editeurs">
      <b-form-input v-model="reference.editeur" :disabled="disabled"/>
    </b-form-group>
    <b-form-group label="Année">
      <b-form-input v-model="reference.annee" :disabled="disabled"/>
    </b-form-group>
    <b-form-group label="Nombre de pages" :state="isNbPageValid">
      <b-form-input v-model="reference.nb_page" :disabled="disabled"/>
    </b-form-group>
    <b-form-group label="Description">
      <b-form-textarea v-model="reference.description"
                       :disabled="disabled"
                       :rows="5" size="sm"/>
    </b-form-group>
    <b-button type="submit" v-if="!disabled" :disabled="isIncorrect || disabled">Enregistrer</b-button>
    <span class="mx-3">{{ message }}</span>
  </b-form>
</template>

<script>
import SuggestionAuteur from "@/components/auteur/SuggestionAuteur";
import BNFSearchBadge from "@/components/badges/BNFSearchBadge";

export default {
  name: "ReferenceLivreFormulaire",
  components: {SuggestionAuteur, BNFSearchBadge},
  props: {
    reference: Object,
    message: {
      type: String,
      default: ''
    },
    onSubmit: Function,
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    isIncorrect: function () {
      return (this.reference.selectedAuthors && this.reference.selectedAuthors.length === 0) ||
          this.reference.titre.length === 0 ||
          this.reference.editeur.length === 0;
    },
    isNbPageValid: function() {
      if(typeof this.reference.nb_page === "string") {
        if(this.reference.nb_page.length === 0) {
          return null;
        }
        let number = parseInt(this.reference.nb_page);
        return Number.isNaN(number);
      }
      return null;
    }
  },
  watch: {
    author_query: function (newValue) {
      this.getSuggestedAuthors(newValue);
    },
    'record.selectedAuthors': function (newValue) {
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