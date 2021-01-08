<template>
  <div>
    <h2>Liste des auteurs</h2>
    <b-list-group>
      <b-list-group-item :key="author.id" v-for="author in authors">
      {{ author.first_name}} {{ author.family_name}}
      <span><b-button :to="'/auteur/lire/'+author.id">Voir/Modifier</b-button></span>
      </b-list-group-item>
    </b-list-group>
    <div v-show="authors.length === 0">
      <p>Il n'y a aucun auteur.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ListeAuteur",
  data: function () {
    return {
      authors: []
    }
  },
  methods: {
    retrieveAuthors: function() {
      axios.get("/api/auteur/liste").then(
          (response) => {
            if(response.data.success) {
              this.authors = response.data.authors;
            }
          }
      ).catch(
          (reason => console.log(reason))
      );
    }
  },
  mounted() {
    this.retrieveAuthors();
  }
}
</script>

<style scoped>

</style>