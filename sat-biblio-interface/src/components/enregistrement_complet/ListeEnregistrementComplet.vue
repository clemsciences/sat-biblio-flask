<template>
  <BContainer>
    <AppTitle info="Le catalogue est la liste des ouvrages dans la bibliothèque."
           id="id-catalogue">
      Catalogue
    </AppTitle>
    <p>Double-cliquez sur la ligne pour voir les détails.</p>
    <BRow class="my-1">
      <BCol lg="4">
        <BFormGroup label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <BButton v-b-toggle.modal-cote class="d-inline-block">
            {{ prefixCoteFiler.length > 0 || numberCoteFilter.length > 0 ? coteFilter : 'Choisir une cote' }}
          </BButton>

          <BModal id="modal-cote" title="Sélection de la cote"
                   ok-title="Valider" cancel-title="Annuler">
            <BFormGroup label="Préfixe">
              <BFormSelect
                  v-model="prefixCoteFiler"
                  :options="[
                  { value: '', text: 'Choix de la cote' },
                  { value: 'A', text: 'A' },
                  { value: 'B', text: 'B' },
                  { value: 'BBH', text: 'BBH' },
                  { value: 'C', text: 'C' },
                  { value: 'D', text: 'D' },
                  { value: 'DOC', text: 'DOC' },
                  { value: 'GH', text: 'GH' },
                  { value: 'FAG', text: 'FAG' },
                  { value: 'FAM', text: 'FAM' },
                  { value: 'FAP', text: 'FAP' },
                  { value: 'MM', text: 'MM' }
                ]"
                  @change="updatePrefixCoteFilter">
              </BFormSelect>
            </BFormGroup>
            <BFormGroup label="Numéro">
              <BFormInput
                  v-model="numberCoteFilter"
                  type="text"
                  pattern="[0-9]*"
                  inputmode="numeric"
                  maxlength="4"
                  @keydown="onlyDigitsKeydown"
                  @paste.prevent="sanitizeDigitsPaste"
                  @input="stripNonDigits"
                  placeholder="Entrez un numéro">
              </BFormInput>
            </BFormGroup>
          </BModal>

          <template #label>
            Cote
            <IBiInfoCircle v-b-tooltip="'La cote est le numéro permettant de localiser l\'ouvrage dans la bibliothèque'"
                    variant="dark"/>
          </template>
        </BFormGroup>
      </BCol>
      <BCol lg="4">
        <BFormGroup label="Auteur" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput v-model="authorFilter" size="sm"
                   placeholder="Filtrer en fonction de l'auteur"/>
        </BFormGroup>
      </BCol>
      <BCol lg="4">
        <BFormGroup label="Aide à la recherche" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput v-model="keywordsFilter" size="sm"
                   placeholder="Filtrer en fonction d'un mot clef"/>
        </BFormGroup>
      </BCol>
      <BCol lg="4">
        <BFormGroup label="Titre" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput v-model="titleFilter" size="sm"
                   placeholder="Filtrer en fonction du titre"/>
        </BFormGroup>
      </BCol>
      <BCol lg="4">
        <BFormGroup label="Année d'obtention" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <div class="d-flex gap-1 align-items-center">
            <BFormSelect v-model="anneeObtentionMode" size="sm" :options="dateFilterModeOptions"/>
            <BFormInput v-if="anneeObtentionMode === 'before' || anneeObtentionMode === 'after'"
                        v-model="anneeObtentionYear" type="number" size="sm"
                        placeholder="Année" class="w-auto"/>
            <template v-if="anneeObtentionMode === 'between'">
              <BFormInput v-model="anneeObtentionYearMin" type="number" size="sm"
                          placeholder="De" class="w-auto"/>
              <BFormInput v-model="anneeObtentionYearMax" type="number" size="sm"
                          placeholder="À" class="w-auto"/>
            </template>
          </div>
        </BFormGroup>
      </BCol>
      <BCol lg="4" v-if="isAdmin">
        <BFormGroup label="Date dernière modif." label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <div class="d-flex gap-1 align-items-center">
            <BFormSelect v-model="dateModifMode" size="sm" :options="dateFilterModeOptions"/>
            <VueDatePicker v-if="dateModifMode === 'before' || dateModifMode === 'after'"
                           v-model="dateModif" placeholder="Date"
                           :locale="dpLocale" :week-start="1" :clearable="true"
                           :time-config="{ enableTimePicker: false }"
                           :formats="{ input: 'dd/MM/yyyy' }"/>
            <template v-if="dateModifMode === 'between'">
              <VueDatePicker v-model="dateModifMin" placeholder="Du"
                             :locale="dpLocale" :week-start="1" :clearable="true"
                             :time-config="{ enableTimePicker: false }"
                             :formats="{ input: 'dd/MM/yyyy' }"/>
              <VueDatePicker v-model="dateModifMax" placeholder="Au"
                             :locale="dpLocale" :week-start="1" :clearable="true"
                             :time-config="{ enableTimePicker: false }"
                             :formats="{ input: 'dd/MM/yyyy' }"/>
            </template>
          </div>
        </BFormGroup>
      </BCol>
      <BCol lg="4">
        <BFormGroup label="" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <BButton @click="exportSearchResult" :disabled="isExporting" v-b-tooltip="'Exporte un fichier Excel contenant les éléments du catalogue qui correspondent aux filtres. Si aucun filtre n\'est mis, alors le catalogue entier est exporté.'">
            {{ isExporting ? 'Export en cours...' : 'Exporter' }}
          </BButton>
          <template #label>
            <IBiInfoCircle v-b-tooltip="'Exporte un fichier Excel contenant les éléments du catalogue qui correspondent aux filtres. Si aucune filtre n\'est mis, alors le catalogue entier est exporté.'"
                    variant="dark"/>
          </template>
        </BFormGroup>
      </BCol>
      <BCol lg="4">
        <BFormGroup label="" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <BButton @click="clearSearchFields" v-b-tooltip="'Réinitialise les filtres de recherche.'">
            Réinitialiser
          </BButton>
          <template #label>
            <IBiInfoCircle v-b-tooltip="'Réinitialise les filtres de recherche.'"
                    variant="dark"/>
          </template>
        </BFormGroup>
      </BCol>
    </BRow>
    <BRow class="my-1">
      <BCol lg="12">
        <BFormGroup label="Trier par" label-cols-sm="2" label-align-sm="right" label-size="sm" class="mb-0">
          <BFormRadioGroup
              v-model="sortBy"
              :options="sortByOptions"
              class="pt-1"
              @change="onSortChange"
          ></BFormRadioGroup>
        </BFormGroup>
      </BCol>
    </BRow>
    <BRow>
      <BPagination
          v-model="currentPage"
          :total-rows="recordFilteredNumber"
          :per-page="perPage"
          aria-controls="myTable"
          class="my-3"/>
      <FilterCount :filtered-item-count="recordFilteredNumber" :total-item-count="recordTotalNumber"/>
    </BRow>

    <BTable striped bordered hover
            :provider="retrieveEnregistrementCompleteList"
            :fields="filteredFields"
            primary-key="id"
            ref="myTable"
            :current-page="currentPage"
            :per-page="perPage"
            :sort-by="tableSortBy"
            @row-dblclicked="goToEnregistrementComplet">
      <template #table-caption>La liste des références bibliographiques dans la base.</template>
    </BTable>

    <BRow>
      <BPagination
          v-model="currentPage"
          :total-rows="recordFilteredNumber"
          :per-page="perPage"
          aria-controls="myTable"
          class="my-3"/>
      <FilterCount :filtered-item-count="recordFilteredNumber" :total-item-count="recordTotalNumber"/>
    </BRow>
  </BContainer>
</template>

<script>
import {exportBookRecordsWithReference, getBookRecordsCount, retrieveBookRecordsWithReference} from "@/services/api.js";
import { fr } from 'date-fns/locale';
import AppTitle from "@/components/visuel/AppTitle.vue";
import FilterCount from "@/components/visuel/FilterCount.vue";
import {
  BButton,
  BCol,
  BContainer,
  BFormGroup,
  BFormInput,
  BFormRadioGroup,
  BFormSelect,
  BModal,
  BPagination,
  BRow,
  BTable
} from "bootstrap-vue-next";

export default {
  name: "ListeEnregistrementComplet",
  components: {
    BButton, BContainer, BRow, BPagination, BCol,
    BFormGroup, BFormInput, BFormRadioGroup, BFormSelect,
    BModal, BTable, AppTitle, FilterCount
  },
  data() {
    return {
      isMounted: false,
      currentPage: 1,
      perPage: 50,
      sortBy: "cote",
      sortDesc: false,
      recordFilteredNumber: 0,
      recordTotalNumber: 0,
      fields: [
        { key: "cote", label: "Cote", sortable: true },
        { key: "reference", label: "Titre", sortable: false },
        { key: "authors", label: "Auteurs", sortable: false },
        { key: "annee_obtention", label: "Année d'obtention", sortable: true },
        { key: "provenance", label: "Provenance", sortable: false },
        { key: "aide_a_la_recherche", label: "Aide à la recherche", sortable: false },
        { key: "observations", label: "Observations", sortable: false },
        { key: "date_derniere_modification", label: "Date dernière modification", sortable: true }
      ],
      prefixCoteFiler: "",
      numberCoteFilter: "",
      authorFilter: "",
      keywordsFilter: "",
      titleFilter: "",
      anneeObtentionMode: "",
      anneeObtentionYear: "",
      anneeObtentionYearMin: "",
      anneeObtentionYearMax: "",
      dateModifMode: "",
      dateModif: null,
      dateModifMin: null,
      dateModifMax: null,
      dpLocale: fr,
      dateFilterModeOptions: [
        { value: "", text: "Aucun filtre" },
        { value: "empty", text: "Vide / non renseigné" },
        { value: "before", text: "Avant" },
        { value: "after", text: "Après" },
        { value: "between", text: "Entre" },
      ],
      isExporting: false,
    }
  },

  computed: {
    // bootstrap-vue-next attend un tableau [{ key, order }] pour le prop sort-by
    tableSortBy() {
      return [{ key: this.sortBy, order: this.sortDesc ? 'desc' : 'asc' }];
    },
    coteFilter() {
      const numValue = parseInt(this.numberCoteFilter);
      if (numValue >= 1 && numValue <= 9) {
        return `${this.prefixCoteFiler} 000${numValue}`;
      } else if (numValue >= 10 && numValue <= 99) {
        return `${this.prefixCoteFiler} 00${numValue}`;
      } else if (numValue >= 100 && numValue <= 999) {
        return `${this.prefixCoteFiler} 0${numValue}`;
      }
      if (this.prefixCoteFiler.length === 0 && this.numberCoteFilter.length === 0) {
        return "";
      }
      return `${this.prefixCoteFiler} ${this.numberCoteFilter}`;
    },
    searchFieldsUsed() {
      return this.coteFilter.length > 0 || this.authorFilter.length > 0
          || this.keywordsFilter.length > 0 || this.titleFilter.length > 0;
    },
    isAdmin() {
      return this.$store.getters.isAdmin;
    },
    filteredFields() {
      if (this.isAdmin) return this.fields;
      return this.fields.filter(f => f.key !== 'date_derniere_modification');
    },
    sortByOptions() {
      const options = [
        { text: 'Cote', value: 'cote' },
        { text: "Année d'obtention", value: 'annee_obtention' },
      ];
      if (this.isAdmin) {
        options.push({ text: 'Date dernière modification', value: 'date_derniere_modification' });
      }
      return options;
    }
  },

  methods: {
    getFilterParams() {
      const parts = [];
      if (this.coteFilter.length > 0) {
        parts.push(`cote=${encodeURI(this.coteFilter)}`);
      }
      if (this.authorFilter.length > 0) {
        parts.push(`author=${encodeURI(this.authorFilter)}`);
      }
      if (this.titleFilter.length > 0) {
        parts.push(`titre=${encodeURI(this.titleFilter)}`);
      }
      if (this.keywordsFilter.length > 0) {
        parts.push(`mot_clef=${encodeURI(this.keywordsFilter)}`);
      }

      // Filtre sur l'année d'obtention
      if (this.anneeObtentionMode === 'empty') {
        parts.push('annee_obtention_mode=empty');
      } else if ((this.anneeObtentionMode === 'before' || this.anneeObtentionMode === 'after')
          && this.anneeObtentionYear) {
        parts.push(`annee_obtention_mode=${this.anneeObtentionMode}`);
        parts.push(`annee_obtention_year=${encodeURI(this.anneeObtentionYear)}`);
      } else if (this.anneeObtentionMode === 'between'
          && (this.anneeObtentionYearMin || this.anneeObtentionYearMax)) {
        parts.push('annee_obtention_mode=between');
        if (this.anneeObtentionYearMin) parts.push(`annee_obtention_year_min=${encodeURI(this.anneeObtentionYearMin)}`);
        if (this.anneeObtentionYearMax) parts.push(`annee_obtention_year_max=${encodeURI(this.anneeObtentionYearMax)}`);
      }

      // Filtre sur la date de dernière modification (réservé aux administrateurs)
      if (this.isAdmin) {
        if (this.dateModifMode === 'empty') {
          parts.push('date_modif_mode=empty');
        } else if (this.dateModifMode === 'before' || this.dateModifMode === 'after') {
          const d = this.formatDateParam(this.dateModif);
          if (d) {
            parts.push(`date_modif_mode=${this.dateModifMode}`);
            parts.push(`date_modif=${d}`);
          }
        } else if (this.dateModifMode === 'between') {
          const dMin = this.formatDateParam(this.dateModifMin);
          const dMax = this.formatDateParam(this.dateModifMax);
          if (dMin || dMax) {
            parts.push('date_modif_mode=between');
            if (dMin) parts.push(`date_modif_min=${dMin}`);
            if (dMax) parts.push(`date_modif_max=${dMax}`);
          }
        }
      }

      return parts.join('&');
    },

    formatDateParam(value) {
      if (!value) return "";
      const date = value instanceof Date ? value : new Date(value);
      if (isNaN(date.getTime())) return "";
      const y = date.getFullYear();
      const m = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${y}-${m}-${day}`;
    },

    onFilterChanged() {
      this.getRecordTotalNumber();
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },

    // -----------------------------------------------------------------------
    // Provider BTable — bootstrap-vue-next passe un contexte avec :
    //   context.sortBy   → tableau [{ key, order }]
    //   context.filter   → valeur du prop filter (non utilisé ici)
    // currentPage et perPage ne sont PAS dans le contexte : on utilise this.*
    // -----------------------------------------------------------------------
    async retrieveEnregistrementCompleteList(context) {
      // Extraire le premier élément du tableau sortBy fourni par bvn
      const sortEntry = Array.isArray(context.sortBy) && context.sortBy.length > 0
          ? context.sortBy[0]
          : { key: this.sortBy, order: this.sortDesc ? 'desc' : 'asc' };

      const sortKey = sortEntry.key || this.sortBy;
      const sortDescValue = sortEntry.order === 'desc';

      let params = `?page=${this.currentPage}`
          + `&size=${this.perPage}`
          + `&sortBy=${sortKey}`
          + `&sortDesc=${sortDescValue ? 'true' : 'false'}`;

      const filterParams = this.getFilterParams();
      if (filterParams.length > 0) {
        params = `${params}&${filterParams}`;
      }

      try {
        const response = await retrieveBookRecordsWithReference(params);
        if (response.data.success) {
          const records = response.data.enregistrements;
          this.recordFilteredNumber = response.data.filtered_total ?? records.length;
          this.recordTotalNumber = response.data.total ?? records.length;
          return records || [];
        }
        return [];
      } catch (reason) {
        console.error(reason);
        return [];
      }
    },

    getRecordTotalNumber() {
      let filterParams = "?result_type=number";
      const remainingFilterParams = this.getFilterParams();
      if (remainingFilterParams.length > 0) {
        filterParams = `${filterParams}&${remainingFilterParams}`;
      }
      getBookRecordsCount(filterParams).then((response) => {
        if (response.data.success) {
          this.recordFilteredNumber = response.data.filtered_total;
          this.recordTotalNumber = response.data.total;
        } else {
          console.error(response.data);
        }
      });
    },

    goToEnregistrementComplet(event) {
      this.$router.push(`/catalogue/lire/${event.item.id}`);
    },

    refreshTable() {
      this.$refs.myTable?.refresh();
    },

    onSortChange() {
      this.currentPage = 1;
      this.sortDesc = false;
      this.reloadWithFilters();
      this.refreshTable();
    },

    reloadWithFilters() {
      const query = {};
      if (this.authorFilter) query.author = encodeURIComponent(this.authorFilter);
      if (this.coteFilter)   query.cote   = encodeURIComponent(this.coteFilter);
      if (this.keywordsFilter) query.keywords = encodeURIComponent(this.keywordsFilter);
      if (this.titleFilter)  query.title  = encodeURIComponent(this.titleFilter);
      if (this.currentPage > 1) query.page = this.currentPage;
      query.sortBy   = this.sortBy;
      query.sortDesc = this.sortDesc;

      this.$router.replace({ query }).catch(err => {
        if (err.name !== 'NavigationDuplicated'
            && !err.message.includes('Avoided redundant navigation')) {
          throw err;
        }
      });
    },

    exportSearchResult() {
      this.isExporting = true;
      const filterParams = this.getFilterParams();
      exportBookRecordsWithReference(filterParams).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute(
            'download',
            `catalogue_export-${new Date().toISOString().slice(0, 19).replace(/[:-]/g, '')}.xlsx`
        );
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }).catch((error) => {
        console.error('Export failed:', error);
      }).finally(() => {
        this.isExporting = false;
      });
    },

    clearSearchFields() {
      this.prefixCoteFiler  = "";
      this.numberCoteFilter = "";
      this.authorFilter     = "";
      this.keywordsFilter   = "";
      this.titleFilter      = "";
      this.anneeObtentionMode    = "";
      this.anneeObtentionYear    = "";
      this.anneeObtentionYearMin = "";
      this.anneeObtentionYearMax = "";
      this.dateModifMode = "";
      this.dateModif     = null;
      this.dateModifMin  = null;
      this.dateModifMax  = null;
      this.$router.replace({ query: {} });
    },

    updatePrefixCoteFilter(event) {
      this.prefixCoteFiler = event;
    },

    onlyDigitsKeydown(e) {
      if (e.ctrlKey || e.metaKey) return;
      const allowed = [
        'Backspace', 'Tab', 'Enter',
        'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
        'Delete', 'Home', 'End'
      ];
      if (allowed.includes(e.key)) return;
      if (/^\d$/.test(e.key)) return;
      e.preventDefault();
    },

    sanitizeDigitsPaste(e) {
      const raw    = (e.clipboardData || window.clipboardData).getData('text') || '';
      const digits = raw.replace(/\D/g, '').slice(0, 4);
      e.target.value       = digits;
      this.numberCoteFilter = digits;
    },

    stripNonDigits(e) {
      const cleaned = String(e.target.value || '').replace(/\D/g, '').slice(0, 4);
      if (cleaned !== e.target.value) {
        e.target.value = cleaned;
      }
      this.numberCoteFilter = cleaned;
    }
  },

  mounted() {
    const q = this.$route.query;

    if (q.cote && q.cote.length > 0) {
      const cote = decodeURIComponent(q.cote);
      const parts = cote.split(' ');
      if (parts.length === 2) {
        this.prefixCoteFiler  = parts[0];
        this.numberCoteFilter = parts[1];
      }
    }
    if (q.title    && q.title.length > 0)    this.titleFilter    = decodeURIComponent(q.title);
    if (q.author   && q.author.length > 0)   this.authorFilter   = decodeURIComponent(q.author);
    if (q.keywords && q.keywords.length > 0) this.keywordsFilter = decodeURIComponent(q.keywords);
    if (q.page)    this.currentPage = parseInt(q.page);
    if (q.sortBy)  this.sortBy      = q.sortBy;
    if (q.sortDesc !== undefined) this.sortDesc = q.sortDesc === 'true';

    this.getRecordTotalNumber();
    this.$nextTick(() => {
      this.isMounted = true;
    });
  },

  watch: {
    coteFilter() {
      this.getRecordTotalNumber();
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    authorFilter() {
      this.getRecordTotalNumber();
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    keywordsFilter() {
      this.getRecordTotalNumber();
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    titleFilter() {
      this.getRecordTotalNumber();
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    anneeObtentionMode() {
      this.onFilterChanged();
    },
    anneeObtentionYear() {
      this.onFilterChanged();
    },
    anneeObtentionYearMin() {
      this.onFilterChanged();
    },
    anneeObtentionYearMax() {
      this.onFilterChanged();
    },
    dateModifMode() {
      this.onFilterChanged();
    },
    dateModif() {
      this.onFilterChanged();
    },
    dateModifMin() {
      this.onFilterChanged();
    },
    dateModifMax() {
      this.onFilterChanged();
    },
    currentPage() {
      this.refreshTable();
    },
    sortBy() {
      this.refreshTable();
    },
    sortDesc() {
      this.refreshTable();
    }
  }
}
</script>

<style scoped>
</style>