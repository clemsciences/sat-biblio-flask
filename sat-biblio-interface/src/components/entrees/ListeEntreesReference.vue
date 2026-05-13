<template>
  <ListEntriesOfEntry :retrieve-list-request="getEntryListAssociatedToReference"
                :go-to="goTo"
                caption="Enregistrement"
                :per-page="perPage"
                :entry-id="referenceId"
                entry-type="record"
  />
</template>

<script>
import ListEntriesOfEntry from "@/components/entrees/ListEntriesOfEntry.vue";
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
      perPage: 20,
    }
  },
  methods: {
    getEntryListAssociatedToReference: getEntryListAssociatedToReference,
    goTo(row) {
      this.$router.push(goToEntryView(row.item.id, row.item.type_string));
    }
  }
}
</script>

<style scoped>

</style>