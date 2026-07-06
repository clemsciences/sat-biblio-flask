<template>
  <BContainer>
    <AppTitle title="Liste des références"
           info=""
           id="id-liste-ref"/>
    <p>Cliquez sur une ligne pour voir les détails.</p>
    <BButton v-if="isMobile" class="mb-2" @click="filtersOpen = !filtersOpen">
      {{ filtersOpen ? 'Masquer les filtres' : 'Afficher les filtres' }}
    </BButton>
    <div v-show="!isMobile || filtersOpen">
    <BRow class="my-3">
      <BCol md="6" lg="4">
        <BFormGroup label="Titre" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput v-model="titreFiltre" size="sm"
                   placeholder="Filtrer en fonction du titre"/>
        </BFormGroup>
      </BCol>
    </BRow>
    </div>
    <BRow>
      <BPagination
        v-model="currentPage"
        :total-rows="refFilteredNumber"
        :per-page="perPage"
        aria-controls="my-table"
        class="my-3"/>
      <FilterCount :filtered-item-count="refFilteredNumber" :total-item-count="refTotalNumber"/>
    </BRow>

    <BTable striped bordered hover
            responsive stacked="md"
            class="tbody-clickable"
            :provider="retrieveRef"
            :fields="fields"
            primary-key="id"
            ref="myTable"
            :per-page="perPage"
            :current-page="currentPage"
            :sort-by="tableSortBy"
            @row-clicked="goToReference">
      <template #table-caption>La liste des références bibliographiques dans la base.</template>

      <template #cell(annee)="data">
        <div v-if="data.item.annee === 's. d.'">Inconnu</div>
        <div v-else>{{ data.item.annee }}</div>
      </template>

      <template #cell(authors)="data">
        <div v-if="data.item.authors === '[collectif] (-)'">Collectif</div>
        <div v-else-if="data.item.authors === '[anonyme] (-)'">Anonyme</div>
        <div v-else>{{ data.item.authors }}</div>
      </template>

      <template #cell(lieu_edition)="data">
        <div v-if="data.item.lieu_edition === 's. l.'">Inconnu</div>
        <div v-else>{{ data.item.lieu_edition }}</div>
      </template>

      <template #cell(editeur)="data">
        <div v-if="data.item.editeur === 's. ed.'">Inconnu</div>
        <div v-else>{{ data.item.editeur }}</div>
      </template>

      <template #cell(nb_page)="data">
        <div v-if="data.item.nb_page === '-1' || data.item.nb_page === ''">Inconnu</div>
        <div v-else>{{ data.item.nb_page }}</div>
      </template>
    </BTable>

    <BRow>
      <BPagination
        v-model="currentPage"
        :total-rows="refFilteredNumber"
        :per-page="perPage"
        aria-controls="my-table"
        class="my-3"/>
      <FilterCount :filtered-item-count="refFilteredNumber" :total-item-count="refTotalNumber"/>
    </BRow>
  </BContainer>
</template>

<script>
import {retrieveBookReferences} from "@/services/api.js";
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
  name: "ListeReferenceLivre",
  components: { AppTitle, FilterCount, BButton, BContainer, BRow, BPagination, BCol, BFormGroup, BFormInput, BTable },
  mixins: [responsiveList],
  data() {
    return {
      isMounted: false,
      currentPage: 1,
      perPage: 50,
      sortBy: "titre",
      refFilteredNumber: 0,
      refTotalNumber: 0,
      fields: [
        { key: "authors",      label: "Auteurs",        sortable: false },
        { key: "titre",        label: "Titre",          sortable: false },
        { key: "lieu_edition", label: "Lieu d'édition", sortable: false },
        { key: "editeur",      label: "Editeur",        sortable: false },
        { key: "annee",        label: "Année",          sortable: false },
        { key: "nb_page",      label: "N° pages",       sortable: false },
        { key: "description",  label: "Description",    sortable: false },
      ],
      titreFiltre: "",
    }
  },

  computed: {
    // bootstrap-vue-next attend un tableau [{ key, order }] pour le prop sort-by
    tableSortBy() {
      return [{ key: this.sortBy, order: 'asc' }];
    },
  },

  methods: {
    // -----------------------------------------------------------------------
    // Provider — ctx.sortBy est un tableau [{ key, order }] en bvn
    // currentPage et perPage ne sont pas dans ctx : on utilise this.*
    // -----------------------------------------------------------------------
    async retrieveRef(ctx) {
      const sortKey = Array.isArray(ctx.sortBy) && ctx.sortBy.length > 0
          ? ctx.sortBy[0].key
          : this.sortBy;

      let params = `?page=${this.currentPage}`
          + `&size=${this.perPage}`
          + `&sortBy=${sortKey}`;

      if (this.titreFiltre.length > 0) {
        params += `&titre=${encodeURI(this.titreFiltre)}`;
      }

      try {
        // ✅ await ajouté
        const response = await retrieveBookReferences(params);
        if (response.data.success) {
          const references = response.data.references ?? [];
          // ✅ Totaux mis à jour avant le return pour que BPagination se recalcule
          this.refFilteredNumber = response.data.filtered_total ?? references.length;
          this.refTotalNumber    = response.data.total          ?? references.length;
          return references;
        }
        this.refFilteredNumber = 0;
        this.refTotalNumber    = 0;
        return [];
      } catch (reason) {
        console.error(reason);
        this.refFilteredNumber = 0;
        this.refTotalNumber    = 0;
        return [];
      }
    },

    goToReference(event) {
      this.$router.push(`/reference-livre/lire/${event.item.id}`);
    },

    refreshTable() {
      this.$refs.myTable?.refresh();
    },
  },

  mounted() {
    // La détection responsive (isMobile / matchMedia) est fournie par le mixin responsiveList.
    this.$nextTick(() => {
      this.isMounted = true;
    });
  },

  watch: {
    titreFiltre() {
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
/* Curseur « main » sur les lignes cliquables (clic → détail). */
.tbody-clickable :deep(tbody tr) {
  cursor: pointer;
}
</style>