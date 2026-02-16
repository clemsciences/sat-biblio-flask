<template>
  <ListeEntreesNonApprouvees
      :retrieve-list-request="retrieveNotValidatedBookRecords"
      :go-to="goTo"
      caption="Enregistrements non validés"
      :per-page="perPage"
      :get-total-number-request="getNotValidatedBookRecordsCount"
      entry-type="enregistrement"
  />
</template>

<script>
import {getNotValidatedBookRecordsCount, retrieveNotValidatedBookRecords} from "@/services/api";
import ListeEntreesNonApprouvees from "@/components/admin/ListeEntreesNonApprouvees.vue";

export default {
  name: "ListeEnregistrementsNonApprouves",
  components: {ListeEntreesNonApprouvees},
  data: function() {
    return {
      perPage: 20,
    }
  },
  methods: {
    retrieveNotValidatedBookRecords: retrieveNotValidatedBookRecords,
    getNotValidatedBookRecordsCount: getNotValidatedBookRecordsCount,
    goTo() {

    }
  }

}
</script>

<style scoped>

</style>