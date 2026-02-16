<template>
  <BContainer>
    <AppTitle info="C'est la page qui permet de gérer les droits de tous les autres utilisateurs."
           id="id-admin">
      Page d'administration
    </AppTitle>

    <BRow v-if="isAdmin">
      <BButton v-b-toggle.collapse-new-user class="m-2">Créer un utilisateur</BButton>
    </BRow>
    <BRow v-if="isAdmin">
      <BCol cols="12">
        <BCollapse id="collapse-new-user">
          <BCard>
            <creation-utilisateur/>
          </BCard>
        </BCollapse>
      </BCol>
    </BRow>
    <BRow v-if="isAdmin">
      <BButton vb--toggle.collapse-users class="m-2"
                @click="forceUsersReload">
        Voir les utilisateurs
      </BButton>
    </BRow>
    <BRow v-if="isAdmin">
      <BCollapse id="collapse-users">
        <ListeUtilisateurs ref="userList" />
      </BCollapse>
    </BRow>

    <BRow v-if="isAdmin">
      <BButton to="/administrateur/imports" class="m-2">Gestionnaire d'importation</BButton>
    </BRow>
    <BRow v-if="isEditor">
      <BButton to="/administrateur/fusionner-auteurs" class="m-2">Fusionner des auteurs</BButton>
    </BRow>
    <BRow>
      <BButton @click="generateArk" class="m-2">Générer ARK</BButton>
      <p v-if="message.length > 0">{{ message }}</p>
    </BRow>

<!--    <BRow>-->
<!--      <BButton @click="importAllRows" class="m-2">Importer le catalogue depuis le CSV</BButton>-->
<!--      <p>{{ importMessage }}</p>-->
<!--    </BRow>-->

<!--    <BRow>-->
<!--      <BButton @click="deleteAllRows" class="m-2">Supprimer le catalogue (pour les tests d'import)</BButton>-->
<!--      <p>{{ message }}</p>-->
<!--    </BRow>-->

  </BContainer>
</template>

<script>
import AppTitle from "@/components/visuel/AppTitle.vue";
import CreationUtilisateur from '@/components/utilisateur/CreationUtilisateur.vue'
import {deleteAllCatalogue, generateArkForAllEntriesMissingOnes, importAllCatalogue} from "@/services/api";
export default {
  name: "AdminView",
  components: {AppTitle, CreationUtilisateur},
  computed: {
    isAdmin() {
      return this.$store.getters.isAdmin;
    },
    isEditor() {
      return this.$store.getters.canEdit;
    }
  },
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