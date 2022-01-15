<template>
  <b-container>
    <ListeEntrees
        :retrieve-list-request="getEntryListAssociatedToAuthor"
        :perPage="perPage"
        :caption="caption"
        :get-total-number-request="getEntryListAssociatedToAuthorCount"
        :go-to="goTo"
    :entry-id="authorId">

    </ListeEntrees >
  </b-container>

</template>

<script>
import ListeEntrees from "@/components/entrees/ListeEntrees";
import {getEntryListAssociatedToAuthor, getEntryListAssociatedToAuthorCount} from "@/services/api";
import {goToEntryView} from "@/services/entries";

export default {
  name: "ListeEntreesAuteur",
  components: {ListeEntrees},
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
    getEntryListAssociatedToAuthorCount: getEntryListAssociatedToAuthorCount,
    goTo: function(row) {
      this.$router.push(goToEntryView(row.id, row.type_string));
    },
  }
}
</script>

<style scoped>

</style>