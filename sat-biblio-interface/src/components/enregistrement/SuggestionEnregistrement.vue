<template>

  <b-form-group label="Enregistrement">
    <vue-typeahead-bootstrap
      v-if="!disabled"
      v-model="recordQuery"
      :data="suggestedRecords"
      :serializer="s => s.text"
      placeholder="Tapez la cote ou le titre de l'enregistrement"
      @hit="addRecord($event)"
      :disabled="disabled"
    />
    <b-form-input v-model="value.text" readonly/>
  </b-form-group>

</template>

<script>
import {searchNearBookRecords} from "@/services/api";

export default {
  name: "SuggestionEnregistrement",
  props: {
    value: Object, // selectedReference
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
    addRecord: function (event) {
      this.recordQuery = "";
      this.$emit('input', event);
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
    recordQuery: function (newValue) {
      this.getSuggestedRecords(newValue);
    },
  }
}
</script>

<style scoped>

</style>