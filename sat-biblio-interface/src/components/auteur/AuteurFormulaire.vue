<template>
    <b-form @submit.prevent="onSubmit">
      <b-form-group label="Prénom">
        <b-form-input type="text" v-model="auteur.first_name" :disabled="disabled"/>
      </b-form-group>
      <b-form-group label="Nom">
        <b-form-input type="text" v-model="auteur.family_name" :disabled="disabled"/>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect || disabled">Enregistrer</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>
</template>

<script>
export default {
  name: "AuteurFormulaire",
  props: {
    auteur: Object,
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