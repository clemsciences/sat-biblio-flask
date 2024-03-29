<template>
  <b-container>
    <!-- liste des dernières actions faites sur le catalogue-->
    <p>Double-cliquez sur la ligne pour voir les détails de l'utilisateur.</p>
    <b-row class="my-1">
      <b-col lg="4">
        <b-form-group label="Prénom" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input type="search" v-model="firstNameFiltre"
                   placeholder="Filtrer en fonction du prénom"/>
        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="Nom de famille" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input type="search" v-model="familyNameFiltre"
                   placeholder="Filtrer en fonction du nom de famille"/>
        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="Rôle" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input type="search" v-model="rightFiltre"
                   placeholder="Filtrer en fonction du rôle"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-pagination
      v-model="currentPage"
      :total-rows="userTotalNumber"
      :per-page="perPage"
      aria-controls="my-table"/>
    <b-table striped bordered hover :items="loadUsers" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             :sort-by="sortBy" @row-dblclicked="goToUser" :filter="onFilter"
             ref="userTable">
      <template #table-caption>La liste des utilisateurs dans la base.</template>
      <template #cell(actions)="user">
        <b-button size="sm" @click="openDeletionUserModal(user)" class="mr-1" v-if="isAdmin">
          Supprimer
        </b-button>
      </template>

    </b-table>

    <b-modal ref="userDeletionModal" title="Suppression d'un utilisateur"
      cancel-title="Annuler" ok-title="Supprimer" @ok="deleteUser(selectedUser)">
      <p>Êtes-vous sûr de supprimer l'utilisateur {{ deletionMessage }} ?</p>
    </b-modal>
  </b-container>
</template>

<script>
import {deleteUser, getUsersCount, retrieveUsers} from "@/services/api";

export default {
  name: "Liste-Utilisateur",
  props: {
    forceUsersReload: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      users: [],
      currentPage: 1,
      perPage: 50,
      sortBy: "family_name",
      userTotalNumber: 0,
      fields: [
        {
          key: 'first_name',
          label: 'Prénom',
          sortable: false
        },
        {
          key: 'family_name',
          label: "Nom de famille",
          sortable: false
        },
        {
          key: 'right',
          label: "rôle",
          sortable: false
        },
        {
          key: 'actions',
          label: 'Actions',
          sortable: false
        }
      ],
      firstNameFiltre: '',
      familyNameFiltre: '',
      rightFiltre: '',
      // region deletion
      selectedUser: {},
      deletionMessage: "",
      // endregion
    }
  },
  methods: {
    loadUsers: function(ctx, callback) {
        let params = "?page="+ctx.currentPage+
          "&size="+ctx.perPage+
          "&sortBy="+ctx.sortBy;

        let filterParams = "";
        if(this.firstNameFiltre.length > 0) {
          filterParams = filterParams+"&first_name="+this.firstNameFiltre;
        }
        if(this.familyNameFiltre.length > 0) {
          filterParams = filterParams+"&family_name="+this.familyNameFiltre;
        }
        if(this.rightFiltre.length > 0) {
          filterParams = filterParams+"&right="+this.rightFiltre;
        }

        if(filterParams.length > 0) {
          params = params + filterParams;
        }
        retrieveUsers(params, this.$store.state.connectionInfo.token).then(
            (response) => {
              if(response.data.success) {
                this.users = response.data.users;
                callback(this.users);
              }
            }
        ).catch(
            (reason) => {
              console.log(reason);
              callback([]);
            }
        );
      return null;
    },
    getUserTotalNumber: function() {
      let filterParams = "";
      if(this.firstNameFiltre.length > 0) {
        filterParams = filterParams+"first_name="+encodeURI(this.firstNameFiltre);
      }
      if(this.familyNameFiltre.length > 0) {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams + "family_name="+encodeURI(this.familyNameFiltre);
      }
      if(this.rightFiltre.length > 0) {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams + "right="+encodeURI(this.rightFiltre);
      }
      if(filterParams.length > 0) {
        filterParams = "?"+filterParams;
      }
      getUsersCount(filterParams, this.$store.state.connectionInfo.token).then(
          (response) => {
            if(response.data.success) {
              this.userTotalNumber = response.data.total;
            }
          }
      )
    },
    goToUser: function(item) {
      this.$router.push(`/utilisateur/lire/${item.id}`);
    },
    openDeletionUserModal: function(user) {
      this.selectedUser = user;
      this.deletionMessage = `${this.selectedUser.item.first_name} ${this.selectedUser.item.family_name}`
      this.$refs.userDeletionModal.show();
    },
    deleteUser: function(user) {
      const userId = user.item.id;
      deleteUser(userId, this.$store.state.connectionInfo.token).then(
          response => {
            if(response.status === 204) {
              this.$refs.userTable.refresh();
              console.log("user deleted");
            } else {
              console.log('user deletion failed');
            }
          }
      );
    }
  },
  mounted() {
    this.getUserTotalNumber();
    this.$refs.userDeletionModal.hide();
  },
  watch: {
    firstNameFiltre: function (newValue, oldValue) {
      if(newValue !== oldValue) {
        this.getUserTotalNumber();
        this.currentPage = 1;
      }
    },
    familyNameFiltre: function () {
      this.getUserTotalNumber();
      this.currentPage = 1
    },
    rightFiltre: function () {
      this.getUserTotalNumber();
      this.currentPage = 1
    },
    forceUsersReload: function() {
      this.getUserTotalNumber();
      this.$refs.userTable.refresh();
    }
  },
  computed: {
    onFilter: function() {
      return `${this.firstNameFiltre} ${this.familyNameFiltre} ${this.rightFiltre}`;
    },
    isAdmin() {
      return this.$store.getters.isAdmin;
    },
  }

}
</script>

<style scoped>

</style>