<template>
  <BContainer>
    <JsonLdHeader :json-data="recordWithReference"/>
    <BForm @submit.prevent>
      <BCard class="mb-3">
        <BCardHeader class="fw-bold bg-primary-subtle">Référence bibliographique</BCardHeader>
        <BCardBody>
          <SuggestionAuteur
              v-model="authors" class="my-3"
              :disabled="disabled"
              ref="authors"/>
          <BFormGroup label="Auteurs tels qu'ils sont mentionnés dans le livre.">
            <BFormInput v-model="authorsForm"
                          :disabled="disabled"
                          ref="authorsForm"/>
          </BFormGroup>
          <BFormGroup>
            <BButton v-if="referenceId != null" @click="goToReference">
              Voir la fiche de la référence bibliographique
            </BButton>
            <p v-else>pas de bouton</p>
          </BFormGroup>
          <BFormGroup label="Titre">
            <BFormInput v-model="titre"
                          :disabled="disabled"
                          ref="title"/>
<!--            <BNFSearchBadge :title="reference.titre" labelPrefix=" - Titre"/>-->
          </BFormGroup>
          <BFormGroup label="Lieu d'édition">
            <BFormInput v-model="lieu_edition"
                          :disabled="disabled"
                          ref="lieu_edition"/>
          </BFormGroup>
          <BFormGroup label="Editeurs">
            <BFormInput v-model="editeur"
                          :disabled="disabled"
                          ref="editeur"/>
          </BFormGroup>
          <BFormGroup label="Année">
            <BFormInput v-model="publication_annee"
                          :disabled="disabled"
                          ref="annee"/>
          </BFormGroup>
          <BFormGroup label="Nombre de pages" :state="isNbPageValid">
            <BFormInput v-if="recordWithReference.nb_page == -1" value="Inconnu" :disabled="disabled"/>
            <BFormInput v-else
                          v-model="nb_page"
                          :disabled="disabled"
                          ref="nb_page"/>
          </BFormGroup>
          <BFormGroup label="Description" v-if="!disabled">
            <BFormTextarea v-model="reference_description"
                             :disabled="disabled"
                             :rows="5" size="sm"
                             ref="description"/>
          </BFormGroup>
        </BCardBody>
      </BCard>

      <BCard class="mb-3">
        <BCardHeader class="fw-bold bg-primary-subtle">Enregistrement</BCardHeader>
        <BCardBody>
          <BFormGroup label="Cote">
            <BFormInput v-model="cote"
                          :disabled="disabled"
                          ref="cote"
            />
          </BFormGroup>
          <BFormGroup label="Année d'obtention">
            <BFormInput v-model="annee_entree"
                          :disabled="disabled"
                          ref="annee_obtention"/>
          </BFormGroup>
<!--          <BFormGroup label="Nombre d'exemplaires supplémentaires">-->
<!--            <BFormInput v-model="recordWithReference.nb_exemplaire_supp"-->
<!--                          ref="nb_exemplaire_supp"-->
<!--                          :disabled="disabled"/>-->
<!--          </BFormGroup>-->
          <BFormGroup label="Provenance">
            <BFormInput v-model="provenance"
                          :disabled="disabled"
                          ref="provenance"/>
          </BFormGroup>
          <BFormGroup label="Aide à la recherche">
            <BFormInput v-model="aide_a_la_recherche"
                          :disabled="disabled"
                          ref="aide_a_la_recherche"/>
          </BFormGroup>
          <BFormGroup label="Observations">
            <BFormInput v-model="observations"
                          :disabled="disabled"
                          ref="observations"/>
          </BFormGroup>
        </BCardBody>
      </BCard>

      <BButton type="submit" v-if="!disabled"
                :disabled="isInvalid() || disabled"
                ref="submit" @click="save" >Enregistrer</BButton>

    </BForm>
    <span class="mx-3">{{ message }}</span>
    
  </BContainer>

</template>

<script>
import SuggestionAuteur from "../auteur/SuggestionAuteur.vue";
import {BookRecordWithReference} from "@/services/objectManager";
import JsonLdHeader from "@/components/web_semantics/JsonLdHeader.vue";
import {BButton, BCard, BCardBody, BCardHeader, BContainer, BForm, BFormGroup, BFormInput, BFormTextarea} from "bootstrap-vue-next";

export default {
  name: "EnregistrementCompletFormulaire",
  components: {BButton, BCard, BCardBody, BCardHeader, BFormTextarea, BFormInput, BContainer, BFormGroup, BForm, JsonLdHeader, SuggestionAuteur},
  props: {
    recordWithReference: {
      type: BookRecordWithReference
    },
    disabled: {
      type: Boolean
    },
    save: {
      type: Function
    },
    message: {
      type: String
    },
    referenceId: {
      type: Number,
      nullable: true
    }

  },
  data() {
    return {

    }
  },
  methods: {
    isInvalid() {
      return false;
    },
    goToReference() {
      this.$router.push(`/reference-livre/lire/${this.referenceId}`);
    }

  },
  computed: {
    authors: {
      get() {
        return this.recordWithReference.authors;
      },
      set(value) {
        this.$emit('update:authors', value);
      }
    },
    authorsForm: {
      get() {
        return this.recordWithReference.authorsForm;
      },
      set(value) {
        this.$emit('update:authorsForm', value);
      }
    },
    titre: {
      get() {
        return this.recordWithReference.titre;
      },
      set(value) {
        this.$emit('update:titre', value);
      }
    },
    lieu_edition: {
      get() {
        return this.recordWithReference.lieu_edition;
      },
      set(value) {
        this.$emit('update:lieu_edition', value);
      }
    },
    editeur: {
      get() {
        return this.recordWithReference.editeur;
      },
      set(value) {
        this.$emit('update:editeur', value);
      }
    },
    publication_annee: {
      get() {
        return this.recordWithReference.publication_annee;
      },
      set(value) {
        this.$emit('update:publication_annee', value);
      }
    },
    nb_page: {
      get() {
        return this.recordWithReference.nb_page;
      },
      set(value) {
        this.$emit('update:nb_page', value);
      }
    },
    reference_description: {
      get() {
        return this.recordWithReference.reference_description;
      },
      set(value) {
        this.$emit('update:reference_description', value);
      }
    },
    cote: {
      get() {
        return this.recordWithReference.cote;
      },
      set(value) {
        this.$emit('update:cote', value);
      }
    },
    annee_entree: {
      get() {
        return this.recordWithReference.annee_entree;
      },
      set(value) {
        this.$emit('update:annee_entree', value);
      }
    },
    provenance: {
      get() {
        return this.recordWithReference.provenance;
      },
      set(value) {
        this.$emit('update:provenance', value);
      }
    },
    aide_a_la_recherche: {
      get() {
        return this.recordWithReference.aide_a_la_recherche;
      },
      set(value) {
        this.$emit('update:aide_a_la_recherche', value);
      }
    },
    observations: {
      get() {
        return this.recordWithReference.observations;
      },
      set(value) {
        this.$emit('update:observations', value);
      }
    },
    isNbPageValid: function() {
      if(typeof this.recordWithReference.nb_page === "string") {
        if(this.recordWithReference.nb_page.length === 0) {
          return null;
        }
        let number = parseInt(this.recordWithReference.nb_page);
        return !Number.isNaN(number);
      }
      return null;
    }
  }
}
</script>

<style scoped>

</style>