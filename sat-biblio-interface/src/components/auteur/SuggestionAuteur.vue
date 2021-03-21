<template>
  <div>
    <b-form-group label="Auteurs">
      <vue-typeahead-bootstrap
        v-model="author_query"
        :data="suggestedAuthors"
        :serializer="s => s.text"
        placeholder="Tapez le prénom ou le nom de l'auteur"
        @hit="addAuthor($event)"
      />
  <!--        <b-form-input readonly v-if="selectedAuthor" v-model="selectedAuthor"/> &lt;!&ndash; pour chercher l'auteur &ndash;&gt;-->
    </b-form-group>
    <b-form-group :label="selectedAuthorsMessage">
      <b-form-select :options="value" :select-size="5" size="sm"></b-form-select>
    </b-form-group>
  </div>
</template>

<script>
import {searchNearAuthors} from "../../services/api";

export default {
name: "SuggestionAuteur",
  props: {
    value: Array,  // selectedAuthors
  },
  data: function () {
    return {
      author_query: '',
      suggestedAuthors: [],
      selectedAuthor: '',
      selectedAuthorsMessage: "Les auteurs sélectionnés vont s'afficher en dessous.",
    }
  },
  methods: {
    getSuggestedAuthors: function (query) {
      if (query.length >= 2) {
        searchNearAuthors(`auteur=${query}`)
            .then((response) => {
              if (response.data.success) {
                this.suggestedAuthors = response.data.suggestedAuthors;
              }
            }).catch();
      }
    },
    addAuthor: function(event) {
      this.selectedAuthor = event;
      this.selectedAuthors.push(event);
      this.author_query = "";
    },
  },
  watch: {
    author_query: function (newValue) {
      this.getSuggestedAuthors(newValue);
    },
    selectedAuthors: function (newValue) {
      if(newValue.length > 1) {
        this.selectedAuthorsMessage = "Auteurs sélectionnés"
      } else {
        this.selectedAuthorsMessage = "Auteur sélectionné"
      }
    }
  }
}
</script>

<style scoped>

</style>