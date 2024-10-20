<template>
  <b-form @submit.prevent>
      <SuggestionReference v-if="record.selectedReference"
                           v-model="record.selectedReference"
                           :disabled="disabled"
                           ref="reference"
                           @keydown.enter="focusNext('cote')"
      />
      <!-- Recherche assisté de la référence -->
      <b-form-group label="Cote">
        <b-form-input v-model="record.cote"
                      :disabled="disabled"
                      ref="cote"
                      @keydown.enter="focusNext('annee_obtention')"
        />
      </b-form-group>
      <b-form-group label="Année d'obtention">
        <b-form-input v-model="record.annee_obtention"
                      :disabled="disabled"
                      ref="annee_obtention"
                      @keydown.enter="focusNext('provenance')"/>
      </b-form-group>
<!--      <b-form-group label="Nombre d'exemplaires supplémentaires">-->
<!--        <b-form-input v-model="record.nb_exemplaire_supp"-->
<!--                      :disabled="disabled"/>-->
<!--      </b-form-group>-->
      <b-form-group label="Provenance">
        <b-form-input v-model="record.provenance"
                      :disabled="disabled"
                      ref="provenance"
                      @keydown.enter="focusNext('aide_a_la_recherche')"/>
      </b-form-group>
      <b-form-group label="Aide à la recherche">
        <b-form-input v-model="record.aide_a_la_recherche"
                      :disabled="disabled"
                      ref="aide_a_la_recherche"
                      @keydown.enter="focusNext('observations')"/>
      </b-form-group>
      <b-form-group label="Observations">
        <b-form-input v-model="record.observations"
                      :disabled="disabled"
                      ref="observations"
                      @keydown.enter="focusNext('ligne')"/>
      </b-form-group>
<!--      </b-form-group><b-form-group label="Commentaire">-->
<!--        <b-form-input v-model="record.commentaire"-->
<!--                      :disabled="disabled"/>-->
<!--      </b-form-group>-->

      <b-form-group label="Ligne" v-if="!disabled">
        <b-form-textarea v-model="record.row"
                         :disabled="disabled"
                         :rows="5" size="sm"
                         row="ligne" ref="ligne"
                         />
<!--        @keydown.enter="focusNext('submit')"-->
      </b-form-group>

      <b-button type="submit" v-if="!disabled"
                :disabled="isIncorrect || disabled"
                ref="submit" @click="onSubmit" >Enregistrer</b-button>
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
  },
  data: function() {
    return {
      refs: ["reference", "cote", "annee_obtention", "provenance", "aide_a_la_recherche", "observations", "ligne", "submit"]
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