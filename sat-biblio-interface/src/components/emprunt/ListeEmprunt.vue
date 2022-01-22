<template>
  <b-container>
    <h2>Liste d'emprunts</h2>
    <p>Double-cliquez sur la ligne pour voir les détails sur un emprunt.</p>
    <b-row class="my-1">
      <b-col lg="4">
        <b-form-group label="Prénom" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input type="search" v-model="firstNameFiltre"
                   placeholder="Filtrer en fonction du prénom"/>

        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="Nom de famille" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input type="search" v-model="familyNameFiltre"
                   placeholder="Filtrer en fonction du nom de famille"/>
        </b-form-group>
      </b-col>
    </b-row>

    <b-pagination v-model="currentPage"
      :total-rows="borrowingTotalNumber"
      :per-page="perPage"
      aria-controls="my-table"/>

    <b-table striped bordered hover :items="retrieveBorrowings" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             :sort-by="sortBy" @row-dblclicked="goToBorrowing" :filter="onFilter">
      <template #table-caption>La liste des emprunts dans la base.</template>
    </b-table>
<!--    <b-list-group>-->
<!--      <b-list-group-item :key="borrow.id" v-for="borrow in borrows">-->
<!--        <router-link :to="">Voir</router-link>-->
<!--        {{ borrow.emprunteur }}-->
<!--        {{ borrow.enregistrement }}-->
<!--        {{ borrow.commentaire }}-->
<!--        {{ borrow.gestionnaire }}-->
<!--        {{ borrow.emprunte }}-->
<!--        {{ borrow.date_retour_prevu }}-->
<!--        {{ borrow.date_retour_reel }}-->
<!--        {{ borrow.rendu }}-->
<!--      </b-list-group-item>-->
<!--    </b-list-group>-->
  </b-container>
</template>

<script>

import {getBorrowingsCount, retrieveBorrowings} from "@/services/api";

export default {
  name: "ListeEmprunt",
  data: function () {
    return {
      borrowings: [],
      currentPage: 1,
      perPage: 10,
      sortBy: "",
      borrowingTotalNumber: 0,
      firstNameFiltre: "",
      familyNameFiltre: "",
      fields: [
        {
          key: "",
          label: "",
          sortable: false
        },
      ]
    }
  },
  methods: {
    retrieveBorrowings: function(ctx, callback) {
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
      retrieveBorrowings(params)
          .then(
              (response) => {
                if(response.data.success) {
                  this.currentPage = 1;
                  this.borrowings = response.data.borrowings;
                  callback(this.borrowings);
                }
              }
          ).catch(
          (reason) => {
            console.log(reason)
            callback([]);
          }
      );
      return null;
    },
    getBorrowingsTotalNumber: function() {
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
      getBorrowingsCount(filterParams).then(
          (response) => {
            if(response.data.success) {
              this.borrowingTotalNumber = response.data.total;
            }
          }
      )
    },
    goToBorrowing: function(item) {
      console.log(item);
      this.$router.push(`/emprunt/${item.id}`)
    }
  },
  mounted() {
    this.getBorrowingsTotalNumber();
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