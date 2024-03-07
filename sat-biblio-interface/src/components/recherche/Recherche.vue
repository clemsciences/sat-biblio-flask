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
        <b-form-input v-model="annee" type="text"/>
      </b-form-group>
      <b-form-group label="Editeur">
        <b-form-input v-model="editor" type="text"/>
      </b-form-group>
      <b-form-group label="Titre">
        <b-form-input v-model="titre" type="text"/>
      </b-form-group>
      <b-form-group label="Cote">
      <b-form-input v-model="cote" type="text"/>
      </b-form-group>
      <b-form-group label="Provenance">
      <b-form-input v-model="provenance" type="text"/>
      </b-form-group>
      <b-form-group label="Mots-clef">
        <b-form-input v-model="keywords" type="text"/>
      </b-form-group>
      <b-button type="submit">Rechercher</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>

    <p v-for="resAuthor in researchedAuthors" :key="resAuthor.id">{{ resAuthor }}</p>

    <p v-for="resRef in researchedRef" :key="resRef.id">{{ resRef }}</p>
    <p v-for="resRecord in researchedRecord" :key="resRecord.id">{{ resRecord}}</p>
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
      researchedAuthors: [],

      titre: "",
      annee: "",
      editor: "",
      researchedRef: [],

      cote: "",
      keywords: "",
      researchedRecord: [],
      provenance: "",

      message: "",
    }
  },
  methods: {
    search: function () {

      const formAuthor = {
        first_name: this.first_name,
        family_name: this.family_name,

      };
      axios.post("/api/authors/chercher", formAuthor).then(
          (response) => {
            if(response.data.success) {
              this.researchedAuthors = response.data.results;
            }
          }
      );
      const formRef = {
        annee: this.annee,
        editeur: this.editor,
        cote: this.cote,
        titre: this.titre
      };
      axios.post("/api/reference-livre/chercher", formRef).then(
          (response) => {
            if(response.data.success) {
              // console.log("rechercher");
              this.researchedRef = response.data.results;
              // if(this.researchedRef.length === 0) {
              //   this.message = "Aucun résultat n'a été trouvé."
              // }
            }
          }
      );

      const formRecord = {
        cote: this.cote,
        annee: this.annee,
        provenance: this.provenance,
        aide_a_la_recherche: this.aide_a_la_recherche,
        valide: this.valide
      };

      axios.post("/api/enregistrement/chercher", formRecord).then(
          (response) => {
            if(response.data.success) {
              this.researchedRecord = response.data.results;
            }
          }
      );
    }
  }
}
</script>

<style scoped>

</style>