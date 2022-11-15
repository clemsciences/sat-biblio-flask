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

    <b-button v-if="value.value > 0" @click="removeRecord" class="m-1">Enlever enregistrement</b-button>
    <b-button v-if="value.value > 0" @click="goToRecord" class="m-1">Voir enregistrement</b-button>
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
    removeRecord: function() {
      this.value.value = -1;
      this.value.text = "";
      this.$emit('input', this.value);
    },
    goToRecord: function() {
      let routeData = this.$router.resolve(`/enregistrement/lire/${this.value.value}`);
      window.open(routeData.href, '_blank');
    },
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
    value: function(newValue) {
      console.log(newValue);
    }
  }
}
</script>

<style scoped>

</style>