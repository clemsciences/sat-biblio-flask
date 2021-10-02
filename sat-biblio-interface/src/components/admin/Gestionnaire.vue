<template>
  <b-container>
    <Title info="Cette page permet au gestionnaire d'accepter ou de refuser des modifications d'une fiche."
           id="id-gestionnaire">
      Page du gestionnaire
    </Title>
    <b-button v-b-toggle.collapse-users>Voir les utilisateurs</b-button>
    <b-collapse id="collapse-users">
      <liste-utilisateur/>
    </b-collapse>
    <b-button>

    </b-button>

  </b-container>
</template>

<script>
import Title from "../visuel/Title";
import ListeUtilisateur from "@/components/admin/ListeUtilisateur";
export default {
name: "Gestionnaire",
  components: {Title, ListeUtilisateur},
  data: function () {
    return {

    }
  },

}
</script>

<style scoped>

</style>