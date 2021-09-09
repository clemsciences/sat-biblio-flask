<template>
  <b-container>
    <Title id="id-lecture-auteur"
           info=""
           title="Auteur"/>
    <AuteurFormulaire
        :on-submit="updateAuthor"
        :auteur="auteur"
        :message="message"
        :disabled="!canModify"
    />

    <b-button class="my-3" v-b-modal.suppression :disabled="!canModify">Supprimer</b-button>

    <b-modal id="suppression" title="Suppression de l'auteur"
      cancel-title="Annuler" ok-title="Supprimer" @ok="deleteAuthor">
      <p>Êtes-vous sûr de supprimer cet auteur ?</p>
    </b-modal>

  </b-container>
</template>

<script>
import {deleteAuthor, retrieveAuthor, updateAuthor} from "@/services/api";
import Title from "@/components/visuel/Title";
import AuteurFormulaire from "@/components/auteur/AuteurFormulaire";
import {mapState} from "vuex";
import {canEdit} from "@/services/rights";

export default {
  name: "LireAuteur",
  components: {AuteurFormulaire, Title},
  data: function () {
    return {
      auteur: {first_name: "", family_name: ""},
      message: ''

    }
  },
  methods: {
    getAuthor: function() {
      retrieveAuthor(this.$route.params.id).then(
        (response) => {
          if(response.data.success) {
            this.auteur.first_name = response.data.author.first_name;
            this.auteur.family_name = response.data.author.family_name;
          } else {
            console.log("erreur de récupération de l'auteur");
          }
        }
      );
    },
    updateAuthor: function() {
      // const formData = {first_name: this.first_name, family_name: this.family_name};
      updateAuthor(this.$route.params.id, this.auteur, this.$store.state.connectionInfo.token).then(
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
      deleteAuthor(this.$route.params.id, this.$store.state.connectionInfo.token).then(
        (response) => {
          if(response.status === 204) {
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
    ...mapState(["connected", "connectionInfo"]),
    canModify: function() {
      return this.connected && canEdit(this.connectionInfo.right);
    }
  }
}
</script>

<style scoped>

</style>