<script>

import Teleport from 'vue2-teleport';
export default {
  name: "JsonLd",
  components: {Teleport},
  props: {
      jsonData: {
        type: Object,
      }
    },

}
</script>

<template>
  <Teleport to="head">
    <component :is="'script'" type="application/ld+json">
      {{ jsonData }}
    </component>
  </Teleport>

</template>

<style scoped>

</style>