<template>
  <div>
    <b-form @submit.prevent="login">
      <b-form-group label="Adresse email">
        <b-form-input v-model="email"></b-form-input>
      </b-form-group>
      <b-form-group label="Mot de passe">
        <b-form-input type="password" v-model="password"></b-form-input>
      </b-form-group>
      <b-button type="submit">Se connecter</b-button> <span class="mx-3">{{ message }}</span>
    </b-form>

  </div>
</template>

<script>
import axios from "axios";
import localStorageManager from "@/services/localstorageManager";

export default {
  name: "Connexion",
  data: function () {
    return {
      email: "",
      password: "",
      message: ""
    }
  },
  methods: {
    login: function () {
      console.log("bonjour");
      const args = {
        email: this.email,
        password: this.password
      };
      axios.post('/api/user/connect', args).then(
          (value) => {
            if (value.data.success && value.data.connectionInfo) {
              localStorageManager.updateSessionInfo(value.data.connectionInfo)

              this.$router.push("/")
              console.log("connected");
            } else {
              this.message = value.data.message;
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