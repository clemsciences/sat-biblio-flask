<template>
  <b-container>
    <Title title="Liste des références"
           info=""
           id="id-liste-ref"/>
    <p>Double-cliquez sur la ligne pour voir les détails.</p>
    <b-row class="my-3">
      <b-col lg="4">
        <b-form-group label="Titre" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input v-model="titreFiltre" placeholder="Filtrer en fonction du titre"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-pagination
      v-model="currentPage"
      :total-rows="refTotalNumber"
      :per-page="perPage"
      aria-controls="my-table"
      class="my-3"/>
    <b-table striped bordered hover :items="retrieveRef" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             :sort-by="sortBy" @row-dblclicked="goToReference" :filter="onFilter">
      <template #table-caption>La liste des références bibliographiques dans la base.</template>
    </b-table>
  </b-container>
</template>

<script>
import {getBookReferencesCount, retrieveBookReferences} from "@/services/api";
import Title from "@/components/visuel/Title";

export default {
  name: "ListeReferenceLivre",
  components: {Title},
  data: function () {
    return {
      references: [],
      currentPage: 1,
      perPage: 50,
      sortBy: "titre",
      refTotalNumber: 0,
      fields: [
        {
          key: "authors",
          label: "Auteurs",
          sortable: false
        },
        {
          key: "titre",
          label: "Titre",
          sortable: false
        },
        {
          key: "lieu_edition",
          label: "Lieu d'édition",
          sortable: false
        },
        {
          key: "editeur",
          label: "Editeur",
          sortable: false
        },
        {
          key: "annee",
          label: "Année",
          sortable: false
        },
        {
          key: "nb_page",
          label: "N° pages",
          sortable: false
        },
      ],
      titreFiltre: ""
    }
  },
  methods: {
    retrieveRef: function (ctx, callback) {
      const params = "?page="+ctx.currentPage+
          "&size="+ctx.perPage+
          "&sortBy="+ctx.sortBy;
      let filterParams = "";
      if(this.titreFiltre.length > 0) {
        filterParams = filterParams+"&titre="+encodeURI(this.titreFiltre);
      }
      retrieveBookReferences(params+filterParams).then(
          (response) => {
            if(response.data.success) {
              // this.currentPage = 1;
              this.references = response.data.references;
              callback(this.references);
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
    getRefTotalNumber: function() {
      let filterParams = "";

      if(this.titreFiltre.length > 0) {
        filterParams = filterParams+"?titre="+encodeURI(this.titreFiltre);
      }
      getBookReferencesCount(filterParams).then(
          (response) => {
            if(response.data.success) {
              this.refTotalNumber = response.data.total;
            }
          }
      )
    },
    goToReference: function (item) {
      this.$router.push(`/reference-livre/lire/${item.id}`);
    }
  },
  mounted() {
    this.getRefTotalNumber();
  },
  watch: {
    titreFiltre: function () {
      this.getRefTotalNumber();
      this.currentPage = 1;
    },
  },
  computed: {
    onFilter() {
      return this.titreFiltre;
    }
  }
}
</script>

<style scoped>

</style>