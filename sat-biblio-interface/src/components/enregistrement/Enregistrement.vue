<template>
  <div>
    <h2>Nouvel enregistrement</h2>
    <b-form @submit.prevent="saveRecord">
      <b-form-group label="Référence">
        <vue-typeahead-bootstrap
          v-model="reference_query"
          :data="suggestedReferences"
          :serializer="s => s.text"
          placeholder="Tapez le titre d'un ouvrage"
          @hit="addReference($event)"
        />
        <b-form-input v-model="selectedReference.text" readonly/>
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
      <b-button type="submit">Enregistrer</b-button><span class="mx-3">{{ message }}</span>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Enregistrement",
  data: function () {
    return {
      reference_query: "",
      reference: {value: -1, text: ""},
      selectedReference: {text: "", value: -1},
      suggestedReferences: [],
      description: "",
      cote: "",
      annee: "",
      nb_exemplaire_supp: 0,
      provenance: "",
      mots_clef: "",
      // validated: false,
      message: ""
    }
  },
  methods: {
    addReference: function (event) {
      this.selectedReference = event;
      this.reference_query = "";
    },
    getSuggestedReferences: function (query) {
      if(query.length >= 2) {
        axios.get("/api/reference-livre/chercher-proches?titre=:query".replace(":query", query))
            .then((response) => {
              if (response.data.success) {
                console.log("suggestedReferences", response.data)
                this.suggestedReferences = response.data.suggestedReferences;
              }
            }).catch();
      }
    },
    saveRecord: function () {
      const formData = {
          id_reference: this.selectedReference.value,
          description: this.description,
          cote: this.cote,
          annee: this.annee,
          nb_exemplaire_supp: this.nb_exemplaire_supp,
          provenance: this.provenance,
          mots_clef: this.mots_clef
      };
      axios.post("/api/enregistrement/creer", formData)
          .then((response) => {
            if(response.data.success) {
              console.log("record saved");
              this.message = "L'enregistrement a été sauvegardé.";
            } else {
              console.log("bizarre");
              this.message = "Echec de la sauvegarde de l'enregistrement.";
            }
          })
          .catch(
            (reason) => {
              console.log(reason);
            }
          );
    }
  },
  watch: {
    reference_query: function (newValue) {
      this.getSuggestedReferences(newValue);
    },
  }
}
</script>

<style scoped>

</style>