<template>
  <BRow align-h="between">
    <BCol cols="8"></BCol>
    <BCol cols="2">
      <BBadge pill :variant="approvedVariant" :id="id">{{ message }}</BBadge>
      <BTooltip :target="id" triggers="hover" class="my-tooltip">
        {{ message }} par le gestionnaire de la bibliothèque.
      </BTooltip>
    </BCol>
  </BRow>
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