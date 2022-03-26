<template>
  <b-container>
    <h2>Export</h2>
    <b-button class="mx-3" @click="exporterPDF">
      Exporter au format PDF
    </b-button>
    <b-button class="mx-3" @click="exporterExcel">
      Exporter au format Excel (.xsl)
    </b-button>


  </b-container>
</template>

<script>
// import { jsPDF } from "jspdf";

import axios from "axios";

export default {
  name: "Export",
  data: function() {
    return {

    }
  },
  methods: {
    exporterExcel: function() {
      axios.get("/export/csv/", ).then(response => {
        const blob = new Blob([response.data], { type: 'text/csv' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = `catalogue-${Date.now()}.csv`
        link.click()
        URL.revokeObjectURL(link.href)
      })
    },
    exporterPDF: function() {
      // const doc = new jsPDF();
      // doc.text("Catalogue", 10, 10);
      // doc.save("catalogue.pdf");


    }
  }
}
</script>

<style scoped>

</style>