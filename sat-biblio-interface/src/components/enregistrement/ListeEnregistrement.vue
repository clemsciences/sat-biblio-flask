<template>
  <BContainer>
    <AppTitle info="Le catalogue est la liste des enregistrements dans la bibliothèque."
    id="id-catalogue">
      Catalogue
    </AppTitle>
    <p>Cliquez sur une ligne pour voir les détails.</p>
    <BButton v-if="isMobile" class="mb-2" @click="filtersOpen = !filtersOpen">
      {{ filtersOpen ? 'Masquer les filtres' : 'Afficher les filtres' }}
    </BButton>
    <div v-show="!isMobile || filtersOpen">
    <BRow class="my-1">
      <BCol md="6" lg="4">
        <BFormGroup label="Cote" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput v-model="coteFilter" size="sm"
                   placeholder="Filtrer en fonction de la cote"/>
        </BFormGroup>
      </BCol>
      <BCol md="6" lg="4">
        <BFormGroup label="Auteur" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput v-model="authorFilter" size="sm"
                   placeholder="Filtrer en fonction de l'auteur"/>
        </BFormGroup>
      </BCol>
      <BCol md="6" lg="4">
        <BFormGroup label="Aide à la recherche" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput v-model="keywordsFilter" size="sm"
                   placeholder="Filtrer en fonction d'un mot clef"/>
        </BFormGroup>
      </BCol>
      <BCol md="6" lg="4">
        <BFormGroup label="Titre" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput v-model="titleFilter" size="sm"
                   placeholder="Filtrer en fonction du titre"/>
        </BFormGroup>
      </BCol>
    </BRow>
    </div>
    <BRow>
      <BPagination
          v-model="currentPage"
          :total-rows="recordFilteredNumber"
          :per-page="perPage"
          aria-controls="my-table"
          class="my-3"/>
      <FilterCount :filtered-item-count="recordFilteredNumber" :total-item-count="recordTotalNumber"/>
    </BRow>

    <BTable striped bordered hover
            responsive stacked="md"
            class="tbody-clickable"
            :provider="retrieveEnregistrementList"
            :fields="fields"
            primary-key="id"
            ref="myTable"
            :per-page="perPage"
            :current-page="currentPage"
            :sort-by="tableSortBy"
            @row-clicked="goToEnregistrement">
      <template #table-caption>La liste des références bibliographiques dans la base.</template>
    </BTable>

    <BRow>
      <BPagination
          v-model="currentPage"
          :total-rows="recordFilteredNumber"
          :per-page="perPage"
          aria-controls="my-table"
          class="my-3"/>
      <FilterCount :filtered-item-count="recordFilteredNumber" :total-item-count="recordTotalNumber"/>
    </BRow>
  </BContainer>
</template>

<script>
import {retrieveBookRecords} from "@/services/api";
import AppTitle from "@/components/visuel/AppTitle.vue";
import FilterCount from "@/components/visuel/FilterCount.vue";
import responsiveList from "@/mixins/responsiveList.js";
import {
  BButton,
  BCol,
  BContainer,
  BFormGroup,
  BFormInput,
  BPagination,
  BRow,
  BTable
} from "bootstrap-vue-next";

export default {
  name: "ListeEnregistrement",
  components: { BButton, BContainer, BRow, BPagination, BCol, BFormGroup, BFormInput, BTable, AppTitle, FilterCount },
  mixins: [responsiveList],
  data() {
    return {
      isMounted: false,
      currentPage: 1,
      perPage: 50,
      sortBy: "cote",
      recordFilteredNumber: 0,
      recordTotalNumber: 0,
      fields: [
        { key: "cote",              label: "Cote",                sortable: false },
        { key: "reference",         label: "Titre",               sortable: false },
        { key: "authors",           label: "Auteurs",             sortable: false },
        { key: "annee_obtention",   label: "Année d'obtention",   sortable: false },
        { key: "provenance",        label: "Provenance",          sortable: false },
        { key: "aide_a_la_recherche", label: "Aide à la recherche", sortable: false },
        { key: "observations",      label: "Observations",        sortable: false },
      ],
      coteFilter: "",
      authorFilter: "",
      keywordsFilter: "",
      titleFilter: "",
    }
  },

  computed: {
    // bootstrap-vue-next attend un tableau [{ key, order }] pour le prop sort-by
    tableSortBy() {
      return [{ key: this.sortBy, order: 'asc' }];
    },
  },

  methods: {
    getFilterParams() {
      const parts = [];
      if (this.coteFilter.length > 0)     parts.push(`cote=${encodeURI(this.coteFilter)}`);
      if (this.authorFilter.length > 0)   parts.push(`author=${encodeURI(this.authorFilter)}`);
      if (this.titleFilter.length > 0)    parts.push(`titre=${encodeURI(this.titleFilter)}`);
      if (this.keywordsFilter.length > 0) parts.push(`mot_clef=${encodeURI(this.keywordsFilter)}`);
      return parts.join('&');
    },

    // -----------------------------------------------------------------------
    // Provider — ctx.sortBy est un tableau [{ key, order }] en bvn
    // currentPage et perPage ne sont pas dans ctx : on utilise this.*
    // -----------------------------------------------------------------------
    async retrieveEnregistrementList(ctx) {
      const sortKey = Array.isArray(ctx.sortBy) && ctx.sortBy.length > 0
          ? ctx.sortBy[0].key
          : this.sortBy;

      let params = `?page=${this.currentPage}`
          + `&size=${this.perPage}`
          + `&sortBy=${sortKey}`;

      const filterParams = this.getFilterParams();
      if (filterParams.length > 0) params += `&${filterParams}`;

      try {
        // ✅ await ajouté
        const response = await retrieveBookRecords(params);
        if (response.data.success) {
          const records = response.data.enregistrements ?? [];
          // ✅ Totaux mis à jour avant le return pour que BPagination se recalcule
          this.recordFilteredNumber = response.data.filtered_total ?? records.length;
          this.recordTotalNumber    = response.data.total          ?? records.length;
          return records;
        }
        this.recordFilteredNumber = 0;
        this.recordTotalNumber    = 0;
        return [];
      } catch (reason) {
        console.error(reason);
        this.recordFilteredNumber = 0;
        this.recordTotalNumber    = 0;
        return [];
      }
    },

    goToEnregistrement(event) {
      this.$router.push(`/enregistrement/lire/${event.item.id}`);
    },

    refreshTable() {
      this.$refs.myTable?.refresh();
    },
  },

  mounted() {
    // La détection responsive (isMobile / matchMedia) est fournie par le mixin responsiveList.
    if (this.$route.query.mot_clef) {
      this.keywordsFilter = this.$route.query.mot_clef;
    }
    this.$nextTick(() => {
      this.isMounted = true;
    });
  },

  watch: {
    coteFilter() {
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    authorFilter() {
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    keywordsFilter() {
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    titleFilter() {
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    currentPage() {
      this.refreshTable();
    },
  },
}
</script>

<style scoped>
/* Curseur « main » sur les lignes cliquables du catalogue (clic → détail). */
.tbody-clickable :deep(tbody tr) {
  cursor: pointer;
}
</style>