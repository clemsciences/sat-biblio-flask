<template>
  <div>
    <h2>Recherche</h2>
    <BForm @submit.prevent="search">
      <BFormGroup label="Prénom">
        <BFormInput v-model="first_name" type="text"/>
      </BFormGroup>
      <BFormGroup label="Nom de famille">
        <BFormInput v-model="family_name" type="text"/>
      </BFormGroup>
      <BFormGroup label="Année">
        <BFormInput v-model="annee" type="text"/>
      </BFormGroup>
      <BFormGroup label="Editeur">
        <BFormInput v-model="editor" type="text"/>
      </BFormGroup>
      <BFormGroup label="Titre">
        <BFormInput v-model="titre" type="text"/>
      </BFormGroup>
      <BFormGroup label="Cote">
      <BFormInput v-model="cote" type="text"/>
      </BFormGroup>
      <BFormGroup label="Provenance">
      <BFormInput v-model="provenance" type="text"/>
      </BFormGroup>
      <BFormGroup label="Mots-clef">
        <BFormInput v-model="keywords" type="text"/>
      </BFormGroup>
      <BButton type="submit">Rechercher</BButton>
      <span class="mx-3">{{ message }}</span>
    </BForm>

    <p v-for="resAuthor in researchedAuthors" :key="resAuthor.id">{{ resAuthor }}</p>

    <p v-for="resRef in researchedRef" :key="resRef.id">{{ resRef }}</p>
    <p v-for="resRecord in researchedRecord" :key="resRecord.id">{{ resRecord}}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RechercheView",
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