<template>
  <span>{{ author.family_name }} ({{ author.first_name }})</span>
</template>

<script>
import {Author} from "@/services/objectManager";

export default {
  name: "AuteurPrettyView",
  props: {
    author: {
      type: Author,
    },
    mode: {
      type: String,
      default: "sat"
    }
  }
}
</script>

<style scoped>

</style>