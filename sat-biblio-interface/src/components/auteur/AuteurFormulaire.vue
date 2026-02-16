<template>
    <BForm @submit.prevent>
      <BFormGroup label="Prénom">
        <BFormInput type="text"
                      v-model="firstName"
                      :disabled="disabled"
                      ref="first_name"/>
      </BFormGroup>
      <BFormGroup label="Nom">
        <BFormInput type="text"
                      v-model="familyName"
                      :disabled="disabled"
                      ref="family_name"/>
      </BFormGroup>
      <BButton type="submit"
                v-if="!disabled"
                :disabled="isIncorrect || disabled"
                ref="submit"
                @click="onSubmit">Enregistrer</BButton>
<!--      <BNFSearchBadge :author="authorString" labelPrefix="- Auteur"/>-->
      <span class="mx-3">{{ message }}</span>
    </BForm>
</template>

<script>
// import BNFSearchBadge from "@/components/badges/BNFSearchBadge";

import {Author} from "@/services/objectManager";

export default {
  name: "AuteurFormulaire",
  components: {/*BNFSearchBadge*/},
  props: {
    auteur: Author,
    onSubmit: Function,
    message: {
      type: String,
      default: ""
    },
    disabled: {
      type: Boolean,
      default: false
    }

  },
  data: function() {
    return {
      refs: ["first_name", "family_name", "submit"]
    }
  },
  computed: {
    firstName: {
      get() {
        return this.auteur.first_name;
      },
      set(value) {
        this.$emit('update:first_name', value);
      }
    },
    familyName: {
      get() {
        return this.auteur.family_name;
      },
      set(value) {
        this.$emit('update:family_name', value);
      }
    },
    isIncorrect: function () {
      return this.auteur.first_name.length === 0 || this.auteur.family_name.length === 0;
    }
  },
  methods: {

  }
}
</script>

<style scoped>

</style>