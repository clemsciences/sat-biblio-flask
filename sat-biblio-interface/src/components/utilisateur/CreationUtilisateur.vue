<template>
  <b-container>
    <Title info="Un utilisateur"
           id="id-user">Création d'un compte utilisateur</Title>
    <b-form @submit.prevent="sendUserCreation" v-if="inForm">
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
      <b-button type="submit">Enregistrer</b-button>
      <span class="mx-3">{{ message }}</span>

    </b-form>
    <div v-else>
      <p>
        Le compte de <i>{{ first_name }} {{ family_name }}</i> a été créé.
        Un courriel a été envoyé à <b>{{ email }}</b>.
        Il faudra valider le compte en cliquant sur le lien donné.
      </p>
      <b-button @click="resetForm">Créer un nouveau compte utilisateur</b-button>
    </div>
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
      message: "",
      inForm: true
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
      } else if(!/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(this.email)) {
        this.message = "L'adresse email donnée est incorrecte.";
      } else if(this.first_name.length === 0) {
        this.message = "Le prénom ne peut être vide.";
      } else if(this.family_name.length === 0) {
        this.message = "Le nom de famille ne peut être vide.";
      } else if(this.password1.length === 0 || this.password2.length === 0) {
        this.message = "Le mot de passe ne peut être vide";
      } else if(this.password1 !== this.password2) {
        this.message = "Les mots de passe doivent être identiques";
      } else if(this.password1.length < 6) {
        this.message = "Le mot de passe doit être composé d'au moins 6 caractères.";
      } else {
        createUser(formData).then(
            (response) => {
              if(response.data.success) {
                this.message = response.data.message;
                this.inForm = false;
              } else {
                if(response.data.message) {
                  this.message = response.data.message;
                } else {
                  this.message = "Impossible de se connecter, veuillez vérifier vos informations de connexion."
                }
              }
            }
        ).catch(
            reason => {
              console.log(reason);
              this.message = "Problème de réseau";
            }
        );
      }
    },
    resetForm() {
      this.inForm = true;
      this.first_name = "";
      this.family_name = "";
      this.email = "";
      this.password1 = "";
      this.password2 = "";
      this.message = "";
    }
  }
}
</script>

<style scoped>

</style>