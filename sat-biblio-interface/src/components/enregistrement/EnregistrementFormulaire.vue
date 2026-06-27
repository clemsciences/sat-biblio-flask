<template>
  <BForm @submit.prevent>
      <SuggestionReference v-if="selectedReference"
                           v-model="selectedReference"
                           :disabled="disabled"
                           ref="reference"
      />
      <!-- Recherche assisté de la référence -->
      <BFormGroup label="Cote">
        <BFormInput v-model="cote"
                      :disabled="disabled"
                      ref="cote"
        />
      </BFormGroup>
      <BFormGroup label="Année d'obtention">
        <BFormInput v-model="annee_obtention"
                      :disabled="disabled"
                      ref="annee_obtention"
        />
      </BFormGroup>
<!--      <BFormGroup label="Nombre d'exemplaires supplémentaires">-->
<!--        <BFormInput v-model="record.nb_exemplaire_supp"-->
<!--                      :disabled="disabled"/>-->
<!--      </BFormGroup>-->
      <BFormGroup label="Provenance">
        <BFormInput v-model="provenance"
                      :disabled="disabled"
                      ref="provenance"
        />
      </BFormGroup>
      <BFormGroup label="Aide à la recherche">
        <BFormInput v-model="aide_a_la_recherche"
                      :disabled="disabled"
                      ref="aide_a_la_recherche"
        />
      </BFormGroup>
      <BFormGroup label="Observations">
        <BFormInput v-model="observations"
                      :disabled="disabled"
                      ref="observations"
        />
      </BFormGroup>
<!--      </BFormGroup><BFormGroup label="Commentaire">-->
<!--        <BFormInput v-model="record.commentaire"-->
<!--                      :disabled="disabled"/>-->
<!--      </BFormGroup>-->

      <BFormGroup label="Ligne" v-if="!disabled">
        <BFormTextarea v-model="row"
                         :disabled="disabled"
                         :rows="5" size="sm"
                         row="ligne" ref="ligne"
                         />
      </BFormGroup>

      <BButton type="submit" v-if="!disabled"
                :disabled="isIncorrect || disabled"
                ref="submit" @click="onSubmit" >Enregistrer</BButton>
      <span class="mx-3">{{ message }}</span>
    </BForm>
</template>

<script>
import SuggestionReference from "@/components/reference_livre/SuggestionReference.vue";

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
    selectedReference: {
      get() {
        return this.record.selectedReference;
      },
      set(value) {
        this.$emit('update:selectedReference', value);
      }
    },
    cote: {
      get() {
        return this.record.cote;
      },
      set(value) {
        this.$emit('update:cote', value);
      }
    },
    annee_obtention: {
      get() {
        return this.record.annee_obtention;
      },
      set(value) {
        this.$emit('update:annee_obtention', value);
      }
    },
    provenance: {
      get() {
        return this.record.provenance;
      },
      set(value) {
        this.$emit('update:provenance', value);
      }
    },
    aide_a_la_recherche: {
      get() {
        return this.record.aide_a_la_recherche;
      },
      set(value) {
        this.$emit('update:aide_a_la_recherche', value);
      }
    },
    observations: {
      get() {
        return this.record.observations;
      },
      set(value) {
        this.$emit('update:observations', value);
      }
    },
    row: {
      get() {
        return this.record.row;
      },
      set(value) {
        this.$emit('update:row', value);
      }
    },
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

  }
}
</script>

<style scoped>

</style>