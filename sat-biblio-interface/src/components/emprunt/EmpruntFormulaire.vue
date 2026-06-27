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
      <VueDatePicker v-model="borrowingDate"
                     placeholder="Date de l'emprunt"
                     :disabled="true"
                     :locale="dpLocale"
                     :week-start="1"
                     :time-config="{ enableTimePicker: false }"
                     :formats="{ input: 'dd/MM/yyyy' }"
                     :aria-labels="dpAriaLabels"
                     :action-row="dpActionRow"
      />
    </BFormGroup>
    <BFormGroup label="Date de retour prévue">
      <VueDatePicker v-model="dateComebackExpected"
                     placeholder="Choisissez une date"
                     :locale="dpLocale"
                     :week-start="1"
                     :time-config="{ enableTimePicker: false }"
                     :formats="{ input: 'dd/MM/yyyy' }"
                     :min-date="minDate"
                     :max-date="maxDate"
                     :clearable="true"
                     :aria-labels="dpAriaLabels"
                     :action-row="dpActionRow"
      />
    </BFormGroup>
    <div v-if="isUpdate">
      <BFormGroup label="Date de retour réel">
        <VueDatePicker v-model="actualComebackDate"
                       placeholder="Choisissez une date"
                       :locale="dpLocale"
                       :week-start="1"
                       :time-config="{ enableTimePicker: false }"
                       :formats="{ input: 'dd/MM/yyyy' }"
                       :min-date="borrowing.borrowingDate"
                       :max-date="today"
                       :clearable="true"
                       :aria-labels="dpAriaLabels"
                       :action-row="dpActionRow"
        />
      </BFormGroup>
    </div>
    <BFormGroup label="Commentaire">
      <BFormTextarea size="3" v-model="comment" :disabled="disabled"/>
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
import { fr } from 'date-fns/locale';


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
      today: today,
      dpLocale: fr,
      dpAriaLabels: {
        prevMonth: 'Mois précédent',
        nextMonth: 'Mois suivant',
        prevYear: 'Année précédente',
        nextYear: 'Année suivante',
        openMonthsOverlay: 'Sélectionner le mois',
        openYearsOverlay: 'Sélectionner l\'année',
        clearInput: 'Réinitialiser',
        calendarIcon: 'Calendrier',
        menu: 'Navigation dans le calendrier',
        input: 'Saisie de date',
        toggleOverlay: 'Basculer la vue',
        openTimePicker: 'Ouvrir le sélecteur d\'heure',
        closeTimePicker: 'Fermer le sélecteur d\'heure',
        timePicker: 'Sélecteur d\'heure',
        amPmButton: 'Basculer AM/PM',
        openTpOverlay: () => '',
        incrementValue: () => '',
        decrementValue: () => '',
      },
      dpActionRow: {
        selectBtnLabel: 'Sélectionner',
        cancelBtnLabel: 'Fermer',
        nowBtnLabel: 'Aujourd\'hui',
      },
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