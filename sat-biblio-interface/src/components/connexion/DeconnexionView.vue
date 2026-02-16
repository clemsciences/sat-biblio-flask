<template>
  <BContainer>
    <AppTitle title="Déconnexion"
      info=""
      id="id-deconnexion"/>
    <p>La déconnexion s'est correctement déroulée.</p>
    <BButton to="/">Retourner à l'accueil</BButton>
  </BContainer>
</template>

<script>
import {disconnectUser} from "@/services/api";
import AppTitle from "@/components/visuel/AppTitle.vue";
export default {
  name: "DeconnexionView",
  components: {AppTitle},
  data: function() {
    return {
      message: "",
    }
  },
  mounted() {
    this.$store.commit("disconnect");
    disconnectUser().then(
      () => {
        this.message = "Vous êtes correctement déconnecté."
      }
    );
  }
}
</script>

<style scoped>

</style>