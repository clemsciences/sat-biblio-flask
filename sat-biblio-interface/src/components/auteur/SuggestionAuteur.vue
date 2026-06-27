<template>
  <BContainer>
    <BFormGroup label="Auteurs" v-if="!disabled">
      <vue-typeahead-bootstrap
        v-model="selectedAuthorTemp"
        :items="fetchAuthors"
        :item-projection="s => s ? s.text : ''"
        :disabled="disabled"
        placeholder="Tapez le prénom ou le nom de l'auteur"
      />
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
      selectedAuthorTemp: null,
      selectedAuthorId: -1,
      selectedAuthorsMessage: "Les auteurs sélectionnés vont s'afficher en dessous.",
    }
  },
  methods: {
    fetchAuthors(query) {
      if (query.length < 2) return Promise.resolve([]);
      return searchNearAuthors(`auteur=${encodeURIComponent(query)}`)
        .then(response => response.data.success ? response.data.suggestedAuthors : []);
    },
    addAuthor: function(item) {
      this.selectedAuthorId = item.value;
      const newValue = [...this.modelValue, item];
      this.$nextTick(() => { this.selectedAuthorTemp = null; });
      this.$emit("update:modelValue", newValue);
    },
    goToAuthor: function() {
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
    selectedAuthorTemp(newItem) {
      if (newItem) this.addAuthor(newItem);
    },
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
