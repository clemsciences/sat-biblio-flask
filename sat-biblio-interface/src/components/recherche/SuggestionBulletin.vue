<template>
  <BContainer>
    <BFormGroup label="Recherche">
      <vue-typeahead-bootstrap
          v-model="namedEntityQuery"
        :items="fetchNamedEntities"
        :item-projection="s => s || ''"
        placeholder="Tapez le nom d'un lieu, d'une personne, etc"
      />
    </BFormGroup>
  </BContainer>
</template>

<script>
import {searchApproximateNamedEntities} from "@/services/api.js";

export default {
  name: "BulletinSuggestion",
  props: ['modelValue'],
  data: function() {
    return {
      namedEntityQuery: '',
    }
  },
  methods: {
    fetchNamedEntities(query) {
      return searchApproximateNamedEntities("?query=" + encodeURIComponent(query))
        .then(response => response.data.suggestions || []);
    },
  },
  watch: {
    namedEntityQuery(newValue) {
      if (newValue) this.$emit("update:modelValue", newValue);
    },
  }
}
</script>

<style scoped>

</style>
