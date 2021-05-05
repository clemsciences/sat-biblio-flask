<template>
  <b-container>
    <b-form @submit.prevent="updateAuthor">
      <b-form-group label="Prénom">
        <b-form-input type="text" v-model="first_name"></b-form-input>
      </b-form-group>
      <b-form-group label="Nom">
        <b-form-input type="text" v-model="family_name"></b-form-input>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect">Enregistrer</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>

    <b-button class="my-3" v-b-modal.suppression>Supprimer</b-button>

    <b-modal id="suppression" title="Suppression de l'auteur"
      cancel-title="Annuler" ok-title="Supprimer" @ok="deleteAuthor">
      <p>Êtes-vous sûr de supprimer cet auteur ?</p>
    </b-modal>

  </b-container>
</template>

<script>
import {deleteAuthor, retrieveAuthor, updateAuthor} from "@/services/api";
export default {
  name: "LireAuteur",
  data: function () {
    return {
    first_name: '',
    family_name: '',
    message: ''

    }
  },
  methods: {
    getAuthor: function() {
      retrieveAuthor(this.$route.params.id).then(
        (response) => {
          if(response.data.success) {
            this.first_name = response.data.author.first_name;
            this.family_name = response.data.author.family_name;
          } else {
            console.log("erreur de récupération de l'auteur");
          }
        }
      );
    },
    updateAuthor: function() {
      const formData = {first_name: this.first_name, family_name: this.family_name};
      updateAuthor(this.$route.params.id, formData).then(
        (response) => {
          if(response.data.success) {
            console.log("modifications enregistrées");
            this.$router.push("/auteur/liste")
          } else {
            console.log("échec de la modification");
          }
        }
      );
    },
    deleteAuthor: function() {
      deleteAuthor(this.$route.params.id).then(
        (response) => {
          if(response.data.success) {
            console.log("la suppression a fonctionné");
            this.$router.replace("/auteur/liste");
          }
        }
      );

    }

  },
  mounted() {
    this.getAuthor();
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