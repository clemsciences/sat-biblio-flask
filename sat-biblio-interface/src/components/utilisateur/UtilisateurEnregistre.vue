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
      if(this.$route.query.inscription_token && this.$route.query.email) {
        confirmUserRegistration(this.$route.query.inscription_token, this.$route.query.email).then(
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