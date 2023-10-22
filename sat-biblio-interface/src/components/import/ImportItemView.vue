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
import {ImportItem, User} from "../../services/objectManager";

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
    this.loadImportItem(this.importItemId);

  },
  methods: {
    loadImportItem(importItemId) {
      console.log("import item in import item view", importItemId)
      getOneImportRequest(importItemId).then(
        (response) => {
          if(response.data.success) {
            console.log(response.data);
            let importData = response.data.import_data;
            if (importData) {
              this.importItem = new ImportItem()
              this.importItem.fromServer(importData);
            }
            let userData = response.data.user_data;
            if (userData) {
              this.importItem.user = new User();
              this.importItem.user.fromServer(userData);
            }
          } else {
            this.importItem = null;
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
  },
  watch: {
    importItemId(newValue) {
      this.loadImportItem(newValue);
    }
  }
}
</script>

<style scoped>

</style>