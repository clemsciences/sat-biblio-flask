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
          <b-input v-model="coteFiltre" size="sm"
                   placeholder="Filtrer en fonction de la cote"/>
        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="Mots-clef" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input v-model="motClefFiltre" size="sm"
                   placeholder="Filtrer en fonction d'un mot clef"/>
        </b-form-group>
      </b-col>
      <b-col lg="4">
        <b-form-group label="Titre" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <b-input v-model="titreFiltre" size="sm"
                   placeholder="Filtrer en fonction du titre"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
    <b-pagination
        v-model="currentPage"
        :total-rows="recordTotalNumber"
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
      enregistrements: [],
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
          key: "annee",
          label: "Année d'obtention",
          sortable: false
        },
        {
          key: "nb_exemplaire_supp",
          label: "N° d'exemplaires supplémentaires",
          sortable: false
        },
        {
          key: "provenance",
          label: "Provenance",
          sortable: false
        },
        {
          key: "mots_clef",
          label: "Mots-clef",
          sortable: false
        },
      ],
      coteFiltre: "",
      motClefFiltre: "",
      titreFiltre: ""
    }
  },
  methods: {
    retrieveEnregistrementList: function (ctx, callback) {
      const params = "?page="+ctx.currentPage+
          "&size="+ctx.perPage+
          "&sortBy="+ctx.sortBy;
      let filterParams = "";
      if(this.coteFiltre.length > 0) {
        filterParams = filterParams+"&cote="+this.coteFiltre;
      }
      if(this.titreFiltre.length > 0) {
        filterParams = filterParams+"&titre="+this.titreFiltre;
      }
      if(this.motClefFiltre.length > 0) {
        filterParams = filterParams+"&mot_clef="+this.motClefFiltre;
      }
      retrieveBookRecords(params+filterParams)
          .then(
              (response) => {
                if(response.data.success) {
                  this.enregistrements = response.data.enregistrements;
                  callback(this.enregistrements);
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
      if(this.coteFiltre.length > 0) {
        filterParams = filterParams+"&cote="+encodeURI(this.coteFiltre);
      }
      if(this.titreFiltre.length > 0) {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams+"titre="+encodeURI(this.titreFiltre);
      }
      if(this.motClefFiltre.length > 0) {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams+"mot_clef="+encodeURI(this.motClefFiltre);
      }

      getBookRecordsCount(filterParams).then(
          (response) => {
            if(response.data.success) {
              this.recordFilteredNumber = response.data.filtered_number;
              this.recordTotalNumber = response.data.total;
            }
          }
      );
    },
    goToEnregistrement: function(item) {
      this.$router.push(`/enregistrement/lire/${item.id}`);
    },
  },
  mounted() {
    this.getRecordTotalNumber();
  },
  watch: {
    coteFiltre: function () {
      this.getRecordTotalNumber();
      this.currentPage = 1;
    },
    motClefFiltre: function () {
      this.getRecordTotalNumber();
      this.currentPage = 1;
    },
    titreFiltre: function () {
      this.getRecordTotalNumber();
      this.currentPage = 1;
    }
  },
  computed: {
    onFilter() {
      return `${this.coteFiltre} ${this.titreFiltre} ${this.motClefFiltre}`;
    }
  }
}
</script>

<style scoped>

</style>