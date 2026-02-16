<template>

  <BFormGroup label="Enregistrement">
    <vue-typeahead-bootstrap
      v-if="!disabled"
      v-model="recordQuery"
      :data="suggestedRecords"
      :serializer="s => s.text"
      placeholder="Tapez la cote ou le titre de l'enregistrement"
      @update:model-value="getSuggestedRecords"
      @hit="addRecord($event)"
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
    modelValue: Object, // selectedReference
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      recordQuery: "",
      // reference: {value: -1, text: ""},
      // selectedReference: {text: "", value: -1},
      suggestedRecords: [],
    }
  },
  methods: {
    removeRecord: function() {
      const newValue = { ...this.modelValue, value: -1, text: "" };
      this.$emit('update:modelValue', newValue);
    },
    goToRecord: function() {
      let routeData = this.$router.resolve(`/enregistrement/lire/${this.modelValue.value}`);
      window.open(routeData.href, '_blank');
    },
    addRecord: function (event) {
      this.recordQuery = "";
      this.$emit('update:modelValue', event);
    },
    getSuggestedRecords: function (query) {
      if(query.length >= 2) {
        searchNearBookRecords(`record=${encodeURIComponent(query)}`)
            .then((response) => {
              if (response.data.success) {
                console.log("suggestedRecords", response.data)
                this.suggestedRecords = response.data.suggestedRecords;
              }
            }).catch();
      }
    },
  },
  watch: {
    // recordQuery: function (newValue) {
    //   this.getSuggestedRecords(newValue);
    // },
    modelValue: function(newValue) {
      console.log(newValue);
    }
  }
}
</script>

<style scoped>

</style>