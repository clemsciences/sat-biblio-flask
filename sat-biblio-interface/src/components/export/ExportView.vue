<template>
  <BContainer>
    <h2>Export</h2>
    <BRow class="m-3">
<!--      <BButton class="mx-3" @click="exporterPDF" :disabled="downloading">-->
<!--        Exporter au format PDF-->
<!--      </BButton>-->
      <BButton class="m-2" @click="exporterExcel" :disabled="generating">
        Générer un export au format Excel (.xlsx)
      </BButton>

      <BButton class="m-2" @click="exporterCSV" :disabled="generating">
        Générer un export au format CSV (.csv)
      </BButton>
      <BFormCheckbox v-model="withWeed">Ajouter les ouvrages désherbés</BFormCheckbox>
      <BFormCheckbox v-model="withAuxiliaryColumns">Ajouter les colonnes auxiliaires</BFormCheckbox>
    </BRow>
<!--    <BRow>-->
      <div v-if="generating"  class="d-flex justify-content-center">
        <BSpinner label="chargement"  class="m-2"/>
        <p class="m-2">{{ message }}</p>
      </div>
      <div v-else>
        <div v-if="linkToDownload.length > 0" class="d-flex justify-content-center">
          <BButton-group>
            <BButton @click="download" class="m-2">Télécharger le document</BButton>
            <BButton @click="cancelDownload">Annuler</BButton>
          </BButton-group>
        </div>
      </div>
<!--    </BRow>-->


  </BContainer>
</template>

<script>
// import { jsPDF } from "jspdf";

import {exportCSVRequest, exportXLSXRequest} from "@/services/api";

export default {
  name: "ExportView",
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
      window.open(`${import.meta.env.VITE_APP_SITE_API_URL}/static/${linkToDownload}`, '_blank');
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