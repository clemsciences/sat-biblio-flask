<template>
  <b-container>
    <ListEntriesOfEntry
        :retrieve-list-request="getLogEventListByUser"
        :perPage="perPage"
        :caption="caption"
        :get-total-number-request="getLogEventListCountByUser"
        :go-to="goTo"
    :entry-id="userId">

    </ListEntriesOfEntry >
  </b-container>
</template>

<script>
import ListEntriesOfEntry from "@/components/entrees/ListEntriesOfEntry";
import {retrieveLogEvents, getLogEventsCount} from "@/services/api";

export default {
  name: "ListeEntreesLogEvent",
  components: {ListEntriesOfEntry},
  props: {
    userId: {
      type: Number
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
    getLogEventListByUser() {
      retrieveLogEvents()
    },
    getLogEventListCountByUser() {
      getLogEventsCount()
    },
    goTo(row) {
      console.log(row);
    }
  }

}
</script>

<style scoped>

</style>