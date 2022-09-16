<template>
  <b-container>
    <h2>Export</h2>
    <b-row class="m-3">
<!--      <b-button class="mx-3" @click="exporterPDF" :disabled="downloading">-->
<!--        Exporter au format PDF-->
<!--      </b-button>-->
      <b-button class="m-2" @click="exporterExcel" :disabled="generating">
        Générer un export au format Excel (.xlsx)
      </b-button>

      <b-button class="m-2" @click="exporterCSV" :disabled="generating">
        Générer un export au format CSV (.csv)
      </b-button>
      <b-checkbox v-model="withWeed">Ajouter les ouvrages désherbés</b-checkbox>
      <b-checkbox v-model="withAuxiliaryColumns">Ajouter les colonnes auxiliaires</b-checkbox>
    </b-row>
<!--    <b-row>-->
      <div v-if="generating"  class="d-flex justify-content-center">
        <b-spinner label="chargement"  class="m-2"/>
        <p class="m-2">{{ message }}</p>
      </div>
      <div v-else>
        <div v-if="linkToDownload.length > 0" class="d-flex justify-content-center">
          <b-button-group>
            <b-button @click="download" class="m-2">Télécharger le document</b-button>
            <b-button @click="cancelDownload">Annuler</b-button>
          </b-button-group>
        </div>
      </div>
<!--    </b-row>-->


  </b-container>
</template>

<script>
// import { jsPDF } from "jspdf";

import {exportCSVRequest, exportXLSXRequest} from "@/services/api";

export default {
  name: "Export",
  data: function() {
    return {
      generating: false,
      message: "",
      linkToDownload: "",
      withWeed: false,
      withAuxiliaryColumns: true
    }
  },
  methods: {
    exporterCSV: function() {
      this.generating = true;
      this.message = "Génération du fichier CSV en cours...";
      exportCSVRequest(this.params).then(response => {
        if(response.data.success) {
          this.linkToDownload = response.data.filename;
        } else {
          this.message = "Erreur lors de la génération du fichier CSV.";
        }
        // const blob = new Blob([response.data], { type: 'text/csv' });
        // const link = document.createElement('a');
        // link.href = URL.createObjectURL(blob);
        // link.download = `catalogue-${Date.now()}.csv`;
        // link.click();
        // URL.revokeObjectURL(link.href);
        this.generating = false;
        this.message = "";
      })
    },
    exporterExcel: function() {
      this.generating = true;
      this.message = "Génération du fichier Excel en cours...";
      // setTimeout(() => {
      //   this.downloading = false;
      // }, 10000);
      exportXLSXRequest(this.params).then(response => {
        if(response.data.success) {
          this.linkToDownload = response.data.filename;
        } else {
          this.message = "Erreur lors de la génération du fichier Excel."
        }
        // const blob = new Blob([response.data], { type: 'application/csv' }); // vnd.openxmlformats-officedocument.spreadsheetml.sheet
        // const link = document.createElement('a');
        // link.href = URL.createObjectURL(blob);
        // link.download = `catalogue-${Date.now()}.xlsx`;
        // link.click();
        // URL.revokeObjectURL(link.href);
        this.generating = false;
      });
    },
    exporterPDF: function() {
      // const doc = new jsPDF();
      // doc.text("Catalogue", 10, 10);
      // doc.save("catalogue.pdf");


    },

    download: function() {
      let linkToDownload = this.linkToDownload;
      window.open(`${process.env.VUE_APP_SITE_API_URL}/static/${linkToDownload}`, '_blank');
    },
    cancelDownload: function() {
      this.linkToDownload = '';
    }
  },
  computed: {
    params: function() {
      let params = [];
      this.withWeed ? params.push("withWeed=1") : params.push("withWeed=0");
      this.withAuxiliaryColumns ? params.push("withAuxiliaryColumns=1") : params.push("withAuxiliaryColumns=0");
      return "?"+params.join("&");
    }
  }
}
</script>

<style scoped>
.my-center {
  position: fixed; top: 50%; left: 50%;
}

</style>