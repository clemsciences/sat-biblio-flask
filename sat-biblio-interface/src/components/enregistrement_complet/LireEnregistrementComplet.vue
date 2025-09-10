<template>
  <b-container>
    <Title title="Enregistrement" info=""/>

    <ReferenceLivrePrettyView :reference="reference"/>

    <EnregistrementCompletFormulaire
        :record-with-reference="bookRecordWithReference"
        :reference-id="referenceId"
        :disabled="!canModify"
        :save="update"
        :message="message"
    />

  </b-container>

</template>

<script>
import Title from "../visuel/Title.vue";
import EnregistrementCompletFormulaire from "./EnregistrementCompletFormulaire.vue";
import {BookRecordWithReference, BookReference} from "@/services/objectManager";
import {retrieveBookRecordWithReference, updateBookRecordWithReference} from "@/services/api";
import {mapState} from "vuex";
import {canEdit} from "@/services/rights";
import ReferenceLivrePrettyView from "@/components/reference_livre/ReferenceLivrePrettyView.vue";

export default {
  name: "LireEnregistrementComplet",
  components: {ReferenceLivrePrettyView, EnregistrementCompletFormulaire, Title},
  data() {
    return {
      bookRecordWithReference: new BookRecordWithReference(),
      message: "",
      recordId: parseInt(this.$route.params.id),
      referenceId: null,
      reference: new BookReference()

    }
  },
  mounted() {
    this.retrieve();
  },
  methods: {
    retrieve() {
      retrieveBookRecordWithReference(this.recordId).then(
          (response) => {
            if(response.data.success) {
              const recordWithReference = response.data.record_with_reference;
              this.referenceId = response.data.reference.id;
              this.reference.annee = response.data.reference.annee;
              this.reference.titre = response.data.reference.titre;
              this.reference.ark_name = response.data.reference.ark_name;
              this.reference.description = response.data.reference.description;
              this.reference.nb_page = response.data.reference.nb_page;
              this.reference.editeur = response.data.reference.editeur;
              this.reference.lieu_edition = response.data.reference.lieu_edition;
              this.reference.selectedAuthors = response.data.reference.selectedAuthors;
              this.reference.authorsForm = response.data.reference.authorsForm;
              console.log(this.reference);

              this.bookRecordWithReference.authors = recordWithReference.authors;
              this.bookRecordWithReference.selectedAuthors = recordWithReference.authors;
              this.bookRecordWithReference.titre = recordWithReference.titre;
              this.bookRecordWithReference.lieu_edition = recordWithReference.lieu_edition;
              this.bookRecordWithReference.editeur = recordWithReference.editeur;
              this.bookRecordWithReference.publication_annee = recordWithReference.publication_annee;
              this.bookRecordWithReference.nb_page = recordWithReference.nb_page;
              this.bookRecordWithReference.valide = recordWithReference.valide;
              this.bookRecordWithReference.reference_description = recordWithReference.description;
              this.bookRecordWithReference.reference_ark_name = recordWithReference.ark_name;

              this.bookRecordWithReference.cote = recordWithReference.cote;
              this.bookRecordWithReference.annee_entree = recordWithReference.annee_entree;
              this.bookRecordWithReference.provenance = recordWithReference.provenance;
              this.bookRecordWithReference.aide_a_la_recherche = recordWithReference.aide_a_la_recherche;
              this.bookRecordWithReference.observations = recordWithReference.observations;
              this.bookRecordWithReference.record_ark_name = recordWithReference.ark_name;
            }
          }
      );
    },
    update() {
      const data = {

      }
      updateBookRecordWithReference(this.recordId, data, this.$store.state.connectionInfo.token).then(
          (response) => {
            if(response.data.success) {
              if(response.data.success) {
                  this.message = "Bien mis à jour.";
                } else {
                  this.message = "Echec de la mise à jour .";
                }
            }
          }
      )
    },
  },
  computed: {
      ...mapState(["connected", "connectionInfo"]),
      canManage() {
        return this.$store.getters.canManage;
      },
      canModify: function() {
        return this.connected && canEdit(this.connectionInfo.right);
      },

    }
}
</script>

<style scoped>

</style>