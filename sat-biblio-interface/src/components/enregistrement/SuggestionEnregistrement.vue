<template>
  <BFormGroup label="Enregistrement">
    <vue-typeahead-bootstrap
      v-if="!disabled"
      v-model="selectedRecordTemp"
      :items="fetchRecords"
      :item-projection="s => s ? s.text : ''"
      placeholder="Tapez la cote ou le titre de l'enregistrement"
      :disabled="disabled"
    />
    <BFormInput :model-value="modelValue.text" readonly/>

    <div v-if="!disabled">
      <BButton v-if="modelValue.value > 0" @click="removeRecord" class="m-1">Enlever enregistrement</BButton>
      <BButton v-if="modelValue.value > 0" @click="goToRecord" class="m-1">Voir enregistrement</BButton>
    </div>
  </BFormGroup>
</template>

<script>
import {searchNearBookRecords} from "@/services/api";

export default {
  name: "RecordSuggestion",
  props: {
    modelValue: Object,
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      selectedRecordTemp: null,
    }
  },
  methods: {
    fetchRecords(query) {
      if (query.length < 2) return Promise.resolve([]);
      return searchNearBookRecords(`record=${encodeURIComponent(query)}`)
        .then(response => response.data.success ? response.data.suggestedRecords : []);
    },
    removeRecord: function() {
      const newValue = { ...this.modelValue, value: -1, text: "" };
      this.$emit('update:modelValue', newValue);
    },
    goToRecord: function() {
      let routeData = this.$router.resolve(`/enregistrement/lire/${this.modelValue.value}`);
      window.open(routeData.href, '_blank');
    },
    addRecord: function (item) {
      this.$nextTick(() => { this.selectedRecordTemp = null; });
      this.$emit('update:modelValue', item);
    },
  },
  watch: {
    selectedRecordTemp(newItem) {
      if (newItem) this.addRecord(newItem);
    },
  }
}
</script>

<style scoped>

</style>
