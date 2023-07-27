<template>
  <b-container>
    <Title
      title="Import de catalogue"
      id="id-import"
      info=""
    />
    <b-card v-if="importItem != null">
      <b-card-title title="Fiche"/>
      <b-card-body>
        <ImportItemForm
         :message="message"
         :disabled="!canModify"
         :import-item="importItem"
         :onSubmit="updateImport"
        />
        <b-button @click="deleteImport">Supprimer</b-button>
      </b-card-body>
    </b-card>
    <p v-else>Sélectionner une fiche</p>
  </b-container>
</template>

<script>
import {getOneImportRequest} from "@/services/api";
import ImportItemForm from "@/components/import/ImportItemForm.vue";
import Title from "@/components/visuel/Title.vue";

export default {
  name: "ImportItem",
  components: {ImportItemForm, Title},
  props: {
    importItemId: {
      type: Number
    }
  },
  data: function() {
    return {
      importItem: null,
      message: "",
      canModify: false
    }
  },
  mounted() {
    this.loadImportItem();

  },
  methods: {
    loadImportItem() {
      console.log("import item in import item view", this.importItemId)
      getOneImportRequest(this.importItemId).then(
        (response) => {
          console.log(response.data);
          if (response.data.import_data) {
            this.importItem = response.data.import_data;
          }
        }
    );
    },
    updateImport() {
      console.error("héhé, on ne modifie rien");
    },
    deleteImport() {
      console.error("hehe, non, on ne supprime rien");
    }

  },
  computed: {
    prettyImport: function() {
      return this.importItem;
    }
  }
}
</script>

<style scoped>

</style>