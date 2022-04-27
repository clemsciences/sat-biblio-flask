<template>
  <b-container>
    <Title title="Nouvelle référence bibliographique - livre"
           info="Une référence bibliographique désigne les informations propres à un livre"
           id="id-ref"/>

    <ReferenceLivreFormulaire
        :reference="reference"
        :on-submit="saveReference"
        :message="message"
    />
  </b-container>
</template>

<script>
import {createBookReference} from "@/services/api";
import Title from "../visuel/Title";
import ReferenceLivreFormulaire from "@/components/reference_livre/ReferenceLivreFormulaire";
import {canManage} from "@/services/rights";

export default {
  name: "ReferenceLivre",
  components: {ReferenceLivreFormulaire, Title},
  data: function () {
    return {
      reference: {
        selectedAuthors: [],
        titre: "",
        lieu_edition: "",
        editeur: "",
        annee: "",
        nb_page: "",
        description: "",
      },
      message: ""
    }
  },
  methods: {
    saveReference: function () {
      const formData = {
        auteurs: this.reference.selectedAuthors,
        titre: this.reference.titre,
        lieu_edition: this.reference.lieu_edition,
        editeur: this.reference.editeur,
        annee: this.reference.annee,
        nb_page: this.reference.nb_page,
        valide: this.isManager,
        description: this.description
      };

      createBookReference(formData, this.$store.state.connectionInfo.token)
        .then(
            (response) => {
              if(response.data.success) {
                this.message = "La référence a été créée."
                console.log("créer une référence livresque");
                this.reference.selectedAuthors = [];
                this.reference.titre = "";
                this.reference.lieu_edition = "";
                this.reference.editeur = "";
                this.reference.annee = "";
                this.reference.nb_page = "";
                this.reference.description = "";
              } else {
                this.message = "La création de la référence a échoué."
              }
            }
        )
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