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
      <b-form-select
          v-model="selectedAuthorId"
          :options="value"
          :select-size="5"
          size="sm"/>
    </b-form-group>
    <b-button class="mx-3" v-if="!disabled" :disabled="value.length === 0 || disabled" @click="removeLastAuthor">
      Enlever auteur
    </b-button>
    <b-button v-if="selectedAuthorId > 0" @click="goToAuthor">Voir auteur</b-button>
<!--    <b-form-group :label="selectedAuthorsMessage">-->
<!--      <b-form-select v-model="selectedAuthorId" -->
<!--                     :options="selectedAuthors" -->
<!--                     :select-size="5" size="sm"/>-->
<!--    </b-form-group>-->
<!--    <b-button v-if="selectedAuthorId > 0" @click="goToAuthor">Voir auteur</b-button>-->
<!--    <b-button class="mx-3"-->
<!--              v-if="selectedAuthorId > 0"-->
<!--              @click="removeSelectedAuthor">Enlever auteur</b-button>-->

<!--    <b-form-group label="Titre">-->
<!--      <b-form-input class="mx-3" v-if="selectedAuthorId >= 0" v-model="titre"></b-form-input>-->
<!--    </b-form-group>-->
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
    goToAuthor: function() {
      console.log(this.selectedAuthorId);
      let routeData = this.$router.resolve(`/auteur/lire/${this.selectedAuthorId}`);
      window.open(routeData.href, '_blank');
    },
    removeLastAuthor: function() {
      // const indexOfAuthor = this.selectedAuthors.indexOf(event);
      // this.selectedAuthors.pop()  // splice(indexOfAuthor, 1);
      this.selectedAuthors = this.selectedAuthors.filter(
          (author) => {
            return author.value !== this.selectedAuthorId;
          }
      );
      this.selectedAuthorId = -1;
      this.$emit("input", this.selectedAuthors);
    }
  },
  watch: {
    author_query: function (newValue) {
      this.getSuggestedAuthors(newValue);
    },
    value: function(newValue) {
      Object.assign(this.selectedAuthors, newValue);
    },
    selectedAuthors: function (newValue) {
      if(newValue.length > 1) {
        this.selectedAuthorsMessage = "Auteurs sélectionnés"
      } else {
        this.selectedAuthorsMessage = "Auteur sélectionné"
      }
    }
  },
}
</script>

<style scoped>

</style>