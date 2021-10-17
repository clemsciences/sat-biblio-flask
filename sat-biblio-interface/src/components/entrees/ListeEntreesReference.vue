<template>
  <ListeEntrees :retrieve-list-request="getEntryListAssociatedToReference"
                :go-to="goTo"
                caption="Enregistrement"
                :per-page="perPage"
                :get-total-number-request="getEntryListAssociatedToReferenceCount"
                :entry-id="referenceId"
  />
</template>

<script>
import ListeEntrees from "@/components/entrees/ListeEntrees";
import {
  getEntryListAssociatedToReference,
  getEntryListAssociatedToReferenceCount
} from "@/services/api";

export default {
  name: "ListeEntreesReference",
  components: {ListeEntrees},
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
    goTo(item) {
      console.log(item);
    }
  }
}
</script>

<style scoped>

</style>