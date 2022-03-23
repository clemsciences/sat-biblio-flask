<template>
  <b-container>
    <h2>Export</h2>
    <b-button class="mx-3" @click="exporterPDF">Exporter au format PDF</b-button>
    <b-button class="mx-3" @click="exporterExcel">Exporter au format Excel (.xsl)</b-button>


  </b-container>
</template>

<script>
// import { jsPDF } from "jspdf";

export default {
  name: "Export",
  data: function() {
    return {

    }
  },
  methods: {
    exporterExcel: function() {

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