<template>
  <b-row>
    <b-col>
      <b-badge pill :variant="borrowingColor" :id="`${recordId}`">{{ message }}</b-badge>
      <b-tooltip :target="`${recordId}`" triggers="hover" class="my-tooltip">
        {{ message }}.
      </b-tooltip>
    </b-col>
  </b-row>
</template>

<script>
import {getCurrentBorrowingStateOfRecord} from "@/services/api";

export default {
  name: "BorrowingState",
  props: {
    recordId: {
      type: Number
    },

  },
  data: function() {
    return {
      isBorrowed: false,

    };
  },
  mounted() {
    this.loadBorrowingState();
  },
  methods: {
    loadBorrowingState() {
      getCurrentBorrowingStateOfRecord(this.recordId).then(
          (response) => {
            if(response.data.success) {
              this.isBorrowed = response.data.is_being_borrowed;
            }
          }
      )

    },
  },
  computed: {
    borrowingColor: function() {
      return this.isBorrowed ? "warning" : "success";
    },
    message: function() {
      return this.isBorrowed ? "Le livre est déjà emprunté" : "Le livre est consultable et il peut être emprunté si vous êtes sociétaire à la SAT."
    }
  }
}
</script>

<style scoped>

</style>