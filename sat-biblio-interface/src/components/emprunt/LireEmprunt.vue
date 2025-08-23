<template>
  <b-container>
    <Title
        id="id-emprunt-lire"
        info="Fiche d'un emprunt de livre."
        title="Emprunt"/>
    <EmpruntFormulaire
      :on-submit="updateBorrowing"
      :borrowing="borrowing"
      :message="message"
      :disabled="!canModify"
      :is-update="true"
    />
    <b-button class="my-3" v-if="canModify" :disabled="!canModify"
              v-b-modal.suppression>
      Supprimer
    </b-button>
    <b-modal id="suppression" title="Suppression de l'emprunt"
        cancel-title="Annuler" ok-title="Supprimer" @ok="deleteBorrowing">
        <p>Êtes-vous sûr de supprimer cet emprunt ?</p>
      </b-modal>
  </b-container>

</template>

<script>
import {deleteBorrowing, retrieveBorrowing, updateBorrowing} from "@/services/api";
import EmpruntFormulaire from "@/components/emprunt/EmpruntFormulaire";
import Title from "@/components/visuel/Title";
import {mapState} from "vuex";
import {canEdit} from "@/services/rights";
import {BookBorrowing} from "@/services/objectManager";

export default {
  name: "LireEmprunt",
  components: {EmpruntFormulaire, Title},
  data: function () {
    return {
      borrowing: new BookBorrowing(),
      message: "",
      borrowingId: parseInt(this.$route.params.id),
    }
  },
  methods: {
    getBorrowing: function() {
      retrieveBorrowing(this.$route.params.id).then(
          (response) => {
            if(response.data.success) {
              console.log(response.data.borrowing);

              let receivedBorrowing = response.data.borrowing;
              this.borrowing.record.value = receivedBorrowing.id_enregistrement;
              this.borrowing.record.text = receivedBorrowing.enregistrement.reference.titre+" "+response.data.borrowing.enregistrement.cote;
              this.borrowing.manager.value = receivedBorrowing.gestionnaire.first_name+" "+response.data.borrowing.gestionnaire.family_name;
              this.borrowing.manager.text = receivedBorrowing.gestionnaire;
              this.borrowing.comment = receivedBorrowing.comment;
              this.borrowing.borrower.value = receivedBorrowing.id_emprunteur;
              // this.borrowing.borrower.text = receivedBorrowing.emprunteur;
              this.borrowing.borrower.text = receivedBorrowing.emprunteur.first_name+" "+response.data.borrowing.emprunteur.family_name;
              this.borrowing.isBorrowed = receivedBorrowing.emprunte;
              this.borrowing.dateComebackExpected = receivedBorrowing.date_retour_prevu;
              this.borrowing.borrowingDate = receivedBorrowing.date_emprunt;
              this.borrowing.actualComebackDate = receivedBorrowing.date_retour_reel;
              this.borrowing.givenBack = receivedBorrowing.rendu;
            }
          }
      ).catch(
          (reason) => {
            console.log(reason)
          }
      )
    },
    updateBorrowing: function () {
      const formData = {
        id_enregistrement: this.borrowing.record.value,
        commentaire: this.borrowing.comment,
        emprunte: this.borrowing.isBorrowed,
        id_emprunteur: this.borrowing.borrower.value,
        date_retour_prevu: this.borrowing.dateComebackExpected,
        date_retour_reel: this.borrowing.actualComebackDate,
        rendu: this.borrowing.givenBack

      };
      updateBorrowing(this.$route.params.id, {borrowing: formData}, this.$store.state.connectionInfo.token).then(
          (response) => {
            if(response.data.success) {
              let receivedBorrowing = response.data.borrowing;
              // this.borrowing.record.value = receivedBorrowing.id_enregistrement;
              // this.borrowing.record.text = receivedBorrowing.enregistrement.reference.titre+" "+response.data.borrowing.enregistrement.cote;
              // this.borrowing.manager.value = receivedBorrowing.gestionnaire.first_name+" "+response.data.borrowing.gestionnaire.family_name;
              // this.borrowing.manager.text = receivedBorrowing.gestionnaire;
              // this.borrowing.comment = receivedBorrowing.comment;
              // this.borrowing.borrower.value = receivedBorrowing.id_emprunteur;
              // // this.borrowing.borrower.text = receivedBorrowing.emprunteur;
              // this.borrowing.borrower.text = receivedBorrowing.emprunteur.first_name+" "+response.data.borrowing.emprunteur.family_name;
              // this.borrowing.isBorrowed = receivedBorrowing.emprunte;
              // this.borrowing.dateComebackExpected = receivedBorrowing.date_retour_prevu;
              // this.borrowing.borrowingDate = receivedBorrowing.date_emprunt;
              // this.borrowing.actualComebackDate = receivedBorrowing.date_retour_reel;
              this.borrowing.givenBack = receivedBorrowing.rendu;
              console.log("new value rendu: "+this.borrowing.givenBack);

              this.message = response.data.message;
            }
          }
      ).catch(
          (reason => {
            console.error("borrowing update failed "+reason);
          })
      );
    },
    deleteBorrowing: function () {
      deleteBorrowing(this.$route.params.id, this.$store.state.connectionInfo.token).then(
          (response) => {
            console.log(response);
            if(response.status === 204) {
              this.$router.replace("/emprunts");
            } else {
              this.message = "Impossible de supprimer l'emprunt.";
            }
          }
      ).catch(

      );
    }
  },
  mounted() {
    this.getBorrowing();
  },
  computed: {
    ...mapState(["connected", "connectionInfo"]),
    canManage() {
      return this.$store.getters.canManage;
    },
    canModify() {
      return this.connected && canEdit(this.connectionInfo.right);
    }
  }
}
</script>

<style scoped>

</style>