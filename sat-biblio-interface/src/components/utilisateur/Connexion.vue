<template>
  <div>
    <b-form @submit.prevent="login">
      <b-form-group label="Adresse email">
        <b-form-input :value="username"></b-form-input>
      </b-form-group>
      <b-form-group label="Mot de passe">
        <b-form-input type="password" :value="password"></b-form-input>
      </b-form-group>
      <b-button type="submit">Se connecter</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Connexion",
  data: function () {
    return {
      username: "",
      password: ""
    }
  },
  methods: {
    login: function () {
      console.log("bonjour");
      const args = {
        username: this.username,
        password: this.password
      };
      axios.post('/api/user/connect', args).then(
          (value) => {
            if (value.data.success) {
              this.$router.push()
              console.log("connected");
            } else {
              console.log("not connected")
            }
          }
      ).catch(
          (reason) => {
            console.log(reason);
          }
      );
    }
  }
}
</script>

<style scoped>

</style>