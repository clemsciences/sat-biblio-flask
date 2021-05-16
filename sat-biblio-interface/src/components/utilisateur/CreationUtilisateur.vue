<template>
  <b-container>
    <Title info="Un utilisateur"
           id="id-user">Création d'un compte utilisateur</Title>
    <b-form @submit.prevent="sendUserCreation">
      <b-form-group label="Prénom">
        <b-form-input v-model="first_name"/>
      </b-form-group>
      <b-form-group label="Nom">
        <b-form-input v-model="family_name"/>
      </b-form-group>
      <b-form-group label="Adresse email">
        <b-form-input v-model="email"/>
      </b-form-group>
      <b-form-group label="Mot de passe">
        <b-form-input type="password" v-model="password1"/>
      </b-form-group>
      <b-form-group label="Confirmation du mot de passe">
        <b-form-input type="password" v-model="password2"/>
      </b-form-group>
      <b-button type="submit">Enregistrer</b-button> <span class="mx-3">{{ message }}</span>
    </b-form>
    <p>{{ message }}</p>
  </b-container>
</template>

<script>
import {createUser} from "@/services/api";
import Title from "@/components/visuel/Title";

export default {
  name: "CreationUtilisateur",
  components: {Title},
  data: function() {
    return {
      first_name: "",
      family_name: "",
      email: "",
      password1: "",
      password2: "",
      message: ""
    }
  },
  methods: {
    sendUserCreation: function() {
      const formData = {
        first_name: this.first_name,
        family_name: this.family_name,
        email: this.email,
        password: this.password1
      }
      if(this.email.length === 0) {
        this.message = "L'adresse email ne peut pas être vide.";
      } else if(this.first_name.length === 0) {
        this.message = "Le prénom ne peut être vide."
      } else if(this.family_name.length === 0) {
        this.message = "Le nom de famille ne peut être vide."
      } else if(this.password1.length === 0 || this.password2.length === 0) {
        this.message = "Le mot de passe ne peut être vide";
      } else if(this.password1 !== this.password2) {
        this.message = "Les mots de passe doivent être identiques"
      } else {
        createUser(formData).then(
            (response) => {
              if(response.data.success) {
                this.$router.push('/');
              } else {
                if(response.data.message) {
                  this.message = response.data.message;
                } else {
                  this.message = "Impossible de se connecter, veuillez vérifier vos informations de connexion."
                }
              }
            }
        )
      }
    }
  }
}
</script>

<style scoped>

</style>