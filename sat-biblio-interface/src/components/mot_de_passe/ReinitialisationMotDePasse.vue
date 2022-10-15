<template>
  <b-container>
    <h2>Changer le mot de passe</h2>
    <p>
      Vous êtes sur le point de changer le mot de passe du compte <b>{{ connectionInfo.email }}</b>.
      Veuillez d'abord entrer le mot de passe actuel, puis entrez deux fois le nouveau mot de passe.
    </p>


    <b-form @submit.prevent="reinitialisePassword">
      <b-form-group label="Le mot de passe actuel">
        <b-form-input type="password" name="current_password" v-model="currentPassword"/>
      </b-form-group>
      <b-form-group label="Le nouveau mot de passe">
        <b-row>
        <b-col cols="9">
        <b-form-input :type="passwordType1" name="password1" v-model="password1"/>
          </b-col>
        <b-col cols="3">
          <b-button @click="togglePasswordType1">{{ this.passwordAction(this.passwordType1) }}</b-button>
        </b-col>
        </b-row>
      </b-form-group>
      <b-form-group label="Le même nouveau mot de passe">
        <b-row>
        <b-col cols="9">
        <b-form-input :type="passwordType2" name="password2" v-model="password2"/>
        </b-col>
        <b-col cols="3">
          <b-button @click="togglePasswordType2">{{ this.passwordAction(this.passwordType2) }}</b-button>
        </b-col>
        </b-row>
      </b-form-group>
      <b-button type="submit" :disabled="areNotEqualAndCorrect">Valider</b-button>
    </b-form>
    <p>{{ message }}</p>
  </b-container>
</template>

<script>
import {recreatePassword} from "@/services/api";
import {mapState} from "vuex";

export default {
  name: "ReinitialisationMotDePasse",
  props: {
    username: {
      type: String,
      default: ''
    },
  },
  data: function () {
    return {
      currentPassword: "",
      password1: "",
      password2: "",
      message: "",
      passwordType1: "password",
      passwordType2: "password",
    }
  },
  methods: {
    reinitialisePassword: function () {
      if(this.password1 === this.password2) {
        recreatePassword(this.currentPassword, this.password1).then(
            (response) => {
              this.message = response.data.message;
              this.currentPassword = "";
              this.password1 = "";
              this.password2 = "";
            }
        ).catch(
            (reason) => {
              this.message = reason.response.data.message;
              console.log(reason);
            }
        );
      }
    },
    togglePasswordType: function(passwordType) {
      if(passwordType === "password") {
        passwordType = "text";
      } else {
        passwordType = "password";
      }
      return passwordType;

    },
    togglePasswordType1: function() {
      this.passwordType1 = this.togglePasswordType(this.passwordType1);
    },
    togglePasswordType2: function() {
      this.passwordType2 = this.togglePasswordType(this.password2);
    },
    passwordAction: function(passwordType) {
      if(passwordType === "password") {
        return "Afficher le mot de passe";
      } else {
        return "Cacher le mot de passe";
      }
    }
  },
  computed: {
    ...mapState(["connectionInfo"]),
    areNotEqualAndCorrect: function () {
      return this.password1 === this.password2 && this.password1.length < 6;
    },
  }
}
</script>

<style scoped>

</style>