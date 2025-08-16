<template>
  <b-container>
    <Title title="Nouvel enregistrement"
           info="Un enregistrement désigne les informations sur un livre tel qu'il est enregistré dans la bibliothèque."
           id="id-record"/>
    <EnregistrementFormulaire
        :record="record"
        :on-submit="saveRecord"
        :message="message"/>
  </b-container>
</template>

<script>
import {createBookRecord} from "@/services/api";
import Title from "../visuel/Title";
import EnregistrementFormulaire from "@/components/enregistrement/EnregistrementFormulaire";
import {canManage} from "@/services/rights";

export default {
  name: "Enregistrement",
  components: {EnregistrementFormulaire, Title},
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