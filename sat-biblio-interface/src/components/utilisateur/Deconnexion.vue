<template>
  <div>
    <h2>Déconnexion</h2>
    <p>La déconnexion s'est correctement déroulée.</p>
    <b-button to="/">Retourner à l'accueil</b-button>
  </div>
</template>

<script>
import axios from "axios";
import localStorageManager from "@/services/localstorageManager";
export default {
  name: "Deconnexion",
  data: function() {
    return {
      message: "",
    }
  },
  mounted() {
    localStorageManager.removeSessionInfo();
    axios.get("/api/user/disconnect").then(
      () => {
        this.$store.commit("disconnect");
        this.message = "Vous êtes correctement déconnecté."
      }
    );
  }
}
</script>

<style scoped>

</style>