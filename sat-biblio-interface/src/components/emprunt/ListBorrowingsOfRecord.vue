<template>
  <div>
    <BorrowingTable v-if="borrowings.length > 0" :borrowings="borrowings"/>
    <p v-else>Cette entrée n'a jamais été empruntée.</p>

  </div>
</template>

<script>
import {getBorrowingStateOfRecord} from "@/services/api";
import BorrowingTable from "@/components/emprunt/BorrowingTable";

export default {
  name: "ListBorrowingsOfRecord",
  components: {BorrowingTable},
  props: {
    recordId: {
      type: Number
    }
  },
  data: function() {
    return {
      borrowings: [],
    };
  },
  mounted() {
    this.loadAllBorrowingsOfRecord();
  },
  methods: {
    loadAllBorrowingsOfRecord() {
      getBorrowingStateOfRecord(this.recordId).then(
          (response) => {
            if(response.data.success) {
              this.borrowings = response.data.borrowings;
              console.log(this.borrowings);
            }
          }
      )
    }
  },

}
</script>

<style scoped>

</style>