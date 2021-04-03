<template>
  <b-container>
    <Title title="Nouvel auteur"
           info="Un auteur est un individu qui a participé à la rédaction d'au moins un ouvrage."
           id="id-auteur"/>
    <b-form @submit.prevent="onSubmit">
      <b-form-group label="Prénom">
        <b-form-input type="text" v-model="first_name"></b-form-input>
      </b-form-group>
      <b-form-group label="Nom">
        <b-form-input type="text" v-model="family_name"></b-form-input>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect">Enregistrer</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>
  </b-container>
</template>

<script>
import {createAuthor} from "../../services/api";
import Title from "../visuel/Title";

export default {
  name: "Auteur",
  components: {Title},
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
                this.first_name = "";
                this.family_name = "";
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
  },
  computed: {
    isIncorrect: function () {
      return this.first_name.length === 0 || this.family_name.length === 0;
    }
  }
}
</script>

<style scoped>

</style>