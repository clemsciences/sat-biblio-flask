<template>
  <b-container>
    <h2>Importation - Exportation</h2>

    <b-row v-if="!isProcessing">
      <b-col>
      <b-card title="Transformation du catalogue">
        <b-card-text>

        </b-card-text>
      <b-form>
        <b-form-group>
          <b-form-file
              browse-text="Explorer"
              v-model="file"
              :state="Boolean(file)"
              placeholder="Choisissez le catalogue à importer"
              drop-placeholder="Lâchez le catalogue à importer ici"
              ref="file-input"
              accept=".csv, .xlsx, .xls"
          />

        <p>{{ file ? file.name : ""}}</p>
      </b-form-group>
      <b-form-group>

        <b-form-radio-group
          v-model="selectedModel"
          :options="options"
          />
      </b-form-group>

      <b-button @click="importExport">Traiter</b-button>

    </b-form>
    </b-card>
        </b-col>
    </b-row>
    <b-card title="Anciennces importation">
      <b-row class="my-3">
          <b-button to="/importation">Importation fine</b-button>
      </b-row>
      <b-row>
          <b-button to="/importation-globale">Importation globale</b-button>
      </b-row>
    </b-card>

    <div v-if="isProcessing">
      <b-spinner label="chargement"  class="m-2"/>
    </div>
  </b-container>
</template>

<script>
import axios from "axios";

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
          {text: "1", value: "1"},
          {text: "2", value: "2"},
      ]

    };
  },
  methods: {
    importExport() {
      if (this.file) {
        this.isProcessing = true;
        let formData = new FormData();
        formData.append("file", this.file);
        formData.append("method", this.selectedModel)
        axios.post("/import-export/process", formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(
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

      }
    }
  }
}
</script>

<style scoped>

</style>