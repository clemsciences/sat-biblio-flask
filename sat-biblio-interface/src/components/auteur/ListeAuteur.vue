<template>
  <BContainer>
    <AppTitle title="Liste des auteurs"
       info=""
       id="id-liste-auteurs"/>
    <p>Double-cliquez sur la ligne pour voir les détails.</p>
    <BRow class="my-1">
      <BCol lg="4">
        <BFormGroup label="Prénom" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput type="search" v-model="firstNameFilter" size="sm"
                      placeholder="Filtrer en fonction du prénom"/>
        </BFormGroup>
      </BCol>
      <BCol lg="4">
        <BFormGroup label="Nom de famille" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput type="search" v-model="familyNameFilter" size="sm"
                      placeholder="Filtrer en fonction du nom de famille"/>
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
    <BRow>
      <BPagination
        v-model="currentPage"
        :total-rows="authorFilteredNumber"
        :per-page="perPage"
        aria-controls="authorTable"
        />
      <FilterCount :filtered-item-count="authorFilteredNumber" :total-item-count="authorTotalNumber"/>
    </BRow>
    <BTable striped bordered hover
            :provider="retrieveAuthors"
            :fields="fields"
            ref="authorTable"
            primary-key="id"
            :per-page="perPage"
            :current-page="currentPage"
            :sort-by="tableSortBy"
            @row-dblclicked="goToAuthor">
      <template #table-caption>La liste des auteurs dans la base.</template>
    </BTable>
    <BRow>
      <BPagination
        v-model="currentPage"
        :total-rows="authorFilteredNumber"
        :per-page="perPage"
        aria-controls="authorTable" />
      <FilterCount :filtered-item-count="authorFilteredNumber" :total-item-count="authorTotalNumber"/>
    </BRow>
  </BContainer>
</template>

<script>
import {getAuthorsCount, retrieveAuthors} from "@/services/api.js";
import AppTitle from "@/components/visuel/AppTitle.vue";
import FilterCount from "@/components/visuel/FilterCount.vue";
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
  name: "ListeAuteur",
  components: {BButton, BContainer, BRow, BPagination, BCol,
    BFormGroup, BFormInput, BTable, AppTitle, FilterCount
  },
  data() {
    return {
      isMounted: false,
      currentPage: 1,
      perPage: 50,
      sortBy: "family_name",
      authorFilteredNumber: 0,
      authorTotalNumber: 0,
      fields: [
        {
          key: 'first_name',
          label: 'Prénom',
          sortable: false
        },
        {
          key: 'family_name',
          label: 'Nom de famille',
          sortable: false
        }
      ],
      firstNameFilter: '',
      familyNameFilter: '',
    }
  },
  methods: {
    // region filtering
    getFilterParams() {
      let filterparams = "";
      if(this.firstNameFilter.length > 0) {
        filterparams = filterparams+"&first_name="+this.firstNameFilter;
      }
      if(this.familyNameFilter.length > 0) {
        filterparams = filterparams+"&family_name="+this.familyNameFilter;
      }
      return filterparams;
    },
    refreshTable() {
      this.$refs.authorTable?.refresh();
    },
    reloadWithFilters() {
      this.refreshTable();
      // if (this.searchFieldsUsed) {
      //   this.$router.replace({
      //     query: {
      //       firstName: encodeURIComponent(this.firstNameFilter),
      //       familyName: encodeURIComponent(this.familyNameFilter),
      //     }
      //   });
      // }
    },
    clearSearchFields() {
      this.firstNameFilter = "";
      this.familyNameFilter = "";
      localStorage.clear();
      this.$router.replace({
        query: {}
      });

    },
    // endregion
    async retrieveAuthors(ctx) {
      const sortEntry = Array.isArray(ctx.sortBy) && ctx.sortBy.length > 0
          ? ctx.sortBy[0]
          : { key: this.sortBy, order: 'asc' };

      const sortKey = sortEntry.key || this.sortBy;
      let params = `?page=${this.currentPage}&size=${this.perPage}&sortBy=${sortKey}`;
      const filterParams = this.getFilterParams();

      if(filterParams.length > 0) {
        params += filterParams;
      }
      try {
        const response = await retrieveAuthors(params);
        if (response.data.success) {
          this.authors = response.data.authors ?? [];
          this.authorFilteredNumber = response.data.filtered_total ?? this.authors.length;
          this.authorTotalNumber = response.data.total ?? this.authors.length;
          // if(this.authorTotalNumber< (this.currentPage-1)*ctx.perPage) {
          //   this.currentPage = 1;
          // }
          return this.authors
        }
      } catch (reason) {
        console.log(reason);
        this.authorTotalNumber = 0;
        this.authorFilteredNumber = 0;
        return [];
      }
      this.authorTotalNumber = 0;
      this.authorFilteredNumber = 0;
      return [];
    },
    getAuthorTotalNumber: function() {
      let filterParams = "";
      if(this.firstNameFilter.length > 0) {

        filterParams = filterParams + "first_name=" + encodeURI(this.firstNameFilter);
      }
      if(this.familyNameFilter.length > 0) {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams + "family_name="+encodeURI(this.familyNameFilter);
      }
      if(filterParams.length > 0) {
        filterParams = "?" + filterParams;
      }
      getAuthorsCount(filterParams).then(
          (response) => {
            if(response.data.success) {
              this.authorFilteredNumber = response.data.filtered_total;
              this.authorTotalNumber = response.data.total;
            }
          }
      )
    },
    goToAuthor: function(event) {
      this.$router.push(`/auteur/lire/${event.item.id}`);
    },

  },
  //beforeMount() {
  //  this.getAuthorTotalNumber();
  //},
  mounted() {
    const query = this.$route.query;
    if(query.firstName && query.firstName.length > 0) {
      this.firstNameFilter = decodeURIComponent(query.firstName);
    }
    if(query.familyName && query.familyName.length > 0) {
      this.familyNameFilter = decodeURIComponent(query.familyName);
    }
    this.$nextTick(() => {
      this.isMounted = true;
    });
  },
  watch: {
    firstNameFilter: function (newValue, oldValue) {
      if(newValue !== oldValue) {
        //this.getAuthorTotalNumber();
        if (this.isMounted) this.currentPage = 1;
        this.reloadWithFilters();
      }
    },
    familyNameFilter: function () {
      //this.getAuthorTotalNumber();
      if (this.isMounted) this.currentPage = 1;
      this.reloadWithFilters();
    },
    currentPage() {
      this.refreshTable();
    }
  },
  computed: {
    tableSortBy() {
      return [{ key: this.sortBy, order: this.sortDesc ? 'desc' : 'asc' }];
    },
    searchFieldsUsed() {
      return this.firstNameFilter.length > 0 || this.familyNameFilter.length > 0;
    }
  }
}
</script>

<style scoped>

</style>