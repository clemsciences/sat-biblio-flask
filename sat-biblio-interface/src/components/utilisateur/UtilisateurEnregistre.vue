<template>
  <b-container>
    <h2>Utilisateur enregistré</h2>
    <p>{{ message }}</p>
  </b-container>
</template>

<script>
import {confirmUserRegistration} from "@/services/api";

export default {
  name: "UtilisateurEnregistre",
  data: function() {
    return {
      message: "En cours de validation...",
    }
  },
  methods: {
    check: function() {
      const inscriptionToken = this.$route.query.inscription_token;
      const emailAddress = this.$route.query.email;
      if(inscriptionToken && emailAddress) {
        confirmUserRegistration(inscriptionToken, emailAddress).then(
            response => {
              this.message = response.data.message;
              console.log(response);
            }
        ).catch(
            reason => {
              this.message = reason.response.data.message
              console.log(reason)
            }
        )
      } else {
        this.message = "Lien invalide";
        console.log("Lien invalide");
      }
    }
  },
  mounted() {
    this.check();
  }
}
</script>

<style scoped>

</style>