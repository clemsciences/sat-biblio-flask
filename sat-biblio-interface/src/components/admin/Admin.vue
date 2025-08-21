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

    <b-row>
      <b-button to="/administrateur/imports" class="m-2">Gestionnaire d'importation</b-button>
    </b-row>
    <b-row>
      <b-button @click="generateArk" class="m-2">Générer ARK</b-button>
      <p v-if="message.length > 0">{{ message }}</p>
    </b-row>

<!--    <b-row>-->
<!--      <b-button @click="importAllRows" class="m-2">Importer le catalogue depuis le CSV</b-button>-->
<!--      <p>{{ importMessage }}</p>-->
<!--    </b-row>-->

<!--    <b-row>-->
<!--      <b-button @click="deleteAllRows" class="m-2">Supprimer le catalogue (pour les tests d'import)</b-button>-->
<!--      <p>{{ message }}</p>-->
<!--    </b-row>-->

  </b-container>
</template>

<script>
import Title from "../visuel/Title";
import CreationUtilisateur from '../utilisateur/CreationUtilisateur'
import ListeUtilisateur from './ListeUtilisateur'
import {deleteAllCatalogue, generateArkForAllEntriesMissingOnes, importAllCatalogue} from "@/services/api";
export default {
  name: "Admin",
  components: {Title, CreationUtilisateur, ListeUtilisateur},
  data: function() {
    return {
      message: '',
      importMessage: '',
    }
  },
  methods: {
    forceUsersReload() {
      this.$refs.userList.getUserTotalNumber();
      this.$refs.userList.$refs.userTable.refresh();
    },
    deleteAllRows() {
      this.message = "En cours de suppression"
      deleteAllCatalogue().then(
          () => {
            this.message = "C'est supprimé";
          }
      )
    },
    importAllRows() {
      this.importMessage = "En cours d'import";
      importAllCatalogue().then(
          () => {
            this.importMessage = "C'est importé";
          }
      )
    },
    generateArk() {
      generateArkForAllEntriesMissingOnes().then((response) => {
        this.arkMessage = response.data.message;
      }).catch((error) => {
        this.arkMessage = error;
      });
    }

  }
}
</script>

<style scoped>

</style>