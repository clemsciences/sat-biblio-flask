<template>
  <BForm @submit.prevent="onSubmit">

    <SuggestionEnregistrement v-model="record"
                              :disabled="disabled || isUpdate"/>
    <div v-if="borrowing.record.value > 0 ">
      <BorrowingState :rendu="isUpdate ? borrowing.givenBack : null" :record-id="borrowing.record.value"/>
    </div>
    <SuggestionUtilisateur label="Emprunteur"
                           v-model="borrower"
                           :disabled="disabled || isUpdate"/>
    <BFormGroup label="Date d'emprunt">
      <b-form-datepicker v-model="borrowingDate"
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
    </BFormGroup>
    <BFormGroup label="Date de retour prévue">
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
                         style="z-index: 900"
                         label-reset-button="Réinitialiser"
                         :reset-button="true"
      />
    </BFormGroup>
    <div v-if="isUpdate">
      <BFormGroup label="Date de retour réel">
        <b-form-datepicker v-model="actualComebackDate"
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
      </BFormGroup>
    </div>
    <BFormGroup label="Commentaire">
      <b-form-textarea size="3" v-model="comment" :disabled="disabled"/>
    </BFormGroup>
    <BButton type="submit" :disabled="isIncorrect || disabled">Enregistrer</BButton>
    <span class="mx-3">{{ message }}</span>
  </BForm>
</template>

<script>
import SuggestionUtilisateur from "@/components/utilisateur/SuggestionUtilisateur.vue";
import SuggestionEnregistrement from "@/components/enregistrement/SuggestionEnregistrement.vue";
import {BookBorrowing} from "@/services/objectManager.js";
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
    record: {
      get() {
        return this.borrowing.record;
      },
      set(value) {
        this.$emit('update:record', value);
      }
    },
    borrower: {
      get() {
        return this.borrowing.borrower;
      },
      set(value) {
        this.$emit('update:borrower', value);
      }
    },
    borrowingDate: {
      get() {
        return this.borrowing.borrowingDate;
      },
      set(value) {
        this.$emit('update:borrowingDate', value);
      }
    },
    dateComebackExpected: {
      get() {
        return this.borrowing.dateComebackExpected;
      },
      set(value) {
        this.$emit('update:dateComebackExpected', value);
      }
    },
    actualComebackDate: {
      get() {
        return this.borrowing.actualComebackDate;
      },
      set(value) {
        this.$emit('update:actualComebackDate', value);
      }
    },
    comment: {
      get() {
        return this.borrowing.comment;
      },
      set(value) {
        this.$emit('update:comment', value);
      }
    },
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