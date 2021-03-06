<template>
  <div>
    {{ username }}
    <b-form @submit="reinitialisePassword">
      <b-form-input name="password1" :value="password1"/>
      <b-form-input name="password2" :value="password2"/>

    </b-form>
  </div>
</template>

<script>
import {recreatePassword} from "../../services/api";

export default {
  name: "ReinitialisationMotDePasse",
  props: ["username"],
  data: function () {
    return {
      password1: "",
      password2: ""
    }
  },
  methods: {
    reinitialisePassword: function () {
      if(this.password1 === this.password2) {
        recreatePassword(this.password1).then();
      }
    }
  }
}
</script>

<style scoped>

</style>