<template>
  <BContainer>
    <AppTitle title="Enregistrement"
           info=""
           id=""/>
    <JsonLdHeader :json-data="record"/>

    <BCard>
      <BCardTitle title="Fiche"/>
      <BCardBody>
<!--        <BNFSearchBadge :title="reference.titre" labelPrefix=" - Titre"/>-->
<!--      <ValidEntry v-if="false" :approved="record.valide"/>-->
      <BorrowingState v-if="isConnected" :recordId="recordId"/>
      <BCardHeader>
        <EnregistrementPrettyView :record="record"/>
      </BCardHeader>
      <EnregistrementFormulaire
          :message="message"
          :on-submit="updateRecord"
          :record="record"
          :disabled="!canModify"
          @update:selectedReference="record.selectedReference = $event"
          @update:cote="record.cote = $event"
          @update:annee_obtention="record.annee_obtention = $event"
          @update:provenance="record.provenance = $event"
          @update:aide_a_la_recherche="record.aide_a_la_recherche = $event"
          @update:observations="record.observations = $event"
          @update:row="record.row = $event"
      />
      <BButton @click="showSuppressionModal = true" class="my-3" v-if="canModify" :disabled="!canModify">Supprimer</BButton>
      <BModal id="suppression" v-model="showSuppressionModal" title="Suppression de l'enregistrement"
          cancel-title="Annuler" ok-title="Supprimer" @ok="deleteRecord">
          <p>Êtes-vous sûr de supprimer cet enregistrement ?</p>
      </BModal>
      <ArkInput :ark-name="record.ark_name"/>
      </BCardBody>
    </BCard>


    <BCard>
        <BCardTitle title="Entrées liées"/>
        <BCardBody>
          <BButton v-b-toggle.collapse-bound class="my-2">Voir les entrées liées</BButton>
          <BCollapse id="collapse-bound" class="my-2">
            <liste-entrees-enregistrement :record-id="recordId"/>
            <list-borrowings-of-record :record-id="recordId"/>
          </BCollapse>
        </BCardBody>
    </BCard>
  </BContainer>
</template>

<script>
import {deleteBookRecord, retrieveBookRecord, updateBookRecord} from "@/services/api.js";
import AppTitle from "@/components/visuel/AppTitle.vue";
import EnregistrementFormulaire from "@/components/enregistrement/EnregistrementFormulaire.vue";
import {mapState} from "vuex";
import {canEdit} from "@/services/rights.js";
// import ValidEntry from "@/components/visuel/ValidEntry";
import ListeEntreesEnregistrement from "@/components/entrees/ListeEntreesEnregistrement.vue";
import BorrowingState from "@/components/emprunt/BorrowingState.vue";
import ListBorrowingsOfRecord from "@/components/emprunt/ListBorrowingsOfRecord.vue";
import EnregistrementPrettyView from "@/components/enregistrement/EnregistrementPrettyView.vue";
import {Record} from "@/services/objectManager.js";
import ArkInput from "@/components/ark/ArkInput.vue";
import JsonLdHeader from "@/components/web_semantics/JsonLdHeader.vue";

export default {
  name: "LireEnregistrement",
  components: {
    JsonLdHeader,
    ArkInput,
    EnregistrementPrettyView,
    ListeEntreesEnregistrement,
    // ValidEntry,
    EnregistrementFormulaire,
    AppTitle,
    BorrowingState,
    ListBorrowingsOfRecord},
  data: function () {
    return {
      record: new Record(),
      message: "",
      recordId: parseInt(this.$route.params.id),
      showSuppressionModal: false,
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
              this.record.reference = value.data.enregistrement.reference;
              // this.record.description = value.data.enregistrement.description;
              this.record.cote = value.data.enregistrement.cote;
              this.record.annee_obtention = value.data.enregistrement.annee_obtention;
              // this.record.nb_exemplaire_supp = value.data.enregistrement.nb_exemplaire_supp;
              this.record.provenance = value.data.enregistrement.provenance;
              this.record.aide_a_la_recherche = value.data.enregistrement.aide_a_la_recherche;
              this.record.observations = value.data.enregistrement.observations;
              this.record.valide = value.data.enregistrement.valide;
              this.record.row = value.data.enregistrement.row;
              this.record.ark_name = value.data.enregistrement.ark_name;

            }
          }
      )
    },
    updateRecord: function() {
      const formData = {
          id_reference: this.record.selectedReference.value,
          // description: this.record.description,
          cote: this.record.cote,
          annee: this.record.annee,
          // nb_exemplaire_supp: this.record.nb_exemplaire_supp,
          provenance: this.record.provenance,
          aide_a_la_recherche: this.record.aide_a_la_recherche,
          observations: this.record.observations,
          commentaire: this.record.commentaire,
          row: this.record.row
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
                if(response.status === 204) {
                  console.log("référence livresque supprimée");
                  this.$router.push("/auteur/liste")
                } else {
                  this.message = "L'enregistrement n'a pas pu être supprimé."
                }
              }
          )
    },
    goToRef: function() {
      let routeData = this.$router.resolve(`/reference-livre/lire/${this.selectedReference.value}`);
      window.open(routeData.href, '_blank');
    },
  },
  mounted() {
    this.getBookRecord();
  },
  computed: {
    ...mapState(["connected", "connectionInfo"]),
    canModify: function() {
      return this.connected && canEdit(this.connectionInfo.right);
    },
    canManage() {
      return this.$store.getters.canManage;
    },
    isConnected() {
      return this.connected;
    }
  }
}
</script>

<style scoped>

</style>