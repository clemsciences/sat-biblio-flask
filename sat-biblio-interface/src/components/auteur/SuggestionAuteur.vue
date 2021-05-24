<template>
  <b-container>
    <b-form-group label="Auteurs">
      <vue-typeahead-bootstrap
        v-model="author_query"
        :data="suggestedAuthors"
        :serializer="s => s.text"
        :disabled="disabled"
        placeholder="Tapez le prénom ou le nom de l'auteur"
        @hit="addAuthor($event)"
      />
  <!--        <b-form-input readonly v-if="selectedAuthor" v-model="selectedAuthor"/> &lt;!&ndash; pour chercher l'auteur &ndash;&gt;-->
    </b-form-group>
    <b-form-group :label="selectedAuthorsMessage">
      <b-form-select :options="value" :select-size="5" size="sm"></b-form-select>
    </b-form-group>
    <b-button :disabled="selectedAuthors.length === 0" @click="removeLastAuthor()">
      Retirer le dernier auteur ajouté
    </b-button>
  </b-container>
</template>

<script>
import {searchNearAuthors} from "@/services/api";

export default {
name: "SuggestionAuteur",
  props: {
    value: Array,  // selectedAuthors
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      author_query: '',
      suggestedAuthors: [],
      selectedAuthor: '',
      selectedAuthors: [],
      selectedAuthorsMessage: "Les auteurs sélectionnés vont s'afficher en dessous.",
    }
  },
  methods: {
    getSuggestedAuthors: function (query) {
      if (query.length >= 2) {
        searchNearAuthors(`auteur=${encodeURIComponent(query)}`)
            .then((response) => {
              if (response.data.success) {
                this.suggestedAuthors = response.data.suggestedAuthors;
              }
            }).catch();
      }
    },
    addAuthor: function(event) {
      // TODO check that chosen Author is not already in selectedAuthors
      this.selectedAuthor = event;
      this.selectedAuthors.push(event);
      this.author_query = "";
      this.$emit("input", this.selectedAuthors);
    },
    removeLastAuthor: function() {
      // const indexOfAuthor = this.selectedAuthors.indexOf(event);
      this.selectedAuthors.pop()  // splice(indexOfAuthor, 1);
      this.$emit("input", this.selectedAuthors);
    }
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