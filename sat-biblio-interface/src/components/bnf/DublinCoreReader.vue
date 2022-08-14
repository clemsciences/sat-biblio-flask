<template>
  <b-container>
    <h3>{{ record.title }}</h3>
    <b-list-group>
      <b-list-group-item>{{ record.description }}</b-list-group-item>
      <b-list-group-item>{{ record.creator }}</b-list-group-item>
      <b-list-group-item>{{ record.publisher }}</b-list-group-item>
      <b-list-group-item>{{ record.date }}</b-list-group-item>
      <b-list-group-item>{{ record.subject }}</b-list-group-item>
      <b-list-group-item>{{ record.type }}</b-list-group-item>
      <b-list-group-item>{{ record.format }}</b-list-group-item>
      <b-list-group-item>{{ record.source }}</b-list-group-item>
      <b-list-group-item>{{ record.relation }}</b-list-group-item>
      <b-list-group-item>{{ record.rights }}</b-list-group-item>

    </b-list-group>

  </b-container>

</template>

<script>
export default {
  name: "DublinCore",
  props: {
    record: Object
  },
  data: function() {
    return {
    };
  }
}
</script>

<style scoped>

</style>