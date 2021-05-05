<template>
  <b-container>
    <h2>Export</h2>
    <b-button class="mx-3" @click="exporterPDF">Exporter au format PDF</b-button>
    <b-button class="mx-3" @click="exporterExcel">Exporter au format Excel (.xsl)</b-button>


  </b-container>
</template>

<script>
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

    }
  }
}
</script>

<style scoped>

</style>