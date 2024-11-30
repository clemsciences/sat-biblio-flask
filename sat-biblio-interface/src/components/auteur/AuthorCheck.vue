<template>


  <b-container>
    <b-form-group label="Auteurs" v-if="!disabled">
      <vue-typeahead-bootstrap
        v-model="author_query"
        :data="suggestedAuthors"
        :serializer="s => s.text"
        :disabled="disabled"
        placeholder="Tapez le prénom ou le nom de l'auteur"

      />
      <div v-if="suggestedAuthors.length > 0">
        <p>{{suggestedAuthors}}</p>
      </div>
      <div v-else>
        <p>C'est un nouvel auteur.</p>
      </div>
    </b-form-group>
  </b-container>

</template>

<script>
import {searchNearAuthors} from "@/services/api";
import {Author} from "@/services/objectManager";

export default {
  name: "AuthorCheck",

  props: {
    value: Author,  // selectedAuthors
    disabled: {
      type: Boolean,
      default: false
    },
  },
  data: function () {
    return {
      author_query: '',
      suggestedAuthors: [],
      selectedAuthorId: -1,
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
      this.selectedAuthorId = event;
      this.selectedAuthors.push(event);
      this.author_query = "";
      this.$emit("input", this.selectedAuthors);
    },
  },
  watch: {
    author_query: function (newValue) {
      this.getSuggestedAuthors(newValue);
    },
    value: {
      handler(newValue) {
        this.author_query = ""
        console.log("youhou")
        if(newValue.first_name) {
          this.author_query = newValue.first_name;
        }
        if(newValue.family_name) {
          if(this.author_query) {
            this.author_query += " ";
          }
          this.author_query += newValue.family_name;
        }
        this.author_query = newValue.first_name + " " + newValue.family_name;
      },
      deep: true
    },
  },
}
</script>

<style scoped>

</style>