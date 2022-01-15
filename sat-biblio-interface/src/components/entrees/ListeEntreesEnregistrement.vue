<template>
  <ListeEntrees :retrieve-list-request="getEntryListAssociatedToBookRecords"
                :go-to="goTo"
                caption="Enregistrement"
                :per-page="perPage"
                :get-total-number-request="getEntryListAssociatedToBookRecordsCount"
                :entry-id="recordId"
  />
</template>

<script>

import ListeEntrees from "@/components/entrees/ListeEntrees";
import {getEntryListAssociatedToBookRecords, getEntryListAssociatedToBookRecordsCount} from "@/services/api";
import {goToEntryView} from "@/services/entries";

export default {
  name: "ListeEntreesEnregistrement",
  components: {ListeEntrees},
  props: {
    recordId: {
      type: Number,
    }
  },
  data: function() {
    return {
      entryCount: 0,
      entries: [],
      perPage: 20,
    }
  },
  methods: {
    getEntryListAssociatedToBookRecords: getEntryListAssociatedToBookRecords,
    getEntryListAssociatedToBookRecordsCount: getEntryListAssociatedToBookRecordsCount,
    goTo(row) {
      this.$router.push(goToEntryView(row.id, row.type_string));

    }
  }

}
</script>

<style scoped>

</style>