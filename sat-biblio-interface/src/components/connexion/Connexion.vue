<template>
  <b-container>
    <Title title="Se connecter"
           info="Il est nécessaire de se connecter si on veut faire des modifications. A contrario, la lecture est accessible par tout le monde."
           id="id-connexion"/>
    <b-form @submit.prevent="login">
      <b-form-group label="Adresse email">
        <b-form-input v-model="email"></b-form-input>
      </b-form-group>
      <b-form-group label="Mot de passe">
        <b-form-input type="password" v-model="password"></b-form-input>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect">Se connecter</b-button> <span class="mx-3">{{ message }}</span>
    </b-form>
    <p class="my-3"><b-button to="/utilisateur/mot-de-passe-oublie">Mot de passe oublié ?</b-button></p>

  </b-container>
</template>

<script>
import {connectUser} from "@/services/api";
import Title from "@/components/visuel/Title";

export default {
  name: "Connexion",
  components: {Title},
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
              const connectionInfo = value.data.connectionInfo;
              const right = value.data.right;
              if(value.data.connected) {
                this.$store.commit("connect", {connectionInfo, right});
              }

              this.$router.push("/")
              console.log("connected");
            } else {
              this.message = value.data.message;
              console.log("not connected");
            }
          }
      ).catch(
          (reason) => {
            if(reason.response && reason.response.data.message) {
              this.message = reason.response.data.message;
            } else {
              this.message = "Problème de réseau";
            }
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