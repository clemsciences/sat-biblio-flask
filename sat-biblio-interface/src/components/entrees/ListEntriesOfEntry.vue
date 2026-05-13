<template>
  <BContainer>
    <BPagination
        v-if="totalNumber > 0"
        v-model="currentPage"
        :total-rows="totalNumber"
        :per-page="perPage"
        aria-controls="my-table"
        class="my-3"/>
    <BTable striped bordered hover
            :provider="retrieveList"
            :fields="fields"
            primary-key="uniqueId"
            ref="myTable"
            :per-page="perPage"
            :current-page="currentPage"
            :sort-by="tableSortBy"
            @row-dblclicked="goTo">
      <template #table-caption v-if="caption.length > 0">{{ caption }}</template>
    </BTable>
    <p v-if="totalNumber === 0 && !isLoading">Il n'y a aucune entrée.</p>
  </BContainer>
</template>

<script>
import {
  BButton, BCol, BContainer, BFormGroup,
  BFormInput, BPagination, BRow, BTable
} from "bootstrap-vue-next";

export default {
  name: "ListEntriesOfEntry",
  components: { BButton, BCol, BContainer, BFormGroup, BFormInput, BPagination, BRow, BTable },
  props: {
    retrieveListRequest: { type: Function },
    perPage:   { type: Number,  default: 20 },
    caption:   { type: String,  default: "" },
    goTo:      { type: Function },
    entryId:   { type: Number },
    entryType: { type: String, required: true }
  },
  data() {
    return {
      isLoading: true,
      totalNumber: 0,
      currentPage: 1,
      sortBy: "type",
      fields: [
        { key: "type_string", label: "Type d'entrée", sortable: true },
        { key: "description", label: "Description",   sortable: false },
      ],
    }
  },
  computed: {
    tableSortBy() {
      return [{ key: this.sortBy, order: 'asc' }];
    }
  },
  methods: {
    async retrieveList(ctx) {
      this.isLoading = true;
      // Extraire la clé de tri depuis le format tableau de bvn
      const sortKey = Array.isArray(ctx.sortBy) && ctx.sortBy.length > 0
          ? ctx.sortBy[0].key
          : this.sortBy;

      const params = "page=" + this.currentPage
          + "&size=" + this.perPage
          + "&sortBy=" + sortKey
          + "&valid=1&type=" + this.entryType;
      try {
        // ✅ await ajouté
        const response = await this.retrieveListRequest(this.entryId, params);
        if (response.data.success) {
          // ✅ map sur le tableau retourné par l'API, pas sur this.entries
          const enrichedEntries = (response.data.entries ?? []).map((value) => {
            value.type_string = response.data.entries[value.type]?.string ?? '';
            value.uniqueId    = `${value.type}-${value.id}`;
            return value;
          });
          this.totalNumber = response.data.total ?? enrichedEntries.length;
          return enrichedEntries;
        }
      } catch (reason) {
        console.error(reason);
      } finally {
        this.isLoading = false;
      }
      this.totalNumber = 0;
      return [];
    },
  },
  watch: {
    currentPage() {
      this.$refs.myTable?.refresh();
    },
    entryId() {
      this.currentPage = 1;
      this.$refs.myTable?.refresh();
    },
    entryType() {
      this.currentPage = 1;
      this.$refs.myTable?.refresh();
    }
  }
}
</script>