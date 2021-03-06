<template>
  <div>
    <h2>Déconnexion</h2>
    <p>La déconnexion s'est correctement déroulée.</p>
    <b-button to="/">Retourner à l'accueil</b-button>
  </div>
</template>

<script>
import localStorageManager from "@/services/localstorageManager";
import {disconnectUser} from "../../services/api";
export default {
  name: "Deconnexion",
  data: function() {
    return {
      message: "",
    }
  },
  mounted() {
    localStorageManager.removeSessionInfo();
    disconnectUser().then(
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