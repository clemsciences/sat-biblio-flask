<template>
  <BContainer>
    <h2>Importation - Exportation</h2>

    <BRow v-if="!isProcessing">
      <BCol>
      <BCard title="Transformation du catalogue">
        <BCardText>

        </BCardText>
      <BForm>
        <BFormGroup>
          <BFormFile
              browse-text="Explorer"
              v-model="file"
              :state="Boolean(file)"
              placeholder="Choisissez le catalogue à importer"
              drop-placeholder="Lâchez le catalogue à importer ici"
              ref="file-input"
              accept=".csv, .xlsx, .xls"
          />

        <p>{{ file ? file.name : ""}}</p>
      </BFormGroup>
      <BFormGroup>

        <BFormRadio-group
          v-model="selectedModel"
          :options="options"
          />
      </BFormGroup>

      <BButton @click="importExport">Traiter</BButton>

    </BForm>
    </BCard>
        </BCol>
    </BRow>

    <div v-if="isProcessing">
      <BSpinner label="chargement"  class="m-2"/>
    </div>
  </BContainer>
</template>

<script>
import {processImportExportRequest} from "@/services/api.js";

export default {
  name: "ImportExport",
  data: function() {
    return {
      file: null,
      isProcessing: false,
      exportFilename: "",
      exportFileUrl: "",
      selectedModel: "",
      options: [
          {text: "1", value: "1", description: "Import format Hamelain"},
          // {text: "2", value: "2", description: ""},
      ]

    };
  },
  methods: {
    importExport() {
      if (this.file) {
        console.log("file imported");
        this.isProcessing = true;
        let formData = new FormData();
        formData.append("file", this.file);
        formData.append("method", this.selectedModel)
        processImportExportRequest(formData, this.$store.state.connectionInfo.token).then(
            (response) => {
              let data = response.data;
              console.log(data);
              console.log(data.type);
              this.isProcessing = false;
            }
        ).catch((reason) => {
          this.isProcessing = false;
          console.error(reason);
        });

      } else {
        console.error("no file");
      }
    }
  }
}
</script>

<style scoped>

</style>