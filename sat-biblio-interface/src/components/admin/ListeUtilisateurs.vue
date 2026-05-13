<template>
  <BContainer>
    <p>Double-cliquez sur la ligne pour voir les détails de l'utilisateur.</p>
    <BRow class="my-1">
      <BCol lg="4">
        <BFormGroup label="Prénom" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput type="search" v-model="firstNameFilter"
                   placeholder="Filtrer en fonction du prénom"/>
        </BFormGroup>
      </BCol>
      <BCol lg="4">
        <BFormGroup label="Nom de famille" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput type="search" v-model="familyNameFilter"
                   placeholder="Filtrer en fonction du nom de famille"/>
        </BFormGroup>
      </BCol>
      <BCol lg="4">
        <BFormGroup label="Rôle" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput type="search" v-model="rightFilter"
                   placeholder="Filtrer en fonction du rôle"/>
        </BFormGroup>
      </BCol>
    </BRow>
    <BPagination
      v-model="currentPage"
      :total-rows="userFilteredNumber"
      :per-page="perPage"
      aria-controls="userTable"/>

    <BTable striped bordered hover
            :provider="loadUsers"
            :fields="fields"
            primary-key="id"
            ref="userTable"
            :per-page="perPage"
            :current-page="currentPage"
            :sort-by="tableSortBy"
            @row-dblclicked="goToUser">
      <template #table-caption>La liste des utilisateurs dans la base.</template>
      <template #cell(actions)="user">
        <BButton size="sm" @click="openDeletionUserModal(user)" class="me-1" v-if="isAdmin">
          Supprimer
        </BButton>
      </template>
    </BTable>

    <BModal ref="userDeletionModal" title="Suppression d'un utilisateur"
      cancel-title="Annuler" ok-title="Supprimer" @ok="deleteUser(selectedUser)">
      <p>Êtes-vous sûr de supprimer l'utilisateur {{ deletionMessage }} ?</p>
    </BModal>
  </BContainer>
</template>

<script>
import {deleteUser, retrieveUsers} from "@/services/api";
import {
  BButton,
  BCol,
  BContainer,
  BFormGroup,
  BFormInput,
  BModal,
  BPagination,
  BRow,
  BTable
} from "bootstrap-vue-next";

export default {
  name: "ListeUtilisateurs",
  components: {
    BButton, BContainer, BRow, BPagination, BCol,
    BFormGroup, BFormInput, BModal, BTable
  },
  props: {
    forceUsersReload: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isMounted: false,
      currentPage: 1,
      perPage: 50,
      sortBy: "family_name",
      userFilteredNumber: 0,
      userTotalNumber: 0,
      fields: [
        { key: 'first_name',   label: 'Prénom',          sortable: false },
        { key: 'family_name',  label: 'Nom de famille',  sortable: false },
        { key: 'right',        label: 'Rôle',            sortable: false },
        { key: 'actions',      label: 'Actions',         sortable: false },
      ],
      firstNameFilter:  '',
      familyNameFilter: '',
      rightFilter:      '',
      // region deletion
      selectedUser:    {},
      deletionMessage: "",
      // endregion
    }
  },

  computed: {
    // bootstrap-vue-next attend un tableau [{ key, order }] pour le prop sort-by
    tableSortBy() {
      return [{ key: this.sortBy, order: 'asc' }];
    },
    isAdmin() {
      return this.$store.getters.isAdmin;
    },
  },

  methods: {
    getFilterParams() {
      const parts = [];
      if (this.firstNameFilter.length > 0)  parts.push(`first_name=${encodeURI(this.firstNameFilter)}`);
      if (this.familyNameFilter.length > 0) parts.push(`family_name=${encodeURI(this.familyNameFilter)}`);
      if (this.rightFilter.length > 0)      parts.push(`right=${encodeURI(this.rightFilter)}`);
      return parts.join('&');
    },

    // -----------------------------------------------------------------------
    // Provider — ctx.sortBy est un tableau [{ key, order }] en bvn
    // currentPage et perPage ne sont pas dans ctx : on utilise this.*
    // -----------------------------------------------------------------------
    async loadUsers(ctx) {
      const sortKey = Array.isArray(ctx.sortBy) && ctx.sortBy.length > 0
          ? ctx.sortBy[0].key
          : this.sortBy;

      let params = `?page=${this.currentPage}`
          + `&size=${this.perPage}`
          + `&sortBy=${sortKey}`;

      const filterParams = this.getFilterParams();
      if (filterParams.length > 0) params += `&${filterParams}`;

      try {
        // ✅ await déjà présent dans l'original, conservé
        const response = await retrieveUsers(params, this.$store.state.connectionInfo.token);
        if (response.data.success) {
          const users = response.data.users ?? [];
          // ✅ Totaux mis à jour avant le return pour que BPagination se recalcule
          this.userFilteredNumber = response.data.filtered_total ?? users.length;
          this.userTotalNumber    = response.data.total          ?? users.length;
          return users;
        }
        this.userFilteredNumber = 0;
        this.userTotalNumber    = 0;
        return [];
      } catch (reason) {
        console.error(reason);
        this.userFilteredNumber = 0;
        this.userTotalNumber    = 0;
        return [];
      }
    },

    goToUser(event) {
      this.$router.push(`/utilisateur/lire/${event.item.id}`);
    },

    openDeletionUserModal(user) {
      this.selectedUser   = user;
      this.deletionMessage = `${user.item.first_name} ${user.item.family_name}`;
      this.$refs.userDeletionModal.show();
    },

    deleteUser(user) {
      const userId = user.item.id;
      deleteUser(userId, this.$store.state.connectionInfo.token).then((response) => {
        if (response.status === 204) {
          this.refreshTable();
          console.log("user deleted");
        } else {
          console.log('user deletion failed');
        }
      });
    },

    refreshTable() {
      this.$refs.userTable?.refresh();
    },
  },

  mounted() {
    // ✅ BModal n'a plus de méthode .hide() à appeler au montage en bvn
    // — le modal est masqué par défaut, l'appel était inutile et causait une erreur
    this.$nextTick(() => {
      this.isMounted = true;
    });
  },

  watch: {
    firstNameFilter(newValue, oldValue) {
      if (newValue !== oldValue) {
        if (this.isMounted) this.currentPage = 1;
        this.refreshTable();
      }
    },
    familyNameFilter() {
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    rightFilter() {
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    currentPage() {
      this.refreshTable();
    },
    forceUsersReload() {
      this.refreshTable();
    },
  },
}
</script>

<style scoped>
</style>