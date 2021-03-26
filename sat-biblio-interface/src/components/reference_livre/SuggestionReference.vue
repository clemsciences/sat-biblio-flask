<template>
  <b-form-group label="Référence">
    <vue-typeahead-bootstrap
      v-model="reference_query"
      :data="suggestedReferences"
      :serializer="s => s.text"
      placeholder="Tapez le titre d'un ouvrage"
      @hit="addReference($event)"
    />
    <b-form-input v-model="value.text" readonly/>
  </b-form-group>
</template>

<script>
import {searchNearBookReferences} from "../../services/api";

export default {
  name: "SuggestionReference",
  props: {
    value: Object // selectedReference
  },
  data: function () {
    return {
      reference_query: "",
      // reference: {value: -1, text: ""},
      // selectedReference: {text: "", value: -1},
      suggestedReferences: [],
    }
  },
  methods: {
    addReference: function (event) {
      this.reference_query = "";
      this.$emit('input', event);      // this.selectedReference = event;
    },
    getSuggestedReferences: function (query) {
      if(query.length >= 2) {
        searchNearBookReferences(`titre=${query}`).then((response) => {
              if (response.data.success) {
                console.log("suggestedReferences", response.data)
                this.suggestedReferences = response.data.suggestedReferences;
              }
            }).catch();
      }
    },
  },
  watch: {
    reference_query: function (newValue) {
      this.getSuggestedReferences(newValue);
    },
  }
}
</script>

<style scoped>

</style>