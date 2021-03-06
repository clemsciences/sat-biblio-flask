<template>
  <div>
    <b-form @submit="passwordForgotten">
      <b-form-input type="email" name="email_address"/>
      <b-form-input/>

    </b-form>
  </div>
</template>

<script>
import {haveForgottenPassword} from "../../services/api";

export default {
  name: "MotDePasseOublie",
  methods: {
    passwordForgotten: function () {
      haveForgottenPassword().then(
          (response) => {
            if(response.data.success) {
              console.log("check if email address is in the base");
            }
          }
      )
    }
  }
}
</script>

<style scoped>

</style>