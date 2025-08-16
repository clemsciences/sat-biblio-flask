<template>
  <b-container>
    <JsonLdHeader :json-data="recordWithReference"/>
    <b-form @submit.prevent>
    <SuggestionAuteur
        v-model="recordWithReference.authors" class="my-3"
        :disabled="disabled"
        ref="authors"/>
    <b-form-group label="Auteurs tels qu'ils sont mentionnés dans le livre.">
      <b-form-input v-model="recordWithReference.authorsForm"
                    :disabled="disabled"
                    ref="authorsForm"/>
    </b-form-group>
    <b-form-group>
      <b-button v-if="referenceId != null" @click="goToReference">
        Voir la fiche de la référence bibliographique
      </b-button>
      <p v-else>pas de bouton</p>
    </b-form-group>


      <b-form-group label="Titre">
      <b-form-input v-model="recordWithReference.titre"
                    :disabled="disabled"
                    ref="title"/>
<!--      <BNFSearchBadge :title="reference.titre" labelPrefix=" - Titre"/>-->
    </b-form-group>
    <b-form-group label="Lieu d'édition">
      <b-form-input v-model="recordWithReference.lieu_edition"
                    :disabled="disabled"
                    ref="lieu_edition"/>
    </b-form-group>
    <b-form-group label="Editeurs">
      <b-form-input v-model="recordWithReference.editeur"
                    :disabled="disabled"
                    ref="editeur"/>
    </b-form-group>
    <b-form-group label="Année">
      <b-form-input v-model="recordWithReference.publication_annee"
                    :disabled="disabled"
                    ref="annee"/>
    </b-form-group>
    <b-form-group label="Nombre de pages" :state="isNbPageValid">
      <b-form-input v-if="recordWithReference.nb_page == -1" value="Inconnu" :disabled="disabled"/>
      <b-form-input v-else
                    v-model="recordWithReference.nb_page"
                    :disabled="disabled"
                    ref="nb_page"/>
    </b-form-group>
    <b-form-group label="Description" v-if="!disabled">
      <b-form-textarea v-model="recordWithReference.reference_description"
                       :disabled="disabled"
                       :rows="5" size="sm"
                       ref="description"/>
    </b-form-group>

      <b-form-group label="Cote">
        <b-form-input v-model="recordWithReference.cote"
                      :disabled="disabled"
                      ref="cote"
        />
      </b-form-group>
      <b-form-group label="Année d'obtention">
        <b-form-input v-model="recordWithReference.annee_entree"
                      :disabled="disabled"
                      ref="annee_obtention"/>
      </b-form-group>
<!--      <b-form-group label="Nombre d'exemplaires supplémentaires">-->
<!--        <b-form-input v-model="record.nb_exemplaire_supp"-->
<!--                      :disabled="disabled"/>-->
<!--      </b-form-group>-->
      <b-form-group label="Provenance">
        <b-form-input v-model="recordWithReference.provenance"
                      :disabled="disabled"
                      ref="provenance"/>
      </b-form-group>
      <b-form-group label="Aide à la recherche">
        <b-form-input v-model="recordWithReference.aide_a_la_recherche"
                      :disabled="disabled"
                      ref="aide_a_la_recherche"/>
      </b-form-group>
      <b-form-group label="Observations">
        <b-form-input v-model="recordWithReference.observations"
                      :disabled="disabled"
                      ref="observations"/>
      </b-form-group>
      <b-button type="submit" v-if="!disabled"
                :disabled="isInvalid() || disabled"
                ref="submit" @click="save" >Enregistrer</b-button>

    </b-form>
    <span class="mx-3">{{ message }}</span>
    
  </b-container>

</template>

<script>
import SuggestionAuteur from "../auteur/SuggestionAuteur.vue";
import {BookRecordWithReference} from "@/services/objectManager";
import JsonLdHeader from "@/components/web_semantics/JsonLdHeader.vue";

export default {
  name: "EnregistrementCompletFormulaire",
  components: {JsonLdHeader, SuggestionAuteur},
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
    isNbPageValid: function() {
      if(typeof this.recordWithReference.nb_page === "string") {
        if(this.recordWithReference.nb_page.length === 0) {
          return null;
        }
        let number = parseInt(this.recordWithReference.nb_page);
        return Number.isNaN(number);
      }
      return null;
    }
  }
}
</script>

<style scoped>

</style>