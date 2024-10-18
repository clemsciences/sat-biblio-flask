<template>
    <b-form @submit.prevent="onSubmit">
      <b-form-group label="Prénom">
        <b-form-input type="text" v-model="auteur.first_name" :disabled="disabled"/>
      </b-form-group>
      <b-form-group label="Nom">
        <b-form-input type="text" v-model="auteur.family_name" :disabled="disabled"/>
      </b-form-group>
      <b-button type="submit" v-if="!disabled" :disabled="isIncorrect || disabled">Enregistrer</b-button>
<!--      <BNFSearchBadge :author="authorString" labelPrefix="- Auteur"/>-->
      <span class="mx-3">{{ message }}</span>
    </b-form>
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
  computed: {
    isIncorrect: function () {

      return this.auteur.first_name.length === 0 || this.auteur.family_name.length === 0;
    }
  }
}
</script>

<style scoped>

</style>