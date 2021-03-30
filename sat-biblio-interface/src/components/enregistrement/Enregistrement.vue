<template>
  <div>
    <h2>Nouvel enregistrement</h2>
    <b-form @submit.prevent="saveRecord">
      <SuggestionReference v-model="selectedReference"/>
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
import {createBookRecord} from "../../services/api";
import SuggestionReference from "../reference_livre/SuggestionReference";

export default {
  name: "Enregistrement",
  components: {SuggestionReference},
  data: function () {
    return {
      selectedReference: {value: -1, text: ""},
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
      createBookRecord(formData)
          .then((response) => {
            if(response.data.success) {
              console.log("record saved");
              this.message = "L'enregistrement a été sauvegardé.";
              this.selectedReference = {value: -1, text: ""};
              this.description = "";
              this.cote = "";
              this.annee = "";
              this.nb_exemplaire_supp = "";
              this.provenance = "";
              this.mots_clef = "";
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
}
</script>

<style scoped>

</style>