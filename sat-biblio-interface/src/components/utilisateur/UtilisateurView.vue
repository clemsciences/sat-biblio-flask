<template>
  <BContainer>
    <AppTitle v-if="managerCanUse && !isMyProfile" title="Page de gestion de l'utilisateur"
           info="Cette page permet au gestionnaire de modifier les droits à un utilisateur."
           id="id-gestionnaire-utilisateur">
    </AppTitle>
    <AppTitle v-else-if="isMyProfile" title="Mon profil"
           info="Cette page permet à l'utilisateur de modifier des informations le concernant."
           id="id-profil-utilisateur">
    </AppTitle>

    <BRow>
      <BForm @submit.prevent="updateUser">
      <BFormGroup label="Prénom">
        <BFormInput type="text" v-model="first_name" :disabled="!isMyProfile"></BFormInput>
      </BFormGroup>
      <BFormGroup label="Nom">
        <BFormInput type="text" v-model="family_name" :disabled="!isMyProfile"></BFormInput>
      </BFormGroup>
      <BFormGroup label="Droit">
        <BFormSelect :disabled="!managerCanUse || (isMyProfile && managerCanUse)"
                       v-model="right" :options="limitedRightsForSelect"
                       :select-size="1" size="sm"/>
      </BFormGroup>
      <BFormGroup label="Adresse email">
        <BFormInput type="text" v-model="emailAddress" disabled/>
      </BFormGroup>
      <BFormGroup>
        <b-form-checkbox :disabled="true" :checked="emailConfirmed">Email confirmé</b-form-checkbox>
      </BFormGroup>
      <BFormGroup>
        <BButton @click="resendConfirmationEmail" :disabled="emailConfirmed">Renvoyer un email de confirmation</BButton>
      </BFormGroup>
      <BButton type="submit" :disabled="isIncorrect">Enregistrer</BButton>
      <span class="mx-3">{{ message }}</span>
    </BForm>
    </BRow>
    <BRow>
      <BButton class="my-3" :disabled="(isAdmin && isMyProfile) || (!isAdmin && !isMyProfile)"
                v-b-toggle.suppression>Supprimer</BButton>
      <BModal id="suppression" title="Suppression de l'enregistrement"
          cancel-title="Annuler" ok-title="Supprimer" @ok="deleteUser">
          <p>Êtes-vous sûr de supprimer votre compte ?</p>
        </BModal>
    </BRow>
  </BContainer>
</template>

<script>
import {rights} from "@/services/rights";
import {deleteUser, resendConfirmationEmail, retrieveUser, updateUser} from "@/services/api";
import AppTitle from "@/components/visuel/AppTitle.vue";

export default {
  name: "UtilisateurView",
  components: {AppTitle},
  data: function() {
    return {
      first_name: '',
      family_name: '',
      right: rights.lecteur.index,
      emailAddress: '',
      message: '',
      emailConfirmed: false,
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
              this.emailConfirmed = response.data.user.confirmed;
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
      updateUser(this.$route.params.id, formData, this.$store.state.connectionInfo.token).then(
          response => {
            console.log(formData);
            console.log(response);
            this.message = response.data.message;
          }
      );
    },
    deleteUser() {
      deleteUser(this.$route.params.id, this.$store.state.connectionInfo.token).then(
          response => {
            if(response.status === 204) {
              this.$router.replace("/");
            } else {
              this.message = "Impossible de supprimer l'utilisateur";
            }
          }
      );
    },
    resendConfirmationEmail() {
      resendConfirmationEmail(this.$route.params.id, this.$store.state.connectionInfo.token).then(
          response => {
            if(response.status === 200) {
              this.message = response.data.message;
            }
          }
      )
    }
  },
  mounted() {
    this.loadUser();
  },
  computed: {
    isMyProfile() {
      return this.emailAddress === this.$store.getters.getConnectionInfo.email;
    },
    isAdmin() {
      return this.$store.getters.isAdmin;
    },
    managerCanUse() {
      console.log(this.$store.getters.getUserRight);
      console.log(rights.gestionnaire.index);
      console.log(this.right);
      return this.$store.getters.getUserRight >= this.right && this.$store.getters.getUserRight >= rights.gestionnaire.index;
    },
    isIncorrect() {
      return this.first_name.length === 0 ||
          this.family_name.length === 0 ||
          !/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(this.emailAddress);
    },
    limitedRightsForSelect() {
      return this.rightsForSelect.filter((item) => item.value <= this.$store.getters.getUserRight );
    }
  }
}
</script>

<style scoped>

</style>