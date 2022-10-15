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
        <b-row>
          <b-col cols="9">
            <b-form-input :type="passwordType1" v-model="password1"/>
          </b-col>
          <b-col cols="3">
            <b-button @click="togglePasswordType1">{{ this.passwordAction(this.passwordType1) }}</b-button>
          </b-col>
        </b-row>
      </b-form-group>
      <b-form-group label="Confirmation du mot de passe">
        <b-row>
          <b-col cols="9">
            <b-form-input :type="passwordType2" v-model="password2"/>
          </b-col>
          <b-col cols="3">
            <b-button @click="togglePasswordType2">{{ this.passwordAction(this.passwordType2) }}</b-button>
          </b-col>
        </b-row>
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
      inForm: true,
      passwordType1: "password",
      passwordType2: "password",
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
      this.passwordType1 = "password";
      this.passwordType2 = "password";
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
      this.passwordType2 = this.togglePasswordType(this.passwordType2)
    },
    passwordAction: function(passwordType) {
      if(passwordType === "password") {
        return "Afficher le mot de passe";
      } else {
        return "Cacher le mot de passe";
      }
    }
  },
}
</script>

<style scoped>

</style>