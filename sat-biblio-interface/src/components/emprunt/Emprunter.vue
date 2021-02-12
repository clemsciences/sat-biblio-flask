<template>
  <div>
    <h2>Emprunter</h2>
    <b-form @submit.prevent="saveBorrowing">
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
      <b-button type="submit">Enregistrer</b-button>
    </b-form>
  </div>
</template>

<script>

import {createBorrowing} from "../../services/api";

export default {
  name: "Emprunter",
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

    saveBorrowing: function () {
      const formData = {
        record: this.record,
        comment: this.comment,
        borrowed: this.borrowed,
        borrower: this.borrower,
        dateComebackExpected: this.dateComebackExpected
      };
      createBorrowing(formData).then(
        (response) => {
          if(response.data.success) {
            console.log("borrowing registered")
          }
        }
    )
    }
  }
}
</script>

<style scoped>

</style>