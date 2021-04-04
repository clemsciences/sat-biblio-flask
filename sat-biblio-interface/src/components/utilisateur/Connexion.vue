<template>
  <div>
    <h2>Connexion</h2>
    <b-form @submit.prevent="login">
      <b-form-group label="Adresse email">
        <b-form-input v-model="email"></b-form-input>
      </b-form-group>
      <b-form-group label="Mot de passe">
        <b-form-input type="password" v-model="password"></b-form-input>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect">Se connecter</b-button> <span class="mx-3">{{ message }}</span>
    </b-form>

  </div>
</template>

<script>
import localStorageManager from "@/services/localstorageManager";
import {connectUser} from "../../services/api";

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
      const args = {
        email: this.email,
        password: this.password
      };
      connectUser(args).then(
          (value) => {
            if (value.data.success && value.data.connectionInfo) {
              localStorageManager.updateSessionInfo(value.data.connectionInfo);
              const connectionInfo = value.data.connectionInfo;
              if(value.data.connected) {
                this.$store.commit("connect", {connectionInfo});
              }

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
            this.message = "Problème de réseau";
          }
      );
    }
  },
  computed: {
    isIncorrect: function () {
      return this.email.length === 0 || this.password.length === 0;
    }
  }
}
</script>

<style scoped>

</style>