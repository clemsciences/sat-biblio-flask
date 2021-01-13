<template>
  <div>
    <h2>Liste des auteurs</h2>
      <p>Double-cliquez sur la ligne pour voir les détails.</p>
    <b-form-group label="Filtre prénom">
      <b-input type="search" v-model="firstNameFiltre"/>
    </b-form-group>
    <b-form-group label="Filtre nom de famille">
      <b-input type="search" v-model="familyNameFiltre"/>
    </b-form-group>
    <b-pagination
      v-model="currentPage"
      :total-rows="authorTotalNumber"
      :per-page="perPage"
      aria-controls="my-table"
    ></b-pagination>
    <b-table striped bordered hover :items="retrieveAuthors" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             :sort-by="sortBy" @row-dblclicked="goToAuthor" :filter="onFilter">
      <template #table-caption>La liste des auteurs dans la base.</template>
    </b-table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ListeAuteur",
  data: function () {
    return {
      authors: [],
      currentPage: 1,
      perPage: 50,
      sortBy: "family_name",
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
      const params = "?page="+ctx.currentPage+
          "&size="+ctx.perPage+
          "&sortBy="+ctx.sortBy;

      let filterParams = "";
      if(this.firstNameFiltre.length > 0) {
        filterParams = filterParams+"&first_name="+this.firstNameFiltre;
      }
      if(this.familyNameFiltre.length > 0) {
        filterParams = filterParams+"&family_name="+this.familyNameFiltre;
      }

      // console.log("bizarre ?");
      let url = "/api/auteur/liste"+params;
      if(filterParams.length > 0) {
        url = url + filterParams;
      }
      axios.get(url).then(
          (response) => {
            if(response.data.success) {
              this.authors = response.data.authors;
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
      let url = "/api/auteur/nombre";
      if(filterParams.length > 0) {
        url = url + "?" + filterParams;
      }
      axios.get(url).then(
          (response) => {
            if(response.data.success) {
              this.authorTotalNumber = response.data.number;
            }
          }
      )
    },
    goToAuthor: function(item) {
      this.$router.push('/auteur/lire/'+item.id);
    }
  },
  mounted() {
    this.getAuthorTotalNumber();
  },
  watch: {
    firstNameFiltre: function () {
      this.getAuthorTotalNumber();
    },
    familyNameFiltre: function () {
      this.getAuthorTotalNumber();
    }
  },
  computed: {
    onFilter: function() {
      return this.firstNameFiltre+" "+this.familyNameFiltre;
    }
  }
}
</script>

<style scoped>

</style>