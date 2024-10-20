<template>
  <b-form @submit.prevent>
    <SuggestionAuteur
        v-if="reference.selectedAuthors"
        v-model="reference.selectedAuthors" class="my-3"
        :disabled="disabled"
        ref="authors"
        @keydown.enter="focusNext('authorsForm')"/>
    <b-form-group label="Auteurs tels qu'ils sont mentionnés dans le livre."
    v-if="reference.authorsForm.length > 0 || !disabled">
      <b-form-input v-model="reference.authorsForm"
                    :disabled="disabled"
                    ref="authorsForm"
                    @keydown.enter="focusNext('title')"/>
    </b-form-group>
    <b-form-group label="Titre">
      <b-form-input v-model="reference.titre"
                    :disabled="disabled"
                    ref="title"
                    @keydown.enter="focusNext('lieu_edition')"/>
<!--      <BNFSearchBadge :title="reference.titre" labelPrefix=" - Titre"/>-->
    </b-form-group>
    <b-form-group label="Lieu d'édition">
      <b-form-input v-model="reference.lieu_edition"
                    :disabled="disabled"
                    ref="lieu_edition"
                    @keydown.enter="focusNext('editeur')"/>
    </b-form-group>
    <b-form-group label="Editeurs">
      <b-form-input v-model="reference.editeur"
                    :disabled="disabled"
                    ref="editeur"
                    @keydown.enter="focusNext('annee')"/>
    </b-form-group>
    <b-form-group label="Année">
      <b-form-input v-model="reference.annee"
                    :disabled="disabled"
                    ref="annee"
                    @keydown.enter="focusNext('nb_page')"/>
    </b-form-group>
    <b-form-group label="Nombre de pages" :state="isNbPageValid">
      <b-form-input v-if="reference.nb_page == -1" value="Inconnu" :disabled="disabled"/>
      <b-form-input v-else
                    v-model="reference.nb_page"
                    :disabled="disabled"
                    ref="nb_page"
                    @keydown.enter="focusNext('description')"/>
    </b-form-group>
    <b-form-group label="Description" v-if="!disabled">
      <b-form-textarea v-model="reference.description"
                       :disabled="disabled"
                       :rows="5" size="sm"
                       ref="description" @keydown.enter="focusNext('submit')"/>
    </b-form-group>
    <b-button type="submit"
              v-if="!disabled"
              :disabled="isIncorrect || disabled"
              @click="onSubmit"
              ref="submit">Enregistrer</b-button>
    <span class="mx-3">{{ message }}</span>
  </b-form>
</template>

<script>
import SuggestionAuteur from "@/components/auteur/SuggestionAuteur";
import {BookReference} from "@/services/objectManager";
// import BNFSearchBadge from "@/components/badges/BNFSearchBadge";

export default {
  name: "ReferenceLivreFormulaire",
  components: {SuggestionAuteur, /*BNFSearchBadge*/},
  props: {
    reference: BookReference,
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
  },
  data: function() {
    return {
      refs: ["authors", "authorsForm", "title", "lieu_edition", "editeur", "annee", "nb_page", "description", "submit"]
    }
  },
  methods: {
    focusNext(ref) {
      if (this.refs.includes(ref)) {
        this.$refs[ref].focus();
      } else {
        console.log("wrong ref")
      }
    }
  }

}
</script>

<style scoped>

</style>