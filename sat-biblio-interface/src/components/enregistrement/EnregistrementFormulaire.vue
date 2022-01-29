<template>
  <b-form @submit.prevent="onSubmit">
      <SuggestionReference v-if="record.selectedReference"
                           v-model="record.selectedReference"
                           :disabled="disabled"/>
      <!-- Recherche assisté de la référence -->
      <b-form-group label="Description">
        <b-form-textarea v-model="record.description"
                         :disabled="disabled"
                         :rows="5" size="sm"/>
      </b-form-group>
      <b-form-group label="Cote">
        <b-form-input v-model="record.cote"
                      :disabled="disabled"/>
      </b-form-group>
      <b-form-group label="Année">
        <b-form-input v-model="record.annee"
                      :disabled="disabled"/>
      </b-form-group>
      <b-form-group label="Nombre d'exemplaires supplémentaires">
        <b-form-input v-model="record.nb_exemplaire_supp"
                      :disabled="disabled"/>
      </b-form-group>
      <b-form-group label="Provenance">
        <b-form-input v-model="record.provenance"
                      :disabled="disabled"/>
      </b-form-group>
      <b-form-group label="Mots-clef">
        <b-form-input v-model="record.mots_clef"
                      :disabled="disabled"/>
      </b-form-group>
      <b-button type="submit" v-if="!disabled"
                :disabled="isIncorrect || disabled">Enregistrer</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>
</template>

<script>
import SuggestionReference from "@/components/reference_livre/SuggestionReference";

export default {
  name: "EnregistrementFormulaire",
  components: {SuggestionReference},
  props: {
    record: Object,
    onSubmit: Function,
    message: String,
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    isIncorrect: function () {
      return this.record.cote.length === 0 ||
          (this.record.selectedReference && this.record.selectedReference.value < 0);
    }
  }
}
</script>

<style scoped>

</style>