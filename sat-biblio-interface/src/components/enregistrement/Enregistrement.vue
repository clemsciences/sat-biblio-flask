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

export default {
  name: "Enregistrement",
  components: {EnregistrementFormulaire, Title},
  data: function () {
    return {
      record: {
        selectedReference: {value: -1, text: ""},
        description: "",
        cote: "",
        annee: "",
        nb_exemplaire_supp: 0,
        provenance: "",
        mots_clef: "",
      },
      // validated: false,
      message: ""
    }
  },
  methods: {
    saveRecord: function () {
      const formData = {
          id_reference: this.record.selectedReference.value,
          description: this.record.description,
          cote: this.record.cote,
          annee: this.record.annee,
          nb_exemplaire_supp: this.record.nb_exemplaire_supp,
          provenance: this.record.provenance,
          mots_clef: this.record.mots_clef
      };
      createBookRecord(formData, this.$store.state.connectionInfo.token)
          .then((response) => {
            if(response.data.success) {
              console.log("record saved");
              this.message = "L'enregistrement a été sauvegardé.";
              this.record.selectedReference = {value: -1, text: ""};
              this.record.description = "";
              this.record.cote = "";
              this.record.annee = "";
              this.record.nb_exemplaire_supp = "";
              this.record.provenance = "";
              this.record.mots_clef = "";
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
}
</script>

<style scoped>

</style>