<template>
  <b-container>
    <Title title="Mot de passe oublié"
           info="Si vous avez oublié votre mot de passe, il est possible d'en générer un nouveau."
           id="id-mot-de-passe-oublié"/>
    <p>Vous avez oublié votre mot de passe.
      Vous pouvez en générer un autre en donnant votre adresse email.
      Vous recevrez un courriel qui contiendra un nouveau mot de passe.
      Libre à vous de le changer une fois votre compte retrouvé.
    </p>
    <b-form @submit.prevent="passwordForgotten" class="my-3">
      <b-form-group label="Adresse email">
        <b-form-input type="email" name="email_address" v-model="emailAddress"/>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect">Demander le changement de mot de passe</b-button>
    </b-form>
    <p>{{ message }}</p>
  </b-container>
</template>

<script>
import {haveForgottenPassword} from "@/services/api";
import Title from "@/components/visuel/Title";

export default {
  name: "MotDePasseOublie",
  components: {Title},
  data: function () {
    return {
      emailAddress: "",
      message: ""
    }
  },
  methods: {
    passwordForgotten: function () {
      haveForgottenPassword({email_address: this.emailAddress}).then(
          (response) => {
            this.message = response.data.message;
          }
      )
          .catch(
          (reason) => {
            this.message = reason.response.data.message;
          }
      )
    }
  },
  computed: {
    isIncorrect: function() {
      return this.emailAddress.length === 0;
    }
  }
}
</script>

<style scoped>

</style>