<template>
  <BFormGroup :label="label">
    <vue-typeahead-bootstrap
        v-if="!disabled"
      v-model="selectedUserTemp"
      :items="fetchUsers"
      :item-projection="s => s ? s.text : ''"
      :min-input-length="1"
      placeholder="Tapez le prénom ou le nom d'un utilisateur"
    />
    <BFormInput :model-value="modelValue.text" readonly :disabled="disabled"/>
    <div v-if="!disabled">
      <BButton v-if="modelValue.value > 0" @click="removeUser" :disabled="disabled" class="m-1">Enlever utilisateur</BButton>
      <BButton v-if="modelValue.value > 0" @click="goToUser" :disabled="disabled" class="m-1">Voir utilisateur</BButton>
    </div>
  </BFormGroup>
</template>

<script>
import {searchNearUsers} from "@/services/api";

export default {
  name: "UserSuggestion",
  props: {
    modelValue: Object,
    label: String,
    disabled: {
      type: Boolean,
      default: false
    },
  },
  data: function () {
    return {
      selectedUserTemp: null,
    }
  },
  methods: {
    fetchUsers(query) {
      if (query.length < 1) return Promise.resolve([]);
      return searchNearUsers(`user=${encodeURIComponent(query)}`)
        .then(response => response.data.success ? response.data.suggestedUsers : []);
    },
    addUser: function (item) {
      this.$nextTick(() => { this.selectedUserTemp = null; });
      this.$emit('update:modelValue', item);
    },
    removeUser: function () {
      const newValue = { ...this.modelValue, value: -1, text: "" };
      this.$emit('update:modelValue', newValue);
    },
    goToUser: function() {
      let routeData = this.$router.resolve(`/utilisateur/lire/${this.modelValue.value}`);
      window.open(routeData.href, '_blank');
    },
  },
  watch: {
    selectedUserTemp(newItem) {
      if (newItem) this.addUser(newItem);
    },
  }
}
</script>

<style scoped>

</style>
