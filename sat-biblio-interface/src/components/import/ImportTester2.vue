<template>
  <b-container>
    <b-row>
      <b-form-input readonly v-model="currentRow"/>
    </b-row>
    <b-row>
      <b-col>
        <b-button @click="goToPreviousRow">Précédent</b-button>
      </b-col>
      <b-col>
        <b-button @click="goToNextRow">Suivant</b-button>
      </b-col>

    </b-row>
    <b-row>

      <b-col cols="10">
        <AuteurFormulaire v-for="author in authors"
                          :key="`${author.first_name}_${author.family_name}`"
                          :auteur="author"
                          :on-submit="saveAuthor"/>
        <ReferenceLivreFormulaire :on-submit="saveReference" :reference="reference"/>
        <EnregistrementFormulaire :on-submit="saveRecord" :record="record"/>
      </b-col>
    </b-row>
    <b-row><b-button @click="saveRow">Sauvegarder la ligne</b-button></b-row>
  </b-container>
</template>

<script>
import axios from "axios";
import AuteurFormulaire from "@/components/auteur/AuteurFormulaire";
import ReferenceLivreFormulaire from "@/components/reference_livre/ReferenceLivreFormulaire";
import EnregistrementFormulaire from "@/components/enregistrement/EnregistrementFormulaire";
import {Author, BookReference, Record} from "@/services/objectManager";

export default {
  name: "ImportTester2",
  components: {
    EnregistrementFormulaire,
    ReferenceLivreFormulaire,
    AuteurFormulaire
  },
  data: function() {
    return {
      rows: [],
      currentRow: 0,
      rowsAlreadySaved: [],

      result: '',
      authorsResult: '',
      refResult: '',
      authors: [new Author()],
      reference: new BookReference(),
      record: new Record(),
    }
  },
  methods: {
    loadRows: function (ctx, callback) {
      let params = `page=${ctx.currentPage}&size=${ctx.perPage}&sortBy=${ctx.sortBy}`;
      axios.get(`/import-csv/?${params}`).then(
          response => {
            this.rows = response.data.rows;
            callback(this.rows);

          }
      ).catch(
          () => {
            callback([]);
          }
      );
      return null;
    },
    goToNextRow: function() {
      if(this.currentRow < this.rows.length -1) {
        this.currentRow += 1;
      }
    },
    goToPreviousRow: function() {
      if(this.currentRow > 0) {
        this.currentRow -= 1;
      }
    },
    saveRow: function() {

    },
    getRowTotalNumber: function() {
      axios.get("/import-csv/count/").then(
          response => {
            if(response.data.success) {
              this.rowTotalNumber = response.data.total;
            }
          }
      );
    },
    showRowProcessing: function (event) {
      // console.log(event);
      axios.get(`/import-csv/rows/${event.index}`).then(
          response => {
            this.result = response.data.data;
            this.refResult = response.data.ref;
            this.authorsResult = response.data.authors;
            this.authors = response.data.ref.authors;
            this.reference = response.data.ref;
            this.record = response.data.record;
            console.log(response.data.record);
          }
      );
    },
    /**
     * Saved rows are rows that are no more useful to save in database.
     */
    getSavedRows: function() {
      // this.rowsAlreadySaved = ;
    },
    /**
     * Get last row which I was working on
     */
    getLastCurrentRow: function() {
      // this.currentRow = ;
    },

    saveAuthor: function() {

    },
    saveReference: function() {

    },
    saveRecord: function () {

    },
    updateLastCurrentRow: function (value) {
      console.log(value);
    },
  },
  mounted() {
    this.getRowTotalNumber();
    this.getSavedRows();
    this.getLastCurrentRow();
  },
  watch: {
    currentRow: function(newValue) {
      console.log(newValue);
      this.updateLastCurrentRow(newValue);
    }
  }
}
</script>

<style scoped>

</style>