<template>
  <b-form @submit.prevent="onSubmit">

    <SuggestionEnregistrement v-model="borrowing.record"
                              :disabled="disabled || isUpdate"/>
    <div v-if="borrowing.record.value > 0 ">
      <BorrowingState :rendu="isUpdate ? borrowing.givenBack : null" :record-id="borrowing.record.value"/>
    </div>
    <SuggestionUtilisateur label="Emprunteur"
                           v-model="borrowing.borrower"
                           :disabled="disabled || isUpdate"/>
    <b-form-group label="Date d'emprunt">
      <b-form-datepicker v-model="borrowing.borrowingDate"
                         placeholder="Date de l'emprunt"
                         :disabled="true"
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
      />
    </b-form-group>
    <b-form-group label="Date de retour prévue">
      <b-form-datepicker v-model="borrowing.dateComebackExpected"
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
                         style="z-index: 900"
                         label-reset-button="Réinitialiser"
                         :reset-button="true"
      />
    </b-form-group>
    <div v-if="isUpdate">
      <b-form-group label="Date de retour réel">
        <b-form-datepicker v-model="borrowing.actualComebackDate"
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
                           label-reset-button="Réinitialiser"
                           locale="fr"
                           start-weekday="1"
                           size="sm"
                           :min="borrowing.borrowingDate"
                           :max="today"
                           style="z-index: 900"
                           :reset-button="true"
        />
      </b-form-group>
    </div>
    <b-form-group label="Commentaire">
      <b-form-textarea size="3" v-model="borrowing.comment" :disabled="disabled"/>
    </b-form-group>
    <b-button type="submit" :disabled="isIncorrect || disabled">Enregistrer</b-button>
    <span class="mx-3">{{ message }}</span>
  </b-form>
</template>

<script>
import SuggestionUtilisateur from "@/components/utilisateur/SuggestionUtilisateur";
import SuggestionEnregistrement from "@/components/enregistrement/SuggestionEnregistrement";
import {BookBorrowing} from "@/services/objectManager";
import BorrowingState from "@/components/emprunt/BorrowingState.vue";


export default {
  name: "EmpruntFormulaire",
  components: {BorrowingState, SuggestionUtilisateur, SuggestionEnregistrement},
  props: {
    borrowing: BookBorrowing,
    onSubmit: Function,
    message: {
      type: String,
      default: ""
    },
    disabled: {
      type: Boolean,
      default: false
    },
    isUpdate: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const minDate = new Date(today)
    const maxDate = new Date(today)
    maxDate.setMonth(maxDate.getMonth() + 3)
    return {
      minDate: minDate,
      maxDate: maxDate,
      today: today
    }
  },
  methods: {},
  computed: {
    isIncorrect: function () {
      return this.borrowing.record.value < 0 ||
          this.borrowing.borrower.value < 0 ||
          !this.borrowing.dateComebackExpected;
    },
  },
}
</script>

<style scoped>

</style>