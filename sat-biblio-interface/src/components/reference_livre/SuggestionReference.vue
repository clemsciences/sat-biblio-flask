<template>
  <BFormGroup label="Référence">
    <vue-typeahead-bootstrap
      v-if="!disabled"
      v-model="selectedReferenceTemp"
      :items="fetchReferences"
      :item-projection="s => s ? s.text : ''"
      placeholder="Tapez le titre d'un ouvrage"
      :disabled="disabled"
    />
    <BFormInput :model-value="selectedReference.text" readonly/>

    <BButton class="my-3" v-if="!disabled"
              :disabled="disabled || Object.keys(selectedReference).length === 0"
              @click="removeReference">
      Enlever référence
    </BButton>
    <BButton v-if="selectedReference.value && selectedReference.value > 0"
              @click="goToReference" class="m-3">
      Voir référence
    </BButton>
  </BFormGroup>
</template>

<script>
import {searchNearBookReferences} from "@/services/api";

export default {
  name: "ReferenceSuggestion",
  props: {
    modelValue: Object, // selectedReference
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      selectedReferenceTemp: null,
      selectedReference: {},
    }
  },
  methods: {
    fetchReferences(query) {
      if (query.length < 2) return Promise.resolve([]);
      return searchNearBookReferences(`titre=${encodeURIComponent(query)}`)
        .then(response => response.data.success ? response.data.suggestedReferences : []);
    },
    addReference: function (item) {
      this.selectedReference = item;
      this.$nextTick(() => { this.selectedReferenceTemp = null; });
      this.$emit('update:modelValue', item);
    },
    goToReference: function() {
      if(this.selectedReference.value) {
        let routeData = this.$router.resolve(`/reference-livre/lire/${this.selectedReference.value}`);
        window.open(routeData.href, '_blank');
      }
    },
    removeReference: function() {
      const newValue = { ...this.selectedReference, value: -1, text: "" };
      this.$emit('update:modelValue', newValue);
    }
  },
  watch: {
    selectedReferenceTemp(newItem) {
      if (newItem) this.addReference(newItem);
    },
    modelValue: function (newValue) {
      this.selectedReference = newValue;
    }
  }
}
</script>

<style scoped>

</style>
