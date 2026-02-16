<template>
  <BContainer>
    <AppTitle title="Nouvel enregistrement"
           info="Un enregistrement désigne les informations sur un livre tel qu'il est enregistré dans la bibliothèque."
           id="id-record"/>
    <EnregistrementFormulaire
        :record="record"
        :on-submit="saveRecord"
        :message="message"
        @update:selectedReference="record.selectedReference = $event"
        @update:cote="record.cote = $event"
        @update:annee_obtention="record.annee_obtention = $event"
        @update:provenance="record.provenance = $event"
        @update:aide_a_la_recherche="record.aide_a_la_recherche = $event"
        @update:observations="record.observations = $event"
        @update:row="record.row = $event"
    />
  </BContainer>
</template>

<script>
import {createBookRecord} from "@/services/api.js";
import AppTitle from "@/components/visuel/AppTitle.vue";
import EnregistrementFormulaire from "@/components/enregistrement/EnregistrementFormulaire.vue";
import {canManage} from "@/services/rights.js";

export default {
  name: "EnregistrementView",
  components: {EnregistrementFormulaire, AppTitle},
  data: function () {
    return {
      record: {
        selectedReference: {value: -1, text: ""},
        cote: "",
        annee_obtention: "",
        commentaire: "",
        nb_exemplaire_supp: 0,
        provenance: "",
        aide_a_la_recherche: "",
        observations: "",
        // region meta
        row: ""
        // endregion
      },
      // validated: false,
      message: ""
    }
  },
  methods: {
    saveRecord: function () {
      const formData = {
          id_reference: this.record.selectedReference.value,
          cote: this.record.cote,
          annee: this.record.annee_obtention,
          nb_exemplaire_supp: this.record.nb_exemplaire_supp,
          provenance: this.record.provenance,
          aide_a_la_recherche: this.record.aide_a_la_recherche,
          valide: this.isManager,
          row: this.record.row
      };
      createBookRecord(formData, this.$store.state.connectionInfo.token)
          .then((response) => {
            if(response.data.success) {
              this.message = "L'enregistrement a été sauvegardé.";
              this.record.clear();
            } else {
              this.message = "Echec de la sauvegarde de l'enregistrement.";
            }
          })
          .catch(
            (reason) => {
              console.log(reason);
            }
          );
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