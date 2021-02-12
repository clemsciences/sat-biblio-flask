<template>
  <div>
    <h2>Nouvel auteur</h2>
    <b-form @submit.prevent="onSubmit">
      <b-form-group label="Prénom">
        <b-form-input type="text" v-model="first_name"></b-form-input>
      </b-form-group>
      <b-form-group label="Nom">
        <b-form-input type="text" v-model="family_name"></b-form-input>
      </b-form-group>
      <b-button type="submit">Valider</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>
  </div>
</template>

<script>
import {createAuthor} from "../../services/api";

export default {
  name: "Auteur",
  data: function () {
    return {
      first_name: '',
      family_name: '',
      message: ''
    };
  },
  methods: {
    onSubmit: function() {
      if (this.first_name.length > 0 && this.family_name.length > 0) {
        const form_data = {
          first_name: this.first_name.trim(),
          family_name: this.family_name.trim()
        };

        createAuthor(form_data).then(
            (response) => {
              if (response.data.success) {
                this.message = "L'auteur " + this.first_name + " " + this.family_name + " a été correctement créé.";
              } else {
                this.message = "Impossible de sauvegarder l'auteur."
              }
            }
        ).catch(
            (reason => {
              console.log(reason);
              this.message = "Il y a une erreur réseau."
            })
        );
      } else if(this.first_name.length === 0) {
        this.message = "Le prénom ne peut être vide.";
      } else if (this.family_name.length === 0) {
        this.message = "Le nom de famille ne peut être vide.";
      }
    }
  }
}
</script>

<style scoped>

</style>