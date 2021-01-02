<template>
  <div>
    <h2>Nouvel enregistrement</h2>
    <b-form @submit.prevent="saveRecord">
      <b-form-group label="Référence">
      <b-form-input v-model="reference"></b-form-input>
      </b-form-group>
      <!-- Recherche assisté de la référence -->
      <b-form-group label="Description">
      <b-form-textarea v-model="description"/>
      </b-form-group>
      <b-form-group label="Cote">
        <b-form-input v-model="cote"/>
      </b-form-group>
      <b-form-group label="Année">
        <b-form-input v-model="annee"/>
      </b-form-group>
      <b-form-group label="Nombre d'exemplaires supplémentaires">
        <b-form-input v-model="nb_exemplaire_supp"/>
      </b-form-group>
      <b-form-group label="Provenance">
        <b-form-input v-model="provenance"/>
      </b-form-group>
      <b-form-group label="Mots-clef">
        <b-form-input v-model="mots_clef"/>
      </b-form-group>
      <b-button type="submit">Enregistrer</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Enregistrement",
  data: function () {
    return {
      reference: "",
      description: "",
      cote: "",
      annee: "",
      nb_exemplaire_supp: 0,
      provenance: "",
      mots_clef: "",
      // validated: false
    }
  },
  methods: {
    saveRecord: function () {
      axios.post("/api/enregistrement/creer")
          .then((response) => {
            if(response.data.success) {
              console.log("record saved");
            }
          })
          .catch();
    }
  }
}
</script>

<style scoped>

</style>