<template>
  <b-container>
    <Title info="Le catalogue est la liste des enregistrements dans la bibliothèque."
    id="id-catalogue">
      Catalogue
    </Title>
    <p>Double-cliquez sur la ligne pour voir les détails.</p>
    <b-row class="my-1">
      <b-col lg="4">
        <b-form-group label="Cote" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input v-model="coteFilter" size="sm"
                   placeholder="Filtrer en fonction de la cote"/>
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

    <b-table striped bordered hover :items="retrieveEnregistrementList" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             :sort-by="sortBy" @row-dblclicked="goToEnregistrement" :filter="onFilter">
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
import {getBookRecordsCount, retrieveBookRecords} from "@/services/api";
import Title from "../visuel/Title";
import FilterCount from "@/components/visuel/FilterCount";

export default {
  name: "ListeEnregistrement",
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
        }
      ],
      coteFilter: "",
      keywordsFilter: "",
      titleFilter: "",
      noChangeIn: 0,
    }
  },
  methods: {
    retrieveEnregistrementList: function (ctx, callback) {
      const params = "?page="+ctx.currentPage+
          "&size="+ctx.perPage+
          "&sortBy="+ctx.sortBy;
      let filterParams = "";
      if(this.coteFilter.length > 0) {
        filterParams = filterParams+"&cote="+this.coteFilter;
      }
      if(this.titleFilter.length > 0) {
        filterParams = filterParams+"&titre="+this.titleFilter;
      }
      if(this.keywordsFilter.length > 0) {
        filterParams = filterParams+"&mot_clef="+this.keywordsFilter;
      }
      retrieveBookRecords(params+filterParams)
          .then(
              (response) => {
                if(response.data.success) {
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
    getRecordTotalNumber: function() {
      let filterParams = "?result_type=number";
      if(this.coteFilter.length > 0) {
        filterParams = filterParams+"&cote="+encodeURI(this.coteFilter);
      }
      if(this.titleFilter.length > 0) {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams+"titre="+encodeURI(this.titleFilter);
      }
      if(this.keywordsFilter.length > 0) {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams+"mot_clef="+encodeURI(this.keywordsFilter);
      }

      getBookRecordsCount(filterParams).then(
          (response) => {
            if(response.data.success) {
              this.recordFilteredNumber = response.data.filtered_total;
              this.recordTotalNumber = response.data.total;
            }
          }
      );
    },
    goToEnregistrement: function(item) {
      this.$router.push(`/enregistrement/lire/${item.id}`);
    },
    // reloadWithFilters() {
    //   this.$router.push({
    //       name: "",
    //       query: {
    //         cote: encodeURIComponent(this.coteFilter),
    //         keyWords: encodeURIComponent(this.keywordsFilter),
    //         title: encodeURIComponent(this.titleFilter),
    //       }
    //   }).then(() => {
    //     window.location.reload();
    //   });
    // }
  },
  mounted() {
    // if(this.$route.query.coteFilter.length > 0) {
    //   this.coteFilter = decodeURIComponent(this.$route.query.coteFilter);
    // }
    // if(this.$route.query.titleFilter.length > 0) {
    //   this.coteFilter = decodeURIComponent(this.$route.query.coteFilter);
    // }
    // if(this.$route.query.keywordsFilter.length > 0) {
    //   this.coteFilter = decodeURIComponent(this.$route.query.coteFilter);
    // }
    this.getRecordTotalNumber();
  },
  watch: {
    coteFilter: function () {
      this.getRecordTotalNumber();
      this.currentPage = 1;
      // this.reloadWithFilters();
    },
    keywordsFilter: function () {
      this.getRecordTotalNumber();
      this.currentPage = 1;
      // this.reloadWithFilters();
    },
    titleFilter: function () {
      this.getRecordTotalNumber();
      this.currentPage = 1;
      // this.reloadWithFilters();
    }
  },
  computed: {
    onFilter() {
      // if(this.noChangeIn > 2000) {
      // }

      return `${this.coteFilter} ${this.titleFilter} ${this.keywordsFilter}`;
    }
  }
}
</script>

<style scoped>

</style>