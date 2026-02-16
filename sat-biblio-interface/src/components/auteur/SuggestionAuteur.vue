<template>
  <BContainer>
    <BFormGroup label="Auteurs" v-if="!disabled">
      <vue-typeahead-bootstrap
        v-model="author_query"
        :data="suggestedAuthors"
        :serializer="s => s.text"
        :disabled="disabled"
        placeholder="Tapez le prénom ou le nom de l'auteur"
        @update:model-value="getSuggestedAuthors"
        @hit="addAuthor($event)"
      />
  <!--        <BFormInput readonly v-if="selectedAuthor" v-model="selectedAuthor"/> &lt;!&ndash; pour chercher l'auteur &ndash;&gt;-->
    </BFormGroup>
    <BFormGroup :label="disabled ? 'Auteurs' : selectedAuthorsMessage">
      <BFormSelect
          :model-value="selectedAuthorId"
          @update:model-value="selectedAuthorId = $event"
          :options="modelValue"
          :select-size="5"
          size="sm"/>
    </BFormGroup>
    <BButton class="m-3" v-if="!disabled" :disabled="modelValue.length === 0 || disabled" @click="removeLastAuthor">
      Enlever auteur
    </BButton>
    <BButton class="m-3" v-if="selectedAuthorId > 0" @click="goToAuthor">Voir auteur</BButton>
    <BButton class="m-3" v-if="!disabled" @click="goToNewAuthor">Créer auteur</BButton>
<!--    <BFormGroup :label="selectedAuthorsMessage">-->
<!--      <BFormSelect v-model="selectedAuthorId" -->
<!--                     :options="selectedAuthors" -->
<!--                     :select-size="5" size="sm"/>-->
<!--    </BFormGroup>-->
<!--    <BButton v-if="selectedAuthorId > 0" @click="goToAuthor">Voir auteur</BButton>-->
<!--    <BButton class="mx-3"-->
<!--              v-if="selectedAuthorId > 0"-->
<!--              @click="removeSelectedAuthor">Enlever auteur</BButton>-->

<!--    <BFormGroup label="Titre">-->
<!--      <BFormInput class="mx-3" v-if="selectedAuthorId >= 0" v-model="titre"></BFormInput>-->
<!--    </BFormGroup>-->
  </BContainer>
</template>

<script>
import {searchNearAuthors} from "@/services/api";

export default {
name: "AuthorSuggestion",
  props: {
    modelValue: Array,  // selectedAuthors
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
      this.selectedAuthorId = event.value;
      const newValue = [...this.modelValue, event];
      this.author_query = "";
      this.$emit("update:modelValue", newValue);
    },
    goToAuthor: function() {
      console.log(this.selectedAuthorId);
      let routeData = this.$router.resolve(`/auteur/lire/${this.selectedAuthorId}`);
      window.open(routeData.href, '_blank');
    },
    goToNewAuthor() {
      let routeData = this.$router.resolve(`/auteur/creer`);
      window.open(routeData.href, '_blank');
    },
    removeLastAuthor: function() {
      const newValue = this.modelValue.filter(
          (author) => {
            return author.value !== this.selectedAuthorId;
          }
      );
      this.selectedAuthorId = -1;
      this.$emit("update:modelValue", newValue);
    }
  },
  watch: {
    // author_query: function (newValue) {
    //   this.getSuggestedAuthors(newValue);
    // },
    modelValue: function (newValue) {
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