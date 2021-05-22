<template>
  <b-container>
    <Title v-if="managerCanUse && !isMyProfile" title="Page de gestion de l'utilisateur"
           info="Cette page permet au gestionnaire de modifier les droits à un utilisateur."
           id="id-gestionnaire-utilisateur">
    </Title>
    <Title v-else-if="isMyProfile" title="Mon profil"
           info="Cette page permet à l'utilisateur de modifier des informations le concernant."
           id="id-profil-utilisateur">
    </Title>

    <b-row>
      <b-form @submit.prevent="updateUser">
      <b-form-group label="Prénom">
        <b-form-input type="text" v-model="first_name" :disabled="!isMyProfile"></b-form-input>
      </b-form-group>
      <b-form-group label="Nom">
        <b-form-input type="text" v-model="family_name" :disabled="!isMyProfile"></b-form-input>
      </b-form-group>
      <b-form-group label="Droit">
        <b-form-select :disabled="!managerCanUse || (isMyProfile && managerCanUse)"
                       v-model="right" :options="rightsForSelect"
                       :select-size="1" size="sm"/>
      </b-form-group>
      <b-form-group label="Adresse email">
        <b-form-input type="text" v-model="emailAddress" disabled/>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect">Enregistrer</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>
    </b-row>
    <b-row>
      <b-button class="my-3" :disabled="!isMyProfile" v-b-modal.suppression>Supprimer</b-button>
      <b-modal id="suppression" title="Suppression de l'enregistrement"
          cancel-title="Annuler" ok-title="Supprimer" @ok="deleteUser">
          <p>Êtes-vous sûr de supprimer votre compte ?</p>
        </b-modal>
    </b-row>
  </b-container>
</template>

<script>
import {rights} from "@/services/rights";
import {deleteUser, retrieveUser, updateUser} from "@/services/api";

export default {
  name: "Utilisateur",
  data: function() {
    return {
      first_name: '',
      family_name: '',
      right: rights.lecteur.index,
      emailAddress: '',
      message: '',
      rightsForSelect: [
        {value: rights.lecteur.index, text: rights.lecteur.string},
        {value: rights.contributeur.index, text: rights.contributeur.string},
        {value: rights.editeur.index, text: rights.editeur.string},
        {value: rights.gestionnaire.index, text: rights.gestionnaire.string},
        {value: rights.administrateur.index, text: rights.administrateur.string},
      ]

    }
  },
  methods: {
    loadUser() {
      retrieveUser(this.$route.params.id, this.$store.state.connectionInfo.token).then(
          (response) => {
            if(response.data.success) {
              this.first_name = response.data.user.first_name;
              this.family_name = response.data.user.family_name;
              this.right = response.data.user.right;
              this.emailAddress = response.data.user.email;
            }
          }
      )
    },
    updateUser() {
      const formData = {
        first_name: this.first_name,
        family_name: this.family_name,
        right: this.right,
        email: this.emailAddress
      };
      updateUser(this.$route.params.id, this.$store.state.connectionInfo.token).then(
          response => {
            console.log(formData);
            console.log(response);
          }
      );
    },
    deleteUser() {
      deleteUser(this.$route.params.id, this.$store.state.connectionInfo.token).then(
          response => {
            if(response.data.success) {
              this.$router.replace("/");
            }
          }
      );
    }
  },
  mounted() {
    this.loadUser();
  },
  computed: {
    isMyProfile() {
      return this.emailAddress === this.$store.getters.getConnectionInfo.email;
    },
    managerCanUse() {
      console.log(this.$store.getters.getUserRight);
      console.log(rights.gestionnaire.index);
      return this.$store.getters.getUserRight >= rights.gestionnaire.index;
    },
    isIncorrect() {
      return this.first_name.length === 0 ||
          this.family_name.length === 0 ||
          !/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(this.emailAddress);
    }
  }
}
</script>

<style scoped>

</style>