<template>
  <b-container>
    <Title info="Importation globale"
           id="id-global-import">
      Importation globale
    </Title>
    <b-row>
      <b-button @click="importAllRows" class="m-2">Importer le catalogue depuis le CSV au format Schweitz</b-button>
      <p>{{ importMessage }}</p>
    </b-row>
  </b-container>

</template>

<script>
import {importAllCatalogue} from "@/services/api";
import Title from "../visuel/Title";
export default {
  name: "GlobalImport",
  components: {Title},
  data: function() {
    return {
      importMessage: ''
    }
  },
  methods: {
    importAllRows() {
      this.importMessage = "En cours d'import";
      importAllCatalogue().then(
          () => {
            this.importMessage = "C'est importé";
          }
      )
    }
  }
}
</script>

<style scoped>

</style>