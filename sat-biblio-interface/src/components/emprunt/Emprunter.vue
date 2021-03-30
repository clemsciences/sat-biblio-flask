<template>
  <div>
    <h2>Emprunter</h2>
    <b-form @submit.prevent="saveBorrowing">

      <SuggestionEnregistrement v-model="record"/>
      <SuggestionUtilisateur label="Emprunteur" v-model="borrower"/>
      <b-form-group label="Date de retour prévue">
        <b-form-datepicker v-model="dateComebackExpected"/>
      </b-form-group>
      <b-form-group label="Commentaire">
        <b-form-textarea size="3" v-model="comment"/>
      </b-form-group>
      <b-button type="submit">Enregistrer</b-button>
    </b-form>
  </div>
</template>

<script>

import {createBorrowing} from "../../services/api";
import SuggestionEnregistrement from "../enregistrement/SuggestionEnregistrement";
import SuggestionUtilisateur from "../utilisateur/SuggestionUtilisateur";

export default {
  name: "Emprunter",
  components: {SuggestionUtilisateur, SuggestionEnregistrement},
  data: function () {
    return {
      record: {value: -1, text: ""},
      comment: "",
      borrower: {value: -1, text: ""},
      isBorrowed: true,
      dateComebackExpected: null,
    }
  },
  methods: {

    saveBorrowing: function () {
      const formData = {
        record: this.record.value,
        comment: this.comment,
        borrowed: this.isBorrowed,
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