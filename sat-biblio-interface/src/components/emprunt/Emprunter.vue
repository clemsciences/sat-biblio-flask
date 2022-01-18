<template>
  <b-container>
    <Title title="Emprunter"
           info="Un emprunt permet à un emprunteur enregistré de ramener un enregistrement chez lui. Lors de l'emprunt, il faut se mettre d'accord sur la date de retour."
           id="id-borrowing"/>
    <b-form @submit.prevent="saveBorrowing">

      <SuggestionEnregistrement v-model="record"/>
      <SuggestionUtilisateur label="Emprunteur" v-model="borrower"/>
      <b-form-group label="Date de retour prévue">
        <b-form-datepicker v-model="dateComebackExpected"
                           placeholder="Choisissez une date"
                           label-close-button="Fermer"
                           label-no-date-selected="Aucune date sélectionnée"
                           label-help="Utilisez les flèches du clavier pour naviguer dans les dates du calendrier"
                           label-calendar="Calendrier"
                           label-nav="Navigation dans le calendrier"
                           label-today="Aujourd'hui"
                           label-prev-month="Mois précédent"
                           label-next-month="Mois suivant"
                           label-current-month="Mois courant"
                           locale="fr"
                           start-weekday="1"
                           size="sm"
                           :min="minDate"
                           :max="maxDate"
                           style="z-index: 9999"
        />
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
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    // 15th two months prior
    const minDate = new Date(today)
    // 15th in two months
    const maxDate = new Date(today)
    maxDate.setMonth(maxDate.getMonth() + 3)
    return {
      record: {value: -1, text: ""},
      comment: "",
      borrower: {value: -1, text: ""},
      isBorrowed: true,
      dateComebackExpected: null,
      message: "",
      minDate: minDate,
      maxDate: maxDate
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
      createBorrowing(formData, this.$store.state.connectionInfo.token).then(
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