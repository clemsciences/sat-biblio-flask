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
    />
    <b-button class="my-3" v-if="canModify" :disabled="!canModify"
              @click="deleteBorrowing"
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
import {deleteBorrowing, retrieveBorrowing, updateBorrowing} from "../../services/api";
import EmpruntFormulaire from "@/components/emprunt/EmpruntFormulaire";
import Title from "@/components/visuel/Title";
import {mapState} from "vuex";
import {canEdit} from "@/services/rights";

export default {
  name: "LireEmprunt",
  components: {EmpruntFormulaire, Title},
  data: function () {
    return {
      borrowing: {
        record: {value: -1, text: ""},
        comment: "",
        borrower: {value: -1, text: ""},
        borrowed: true,
        dateComebackExpected: null,
        borrowingDate: null,
        actualComebackDate: null,
        givenBack: false,
        manager: {value: -1, text: ""},
      },
      message: "",
      borrowingId: parseInt(this.$route.params.id),
    }
  },
  methods: {
    getBorrowing: function() {
      retrieveBorrowing(this.$route.params.id).then(
          (response) => {
            if(response.data.success) {
              console.log(response);
              this.borrowing.record.value = response.data.borrowing.id_enregistrement;
              this.borrowing.record.text = response.data.borrowing.enregistrement.reference.titre+" "+response.data.borrowing.enregistrement.cote;
              this.borrowing.manager.value = response.data.borrowing.gestionnaire.first_name+" "+response.data.borrowing.gestionnaire.family_name;
              this.borrowing.manager.text = response.data.borrowing.gestionnaire;
              this.borrowing.comment = response.data.borrowing.comment;
              this.borrowing.borrower.value = response.data.borrowing.id_emprunteur;
              // this.borrowing.borrower.text = response.data.borrowing.emprunteur;
              this.borrowing.borrower.text = response.data.borrowing.emprunteur.first_name+" "+response.data.borrowing.emprunteur.family_name;
              this.borrowing.borrowed = response.data.borrowing.emprunte;
              this.borrowing.dateComebackExpected = response.data.borrowing.date_retour_prevu;
              this.borrowing.borrowingDate = response.data.borrowing.date_emprunt;
              this.borrowing.actualComebackDate = response.data.borrowing.date_retour_reel;
              this.borrowing.givenBack = response.data.borrowing.rendu;
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
        record: this.borrowing.record,
        comment: this.borrowing.comment,
        borrowed: this.borrowing.borrowed,
        borrower: this.borrowing.borrower,
        dateComebackExpected: this.borrowing.dateComebackExpected
      };
      updateBorrowing(this.$route.params.id, formData, this.$store.state.connectionInfo.token).then(
          (response) => {
            if(response.data.success) {
              console.log("borrowing updated");
            }
          }
      ).catch(
          (reason => {
            console.log("borrowing update failed "+reason);
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