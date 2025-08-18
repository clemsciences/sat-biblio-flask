<template>
  <b-form-group :label="label">
    <vue-typeahead-bootstrap
        v-if="!disabled"
      v-model="userQuery"
      :data="suggestedUsers"
      :serializer="s => s.text"
      placeholder="Tapez le prénom ou le nom d'un utilisateur"
      @hit="addUser($event)"
    />
    <b-form-input v-model="value.text" readonly :disabled="disabled"/>
    <div v-if="!disabled">
      <b-button v-if="value.value > 0" @click="removeUser" :disabled="disabled" class="m-1">Enlever utilisateur</b-button>
      <b-button v-if="value.value > 0" @click="goToUser" :disabled="disabled" class="m-1">Voir utilisateur</b-button>
    </div>

  </b-form-group>
</template>

<script>
import {searchNearUsers} from "@/services/api";

export default {
  name: "SuggestionUtilisateur",
  props: {
    value: Object, // selectedReference
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
      this.$emit('input', event);      // this.selectedReference = event;
    },
    removeUser: function () {
      this.value.value = -1;
      this.value.text = "";
      this.$emit('input', this.value);
    },
    goToUser: function() {
      let routeData = this.$router.resolve(`/utilisateur/lire/${this.value.value}`);
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
    userQuery: function (newValue) {
      this.getSuggestedUsers(newValue);
    },
  }
}
</script>

<style scoped>

</style>