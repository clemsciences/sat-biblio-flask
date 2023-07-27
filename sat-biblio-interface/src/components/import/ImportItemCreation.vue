<template>
  <b-container>
    <b-form @submit.prevent="saveImportItem">
<!--    <b-form-group label="Fichier">-->
<!--      <b-form-file-->
<!--          browse-text="Explorer"-->
<!--          v-model="file"-->
<!--          :state="Boolean(file)"-->
<!--          placeholder="Choisissez le catalogue à importer"-->
<!--          drop-placeholder="Lâchez le catalogue à importer ici"-->
<!--          ref="file-input"-->
<!--          accept=".csv, .xlsx, .xls"-->
<!--      />-->

<!--    <p>{{ file ? file.name : ""}}</p>-->
<!--  </b-form-group>-->
    <b-form-group label="Nom du fichier">
      <b-form-input v-model="importItem.filename" :disabled="true"/>
    </b-form-group>
      <b-form-group label="Nombre de lignes à ignorer au début du fichier">
        <b-form-input v-model="importItem.firstRowsToIgnoreNumber" type="number" min="0"/>
      </b-form-group>
      <b-form-group label="Nombre de lignes à afficher après les lignes ignorées">
        <b-form-input v-model="importItem.rowsToPreviewNumber" type="number" min="0"/>
      </b-form-group>
      <b-form-group label="Ne conserver que les entrées vérifiées">
        <b-form-checkbox v-model="importItem.filterByVerifiedEntry"/>
      </b-form-group>
<!--    <b-form-group>-->
    <b-row class="m-2">
      <b-button @click="checkImport">Vérifier</b-button>
      <div v-if="checked" class="mx-2">
        <div v-if="columnFitness">
          <b-icon icon="hand-thumbs-up"/>
        </div>
        <div v-else>
          <b-icon icon="hand-thumbs-down"/>
        </div>
      </div>
    </b-row>
<!--    </b-form-group>-->
    <b-form-group class="m-2">
      <b-button @click="previewImport">Prévisualiser</b-button>
      <div v-if="isPreviewing">
        <p>La <b>première ligne</b> correspond aux colonnes de référence qu'il faut suivre.
          <br/>La <b>deuxième ligne</b> correspond aux colonnes du fichier importé.
          <br/>Le <b>reste des lignes</b> correspond à des exemples.
        </p>
        <p>Nombre de lignes ajoutées {{ numberOfImportedRows }}</p>
        <b-table responsive striped bordered hover
                 :items="previewedRows"
                 :busy="isPreviewLoading">
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Chargement...</strong>
            </div>
          </template>
        </b-table>
      </div>
    </b-form-group>
    <b-form-group label="Description" v-if="columnFitness">
      <b-form-textarea v-model="importItem.description" :disabled="disabled"/>
    </b-form-group>
    <b-row class="m-2" v-if="columnFitness">
      <p>{{ isIncorrect }} {{ disabled }}</p>
      <b-button type="submit" :disabled="isIncorrect || disabled">Enregistrer</b-button>
      <div v-if="isImporting">
        <b-spinner label="Importation en cours..." class="m-2"/>
      </div>
      <span class="mx-3">{{ message }}</span>
    </b-row>
  </b-form>
  </b-container>
</template>

<script>
import {
  previewCatalogueRequest,
  checkColumnsRequest,
  getCatalogueInfoByKey,
  importCatalogueFromFileRequest,
} from "@/services/api";

import {canManage} from "@/services/rights";

export default {
  name: "ImportItemCreation",
  components: {},
  props: {
    selectedKey: {
      type: String,
      optional: false
    },
    fullFilename: {
      type: String,
    }
  },
  data: function() {
    return {
      // file: null,
      isImporting: false, // is importing catalogue into database
      disabled: false,
      importItem: {
        description: "",
        filename: "",
        datetime: "",
        fullPath: "",
        firstRowsToIgnoreNumber: 0,
        rowsToPreviewNumber: 1,
        filterByVerifiedEntry: 0,
        key: ""
      },
      message: "",
      isPreviewing: false,
      isPreviewLoading: false, // loading preview table
      previewedRows: [],
      checked: false,
      checkOk: false,
      numberOfImportedRows: 0,

      columnFitness: false
    }
  },
  mounted() {
    this.loadFilename();
    this.importItem.key = this.selectedKey;
  },
  methods: {
    loadFilename() {
      console.log("bizarre", this.selectedKey);
      if(this.selectedKey) {
        getCatalogueInfoByKey(this.selectedKey).then(
            (response) => {
              if (response.data.success) {
                const catalogueInfo = response.data.info;
                if (catalogueInfo) {
                  this.importItem.filename = catalogueInfo.filename;
                  this.importItem.fullPath = response.data.path;
                } else {
                  this.importItem.filename = "";
                  this.importItem.fullPath = "";
                }
              }
            }
        );
      }
    },
    saveImportItem: function () {
      console.log("file imported");
      this.isProcessing = true;
      this.disabled = true;
      this.isImporting = true;
      importCatalogueFromFileRequest(this.importItem,
          this.$store.state.connectionInfo.token).then(
          (response) => {
            let data = response.data;
            console.log(data);
            this.isProcessing = false;
            this.disabled = false;
            this.isImporting = false;
          }
      ).catch((reason) => {
        this.isProcessing = false;
        this.disabled = false;
        this.isImporting = false;
        this.message = "La création de l'import a échoué.";
        console.error(reason);
      });
    },
    checkImport() {
      this.checked = false;
      checkColumnsRequest(this.selectedKey, this.importItem.firstRowsToIgnoreNumber).then(
          (response) => {
            console.log(response.data.file_check);
            let l = response.data.file_check.filter((item, index) => {
              return item !== index;
            });
            this.checked = true;
            this.checkOk = l.length === 0;
            this.columnFitness = l.length === 0;
          }
      );
    },
    previewImport() {
      this.isPreviewing = !this.isPreviewing;
      if (this.isPreviewing) {
        this.isPreviewLoading = true;
        previewCatalogueRequest(
            this.selectedKey,
            this.importItem.firstRowsToIgnoreNumber,
            this.importItem.rowsToPreviewNumber,
            this.importItem.filterByVerifiedEntry ? 1 : 0
        ).then(
            (response) => {
              console.log(response.data);
              this.previewedRows = [response.data.column_reference];
              this.previewedRows.push(response.data.check);
              console.log(response.data.actual_columns);
              this.previewedRows.push(response.data.actual_columns);
              response.data.first_rows.forEach((item) => {
                this.previewedRows.push(item);
              });
              this.numberOfImportedRows = response.data.number_of_rows;

              this.isPreviewLoading = false;
            }
        );
      } else {
        this.column_reference = [];
        this.previewedRows = [];
        this.isPreviewLoading = false;
      }
    }

  },
  computed: {
    isManager: function() {
      return canManage(this.$store.getters.getUserRight);
    },
    isIncorrect() {
      return this.importItem.description.length === 0 ||
          this.importItem.filename.length === 0;
    }
  }
}
</script>

<style scoped>

</style>