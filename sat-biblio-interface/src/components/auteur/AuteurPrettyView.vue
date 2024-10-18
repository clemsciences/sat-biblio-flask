<template>
  <div>
    <span v-if="author.family_name === '[collectif] (-)'">
      Collectif
    </span>
    <span v-else-if="author.family_name === '[anonyme] (-)'">
      Anonyme
    </span>
    <span v-else>
      {{ author.family_name }} ({{ author.first_name }})
    </span>
  </div>
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