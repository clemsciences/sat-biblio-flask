<template>
  <BContainer>
    <h2>Gestion des images</h2>
    <BRow>
      <BCol cols="6">
        <b-form-file v-model="files"
                     :state="Boolean(files)"
                     placeholder="Choisissez une image ou une archive compressée d'images en .zip"
                     drop-placeholder="Lâchez l'image ou l'archive compressée d'images ici"
                     multiple
                     ref="file-input"
                     accept=".jpg, .png, .gif, .zip"
        />
        <BListGroup>
          <BListGroupItem v-for="file in files" :key="file.name">{{ file ? file.name : ""}}</BListGroupItem>
<!--          <BListGroupItem></BListGroupItem>-->
        </BListGroup>

        <BButton @click="clearFiles">Remettre à zéro</BButton>


      </BCol>
      <BCol cols="6">

      </BCol>
    </BRow>
    <BRow>
      <BCol cols="6">

        <BFormRadio-group
        v-model="selectedModel"
        :options="options"

        />

        <BButton @click="processFiles">Traiter</BButton>



      </BCol>
      <BCol cols="6">

      </BCol>
    </BRow>
  </BContainer>
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