<template>
  <b-row align-h="between">
    <b-col cols="8"></b-col>
    <b-col cols="2">
      <b-badge pill :variant="approvedVariant" :id="id">{{ message }}</b-badge>
      <b-tooltip :target="id" triggers="hover" class="my-tooltip">
        {{ message }} par le gestionnaire de la bibliothèque.
      </b-tooltip>
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: "ValidEntry",
  props: {
    approved: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      id: "a"
    }
  },
  computed: {
    approvedVariant: function() {
      return this.approved ? "success" : "danger";
    },
    message() {
      return this.approved ? "Approuvé" : "Pas encore approuvé";
    }
  }
}
</script>

<style scoped>

</style>