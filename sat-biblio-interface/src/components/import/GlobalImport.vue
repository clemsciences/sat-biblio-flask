<template>
  <BContainer>
    <AppTitle info="Importation globale"
           id="id-global-import">
      Importation globale
    </AppTitle>
    <BRow>
      <BButton @click="importAllRows" class="m-2">Importer le catalogue depuis le CSV au format Schweitz</BButton>
      <p>{{ importMessage }}</p>
    </BRow>
  </BContainer>

</template>

<script>
import {importAllCatalogue} from "@/services/api.js";
import AppTitle from "@/components/visuel/AppTitle.vue";
export default {
  name: "GlobalImport",
  components: {AppTitle},
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