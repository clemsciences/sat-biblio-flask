<template>
  <b-container>
    <h2>Gestion des images</h2>
    <b-row>
      <b-col cols="6">
        <b-form-file v-model="files"
                     :state="Boolean(files)"
                     placeholder="Choisissez une image ou une archive compressée d'images en .zip"
                     drop-placeholder="Lâchez l'image ou l'archive compressée d'images ici"
                     multiple
                     ref="file-input"
                     accept=".jpg, .png, .gif, .zip"
        />
        <b-list-group>
          <b-list-group-item v-for="file in files" :key="file.name">{{ file ? file.name : ""}}</b-list-group-item>
<!--          <b-list-group-item></b-list-group-item>-->
        </b-list-group>

        <b-button @click="clearFiles">Remettre à zéro</b-button>


      </b-col>
      <b-col cols="6">

      </b-col>
    </b-row>
    <b-row>
      <b-col cols="6">

        <b-form-radio-group
        v-model="selectedModel"
        :options="options"

        />

        <b-button @click="processFiles">Traiter</b-button>



      </b-col>
      <b-col cols="6">

      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";

export default {
  name: "ImageManager",
  data: function() {
    return {
      files: [],
      selectedModel: "",
      options: [
        {text: "1", value: "1"},
        {text: "2", value: "2"},
      ]
    }
  },
  methods: {
    clearFiles() {
      this.$refs["file-input"].reset();
    },
    processFiles() {
      console.log(`${this.selectedModel} ${this.files}`);
      axios.post("/", ).then(
          (response) => {
            console.log(response.data);

          }
      ).catch((reason) => {
        console.log(reason);
      })
    }
  }
}
</script>

<style scoped>

</style>