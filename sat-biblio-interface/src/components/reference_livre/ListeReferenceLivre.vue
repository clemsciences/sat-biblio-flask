<template>
  <BContainer>
    <AppTitle title="Liste des références"
           info=""
           id="id-liste-ref"/>
    <p>Double-cliquez sur la ligne pour voir les détails.</p>
    <BRow class="my-3">
      <BCol lg="4">
        <BFormGroup label="Titre" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput v-model="titreFiltre" size="sm"
                   placeholder="Filtrer en fonction du titre"/>
        </BFormGroup>
      </BCol>
    </BRow>
    <BRow>
    <BPagination
      v-model="currentPage"
      :total-rows="refFilteredNumber"
      :per-page="perPage"
      aria-controls="my-table"
      class="my-3"/>
      <FilterCount :filtered-item-count="refFilteredNumber" :total-item-count="refTotalNumber"/>
    </BRow>
    <BTable striped bordered hover :items="retrieveRef" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             :sort-by="sortBy" @row-dblclicked="goToReference" :filter="onFilter">
      <template #table-caption>La liste des références bibliographiques dans la base.</template>

      <template #cell(annee)="data">
        <div v-if="data.item.annee === 's. d.'">Inconnu</div><div v-else>{{ data.item.annee }}</div>
      </template>

      <template #cell(authors)="data">
        <div v-if="data.item.authors === '[collectif] (-)'">Collectif</div>
        <div v-else-if="data.item.authors === '[anonyme] (-)'">Anonyme</div>
        <div v-else>{{data.item.authors}}</div>
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
        <div v-if="data.item.nb_page === '-1' || data.item.nb_page === ''">Inconnu</div><div v-else>{{ data.item.nb_page }}</div>
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
import {getBookReferencesCount, retrieveBookReferences} from "@/services/api.js";
import AppTitle from "@/components/visuel/AppTitle.vue";
import FilterCount from "@/components/visuel/FilterCount.vue";

export default {
  name: "ListeReferenceLivre",
  components: {AppTitle, FilterCount},
  data: function () {
    return {
      references: [],
      currentPage: 1,
      perPage: 50,
      sortBy: "titre",
      refFilteredNumber: 0,
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
        {
          key: "description",
          label: "Description",
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
            console.error(reason);
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
              this.refFilteredNumber = response.data.filtered_total;
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