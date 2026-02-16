<template>
  <BContainer>
    <BListGroup>
      <BListGroupItem v-for="item in works" :key="item.id_">
        <router-link :to="{ name: 'works-item', params: {id: item.id_}}">{{ item.publication_type }} {{ item.year }}</router-link>
      </BListGroupItem>
    </BListGroup>
  </BContainer>

</template>

<script>
import {getPublishedWorks} from "@/services/api";

export default {
  name: "WorkListView",
  data: function() {
    return {
      works: []
    };
  },
  mounted() {
    this.retrieveWorkList();
  },
  methods: {
    retrieveWorkList() {
      getPublishedWorks("").then((value) => {
        if(value.data.success) {
          this.works = value.data.result;
        }

      });

    }
  }
}
</script>

<style scoped>

</style>