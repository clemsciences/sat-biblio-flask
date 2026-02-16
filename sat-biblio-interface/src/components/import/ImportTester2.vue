<template>
  <BContainer>
    <h2>Importation fine</h2>
    <BRow class="m-1">
      <BCol cols="3">
        <BButton-toolbar>
          <BButton-group>
            <BButton @click="goToPreviousRow">&lsaquo;</BButton>
          </BButton-group>
          <b-input-group>
            <BFormInput style="width: 100px" readonly v-model="currentRow"
            class="text-center"/>
          </b-input-group>
          <BButton-group>
            <BButton @click="goToNextRow">&rsaquo;</BButton>
          </BButton-group>
        </BButton-toolbar>
      </BCol>
      <BCol cols="2">
        <BButton @click="goToNextNotMarkedRow" size="sm">Aller au prochain<br/>non marqué</BButton>
      </BCol>
      <BCol cols="2">
        <BButton class="m-2" size="sm" @click="saveRow">Sauvegarder la ligne</BButton>
      </BCol>
      <BCol cols="1">
        <p :style="colorAlreadyStored" class="m-1" >{{ textAlreadyStored }}</p>
      </BCol>
      <BCol cols="4">
        <BRow>
          <BButton class="m-1" @click="markAsNotProcessed" size="sm">Marquer comme non traité</BButton>
          <BButton class="m-1" @click="markAsProcessed" size="sm">Marquer comme traité</BButton>
        </BRow>
      </BCol>

    </BRow>
    <BRow>

      <BCol cols="4">
        <BRow>
        <h4>Auteurs</h4>
        </BRow>
        <BRow>
          <BCol>
            <BButton @click="saveAuthors" size="sm">Enregistrer</BButton>
          </BCol>
          <BCol>
            <BButton @click="addAuthor" size="sm">Ajouter</BButton>
          </BCol>
          <BButton @click="removeAuthor" size="sm">Supprimer</BButton>
        </BRow>
        <BRow>
          <AuteurFormulaire v-for="author in authors"
                            :key="`author-${authors.indexOf(author)}`"
                            :auteur="author"
                            :on-submit="saveAuthor"
                            @update:first_name="author.first_name = $event"
                            @update:family_name="author.family_name = $event"/>
        </BRow>
      </BCol>
      <BCol cols="4">
        <h4>Références</h4>
        <!-- Saved authors -->
        <BButton @click="saveReference" :disabled="!refSaved">Sauvegarder référence</BButton>
        <ReferenceLivreFormulaire :on-submit="saveReference" :reference="reference"/>
      </BCol>
      <BCol cols="4">
        <h4>Enregistrements</h4>
        <BButton @click="saveRecord" :disabled="!recordSaved">Sauvegarder enregistrement</BButton>
        <EnregistrementFormulaire :on-submit="saveRecord" :record="record"
                                  @update:selectedReference="record.selectedReference = $event"
                                  @update:cote="record.cote = $event"
                                  @update:annee_obtention="record.annee_obtention = $event"
                                  @update:provenance="record.provenance = $event"
                                  @update:aide_a_la_recherche="record.aide_a_la_recherche = $event"
                                  @update:observations="record.observations = $event"
                                  @update:row="record.row = $event"
        />
      </BCol>
    </BRow>
  </BContainer>
</template>

<script>
import axios from "axios";
import AuteurFormulaire from "@/components/auteur/AuteurFormulaire.vue";
import ReferenceLivreFormulaire from "@/components/reference_livre/ReferenceLivreFormulaire.vue";
import EnregistrementFormulaire from "@/components/enregistrement/EnregistrementFormulaire.vue";
import {Author, BookReference, Record} from "@/services/objectManager.js";
import {
  createAuthor,
  createBookRecord,
  createBookReference,
  goToNextNotMarkedRow,
  markRowAsNotProcessed,
  markRowAsProcessed
} from "@/services/api";

export default {
  name: "ImportTesterView",
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
      console.log("nothing is done when saving 1 author.")
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