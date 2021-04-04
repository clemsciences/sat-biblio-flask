<template>
  <b-container>
    <Title title="Emprunter"
           info="Un emprunt permet à un emprunteur enregistré de ramener un enregistrement chez lui. Lors de l'emprunt, il faut se mettre d'accord sur la date de retour."
           id="id-borrowing"/>
    <b-form @submit.prevent="saveBorrowing">

      <SuggestionEnregistrement v-model="record"/>
      <SuggestionUtilisateur label="Emprunteur" v-model="borrower"/>
      <b-form-group label="Date de retour prévue">
        <b-form-datepicker v-model="dateComebackExpected"/>
      </b-form-group>
      <b-form-group label="Commentaire">
        <b-form-textarea size="3" v-model="comment"/>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect">Enregistrer</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>
  </b-container>
</template>

<script>

import {createBorrowing} from "../../services/api";
import SuggestionEnregistrement from "../enregistrement/SuggestionEnregistrement";
import SuggestionUtilisateur from "../utilisateur/SuggestionUtilisateur";
import Title from "../visuel/Title";

export default {
  name: "Emprunter",
  components: {Title, SuggestionUtilisateur, SuggestionEnregistrement},
  data: function () {
    return {
      record: {value: -1, text: ""},
      comment: "",
      borrower: {value: -1, text: ""},
      isBorrowed: true,
      dateComebackExpected: null,
      message: ""
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
            console.log("borrowing registered");
            this.message = "L'emprunt a correctement été enregistré. Un courriel a été envoyé à l'emprunteur."
          } else {
            this.message = "Echec de l'enregistrement de l'emprunt."
          }
        }
    )
    }
  },
  computed: {
    isIncorrect: function () {
      return this.record.value < 0 || this.borrower.length === 0;
    }
  }
}
</script>

<style scoped>

</style>