<template>
  <b-form-group :label="label">
    <vue-typeahead-bootstrap
      v-model="userQuery"
      :data="suggestedUsers"
      :serializer="s => s.text"
      placeholder="Tapez le prénom ou le nom d'un utilisateur"
      @hit="addUser($event)"
    />
    <b-form-input v-model="value.text" readonly/>
  </b-form-group>
</template>

<script>
import {searchNearUsers} from "../../services/api";

export default {
  name: "SuggestionUtilisateur",
  props: {
    value: Object, // selectedReference
    label: String
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
    getSuggestedUsers: function (query) {
      if(query.length >= 1) {
        searchNearUsers(`user=${query}`).then((response) => {
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