<template>
  <BRow align-h="between" class="my-2">
    <BCol cols="8">
      <h2><slot>{{ title }}</slot></h2>
    </BCol>
    <BCol cols="2" v-if="info.length > 0">
      <InfoButton :label="info" :id="id"/>
    </BCol>
  </BRow>
</template>

<script>
import InfoButton from "./InfoButton.vue";
export default {
  name: "AppTitle",
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