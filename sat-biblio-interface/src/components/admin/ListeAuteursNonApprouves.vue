<template>
  <ListeEntreesNonApprouvees
     :retrieve-list-request="retrieveNotValidatedAuthors"
      :go-to="goTo"
      caption="Auteur"
      :per-page="perPage"
      entry-type="auteur"
  />
</template>

<script>
import {
  retrieveNotValidatedAuthors,
} from "@/services/api";
import ListeEntreesNonApprouvees from "@/components/admin/ListeEntreesNonApprouvees.vue";
export default {
  name: "ListeAuteursNonApprouves",
  components: {ListeEntreesNonApprouvees},
  methods: {
    retrieveNotValidatedAuthors: retrieveNotValidatedAuthors,
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