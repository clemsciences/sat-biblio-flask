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
import {getEntryListAssociatedToAuthor, getEntryListAssociatedToAuthorCount} from "@/services/api.js";
import {goToEntryView} from "@/services/entries.js";
import {
  BButton,
  BCol,
  BContainer,
  BFormGroup,
  BFormInput, BFormRadioGroup, BFormSelect, BModal,
  BPagination,
  BRow,
  BTable
} from "bootstrap-vue-next";
import AppTitle from "@/components/visuel/AppTitle.vue";
import FilterCount from "@/components/visuel/FilterCount.vue";
export default {
  name: "ListeEntreesAuteur",
  components: {ListEntriesOfEntry, BButton, BContainer, BRow, BPagination, BCol,
    BFormGroup, BFormInput, BFormRadioGroup, BFormSelect,
    BModal, BTable, AppTitle, FilterCount},
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