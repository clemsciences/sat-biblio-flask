<template>
  <b-container>
    <Title title="Nouvel auteur"
           info="Un auteur est un individu qui a participé à la rédaction d'au moins un ouvrage."
           id="id-auteur"/>
    <AuteurFormulaire
        :auteur="auteur"
        :on-submit="onSubmit"
        :message="message"/>
  </b-container>
</template>

<script>
import {createAuthor} from "@/services/api";
import Title from "../visuel/Title";
import AuteurFormulaire from "@/components/auteur/AuteurFormulaire";
import {canManage} from "@/services/rights";
import {Author} from "@/services/objectManager";

export default {
  name: "Auteur",
  components: {AuteurFormulaire, Title},
  data: function () {
    return {
      auteur: new Author(),
      message: ''
    };
  },
  mounted() {
    this.auteur.validated = this.isManager;
  },
  methods: {
    onSubmit: function() {
      if (this.auteur.first_name.length > 0 && this.auteur.family_name.length > 0) {
        createAuthor(this.auteur, this.$store.state.connectionInfo.token).then(
            (response) => {
              if (response.data.success) {
                this.message = "L'auteur " + this.auteur.first_name + " " + this.auteur.family_name + " a été correctement créé.";
                this.first_name = "";
                this.family_name = "";
              } else {
                this.message = "Impossible de sauvegarder l'auteur."
              }
            }
        ).catch(
            (reason => {
              if(reason.response.data && reason.response.data.message) {
                this.message = reason.response.data.message
              } else {
                this.message = "Il y a une erreur réseau."
              }
            })
        );
      } else if(this.auteur.first_name.length === 0) {
        this.message = "Le prénom ne peut être vide.";
      } else if (this.auteur.family_name.length === 0) {
        this.message = "Le nom de famille ne peut être vide.";
      }
    }
  },
  computed: {
    isManager: function() {
      return canManage(this.$store.getters.getUserRight);
    }
  }
}
</script>

<style scoped>

</style>