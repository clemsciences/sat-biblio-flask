<template>
  <div>
    <h2>Catalogue</h2>
    <b-list-group>
      <b-list-group-item :key="enregistrement.id" v-for="enregistrement in enregistrements">
        {{ enregistrement.reference.titre }}
        {{ enregistrement.description }}
        {{ enregistrement.cote }}
        {{ enregistrement.annee }}
        {{ enregistrement.nb_exemplaire_supp }}
        {{ enregistrement.provenance }}
        {{ enregistrement.mots_clef }}
        {{ enregistrement.valide }}
      </b-list-group-item>
    </b-list-group>
    <div v-show="enregistrements.length === 0">
      <p>Il n'y a aucun enregistrement.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ListeEnregistrement",
  data: function () {
    return {
      enregistrements: []
    }
  },
  methods: {
    retrieveEnregistrementList: function () {
      axios.get("/api/enregistrement/liste")
          .then(
              (response) => {
                if(response.data.success) {
                  console.log("youhou");
                }
              }
          );
    }
  },
  mounted() {
    this.retrieveEnregistrementList();
  }
}
</script>

<style scoped>

</style>