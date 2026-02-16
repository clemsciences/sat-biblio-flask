<template>
  <BContainer>
    <AppTitle title="Nouvel enregistrement"
           id="id-enregistrement-complet"
           info=""
    />
    <EnregistrementCompletFormulaire
      :record-with-reference="recordWithReference"
      :save="save"
      :disabled="!canModify"
      :message="message"
      @update:authors="recordWithReference.authors = $event"
      @update:authorsForm="recordWithReference.authorsForm = $event"
      @update:titre="recordWithReference.titre = $event"
      @update:lieu_edition="recordWithReference.lieu_edition = $event"
      @update:editeur="recordWithReference.editeur = $event"
      @update:publication_annee="recordWithReference.publication_annee = $event"
      @update:nb_page="recordWithReference.nb_page = $event"
      @update:reference_description="recordWithReference.reference_description = $event"
      @update:cote="recordWithReference.cote = $event"
      @update:annee_entree="recordWithReference.annee_entree = $event"
      @update:provenance="recordWithReference.provenance = $event"
      @update:aide_a_la_recherche="recordWithReference.aide_a_la_recherche = $event"
      @update:observations="recordWithReference.observations = $event"
    />


  </BContainer>

</template>

<script>

import AppTitle from "../visuel/AppTitle.vue";
import {BookRecordWithReference} from "@/services/objectManager";
import {canContribute, canEdit} from "@/services/rights";
import EnregistrementCompletFormulaire from "./EnregistrementCompletFormulaire.vue";
import {createBookRecordWithReference} from "@/services/api";
import {mapState} from "vuex";

export default {
  name: "CreationEnregistrementComplet",
  components: {EnregistrementCompletFormulaire, AppTitle},
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      message: "",
      recordWithReference: new BookRecordWithReference(),
      authors: [],
    }
  },
  mounted() {

  },
  methods: {
    save() {
      createBookRecordWithReference(this.recordWithReference, this.$store.state.connectionInfo.token).then(
          (response) => {
            if(response.data.success) {
              this.recordWithReference.clear();
              this.message = "Enregistrement effectué."
            } else {
              this.message = "Echec de la sauvegarde"
            }
          }
      )

    }
  },
  computed: {
    ...mapState(["connected", "connectionInfo"]),
    isManager: function() {
      return canContribute(this.$store.getters.getUserRight);
    },
    canModify: function() {
      return this.connected && canEdit(this.connectionInfo.right);
    },
  }

}
</script>

<style scoped>

</style>