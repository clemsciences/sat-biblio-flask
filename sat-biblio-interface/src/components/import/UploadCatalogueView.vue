<template>
  <b-container>
    <b-form @submit.prevent="saveCatalogueItem">
      <b-form-group label="Fichier">
      <b-form-file
          browse-text="Explorer"
          v-model="file"
          :state="Boolean(file)"
          placeholder="Choisissez le catalogue à importer"
          drop-placeholder="Lâchez le catalogue à importer ici"
          ref="file-input"
          accept=".csv, .xlsx, .xls"
      />
        <b-button @click="removeFile" :disabled="file === null">Annuler</b-button>
        <b-button type="submit" :disabled="file === null">{{ file ? `Téléverser ${file.name}` : "Téléverser"}}</b-button>
        <div v-if="isUploading">
          <b-spinner label="Importation en cours..." class="m-2"/>
        </div>

    <p>{{ file ? file.name : ""}}</p>

  </b-form-group>
    </b-form>
  </b-container>

</template>

<script>
import {uploadOneCatalogueRequest} from "@/services/api";

export default {
  name: "UploadCatalogueView",
  data: function() {
    return {
      file: null,
      isUploading: false,
      filename: "",
    }
  },
  methods: {
    removeFile() {
      this.file = null;
    },
    saveCatalogueItem() {
      console.log("coucou");
      if (this.file) {
        let formData = new FormData();
        formData.append("file", this.file);
        formData.append("filename", this.filename);
        this.isUploading = true;
        uploadOneCatalogueRequest(formData, this.$store.state.connectionInfo.token).then(
            (response) => {
              this.$emit("upload-finished", true)
              let data = response.data;
              console.log(data);
              this.isUploading = false;
              console.log(data.key);
            }
        ).catch((reason) => {
          this.isUploading = false;
          this.message = "Le téléversement du catalogue a échoué."
          console.error(reason);
        })
      }
    }
  }
}
</script>

<style scoped>

</style>