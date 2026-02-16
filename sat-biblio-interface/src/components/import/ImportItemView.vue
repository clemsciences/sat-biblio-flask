<template>
  <BContainer>
    <AppTitle
      title="Import de catalogue"
      id="id-import"
      info=""
    />
    <BCard v-if="importItem != null">
      <BCardTitle title="Fiche"/>
      <BCardBody>
        <ImportItemForm
         :message="message"
         :disabled="!canModify"
         :import-item="importItem"
         :onSubmit="updateImport"
         @update:filename="importItem.filename = $event"
         @update:startDate="importItem.startDate = $event"
         @update:endDate="importItem.endDate = $event"
         @update:description="importItem.description = $event"
         @update:status="importItem.status = $event"
         @update:user="importItem.user = $event"
        />
        <BButton @click="deleteImport">Supprimer</BButton>
      </BCardBody>
    </BCard>
    <p v-else>Sélectionner une fiche</p>
  </BContainer>
</template>

<script>
import {getOneImportRequest} from "@/services/api";
import ImportItemForm from "@/components/import/ImportItemForm.vue";
import AppTitle from "@/components/visuel/AppTitle.vue";
import {ImportItem, User} from "../../services/objectManager";

export default {
  name: "ImportItemView",
  components: {ImportItemForm, AppTitle},
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