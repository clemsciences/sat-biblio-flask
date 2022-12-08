<template>
  <b-container>
    <b-form-group label="Recherche">
      <vue-typeahead-bootstrap
          v-model="namedEntityQuery"
        :data="suggestedNamedEntities"
        :serializer="s => s"
        placeholder="Tapez le nom d'un lieu, d'une personne, etc"
        @hit="addNamedEntity($event)"
      />
    </b-form-group>
  </b-container>

</template>

<script>
import {searchApproximateNamedEntities} from "@/services/api";

export default {
  name: "SuggestionBulletin",
  data: function() {
    return {
      namedEntityQuery: '',
      suggestedNamedEntities: [],
      // selectedNamedEntityId: -1,

    }
  },
  methods: {
    addNamedEntity: function (event) {
      // this.selectedNamedEntityId = event;
      this.namedEntityQuery = event;
      this.$emit("input", this.namedEntityQuery);
    },

    getSuggestedNamedEntities(query) {
      // if (query.length >= 2) {
        searchApproximateNamedEntities("?query="+encodeURIComponent(query)).then(
            (response) => {
              this.suggestedNamedEntities = response.data.suggestions;
            }
        );
      // } else {
      //   searchWorks(encodeURIComponent(`?approximate=false&query=${query}`)).then(
      //       (response) => {
      //         this.suggestedNamedEntities = response.data.suggestions;
      //       }
      //   );
      // }
    }
  },
  watch: {
    namedEntityQuery: function(newValue) {
      this.getSuggestedNamedEntities(newValue);
    }
  }

}
</script>

<style scoped>

</style>