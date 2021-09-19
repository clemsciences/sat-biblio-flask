<template>
  <b-container>
    <h2>Importation</h2>
    <b-row class="m-2">
      <b-col>
        <b-button @click="goToPreviousRow">Précédent</b-button>
      </b-col>
      <b-col>
        <b-form-input style="width: 100px" readonly v-model="currentRow"/>
      </b-col>
      <b-col>
        <b-button @click="goToNextRow">Suivant</b-button>
      </b-col>
      <b-btn @click="goToNextNotMarkedRow">Aller au prochain<br/>non marqué</b-btn>
      <b-col>
        <b-button class="m-2" @click="saveRow">Sauvegarder la ligne</b-button>
      </b-col>

    </b-row>
    <b-row>
      <b-col cols="2">
        <p :style="colorAlreadyStored" class="m-2">{{ textAlreadyStored }}</p>
      </b-col>
      <b-col cols="4">
        <b-row>
          <b-button @click="markAsNotProcessed">Marquer comme non traité</b-button>
          <b-button @click="markAsProcessed">Marquer comme traité</b-button>
        </b-row>
      </b-col>
    </b-row>
    <b-row>

      <b-col cols="4">
        <b-row>
        <h4>Auteurs</h4>
        </b-row>
        <b-row>
          <b-col>
            <b-button @click="saveAuthors">Enregistrer</b-button>
          </b-col>
          <b-col>
            <b-button @click="addAuthor">Ajouter</b-button>
          </b-col>
          <b-button @click="removeAuthor">Supprimer</b-button>
        </b-row>
        <b-row>
          <AuteurFormulaire v-for="author in authors"
                            :key="`author-${authors.indexOf(author)}`"
                            :auteur="author"
                            :on-submit="saveAuthor"/>
        </b-row>
      </b-col>
      <b-col cols="4">
        <h4>Références</h4>
        <!-- Saved authors -->
        <b-button @click="saveReference" :disabled="!refSaved">Sauvegarder référence</b-button>
        <ReferenceLivreFormulaire :on-submit="saveReference" :reference="reference"/>
      </b-col>
      <b-col cols="4">
        <h4>Enregistrements</h4>
        <b-button @click="saveRecord" :disabled="!recordSaved">Sauvegarder enregistrement</b-button>
        <EnregistrementFormulaire :on-submit="saveRecord" :record="record"/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";
import AuteurFormulaire from "@/components/auteur/AuteurFormulaire";
import ReferenceLivreFormulaire from "@/components/reference_livre/ReferenceLivreFormulaire";
import EnregistrementFormulaire from "@/components/enregistrement/EnregistrementFormulaire";
import {Author, BookReference, Record} from "@/services/objectManager";
import {
  createAuthor,
  createBookRecord,
  createBookReference,
  goToNextNotMarkedRow,
  markRowAsNotProcessed,
  markRowAsProcessed
} from "@/services/api";

export default {
  name: "ImportTester2",
  components: {
    EnregistrementFormulaire,
    ReferenceLivreFormulaire,
    AuteurFormulaire
  },
  data: function() {
    return {
      // region rows
      numberRows: 0,
      currentRow: 0,
      rowsAlreadySaved: [],
      textAlreadyStored: '',
      colorAlreadyStored: {backgroundColor: 'red'},
      // endregion
      // region authors
      authorsResult: '',
      authors: [new Author()],
      // endregion
      // region reference
      refResult: '',
      reference: new BookReference(),
      refSaved: false,

      // endregion
      // region record
      record: new Record(),
      recordSaved: false,
      // endregion
    }
  },
  methods: {
    loadRow: function(index) {
      axios.get(`/import-csv/rows/${index}`).then(
          response => {
            this.refResult = response.data.ref;
            this.authorsResult = response.data.authors;
            this.authors = response.data.ref.authors;
            this.reference = response.data.ref;
            this.record = response.data.record;

            if(response.data.already_stored) {
              this.textAlreadyStored = "Déjà enregistré";
              this.colorAlreadyStored = {backgroundColor: 'green'};
            } else {
              this.textAlreadyStored = "Pas enregistré";
              this.colorAlreadyStored = {backgroundColor: 'red'};
            }
            // console.log(response.data.record);
          }
      );
    },
    // loadRows: function (callback) {
    //   let params = `page=${this.currentRow}&size=1`;
    //   axios.get(`/import-csv/?${params}`).then(
    //       response => {
    //         this.rows = response.data.rows;
    //         callback(this.rows);
    //
    //       }
    //   ).catch(
    //       () => {
    //         callback([]);
    //       }
    //   );
    //   return null;
    // },
    goToNextRow: function() {
      if(this.currentRow < this.numberRows -1) {
        this.currentRow += 1;
        this.refSaved = false;
        this.recordSaved = false;
      }
    },
    goToPreviousRow: function() {
      if(this.currentRow > 0) {
        this.currentRow -= 1;
        this.refSaved = false;
        this.recordSaved = false;
      }
    },
    goToNextNotMarkedRow: function() {
      goToNextNotMarkedRow(this.currentRow).then(
          (response) => {
            this.currentRow = response.data.n;
            this.refSaved = false;
            this.recordSaved = false;
          }
      );
    },
    saveRow: function() {
      // this.saveAuthors();
      // this.saveReference();
      // this.saveRecord();
      markRowAsProcessed(this.currentRow).then(
          () => {
            console.log("marked row as processed");
          }
      );

    },
    getRowTotalNumber: function() {
      axios.get("/import-csv/count/").then(
          response => {
            if(response.data.success) {
              this.numberRows = response.data.total;
            }
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
    markAsNotProcessed: function() {
      markRowAsNotProcessed(this.currentRow).then(
          () => {
            this.textAlreadyStored = "Pas enregistré";
            this.colorAlreadyStored = {backgroundColor: 'red'};
          }
      );
    },
    markAsProcessed: function() {
      markRowAsProcessed(this.currentRow).then(
          () => {
              this.textAlreadyStored = "Déjà enregistré";
              this.colorAlreadyStored = {backgroundColor: 'green'};
          }
      )
    },
    saveAuthor: function() {
      // nothing
    },
    saveAuthors: function() {
      const that = this;
      this.authors.forEach(function(value) {
        console.log(value)
        createAuthor(value, that.$store.state.connectionInfo.token).then(
            (response) => {
              if (response.data.success) {
                if(typeof that.reference.auteurs === "undefined") {
                  that.reference.auteurs = [];
                }
                that.refSaved = true;
                that.reference.auteurs.push({value: response.data.id});
                console.log("auteur sauvegardé");
              } else {
                console.log("Impossible de sauvegarder l'auteur.");
              }
            }
        ).catch(
            (reason => {
              if(reason.response.data && reason.response.data.message) {
                console.log(reason.response.data.message);
              } else {
                console.log("Il y a une erreur réseau.");
              }
            })
        );
      });

    },
    saveReference: function() {
      console.group("reference");
      console.log(this.reference);
      console.groupEnd();
      createBookReference(this.reference, this.$store.state.connectionInfo.token)
        .then(
            (response) => {
              if(response.data.success) {
                this.record.id_reference = response.data.id;
                this.recordSaved = true;
                console.group("La référence a été créée.");
                console.log("créer une référence livresque");
                console.groupEnd();
              } else {
                console.log("La création de la référence a échoué.");
              }
            }
        ).catch(
          (reason) => {
            console.group("La création de la référence a échoué.");
            console.log(reason);
            console.groupEnd();
          }
      );
    },
    saveRecord: function () {
      createBookRecord(this.record, this.$store.state.connectionInfo.token)
          .then((response) => {
            if(response.data.success) {
              console.group("record saved");
              console.log("L'enregistrement a été sauvegardé.");
              console.groupEnd();
              markRowAsProcessed(this.currentRow).then(
                  () => {
                    this.textAlreadyStored = "Déjà enregistré";
                    this.colorAlreadyStored = {backgroundColor: 'green'};
                    console.log("marked row as processed");
                  }
              );
            } else {
              console.group("bizarre");
              console.log("Echec de la sauvegarde de l'enregistrement.");
              console.groupEnd();
            }
          })
          .catch(
            (reason) => {
              console.group("save record failed");
              console.log(reason);
              console.groupEnd();
            }
          );
    },
    updateLastCurrentRow: function (value) {
      console.log(value);
      this.loadRow(value);

    },
    addAuthor: function() {
      this.authors.push(new Author());
    },
    removeAuthor: function () {
      this.authors.pop();
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