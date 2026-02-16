<script>

export default {
  name: "JsonLdHeader",
  components: {},
  props: {
      jsonData: {
        type: Object,
      }
    },

}
</script>

<template>
  <teleport to="head">
    <component :is="'script'" type="application/ld+json">
      {{ jsonData }}
    </component>
  </teleport>

</template>

<style scoped>

</style>