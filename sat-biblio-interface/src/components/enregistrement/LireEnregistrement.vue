<template>
  <b-container>
    <Title title="Enregistrement"
           info=""
           id=""/>
    <EnregistrementFormulaire
        :message="message"
        :on-submit="updateRecord"
        :record="record"
        :disabled="!canModify"
    />
    <b-button v-b-modal.suppression class="my-3" :disabled="!canModify">Supprimer</b-button>
    <b-modal id="suppression" title="Suppression de l'enregistrement"
        cancel-title="Annuler" ok-title="Supprimer" @ok="deleteRecord">
        <p>Êtes-vous sûr de supprimer cet enregistrement ?</p>
      </b-modal>
  </b-container>
</template>

<script>
import {deleteBookRecord, retrieveBookRecord, updateBookRecord} from "@/services/api";
import Title from "../visuel/Title";
import EnregistrementFormulaire from "@/components/enregistrement/EnregistrementFormulaire";
import {mapState} from "vuex";
import {canEdit} from "@/services/rights";

export default {
  name: "LireEnregistrement",
  components: {EnregistrementFormulaire, Title},
  data: function () {
    return {
      record: {
        reference: {value: -1, text: ""},
        selectedReference: {text: "", value: -1},
        suggestedReferences: [],
        description: "",
        cote: "",
        annee: "",
        nb_exemplaire_supp: 0,
        provenance: "",
        mots_clef: "",
        validated: false,
      },
      message: "",
    }
  },
  methods: {
    addReference: function(event) {
      this.record.selectedReference = event;
    },
    getBookRecord: function() {
      retrieveBookRecord(this.$route.params.id).then(
          (value) => {
            if(value.data.success && value.data.enregistrement) {
              this.record.selectedReference = value.data.enregistrement.reference;
              this.record.description = value.data.enregistrement.description;
              this.record.cote = value.data.enregistrement.cote;
              this.record.annee = value.data.enregistrement.annee;
              this.record.nb_exemplaire_supp = value.data.enregistrement.nb_exemplaire_supp;
              this.record.provenance = value.data.enregistrement.provenance;
              this.record.mots_clef = value.data.enregistrement.mots_clef;
              this.record.validated = value.data.enregistrement.validated;
            }
          }
      )
    },
    updateRecord: function() {
      const formData = {
          id_reference: this.record.selectedReference.value,
          description: this.record.description,
          cote: this.record.cote,
          annee: this.record.annee,
          nb_exemplaire_supp: this.record.nb_exemplaire_supp,
          provenance: this.record.provenance,
          mots_clef: this.record.mots_clef
      };
      updateBookRecord(this.$route.params.id, formData, this.$store.state.connectionInfo.token)
          .then((response) => {
            if(response.data.success) {
              console.log("record saved");
              this.message = "L'enregistrement a été mise à jour.";
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
    },
    deleteRecord: function() {
      deleteBookRecord(this.$route.params.id, this.$store.state.connectionInfo.token)
          .then(
              (response) => {
                if(response.data.success) {
                  console.log("référence livresque supprimée");
                  this.$router.push("/auteur/liste")
                } else {
                  this.message = "La référence n'a pas pu être supprimée."
                }
              }
          )
    },
    goToRef: function() {
      let routeData = this.$router.resolve(`/reference-livre/lire/${this.selectedReference.value}`);
      window.open(routeData.href, '_blank');
    }
  },
  mounted() {
    this.getBookRecord();
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