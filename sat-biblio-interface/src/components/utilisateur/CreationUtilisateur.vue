<template>
  <div>
    <b-form @submit="sendUserCreation">
      <label>Prénom</label>
      <b-form-input name="first_name"></b-form-input>
      <label>Nom</label>
      <b-form-input name="family_name"/>
      <label>Adresse email</label>
      <b-form-input name="email_address"/>
      <label>Mot de passe</label>
      <b-form-input type="password" :value="password1"/>
      <label>Confirmation du mot de passe</label>
      <b-form-input type="password" :value="password2"/>
      <b-form-input type="submit"/>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CreationUtilisateur",
  data: function() {
    return {
      password1: "",
      password2: ""

    }
  },
  methods: {
    sendUserCreation: function() {
      if(this.password1 === this.password2) {
        axios.post('/api/user/create').then()
      } else {
        console.log("Le mot de passe donné est différent du mot de passe de confirmation. Ils doivent être identiques.")
      }
    }
  }
}
</script>

<style scoped>

</style>