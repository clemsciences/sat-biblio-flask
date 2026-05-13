<template>
  <ListEntriesOfEntry
      :retrieve-list-request="getEntryListAssociatedToBookRecords"
      :go-to="goTo"
      caption="Enregistrement"
      :per-page="perPage"
      :entry-id="recordId"
      entry-type="reference"
  />
</template>

<script>

import ListEntriesOfEntry from "@/components/entrees/ListEntriesOfEntry.vue";
import {getEntryListAssociatedToBookRecords, getEntryListAssociatedToBookRecordsCount} from "@/services/api.js";
import {goToEntryView} from "@/services/entries";

export default {
  name: "ListeEntreesEnregistrement",
  components: {ListEntriesOfEntry},
  props: {
    recordId: {
      type: Number,
    }
  },
  data: function() {
    return {
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