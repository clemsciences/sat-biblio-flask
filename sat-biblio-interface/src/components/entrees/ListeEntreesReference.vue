<template>
  <ListEntriesOfEntry :retrieve-list-request="getEntryListAssociatedToReference"
                :go-to="goTo"
                caption="Enregistrement"
                :per-page="perPage"
                :get-total-number-request="getEntryListAssociatedToReferenceCount"
                :entry-id="referenceId"
  />
</template>

<script>
import ListEntriesOfEntry from "@/components/entrees/ListEntriesOfEntry";
import {
  getEntryListAssociatedToReference,
  getEntryListAssociatedToReferenceCount
} from "@/services/api";
import {goToEntryView} from "@/services/entries";

export default {
  name: "ListeEntreesReference",
  components: {ListEntriesOfEntry},
  props: {
    referenceId: {
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
    getEntryListAssociatedToReference: getEntryListAssociatedToReference,
    getEntryListAssociatedToReferenceCount: getEntryListAssociatedToReferenceCount,
    goTo(row) {
      this.$router.push(goToEntryView(row.id, row.type_string));
    }
  }
}
</script>

<style scoped>

</style>