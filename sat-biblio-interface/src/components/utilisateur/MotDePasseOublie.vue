<template>
  <div>
    <b-form @submit="passwordForgotten">
      <b-form-input type="email" name="email_address"/>
      <b-form-input/>

    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MotDePasseOublie",
  methods: {
    passwordForgotten: function () {
      axios.post('/api/user/forgotten_password').then(
          (response) => {
            if(response.data.result) {
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