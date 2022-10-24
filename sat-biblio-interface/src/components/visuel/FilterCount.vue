<template>
  <div>
    <b-badge id="filter-count" variant="secondary" class="m-3">{{ filteredItemCount }}/{{ totalItemCount }}</b-badge>
    <b-tooltip target="filter-count" triggers="hover" style="text-justify: auto;">
      Il y a {{ filteredItemCount }} éléments qui ont été filtrés parmi les {{ totalItemCount }} élements au total.
    </b-tooltip>
  </div>
</template>

<script>
export default {
  name: "FilterCount",
  props: {
    filteredItemCount: {
      type: Number
    },
    totalItemCount: {
      type: Number
    }
  }
}
</script>

<style scoped>

</style>