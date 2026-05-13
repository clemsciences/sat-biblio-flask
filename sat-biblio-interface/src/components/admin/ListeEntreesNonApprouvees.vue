<template>
  <BContainer>
    <BPagination
      v-if="entryTotalNumber > 0"
      v-model="currentPage"
      :total-rows="entryTotalNumber"
      :per-page="perPage"
      aria-controls="my-table"
      class="my-3"/>

    <!-- ✅ BTable toujours présent pour que le provider puisse s'exécuter -->
    <BTable striped bordered hover
            :provider="loadEntries"
            :fields="fields"
            primary-key="description"
            ref="entriesTable"
            :per-page="perPage"
            :current-page="currentPage"
            @row-dblclicked="goToEntry">
      <template #table-caption>La liste des entrées pas encore approuvées.</template>
      <template #cell(actions)="entry">
        <BButton size="sm" @click="approve(entry)" class="me-1" v-if="isManager">
          Approuver
        </BButton>
      </template>
    </BTable>

    <p v-if="entryTotalNumber === 0 && !isLoading">
      Il n'y a aucune entrée de type {{ entryType }} à valider.
    </p>
  </BContainer>
</template>

<script>
import {canManage} from "@/services/rights";
import {
  BButton,
  BContainer,
  BPagination,
  BTable
} from "bootstrap-vue-next";

export default {
  name: "ListeEntreesNonApprouvees",
  components: { BButton, BContainer, BPagination, BTable },
  props: {
    retrieveListRequest: {
      type: Function,
    },
    perPage: {
      type: Number,
      default: 20,
    },
    goTo: {
      type: Function,
    },
    entryType: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      isMounted: false,
      isLoading: true,
      entryTotalNumber: 0,
      currentPage: 1,
      fields: [
        { key: 'contributor', label: 'Contributeur', sortable: false },
        { key: 'type',        label: 'Type',         sortable: false },
        { key: 'description', label: 'Description',  sortable: false },
        { key: 'actions',     label: 'Actions',      sortable: false },
      ],
    }
  },

  computed: {
    isManager() {
      return canManage(this.$store.getters.getUserRight);
    },
  },

  methods: {
    approve(entry) {
      // TODO
      console.log(entry);
    },
    goToEntry(entry) {
      // TODO
      console.log(entry);
    },

    // -----------------------------------------------------------------------
    // Provider — currentPage et perPage ne sont pas dans ctx : on utilise this.*
    // ✅ await ajouté sur retrieveListRequest
    // -----------------------------------------------------------------------
    async loadEntries() {
      this.isLoading = true;
      const params = `page=${this.currentPage}&size=${this.perPage}`;
      try {
        const response = await this.retrieveListRequest(params);
        if (response.data.success) {
          const entries = response.data.entries ?? [];
          // ✅ Total mis à jour avant le return pour que BPagination se recalcule
          this.entryTotalNumber = response.data.total ?? entries.length;
          return entries;
        }
        this.entryTotalNumber = 0;
        return [];
      } catch (reason) {
        console.error(reason);
        this.entryTotalNumber = 0;
        return [];
      } finally {
        this.isLoading = false;
      }
    },

    refreshTable() {
      this.$refs.entriesTable?.refresh();
    },
  },

  mounted() {
    this.$nextTick(() => {
      this.isMounted = true;
    });
  },

  watch: {
    currentPage() {
      this.refreshTable();
    },
    entryType() {
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
  },
}
</script>

<style scoped>
</style>