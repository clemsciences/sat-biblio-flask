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
import {BookBorrowing} from "@/services/objectManager";

export default {
  name: "Emprunter",
  components: {Title, EmpruntFormulaire},
  data: function () {
    return {
      borrowing: new BookBorrowing(),
      message: "",
    }
  },
  mounted() {
    this.reinit();
  },
  methods: {
    saveBorrowing: function () {
      this.borrowing.isBorrowed = true;
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
            this.reinitBorrowing();
            this.message = "L'emprunt a correctement été enregistré. Un courriel a été envoyé à l'emprunteur.";
          } else {
            this.message = `Echec de l'enregistrement de l'emprunt.${response.data.message.length > 0 ? ' '+response.data.message : ''}`;
          }
        }
    )
    },
    reinitBorrowing() {
      this.borrowing.clear();
      this.borrowing.isBorrowed = false;
      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      this.borrowing.borrowingDate = today;
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