<template>
  <div>
    <h2>Emprunt</h2>
    <b-form @submit.prevent="updateBorrowing">
      <b-form-group label="Enregistrement">
        <b-form-input v-model="record"/>
      </b-form-group>
      <b-form-group label="Emprunteur">
        <b-form-input v-model="borrower"/>
      </b-form-group>
      <b-form-group label="Date de retour prévue">
        <b-form-datepicker v-model="dateComebackExpected"/>
      </b-form-group>
      <b-form-group label="Commentaire">
        <b-form-input v-model="comment"/>
      </b-form-group>
      <b-button type="submit">Sauvegarder</b-button>
    </b-form>
    <b-button @click="deleteBorrowing">Supprimer</b-button>
  </div>

</template>

<script>
import {deleteBorrowing, retrieveBorrowing, updateBorrowing} from "../../services/api";

export default {
  name: "LireEmprunt",
  data: function () {
    return {
      record: "",
      comment: "",
      borrower: "",
      borrowed: true,
      dateComebackExpected: null,
    }
  },
  methods: {
    getBorrowing: function() {
      retrieveBorrowing(this.$route.params.id).then(
          (response) => {
            if(response.data.success) {
              console.log(response);
              this.record = response.data.borrowing.record;
              this.comment = response.data.borrowing.comment;
              this.borrower = response.data.borrowing.borrower;
              this.borrowed = response.data.borrowing.borrowed;
              this.dateComebackExpected = response.data.borrowing.dateComebackExpected;
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
        record: this.record,
        comment: this.comment,
        borrowed: this.borrowed,
        borrower: this.borrower,
        dateComebackExpected: this.dateComebackExpected
      };
      updateBorrowing(this.$route.params.id, formData).then(
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
      deleteBorrowing(this.$route.params.id).then(
          (response) => {
            console.log(response);
            this.$router.replace("/emprunts");
          }
      ).catch(

      );
    }
  },
  mounted() {
    this.getBorrowing();
  }

}
</script>

<style scoped>

</style>