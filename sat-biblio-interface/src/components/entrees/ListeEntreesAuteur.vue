<template>
  <BContainer>
    <ListEntriesOfEntry
        :retrieve-list-request="getEntryListAssociatedToAuthor"
        :perPage="perPage"
        :caption="caption"
        :go-to="goTo"
        :entry-id="authorId"
        entry-type="reference">

    </ListEntriesOfEntry >
  </BContainer>

</template>

<script>
import ListEntriesOfEntry from "@/components/entrees/ListEntriesOfEntry.vue";
import {getEntryListAssociatedToAuthor} from "@/services/api.js";
import {goToEntryView} from "@/services/entries.js";
import {
  BContainer
} from "bootstrap-vue-next";
export default {
  name: "ListeEntreesAuteur",
  components: {ListEntriesOfEntry, BContainer},
  props: {
    authorId: {
      type: Number,
    }
  },
  data: function() {
    return {
      perPage: 20,
      caption: "",
      entryCount: 0,
      entries: []
    }
  },
  methods: {
    getEntryListAssociatedToAuthor: getEntryListAssociatedToAuthor,
    goTo: function(row) {
      this.$router.push(goToEntryView(row.id, row.type_string));
    },
  }
}
</script>

<style scoped>

</style>