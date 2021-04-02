<template>
  <b-row align-h="between" class="my-2">
    <b-col cols="8">
      <h2><slot>{{ title }}</slot></h2>
    </b-col>
    <b-col cols="2" v-if="info.length > 0">
      <InfoButton :label="info" :id="id"/>
    </b-col>
  </b-row>
</template>

<script>
import InfoButton from "./InfoButton";
export default {
  name: "Title",
  components: {InfoButton},
  props: {
    title: String,
    info: String,
    id: String
  }
}
</script>

<style scoped>

</style>