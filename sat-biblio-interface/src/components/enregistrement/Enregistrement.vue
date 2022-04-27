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
        annee: "",
        nb_exemplaire_supp: 0,
        provenance: "",
        mots_clef: "",
        row: ""
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
          annee: this.record.annee,
          nb_exemplaire_supp: this.record.nb_exemplaire_supp,
          provenance: this.record.provenance,
          mots_clef: this.record.mots_clef,
          valide: this.isManager,
          row: this.row
      };
      createBookRecord(formData, this.$store.state.connectionInfo.token)
          .then((response) => {
            if(response.data.success) {
              console.log("record saved");
              this.message = "L'enregistrement a été sauvegardé.";
              this.record.selectedReference = {value: -1, text: ""};
              this.record.cote = "";
              this.record.annee = "";
              this.record.nb_exemplaire_supp = "";
              this.record.provenance = "";
              this.record.mots_clef = "";
              this.record.row = "";
            } else {
              console.log("bizarre");
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