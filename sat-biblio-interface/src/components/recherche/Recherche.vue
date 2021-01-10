<template>
  <div>
    <h2>Recherche</h2>
    <b-form @submit.prevent="search">
      <b-form-group label="Prénom">
        <b-form-input v-model="first_name" type="text"/>
      </b-form-group>
      <b-form-group label="Nom de famille">
        <b-form-input v-model="family_name" type="text"/>
      </b-form-group>
      <b-form-group label="Année">
        <b-form-input v-model="year" type="text"/>
      </b-form-group>
      <b-form-group label="Editeur">
        <b-form-input v-model="editor" type="text"/>
      </b-form-group>
      <b-form-group label="Mots-clef">
        <b-form-input v-model="keywords" type="text"/>
      </b-form-group>
      <b-form-group label="Cote">
      <b-form-input v-model="cote" type="text"/>
      </b-form-group>
      <b-button type="submit">Rechercher</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>

    <p v-for="resultat in resultats" :key="resultat.id">{{ resultat }}</p>
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
      cote: "",
      keywords: "",

      message: ""
    }
  },
  methods: {
    search: function () {
      const formData = {
        first_name: this.first_name,
        family_name: this.family_name,
        year: this.year,
        editor: this.editor,
        keywords: this.keywords,
        cote: this.cote
      };
      axios.post("/api/rechercher", formData).then(
          (response) => {
            if(response.data.success) {
              console.log("rechercher");
              this.resultats = response.data.resultats;
              if(this.resultats.length === 0) {
                this.message = "Aucun résultat n'a été trouvé."
              }
            }
          }
      )
    }
  }
}
</script>

<style scoped>

</style>