<template>
  <ListeEntreesNonApprouvees
      :go-to="goTo"
      :retrieve-list-request="retrieveNotValidatedBookReferences"
      :get-total-number-request="getNotValidatedBookReferencesCount"
      :per-page="perPage"
      entry-type="référence bibliographique"
    />

</template>

<script>
import ListeEntreesNonApprouvees from "@/components/admin/ListeEntreesNonApprouvees";
import {getNotValidatedBookReferencesCount, retrieveNotValidatedBookReferences} from "@/services/api";
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
    getNotValidatedBookReferencesCount: getNotValidatedBookReferencesCount,
    goTo() {

    }
  }
}
</script>

<style scoped>

</style>