<template>
  <ListeEntreesNonApprouvees
  :retrieve-list-request="retrieveNotValidatedAuthors"
      :go-to="goTo"
      caption="Auteur"
      :per-page="perPage"
      :get-total-number-request="getNotValidatedAuthorsCount"
      entry-type="auteur"
  />
</template>

<script>
import {
  getNotValidatedAuthorsCount,
  retrieveNotValidatedAuthors,
} from "@/services/api";
import ListeEntreesNonApprouvees from "@/components/admin/ListeEntreesNonApprouvees";
export default {
  name: "ListeAuteursNonApprouves",
  components: {ListeEntreesNonApprouvees},
  methods: {
    retrieveNotValidatedAuthors: retrieveNotValidatedAuthors,
    getNotValidatedAuthorsCount: getNotValidatedAuthorsCount,
    goTo() {

    },

  },
  data: function () {
    return {
      perPage: 20,

    }
  }
}
</script>

<style scoped>

</style>