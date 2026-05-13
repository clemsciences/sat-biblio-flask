<template>
  <BContainer>
    <h2>Liste d'emprunts</h2>
    <p>Double-cliquez sur la ligne pour voir les détails sur un emprunt.</p>
    <BRow>
      <BFormGroup label="Filtrer par retard" v-slot="{ ariaDescribedby }">
        <BFormRadioGroup
          id="radio-group-1"
          v-model="lateStateSelected"
          :options="lateStateOptions"
          :aria-describedby="ariaDescribedby"
        ></BFormRadioGroup>
      </BFormGroup>
    </BRow>
    <BRow>
      <BPagination
        v-model="currentPage"
        :total-rows="borrowingFilteredNumber"
        :per-page="perPage"
        aria-controls="my-table"/>
      <FilterCount :filtered-item-count="borrowingFilteredNumber" :total-item-count="borrowingTotalNumber"/>
    </BRow>

    <BTable striped bordered hover
            :provider="retrieveBorrowings"
            :fields="fields"
            primary-key="id"
            ref="myTable"
            :per-page="perPage"
            :current-page="currentPage"
            :sort-by="tableSortBy"
            @row-dblclicked="goToBorrowing">
      <template #table-caption>La liste des emprunts dans la base.</template>

      <template #cell(emprunteur)="data">
        {{ data.item.emprunteur.first_name }} {{ data.item.emprunteur.family_name }}
      </template>
      <template #cell(enregistrement)="data">
        {{ data.item.enregistrement.reference.titre }} ({{ data.item.enregistrement.cote }})
      </template>
      <template #cell(gestionnaire)="data">
        {{ data.item.gestionnaire.first_name }} {{ data.item.gestionnaire.family_name }}
      </template>
      <template #cell(rendu)="data">
        <div v-if="data.item.rendu">Oui</div><div v-else>Non</div>
      </template>
      <template #cell(emprunte)="data">
        <div v-if="data.item.emprunte">Oui</div><div v-else>Non</div>
      </template>
      <template #cell(date_emprunt)="data">
        {{ fromISOtoFrenchDateFormat(data.item.date_emprunt) }}
      </template>
      <template #cell(date_retour_prevu)="data">
        {{ fromISOtoFrenchDateFormat(data.item.date_retour_prevu) }}
      </template>
      <template #cell(date_retour_reel)="data">
        {{ fromISOtoFrenchDateFormat(data.item.date_retour_reel) }}
      </template>
    </BTable>

    <BRow>
      <BPagination
        v-model="currentPage"
        :total-rows="borrowingFilteredNumber"
        :per-page="perPage"
        aria-controls="my-table"/>
      <FilterCount :filtered-item-count="borrowingFilteredNumber" :total-item-count="borrowingTotalNumber"/>
    </BRow>
  </BContainer>
</template>

<script>
import {retrieveBorrowings} from "@/services/api.js";
import FilterCount from "@/components/visuel/FilterCount.vue";
import {
  BContainer,
  BFormGroup,
  BFormRadioGroup,
  BPagination,
  BRow,
  BTable
} from "bootstrap-vue-next";

export default {
  name: "ListeEmprunt",
  components: { BContainer, BRow, BPagination, BFormGroup, BFormRadioGroup, BTable, FilterCount },
  data() {
    return {
      isMounted: false,
      currentPage: 1,
      perPage: 10,
      sortBy: "",
      borrowingFilteredNumber: 0,
      borrowingTotalNumber: 0,
      lateStateSelected: "all",
      lateStateOptions: [
        { text: "En retard",      value: "late" },
        { text: "Dans les temps", value: "on_time" },
        { text: "Tous",           value: "all" },
      ],
      fields: [
        { key: "enregistrement",    label: "Livre",                sortable: false },
        { key: "date_emprunt",      label: "Date d'emprunt",       sortable: false },
        { key: "emprunte",          label: "Emprunté ?",           sortable: false },
        { key: "rendu",             label: "Rendu ?",              sortable: false },
        { key: "date_retour_prevu", label: "Date de retour prévu", sortable: false },
        { key: "date_retour_reel",  label: "Date de retour réel",  sortable: false },
        { key: "emprunteur",        label: "Emprunteur",           sortable: false },
        { key: "gestionnaire",      label: "Gestionnaire",         sortable: false },
        { key: "comment",           label: "Commentaire",          sortable: false },
      ],
    }
  },

  computed: {
    // bootstrap-vue-next attend un tableau [{ key, order }] pour le prop sort-by
    tableSortBy() {
      if (!this.sortBy) return [];
      return [{ key: this.sortBy, order: 'asc' }];
    },
  },

  methods: {
    getLateFilterParam() {
      if (this.lateStateSelected === "late")    return "late=true";
      if (this.lateStateSelected === "on_time") return "on_time=true";
      return "all=true";
    },

    // -----------------------------------------------------------------------
    // Provider — ctx.sortBy est un tableau [{ key, order }] en bvn
    // currentPage et perPage ne sont pas dans ctx : on utilise this.*
    // -----------------------------------------------------------------------
    async retrieveBorrowings(ctx) {
      const sortKey = Array.isArray(ctx.sortBy) && ctx.sortBy.length > 0
          ? ctx.sortBy[0].key
          : this.sortBy;

      let params = `?page=${this.currentPage}`
          + `&size=${this.perPage}`
          + (sortKey ? `&sortBy=${sortKey}` : "")
          + `&${this.getLateFilterParam()}`;

      try {
        // ✅ await ajouté
        const response = await retrieveBorrowings(params);
        if (response.data.success) {
          const borrowings = (response.data.borrowings ?? []).map((value) => ({
            ...value,
            _rowVariant: this.isBorrowingLate(value) ? '' : 'warning'
          }));
          // ✅ Totaux mis à jour avant le return pour que BPagination se recalcule
          this.borrowingFilteredNumber = response.data.filtered_total ?? borrowings.length;
          this.borrowingTotalNumber    = response.data.total          ?? borrowings.length;
          return borrowings;
        }
        this.borrowingFilteredNumber = 0;
        this.borrowingTotalNumber    = 0;
        return [];
      } catch (reason) {
        console.error(reason);
        this.borrowingFilteredNumber = 0;
        this.borrowingTotalNumber    = 0;
        return [];
      }
    },

    goToBorrowing(event) {
      this.$router.push(`/emprunt/${event.item.id}`);
    },

    isBorrowingLate(item) {
      if (item.rendu) return true;
      const now = new Date();
      // ✅ Correction du bug original : getMonth()+1 et getDate() (pas getDay())
      const mm    = String(now.getMonth() + 1).padStart(2, '0');
      const dd    = String(now.getDate()).padStart(2, '0');
      const today = `${now.getFullYear()}-${mm}-${dd}`;
      return today < item.date_retour_prevu;
    },

    fromISOtoFrenchDateFormat(isoDate) {
      if (typeof isoDate !== "undefined" && isoDate) {
        const l = isoDate.split("-");
        if (l.length === 3) {
          return `${l[2]}/${l[1]}/${l[0]}`;
        }
      }
      return "";
    },

    refreshTable() {
      this.$refs.myTable?.refresh();
    },
  },

  mounted() {
    this.$nextTick(() => {
      this.isMounted = true;
    });
  },

  watch: {
    lateStateSelected() {
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
</style>