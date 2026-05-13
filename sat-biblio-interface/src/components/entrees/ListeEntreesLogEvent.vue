<template>
  <BContainer>
    <ListEntriesOfEntry
        :retrieve-list-request="getLogEventListByUser"
        :perPage="perPage"
        :caption="caption"
        :go-to="goTo"
    :entry-id="userId">

    </ListEntriesOfEntry >
  </BContainer>
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
    }
  },
  methods: {
    getLogEventListByUser() {
      retrieveLogEvents()
    },
    goTo(row) {
      console.log(row);
    }
  }

}
</script>

<style scoped>

</style>