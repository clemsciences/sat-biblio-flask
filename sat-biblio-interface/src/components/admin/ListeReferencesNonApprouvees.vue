<template>
  <ListeEntreesNonApprouvees
      :go-to="goTo"
      :retrieve-list-request="retrieveNotValidatedBookReferences"
      :per-page="perPage"
      entry-type="référence bibliographique"
    />

</template>

<script>
import ListeEntreesNonApprouvees from "@/components/admin/ListeEntreesNonApprouvees.vue";
import {getNotValidatedBookReferencesCount, retrieveNotValidatedBookReferences} from "@/services/api.js";
export default {
  name: "ListeReferencesNonApprouvees",
  components: {ListeEntreesNonApprouvees},
  data: function() {
    return {
      perPage: 20,
    }
  },
  methods: {
    retrieveNotValidatedBookReferences: retrieveNotValidatedBookReferences,
    goTo() {

    }
  }
}
</script>

<style scoped>

</style>