<template>
  <b-container>
    <Title info="Le catalogue est la liste des ouvrages dans la bibliothèque."
           id="id-catalogue">
      Catalogue
    </Title>
    <p>Double-cliquez sur la ligne pour voir les détails.</p>
    <b-row class="my-1">
      <b-col lg="4">
        <b-form-group label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <b-button v-b-modal.modal-cote class="d-inline-block">
            {{ prefixCoteFiler.length > 0 || numberCoteFilter.length > 0 ? coteFilter : 'Choisir une cote' }}
          </b-button>

          <b-modal id="modal-cote" title="Sélection de la cote"
                   ok-title="Valider" cancel-title="Annuler">
            <b-form-group label="Préfixe">
              <b-form-select
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
              </b-form-select>
            </b-form-group>
            <b-form-group label="Numéro">
              <b-form-input
                  v-model="numberCoteFilter"
                  type="text"
                  pattern="[0-9]*"
                  inputmode="numeric"
                  maxlength="4"
                  @keydown="onlyDigitsKeydown"
                  @paste.prevent="sanitizeDigitsPaste"
                  @input="stripNonDigits"
                  placeholder="Entrez un numéro">
              </b-form-input>
            </b-form-group>
          </b-modal>

          <template #label>
            Cote
            <b-icon icon="info-circle" v-b-tooltip.hover
                    title="La cote est le numéro permettant de localiser l'ouvrage dans la bibliothèque"
                    variant="dark"/>
          </template>
        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="Auteur" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <b-input v-model="authorFilter" size="sm"
                   placeholder="Filtrer en fonction de l'auteur"/>
        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="Aide à la recherche" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <b-input v-model="keywordsFilter" size="sm"
                   placeholder="Filtrer en fonction d'un mot clef"/>
        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="Titre" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <b-input v-model="titleFilter" size="sm"
                   placeholder="Filtrer en fonction du titre"/>
        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <b-button @click="exportSearchResult" :disabled="isExporting" v-b-tooltip.hover
                    title="Exporte un fichier Excel contenant les éléments du catalogue qui correspondent aux filtres. Si aucun filtre n'est mis, alors le catalogue entier est exporté.">
            {{ isExporting ? 'Export en cours...' : 'Exporter' }}
          </b-button>
          <template #label>
            <b-icon icon="info-circle" v-b-tooltip.hover
                    title="Exporte un fichier Excel contenant les éléments du catalogue qui correspondent aux filtres. Si aucune filtre n'est mis, alors le catalogue entier est exporté."
                    variant="dark"/>
          </template>
        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="" label-cols-sm="3"
                      label-align-sm="right" label-size="sm" class="mb-0">
          <b-button @click="clearSearchFields" :disabled="!searchFieldsUsed" v-b-tooltip.hover
                    title="Réinitialise les filtres de recherche.">
            Réinitialiser
          </b-button>
          <template #label>
            <b-icon icon="info-circle" v-b-tooltip.hover
                    title="Réinitialise les filtres de recherche."
                    variant="dark"/>
          </template>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-pagination
          v-model="currentPage"
          :total-rows="recordFilteredNumber"
          :per-page="perPage"
          aria-controls="my-table"
          class="my-3"/>
      <filter-count :filtered-item-count="recordFilteredNumber" :total-item-count="recordTotalNumber"/>
    </b-row>

    <b-table striped bordered hover :items="retrieveEnregistrementCompleteList" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             :sort-by="sortBy" @row-dblclicked="goToEnregistrementComplet" :filter="onFilter">
      <template #table-caption>La liste des références bibliographiques dans la base.</template>
    </b-table>

    <b-row>
      <b-pagination
          v-model="currentPage"
          :total-rows="recordFilteredNumber"
          :per-page="perPage"
          aria-controls="my-table"
          class="my-3"/>
      <filter-count :filtered-item-count="recordFilteredNumber" :total-item-count="recordTotalNumber"/>
    </b-row>
  </b-container>
</template>
<script>
import {exportBookRecordsWithReference, getBookRecordsCount, retrieveBookRecords} from "@/services/api";
import Title from "../visuel/Title";
import FilterCount from "@/components/visuel/FilterCount";

export default {
  name: "ListeEnregistrementComplet",
  components: {Title, FilterCount},
  data: function () {
    return {
      records: [],
      currentPage: 1,
      perPage: 50,
      sortBy: "cote",
      recordFilteredNumber: 0,
      recordTotalNumber: 0,
      fields: [
        {
          key: "cote",
          label: "Cote",
          sortable: false
        },
        {
          key: "reference",
          label: "Titre",
          sortable: false
        },
        {
          key: "authors",
          label: "Auteurs",
          sortable: false
        },
        /*{
          key: "description",
          label: "Description",
          sortable: false
        },*/
        {
          key: "annee_obtention",
          label: "Année d'obtention",
          sortable: false
        },
        // {
        //   key: "nb_exemplaire_supp",
        //   label: "N° d'exemplaires supplémentaires",
        //   sortable: false
        // },
        {
          key: "provenance",
          label: "Provenance",
          sortable: false
        },
        {
          key: "aide_a_la_recherche",
          label: "Aide à la recherche",
          sortable: false
        },
        {
          key: "observations",
          label: "Observations",
          sortable: false
        },

      ],
      prefixCoteFiler: "",
      numberCoteFilter: "",
      //coteFilter: "",
      authorFilter: "",
      keywordsFilter: "",
      titleFilter: "",
      noChangeIn: 0,
      isExporting: false,
    }
  },
  methods: {

    getFilterParams() {
      let filterParams = "";
      if (this.coteFilter.length > 0) {
        filterParams = `${filterParams}&cote=${encodeURI(this.coteFilter)}`;
      }
      // if(this.authorFilter.length > 0) {
      //   filterParams = `${filterParams}&author=${encodeURI(this.authorFilter)}`;
      // }
      if (this.authorFilter.length > 0) {
        if (filterParams.length > 0) {
          filterParams = `${filterParams}&`;
        }
        filterParams = `${filterParams}author=${encodeURI(this.authorFilter)}`;
      }
      // if(this.titleFilter.length > 0) {
      //   filterParams = `${filterParams}&titre=${encodeURI(this.titleFilter)}`;
      // }
      if (this.titleFilter.length > 0) {
        if (filterParams.length > 0) {
          filterParams = `${filterParams}&`;
        }
        filterParams = `${filterParams}titre=${encodeURI(this.titleFilter)}`;
      }
      // if(this.keywordsFilter.length > 0) {
      //   filterParams = `${filterParams}&mot_clef=${encodeURI(this.keywordsFilter)}`;
      // }
      if (this.keywordsFilter.length > 0) {
        if (filterParams.length > 0) {
          filterParams = `${filterParams}&`;
        }
        filterParams = `${filterParams}mot_clef=${encodeURI(this.keywordsFilter)}`;
      }
      return filterParams;
    },
    retrieveEnregistrementCompleteList: function (ctx, callback) {
      const params = "?page=" + ctx.currentPage +
          "&size=" + ctx.perPage +
          "&sortBy=" + ctx.sortBy;
      let filterParams = "";
      filterParams = this.getFilterParams();
      retrieveBookRecords(`${params}&${filterParams}`)
          .then(
              (response) => {
                if (response.data.success) {
                  this.records = response.data.enregistrements;
                  callback(this.records);
                }
              }
          ).catch(
          (reason) => {
            console.log(reason);
            callback([]);
          }
      );
    },
    getRecordTotalNumber: function () {
      let filterParams = "?result_type=number";
      filterParams = `${filterParams}&${this.getFilterParams()}`;

      getBookRecordsCount(filterParams).then(
          (response) => {
            if (response.data.success) {
              this.recordFilteredNumber = response.data.filtered_total;
              this.recordTotalNumber = response.data.total;
            } else {
              console.error(response.data);
            }
          }
      );
    },
    goToEnregistrementComplet: function (item) {
      this.$router.push(`/catalogue/lire/${item.id}`);
    },
    reloadWithFilters() {
      if (this.onFilter.trim().length > 0) {
        this.$router.replace({
          query: {
            author: encodeURIComponent(this.authorFilter),
            cote: encodeURIComponent(this.coteFilter),
            keywords: encodeURIComponent(this.keywordsFilter),
            title: encodeURIComponent(this.titleFilter),
          }
        });
      }
    },
    exportSearchResult() {
      this.isExporting = true;
      let filterParams = this.getFilterParams();

      exportBookRecordsWithReference(filterParams
      ).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `catalogue_export-${new Date().toISOString().slice(0, 19).replace(/[:-]/g, '')}.xlsx`);
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
      //this.coteFilter = "";
      this.prefixCoteFiler = "";
      this.numberCoteFilter = "";
      this.authorFilter = "";
      this.keywordsFilter = "";
      this.titleFilter = "";
      localStorage.clear();
      this.$router.replace({
        query: {}
      });
    },
    updatePrefixCoteFilter(event) {
      console.log("event: ", event);
      this.prefixCoteFiler = event;
    },
    // region only digits
    /** Allow only digits and necessary control/navigation keys
     *
     * @param e event
     */
    onlyDigitsKeydown(e) {
      // Allow shortcuts like Ctrl/Cmd+A/C/X/V/Z/Y
      if (e.ctrlKey || e.metaKey) return;
      const allowed = [
        'Backspace', 'Tab', 'Enter',
        'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
        'Delete', 'Home', 'End'
      ];
      if (allowed.includes(e.key)) return;
      // Allow digits 0-9 (top row and numpad)
      if (/^\d$/.test(e.key)) return;
      // Block everything else (e, E, +, -, ., etc.)
      e.preventDefault();
    },
    /** Clean pasted content to digits only (limit to 4 digits for 1..9999)
     *
     * @param e event
     */
    sanitizeDigitsPaste(e) {
      const raw = (e.clipboardData || window.clipboardData).getData('text') || '';
      const digits = raw.replace(/\D/g, '').slice(0, 4);
      e.target.value = digits;
      this.numberCoteFilter = digits;
    },

    /** Ensure input stays digits-only and within length limit even if injected
     *
     * @param e event
     */
    stripNonDigits(e) {
      const cleaned = String(e.target.value || '').replace(/\D/g, '').slice(0, 4);
      if (cleaned !== e.target.value) {
        e.target.value = cleaned;
      }
      this.numberCoteFilter = cleaned;
    }
    // endregion
  },

  mounted() {
    if (this.$route.query.cote.length > 0) {
      const cote = decodeURIComponent(this.$route.query.cote);
      const coteParts = cote.split(' ');
      if (coteParts.length === 2) {
        this.prefixCoteFiler = coteParts[0];
        this.numberCoteFilter = coteParts[1];
      }
    }
    if (this.$route.query.title.length > 0) {
      this.titleFilter = decodeURIComponent(this.$route.query.title);
    }
    if (this.$route.query.author.length > 0) {
      this.authorFilter = decodeURIComponent(this.$route.query.author);
    }
    if (this.$route.query.keywords.length > 0) {
      this.keywordsFilter = decodeURIComponent(this.$route.query.keywords);
    }
    this.getRecordTotalNumber();
  },
  watch: {
    coteFilter: function () {
      this.getRecordTotalNumber();
      this.currentPage = 1;
      this.reloadWithFilters();
    },
    authorFilter() {
      this.getRecordTotalNumber();
      this.currentPage = 1;
      this.reloadWithFilters();
    },
    keywordsFilter: function () {
      this.getRecordTotalNumber();
      this.currentPage = 1;
      this.reloadWithFilters();
    },
    titleFilter: function () {
      this.getRecordTotalNumber();
      this.currentPage = 1;
      this.reloadWithFilters();
    }
  },
  computed: {
    onFilter() {
      return `${this.coteFilter} ${this.titleFilter} ${this.keywordsFilter} ${this.authorFilter}`;
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
      return `${this.prefixCoteFiler} ${this.numberCoteFilter}`;
    },
    searchFieldsUsed() {
      return this.coteFilter.length > 0 || this.authorFilter.length > 0 || this.keywordsFilter.length > 0 || this.titleFilter.length > 0;
    }
  }
}
</script>
<style scoped>

</style>