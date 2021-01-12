<template>
  <div>
    <h2>Export</h2>
    <b-button @click="exporterPDF">Exporter au format PDF</b-button>
    <b-button @click="exporterExcel">Exporter au format Excel (.xsl)</b-button>


  </div>
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

    }
  }
}
</script>

<style scoped>

</style>