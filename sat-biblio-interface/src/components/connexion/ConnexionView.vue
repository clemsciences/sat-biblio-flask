<template>
  <BContainer>
    <AppTitle title="Se connecter"
           info="Il est nécessaire de se connecter si on veut faire des modifications. A contrario, la lecture est accessible par tout le monde."
           id="id-connexion"/>
    <BForm @submit.prevent="login">
      <BFormGroup label="Adresse email">
        <BFormInput v-model="email"></BFormInput>
      </BFormGroup>
      <BFormGroup label="Mot de passe">
        <BRow>
          <BCol cols="9">
            <BFormInput :type="passwordType" v-model="password"></BFormInput>
          </BCol>
          <BCol cols="3">
            <BButton @click="togglePasswordType">{{ passwordAction }}</BButton>
          </BCol>
        </BRow>
      </BFormGroup>
      <BButton type="submit" :disabled="isIncorrect">Se connecter</BButton> <span class="mx-3">{{ message }}</span>
    </BForm>
    <p class="my-3"><BButton to="/utilisateur/mot-de-passe-oublie">Mot de passe oublié ?</BButton></p>

  </BContainer>
</template>

<script>
import {connectUser} from "@/services/api";
import AppTitle from "@/components/visuel/AppTitle.vue";
import {BButton, BCol, BFormGroup, BFormInput, BForm, BRow, BContainer} from "bootstrap-vue-next";

export default {
  name: "ConnexionView",
  components: {BButton, BCol, BRow, BFormGroup, BFormInput, BForm, BContainer, AppTitle},
  data: function () {
    return {
      email: "",
      password: "",
      message: "",
      passwordType: "password"
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
    },

    togglePasswordType: function() {
      if(this.passwordType === "password") {
        this.passwordType = "text";
      } else {
        this.passwordType = "password";
      }
    }
  },
  computed: {
    isIncorrect: function () {
      return this.email.length === 0 || this.password.length === 0;
    },
    passwordAction: function() {
      if(this.passwordType === "password") {
        return "Afficher le mot de passe";
      } else {
        return "Cacher le mot de passe";
      }
    }
  }
}
</script>

<style scoped>

</style>