<template>
  <div>
    <h2>Liste des références</h2>
    <b-form @submit.prevent="">
<!--      <b-form-group>-->
<!--        <b-form-input v-model=""/>-->
<!--      </b-form-group>-->
      <b-list-group>
        <b-list-group-item :key="reference.id" v-for="reference in references">{{ reference.titre }}</b-list-group-item>
      </b-list-group>

    </b-form>
    <div v-show="references.length === 0">
      <p>Il n'y a aucune référence.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ListeReferenceLivre",
  data: function () {
    return {
      references: []
    }
  },
  methods: {
    retrieveReferenceList: function () {
      axios.get("/api/reference-livre/liste").then(
          (response) => {
            if(response.data.success) {
              this.references = response.data.references;
            }
          }
      )
    }
  },
  mounted() {
    this.retrieveReferenceList();
  }
}
</script>

<style scoped>

</style>