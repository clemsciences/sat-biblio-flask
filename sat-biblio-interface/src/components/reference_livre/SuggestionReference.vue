<template>
  <BFormGroup label="Référence">
    <vue-typeahead-bootstrap
      v-if="!disabled"
      v-model="reference_query"
      :data="suggestedReferences"
      :serializer="s => s.text"
      placeholder="Tapez le titre d'un ouvrage"
      @update:model-value="getSuggestedReferences"
      @hit="addReference($event)"
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
      reference_query: "",
      // reference: {value: -1, text: ""},
      // selectedReference: {text: "", value: -1},
      suggestedReferences: [],
      selectedReference: {},
    }
  },
  methods: {
    addReference: function (event) {
      this.reference_query = "";
      this.selectedReference = event;
      console.log(event);
      this.$emit('update:modelValue', event);      // this.selectedReference = event;
    },
    goToReference: function() {
      if(this.selectedReference.value) {
        let routeData = this.$router.resolve(`/reference-livre/lire/${this.selectedReference.value}`);
        window.open(routeData.href, '_blank');
      }
    },
    getSuggestedReferences: function (query) {
      if(query.length >= 2) {
        searchNearBookReferences(`titre=${encodeURIComponent(query)}`)
            .then((response) => {
              if (response.data.success) {
                console.log("suggestedReferences", response.data)
                this.suggestedReferences = response.data.suggestedReferences;
              }
            }).catch();
      }
    },
    removeReference: function() {
      const newValue = { ...this.selectedReference, value: -1, text: "" };
      this.$emit('update:modelValue', newValue);
    }
  },
  watch: {
    // reference_query: function (newValue) {
    //   this.getSuggestedReferences(newValue);
    // },
    modelValue: function (newValue) {
      this.selectedReference = newValue;
    }
  }
}
</script>

<style scoped>

</style>