<template>
  <div>
    <b-form @submit.prevent="updateRecord">
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
      <b-button v-show="selectedReference.value > 0" @click="goToRef">
        Voir référence bibliographique
      </b-button>
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
      <b-button type="submit">Valider</b-button><span class="mx-3">{{ message }}</span>
      </b-form>
      <b-button v-b-modal.suppression class="my-3">Supprimer</b-button>
      <b-modal id="suppression" title="Suppression de l'enregistrement"
          cancel-title="Annuler" ok-title="Supprimer" @ok="deleteRecord">
          <p>Êtes-vous sûr de supprimer cet enregistrement ?</p>
        </b-modal>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LireEnregistrement",
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
      validated: false,
      message: "",

    }
  },
  methods: {
    addReference: function(event) {
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
    loadRecord: function() {
      axios.get('/api/enregistrement/lire/'+this.$route.params.id).then(
          (value) => {
            if(value.data.success && value.data.enregistrement) {
              this.selectedReference = value.data.enregistrement.reference;
              this.description = value.data.enregistrement.description;
              this.cote = value.data.enregistrement.cote;
              this.annee = value.data.enregistrement.annee;
              this.nb_exemplaire_supp = value.data.enregistrement.nb_exemplaire_supp;
              this.provenance = value.data.enregistrement.provenance;
              this.mots_clef = value.data.enregistrement.mots_clef;
              this.validated = value.data.enregistrement.validated;
            }
          }
      )
    },
    updateRecord: function() {
      const formData = {
          id_reference: this.selectedReference.value,
          description: this.description,
          cote: this.cote,
          annee: this.annee,
          nb_exemplaire_supp: this.nb_exemplaire_supp,
          provenance: this.provenance,
          mots_clef: this.mots_clef
      };
      axios.post("/api/enregistrement/modifier/"+this.$route.params.id, formData)
          .then((response) => {
            if(response.data.success) {
              console.log("record saved");
              this.message = "L'enregistrement a été mise à jour.";
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
    },
    deleteRecord: function() {
      axios.get("/api/enregistrement/supprimer/"+this.$route.params.id)
          .then(
              (response) => {
                if(response.data.success) {
                  console.log("référence livresque supprimée");
                  this.$router.push("/auteur/liste")
                } else {
                  this.saveMessage = "La référence n'a pas pu être supprimée."
                }
              }
          )
    },
    goToRef: function() {
      let routeData = this.$router.resolve("/reference-livre/lire/"+this.selectedReference.value);
      window.open(routeData.href, '_blank');
    }
  },
  mounted() {
    this.loadRecord();
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