<template>
  <BForm @submit.prevent>
    <SuggestionAuteur
        v-if="selectedAuthors"
        v-model="selectedAuthors" class="my-3"
        :disabled="disabled"
        ref="authors"
    />
    <BFormGroup label="Auteurs tels qu'ils sont mentionnés dans le livre."
    v-if="authorsForm.length > 0 || !disabled">
      <BFormInput v-model="authorsForm"
                    :disabled="disabled"
                    ref="authorsForm"
      />
    </BFormGroup>
    <BFormGroup label="Titre">
      <BFormInput v-model="titre"
                    :disabled="disabled"
                    ref="title"
      />
<!--      <BNFSearchBadge :title="reference.titre" labelPrefix=" - Titre"/>-->
    </BFormGroup>
    <BFormGroup label="Lieu d'édition">
      <BFormInput v-model="lieu_edition"
                    :disabled="disabled"
                    ref="lieu_edition"
      />
    </BFormGroup>
    <BFormGroup label="Editeurs">
      <BFormInput v-model="editeur"
                    :disabled="disabled"
                    ref="editeur"
      />
    </BFormGroup>
    <BFormGroup label="Année">
      <BFormInput v-model="annee"
                    :disabled="disabled"
                    ref="annee"
      />
    </BFormGroup>
    <BFormGroup label="Nombre de pages" :state="isNbPageValid">
      <BFormInput v-if="reference.nb_page == -1" value="Inconnu" :disabled="disabled"/>
      <BFormInput v-else
                    v-model="nb_page"
                    :disabled="disabled"
                    ref="nb_page"
      />
    </BFormGroup>
    <BFormGroup label="Description" v-if="!disabled">
      <BFormTextarea v-model="description"
                       :disabled="disabled"
                       :rows="5" size="sm"
                       ref="description"
      />
    </BFormGroup>
    <BButton type="submit"
              v-if="!disabled"
              :disabled="isIncorrect || disabled"
              @click="onSubmit"
              ref="submit">Enregistrer</BButton>
    <span class="mx-3">{{ message }}</span>
  </BForm>
</template>

<script>
import SuggestionAuteur from "@/components/auteur/SuggestionAuteur.vue";
import {BookReference} from "@/services/objectManager.js";
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
    selectedAuthors: {
      get() {
        return this.reference.selectedAuthors;
      },
      set(value) {
        this.$emit('update:selectedAuthors', value);
      }
    },
    authorsForm: {
      get() {
        return this.reference.authorsForm;
      },
      set(value) {
        this.$emit('update:authorsForm', value);
      }
    },
    titre: {
      get() {
        return this.reference.titre;
      },
      set(value) {
        this.$emit('update:titre', value);
      }
    },
    lieu_edition: {
      get() {
        return this.reference.lieu_edition;
      },
      set(value) {
        this.$emit('update:lieu_edition', value);
      }
    },
    editeur: {
      get() {
        return this.reference.editeur;
      },
      set(value) {
        this.$emit('update:editeur', value);
      }
    },
    annee: {
      get() {
        return this.reference.annee;
      },
      set(value) {
        this.$emit('update:annee', value);
      }
    },
    nb_page: {
      get() {
        return this.reference.nb_page;
      },
      set(value) {
        this.$emit('update:nb_page', value);
      }
    },
    description: {
      get() {
        return this.reference.description;
      },
      set(value) {
        this.$emit('update:description', value);
      }
    },
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
  }

}
</script>

<style scoped>

</style>