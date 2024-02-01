<template>
  <b-container>
    <Title title="Liste des auteurs"
       info=""
       id="id-liste-auteurs"/>
    <p>Double-cliquez sur la ligne pour voir les détails.</p>
    <b-row class="my-1">
      <b-col lg="4">
        <b-form-group label="Prénom" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input type="search" v-model="firstNameFiltre" size="sm"
                   placeholder="Filtrer en fonction du prénom"/>
        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="Nom de famille" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input type="search" v-model="familyNameFiltre" size="sm"
                   placeholder="Filtrer en fonction du nom de famille"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-pagination
        v-model="currentPage"
        :total-rows="authorTotalNumber"
        :per-page="perPage"
        aria-controls="my-table" />
      <filter-count :filtered-item-count="authorFilteredNumber" :total-item-count="authorTotalNumber"/>
    </b-row>
    <b-table striped bordered hover :items="retrieveAuthors" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             :sort-by="sortBy" @row-dblclicked="goToAuthor" :filter="onFilter">
      <template #table-caption>La liste des auteurs dans la base.</template>
    </b-table>
    <b-row>
      <b-pagination
        v-model="currentPage"
        :total-rows="authorTotalNumber"
        :per-page="perPage"
        aria-controls="my-table" />
      <filter-count :filtered-item-count="authorFilteredNumber" :total-item-count="authorTotalNumber"/>
    </b-row>
  </b-container>
</template>

<script>

import {getAuthorsCount, retrieveAuthors} from "@/services/api";
import Title from "@/components/visuel/Title";
import FilterCount from "@/components/visuel/FilterCount";

export default {
  name: "ListeAuteur",
  components: {Title, FilterCount},
  data: function () {
    return {
      authors: [],
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
      firstNameFiltre: '',
      familyNameFiltre: ''
    }
  },
  methods: {
    retrieveAuthors: function(ctx, callback) {
      let params = "?page="+ctx.currentPage+
          "&size="+ctx.perPage+
          "&sortBy="+ctx.sortBy;

      let filterParams = "";
      if(this.firstNameFiltre.length > 0) {
        filterParams = filterParams+"&first_name="+this.firstNameFiltre;
      }
      if(this.familyNameFiltre.length > 0) {
        filterParams = filterParams+"&family_name="+this.familyNameFiltre;
      }

      if(filterParams.length > 0) {
        params = params + filterParams;
      }
      retrieveAuthors(params).then(
          (response) => {
            if(response.data.success) {
              this.authors = response.data.authors;
              // if(this.authorTotalNumber< (this.currentPage-1)*ctx.perPage) {
              //   this.currentPage = 1;
              // }
              callback(this.authors);
            }
          }
      ).catch(
          (reason) => {
            console.log(reason);
            callback([]);
          }
      );
      return null;
    },
    getAuthorTotalNumber: function() {
      let filterParams = "";
      if(this.firstNameFiltre.length > 0) {

        filterParams = filterParams + "first_name=" + encodeURI(this.firstNameFiltre);
      }
      if(this.familyNameFiltre.length > 0) {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams + "family_name="+encodeURI(this.familyNameFiltre);
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
    goToAuthor: function(item) {
      this.$router.push(`/auteur/lire/${item.id}`);
    }
  },
  mounted() {
    this.getAuthorTotalNumber();
  },
  watch: {
    firstNameFiltre: function (newValue, oldValue) {
      if(newValue !== oldValue) {
        this.getAuthorTotalNumber();
        this.currentPage = 1;
      }
    },
    familyNameFiltre: function () {
      this.getAuthorTotalNumber();
      this.currentPage = 1
    }
  },
  computed: {
    onFilter: function() {
      return `${this.firstNameFiltre} ${this.familyNameFiltre}`;
    }
  }
}
</script>

<style scoped>

</style>