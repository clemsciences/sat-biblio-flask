<template>
  <div>
    <h2>Recherche</h2>
    <b-form @submit.prevent="search">
      <b-form-group label-for="first_name" label="Prénom">
        <b-form-input id="first_name" name="first_name" type="text"/>
      </b-form-group>
      <b-form-group label="Nom de famille" label-for="family_name">
        <b-form-input id="family_name" name="family_name" type="text"/>
      </b-form-group>
      <b-form-group label-for="year" label="Année">
        <b-form-input id="year" name="year" type="text"/>
      </b-form-group>
      <b-form-group label-for="editor" label="Editeur">
        <b-form-input id="editor" name="editor" type="text"/>
      </b-form-group>
      <b-form-group label-for="keywords" label="Mots-clef">
        <b-form-input id="keywords" name="keywords" :value="keywords"/>
      </b-form-group>
      <b-button type="submit">Rechercher</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Recherche",
  data: function () {
    return {
      first_name: "",
      family_name: "",
      year: "",
      editor: "",
      keywords: ""
    }
  },
  methods: {
    search: function () {
      const formData = {
        first_name: this.first_name,
        family_name: this.family_name,
        year: this.year,
        editor: this.editor,
        keywords: this.keywords
      };
      axios.post("/api/recherche/rechercher", formData).then(
          (response) => {
            if(response.data.success) {
              console.log("rechercher");
            }
          }
      )
    }
  }
}
</script>

<style scoped>

</style>