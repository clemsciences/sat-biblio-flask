<template>
  <b-container>
    <Title title="Déconnexion"
      info=""
      id="id-deconnexion"/>
    <p>La déconnexion s'est correctement déroulée.</p>
    <b-button to="/">Retourner à l'accueil</b-button>
  </b-container>
</template>

<script>
import localStorageManager from "@/services/localstorageManager";
import {disconnectUser} from "@/services/api";
import Title from "@/components/visuel/Title";
export default {
  name: "Deconnexion",
  components: {Title},
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