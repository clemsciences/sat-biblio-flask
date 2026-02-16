<template>
  <BContainer>
    <AppTitle title="Nouvelle référence bibliographique - livre"
           info="Une référence bibliographique désigne les informations propres à un livre"
           id="id-ref"/>
    <div v-if="reference">
      <ReferenceLivrePrettyView :reference="reference"/>

      <ReferenceLivreFormulaire
          :reference="reference"
          :on-submit="saveReference"
          :message="message"
          @update:selectedAuthors="reference.selectedAuthors = $event"
          @update:authorsForm="reference.authorsForm = $event"
          @update:titre="reference.titre = $event"
          @update:lieu_edition="reference.lieu_edition = $event"
          @update:editeur="reference.editeur = $event"
          @update:annee="reference.annee = $event"
          @update:nb_page="reference.nb_page = $event"
          @update:description="reference.description = $event"
      />
    </div>

  </BContainer>
</template>

<script>
import {createBookReference} from "@/services/api.js";
import AppTitle from "@/components/visuel/AppTitle.vue";
import ReferenceLivreFormulaire from "@/components/reference_livre/ReferenceLivreFormulaire.vue";
import {canManage} from "@/services/rights.js";
import ReferenceLivrePrettyView from "@/components/reference_livre/ReferenceLivrePrettyView.vue";
import {BookReference} from "@/services/objectManager.js";

export default {
  name: "ReferenceLivre",
  components: {ReferenceLivrePrettyView, ReferenceLivreFormulaire, AppTitle},
  data: function () {
    return {
      reference: null,
      message: ""
    }
  },
  mounted() {
    this.reference = new BookReference();
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
        description: this.reference.description
      };

      createBookReference(formData, this.$store.state.connectionInfo.token)
        .then(
            (response) => {
              if(response.data.success) {
                this.message = "La référence a été créée."
                this.reference.clear();
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