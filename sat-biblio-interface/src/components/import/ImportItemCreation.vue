<template>
  <BContainer>
    <BForm @submit.prevent="saveImportItem">
<!--    <BFormGroup label="Fichier">-->
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
<!--  </BFormGroup>-->
    <BFormGroup label="Nom du fichier">
      <BFormInput v-model="importItem.filename" :disabled="true"/>
    </BFormGroup>
      <BFormGroup label="Nombre de lignes à ignorer au début du fichier">
        <BFormInput v-model="importItem.firstRowsToIgnoreNumber" type="number" min="0"/>
      </BFormGroup>
      <BFormGroup label="Nombre de lignes à afficher après les lignes ignorées">
        <BFormInput v-model="importItem.rowsToPreviewNumber" type="number" min="0"/>
      </BFormGroup>
      <BFormGroup label="Ne conserver que les entrées vérifiées">
        <BFormCheckbox v-model="importItem.filterByVerifiedEntry"/>
      </BFormGroup>
<!--    <BFormGroup>-->
    <BRow class="m-2">
      <BButton @click="checkImport">Vérifier</BButton>
      <div v-if="checked" class="mx-2">
        <div v-if="columnFitness">
          <IBiHandThumbsUp/>
        </div>
        <div v-else>
          <IBiHandThumbsDown/>
        </div>
      </div>
    </BRow>
<!--    </BFormGroup>-->
    <BFormGroup class="m-2">
      <BButton @click="previewImport">Prévisualiser</BButton>
      <div v-if="isPreviewing">
        <BButton @click="downloadCatalogueToFix">Télécharger le catalogue à corriger</BButton>
        <p>La <b>première ligne</b> correspond aux colonnes de référence qu'il faut suivre.
          <br/>La <b>deuxième ligne</b> correspond aux colonnes du fichier importé.
          <br/>Le <b>reste des lignes</b> correspond à des exemples.
        </p>
        <p>Nombre de lignes ajoutées {{ numberOfImportedRows }}</p>
        <BTable responsive striped bordered hover
                 :items="previewedRows"
                 :busy="isPreviewLoading">
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <BSpinner class="align-middle"></BSpinner>
              <strong>Chargement...</strong>
            </div>
          </template>
        </BTable>

      </div>
    </BFormGroup>
    <BFormGroup label="Description" v-if="columnFitness">
      <BFormTextarea v-model="importItem.description" :disabled="disabled"/>
    </BFormGroup>
    <BRow class="m-2" v-if="columnFitness">
<!--      <p>{{ isIncorrect }} {{ disabled }}</p>-->
      <BButton type="submit" :disabled="isIncorrect || disabled">Enregistrer</BButton>
      <div v-if="isImporting">
        <BSpinner label="Importation en cours..." class="m-2"/>
      </div>
      <span class="mx-3">{{ message }}</span>
    </BRow>
  </BForm>
  </BContainer>
</template>

<script>
import {
  previewCatalogueRequest,
  checkColumnsRequest,
  getCatalogueInfoByKey,
  importCatalogueFromFileRequest,
} from "@/services/api";

import {canManage} from "@/services/rights";
import {downloadCatalogueToFix} from "@/services/api";

export default {
  name: "ImportItemCreation",
  components: {},
  props: {
    selectedKey: {
      type: String,
      optional: false
    },
    // fullFilename: {
    //   type: String,
    // }
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
    this.importItem.key = this.selectedKey;
    this.loadFilename();
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
              } else {
                console.error("impossible to retrieve filename")
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
    downloadCatalogueToFix() {
      downloadCatalogueToFix(this.selectedKey).then(
          (response) => {
            console.log(response);
            // let linkToDownload = response.data.linkToDownload;
            // window.open(`${process.env.VUE_APP_SITE_API_URL}/static/${linkToDownload}`, '_blank');
        }
      )

    },
    checkImport() {
      this.checked = false;
      checkColumnsRequest(this.selectedKey, this.importItem.firstRowsToIgnoreNumber).then(
          (response) => {
            if(response.data.success) {
              console.log(response.data.file_check);
              if (response.data.file_check) {
                let l = response.data.file_check.filter((item, index) => {
                  return item !== index;
                });
                this.checked = true;
                this.checkOk = l.length === 0;
                this.columnFitness = l.length === 0;
              } else {
                this.checked = false;
                this.checkOk = false;
                this.columnFitness = false;
              }
            } else {
              console.error("check failed");
            }
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
              if(response.data.success) {
                console.log(response.data);
                this.previewedRows = [response.data.column_reference];
                this.previewedRows.push(response.data.check);
                console.log(response.data.actual_columns);
                this.previewedRows.push(response.data.actual_columns);
                response.data.first_rows.forEach((item) => {
                  this.previewedRows.push(item);
                });
                this.numberOfImportedRows = response.data.number_of_rows;
              } else {
                console.error("preview has failed");
              }

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
  },
  watch: {
    selectedKey: function (newValue) {
      this.importItem.key = newValue;
      this.loadFilename();
    }
  }
}
</script>

<style scoped>

</style>