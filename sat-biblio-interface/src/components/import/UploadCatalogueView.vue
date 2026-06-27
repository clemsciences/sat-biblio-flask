<template>
  <BContainer>
    <BForm @submit.prevent="saveCatalogueItem">
      <BFormGroup label="Fichier">
      <BFormFile
          browse-text="Explorer"
          v-model="file"
          :state="Boolean(file)"
          placeholder="Choisissez le catalogue à importer"
          drop-placeholder="Lâchez le catalogue à importer ici"
          ref="file-input"
          accept=".csv, .xlsx, .xls"
      />
        <BButton @click="removeFile" :disabled="file === null">Annuler</BButton>
        <BButton type="submit" :disabled="file === null">{{ file ? `Téléverser ${file.name}` : "Téléverser"}}</BButton>
        <div v-if="isUploading">
          <BSpinner label="Importation en cours..." class="m-2"/>
        </div>

    <p>{{ file ? file.name : ""}}</p>

  </BFormGroup>
    </BForm>
  </BContainer>

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