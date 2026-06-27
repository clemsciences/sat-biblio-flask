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
      <div v-if="suggestedAuthors.length > 0">
        <p>{{suggestedAuthors}}</p>
      </div>
      <div v-else>
        <p>C'est un nouvel auteur.</p>
      </div>
    </BFormGroup>
  </BContainer>
</template>

<script>
import {searchNearAuthors} from "@/services/api";
import {Author} from "@/services/objectManager";

export default {
  name: "AuthorCheck",

  props: {
    modelValue: Author,
    disabled: {
      type: Boolean,
      default: false
    },
  },
  data: function () {
    return {
      selectedAuthorTemp: null,
      suggestedAuthors: [],
      selectedAuthorId: -1,
    }
  },
  methods: {
    fetchAuthors(query) {
      if (query.length < 2) return Promise.resolve([]);
      return searchNearAuthors(`auteur=${encodeURIComponent(query)}`)
        .then(response => {
          if (response.data.success) {
            this.suggestedAuthors = response.data.suggestedAuthors;
            return response.data.suggestedAuthors;
          }
          return [];
        });
    },
    addAuthor: function(item) {
      this.selectedAuthorId = item.value;
      this.$nextTick(() => { this.selectedAuthorTemp = null; });
      this.$emit("update:modelValue", item);
    },
  },
  watch: {
    selectedAuthorTemp(newItem) {
      if (newItem) this.addAuthor(newItem);
    },
    modelValue: {
      handler(newValue) {
        if (newValue) {
          this.selectedAuthorTemp = newValue.first_name || newValue.family_name
            ? { text: `${newValue.first_name || ''} ${newValue.family_name || ''}`.trim(), value: null }
            : null;
        }
      },
      deep: true
    },
  },
}
</script>

<style scoped>

</style>
