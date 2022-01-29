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
        <b-form-input type="password" name="password1" v-model="password1"/>
      </b-form-group>
      <b-form-group label="Le même nouveau mot de passe">
        <b-form-input type="password" name="password2" v-model="password2"/>
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
    }
  },
  computed: {
    ...mapState(["connectionInfo"]),
    areNotEqualAndCorrect: function () {
      return this.password1 === this.password2 && this.password1.length < 6;
    }
  }
}
</script>

<style scoped>

</style>