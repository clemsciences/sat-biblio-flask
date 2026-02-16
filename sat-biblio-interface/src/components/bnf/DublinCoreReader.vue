<template>
  <BContainer>
    <h3>{{ record.title }}</h3>
    <BListGroup>
      <BListGroupItem>{{ record.description }}</BListGroupItem>
      <BListGroupItem>{{ record.creator }}</BListGroupItem>
      <BListGroupItem>{{ record.publisher }}</BListGroupItem>
      <BListGroupItem>{{ record.date }}</BListGroupItem>
      <BListGroupItem>{{ record.subject }}</BListGroupItem>
      <BListGroupItem>{{ record.type }}</BListGroupItem>
      <BListGroupItem>{{ record.format }}</BListGroupItem>
      <BListGroupItem>{{ record.source }}</BListGroupItem>
      <BListGroupItem>{{ record.relation }}</BListGroupItem>
      <BListGroupItem>{{ record.rights }}</BListGroupItem>

    </BListGroup>

  </BContainer>

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