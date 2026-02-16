<template>
  <BFormGroup :label="label">
    <vue-typeahead-bootstrap
        v-if="!disabled"
      v-model="userQuery"
      :data="suggestedUsers"
      :serializer="s => s.text"
      placeholder="Tapez le prénom ou le nom d'un utilisateur"
      @update:model-value="getSuggestedUsers"
      @hit="addUser($event)"
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
    modelValue: Object, // selectedReference
    label: String,
    disabled: {
      type: Boolean,
      default: false
    },
  },
  data: function () {
    return {
      userQuery: "",
      // reference: {value: -1, text: ""},
      // selectedReference: {text: "", value: -1},
      suggestedUsers: [],
    }
  },
  methods: {
    addUser: function (event) {
      this.userQuery = "";
      this.$emit('update:modelValue', event);      // this.selectedReference = event;
    },
    removeUser: function () {
      const newValue = { ...this.modelValue, value: -1, text: "" };
      this.$emit('update:modelValue', newValue);
    },
    goToUser: function() {
      let routeData = this.$router.resolve(`/utilisateur/lire/${this.modelValue.value}`);
      window.open(routeData.href, '_blank');
    },
    getSuggestedUsers: function (query) {
      if(query.length >= 1) {
        searchNearUsers(`user=${encodeURIComponent(query)}`).then((response) => {
          if (response.data.success) {
            console.log("suggestedUsers", response.data)
            this.suggestedUsers = response.data.suggestedUsers;
          }
        }).catch();
      }
    },
  },
  watch: {
    // userQuery: function (newValue) {
    //   this.getSuggestedUsers(newValue);
    // },
  }
}
</script>

<style scoped>

</style>