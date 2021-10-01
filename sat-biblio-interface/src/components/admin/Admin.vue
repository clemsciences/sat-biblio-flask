<template>
  <b-container>
    <Title info="C'est la page qui permet de gérer les droits de tous les autres utilisateurs."
           id="id-admin">
      Page d'administration
    </Title>

    <b-row>
      <b-button v-b-toggle.collapse-new-user class="m-2">Créer un utilisateur</b-button>
    </b-row>
    <b-row>
      <b-col cols="12">
        <b-collapse id="collapse-new-user">
          <b-card>
            <creation-utilisateur/>
          </b-card>
        </b-collapse>
      </b-col>
    </b-row>
    <b-row>
      <b-button v-b-toggle.collapse-users class="m-2"
                @click="forceUsersReload">
        Voir les utilisateurs
      </b-button>
    </b-row>
    <b-row>
      <b-collapse id="collapse-users">
        <liste-utilisateur ref="userList" />
      </b-collapse>
    </b-row>

  </b-container>
</template>

<script>
import Title from "../visuel/Title";
import CreationUtilisateur from '../utilisateur/CreationUtilisateur'
import ListeUtilisateur from './ListeUtilisateur'
export default {
  name: "Admin",
  components: {Title, CreationUtilisateur, ListeUtilisateur},
  methods: {
    forceUsersReload() {
      this.$refs.userList.getUserTotalNumber();
      this.$refs.userList.$refs.userTable.refresh();
    },

  }
}
</script>

<style scoped>

</style>