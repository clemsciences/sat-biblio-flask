<template>
  <b-container>
    <Title title="Emprunter"
           info="Un emprunt permet à un emprunteur enregistré de ramener un enregistrement chez lui. Lors de l'emprunt, il faut se mettre d'accord sur la date de retour."
           id="id-borrowing"/>
    <EmpruntFormulaire
        :borrowing="borrowing"
        :on-submit="saveBorrowing"
        :message="message"
        :is-update="false"
    />
    <b-button class="my-3" v-if="message.length > 0 || !isIncorrect" @click="reinit">Réinitialiser</b-button>

  </b-container>
</template>

<script>

import {createBorrowing} from "@/services/api";
import EmpruntFormulaire from "@/components/emprunt/EmpruntFormulaire";
import Title from "../visuel/Title";

export default {
  name: "Emprunter",
  components: {Title, EmpruntFormulaire},
  data: function () {
    return {
      borrowing: {
        record: {value: -1, text: ""},
        comment: "",
        borrower: {value: -1, text: ""},
        isBorrowed: true,
        dateComebackExpected: null,
      },
      message: "",
    }
  },
  methods: {
    saveBorrowing: function () {
      const formData = {
        record: this.borrowing.record.value,
        comment: this.borrowing.comment,
        borrowed: this.borrowing.isBorrowed,
        borrower: this.borrowing.borrower.value,
        dateComebackExpected: this.borrowing.dateComebackExpected,
      };
      createBorrowing(formData, this.$store.state.connectionInfo.token).then(
        (response) => {
          if(response.data.success) {
            console.log("borrowing registered");
            this.reinitBorrowing()
            this.message = "L'emprunt a correctement été enregistré. Un courriel a été envoyé à l'emprunteur.";
          } else {
            this.message = "Echec de l'enregistrement de l'emprunt.";
          }
        }
    )
    },
    reinitBorrowing() {
      this.borrowing.record = {value: -1, text: ""};
      this.borrowing.comment = "";
      this.borrowing.borrower = {value: -1, text: ""};
      this.borrowing.isBorrowed = true;
      this.borrowing.dateComebackExpected = null;
    },
    reinit() {
      this.reinitBorrowing();
      this.message = "";
    }
  },
  computed: {
    isIncorrect: function () {
      return Object.keys(this.borrowing.record).length === 0 ||
          this.borrowing.record.value < 0 ||
          this.borrowing.borrower.value < 0 ||
          Object.keys(this.borrowing.borrower).length === 0 ||
          !this.borrowing.dateComebackExpected ;
    }
  },
  watch: {
    borrowing: {
      handler(newV) {
        console.log("newV", newV);
      },
      deep: true
    }

  }
}
</script>

<style scoped>

</style>