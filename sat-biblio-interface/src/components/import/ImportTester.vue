<template>
  <b-container>
    <b-row>
      <b-col cols="8">
        <b-pagination
          v-model="currentPage"
          :total-rows="rowTotalNumber"
          :per-page="perPage"
          aria-controls="my-table"/>
        <b-table striped bordered hover :items="loadRows" :fields="fields"
                 primary-key="id" :per-page="perPage" :current-page="currentPage"
                 @row-dblclicked="showRowProcessing">
          <template #table-caption>La liste des entrées dans la base actuelle.</template>
        </b-table>
      </b-col>
      <b-col cols="4">
        <AuteurFormulaire v-for="author in authors"
                          :key="`${author.first_name}_${author.family_name}`"
                          :auteur="author"
                          :on-submit="saveAuthor"/>
        <ReferenceLivreFormulaire :on-submit="saveReference" :reference="reference"/>
        <EnregistrementFormulaire :on-submit="saveRecord" :record="record"/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";
import AuteurFormulaire from "@/components/auteur/AuteurFormulaire";
import ReferenceLivreFormulaire from "@/components/reference_livre/ReferenceLivreFormulaire";
import EnregistrementFormulaire from "@/components/enregistrement/EnregistrementFormulaire";
import {Author, BookReference, Record} from "@/services/objectManager";

export default {
  name: "ImportTester",
  components: {
    EnregistrementFormulaire,
    ReferenceLivreFormulaire,
    AuteurFormulaire
  },
  data: function() {
    return {
      rows: [],
      currentPage: 1,
      perPage: 10,
      rowTotalNumber: 0,
      result: '',
      authorsResult: '',
      refResult: '',
      authors: [new Author()],
      reference: new BookReference(),
      record: new Record(),
      fields: [
        {
          key: 'description',
          label: 'Description',
          sortable: false,
          colspan: 4
        },
        {
          key: 'cote',
          label: 'Cote',
          sortable: false,
          colspan: 1
        },
        // {
        //   key: 'nb_supp',
        //   label: 'Nombre supplémentaire',
        //   sortable: false,
        //   colspan: 1
        // },
        {
          key: 'annee',
          label: 'Année',
          sortable: false,
          colspan: 1
        },
        {
          key: 'provenance',
          label: 'Provenance',
          sortable: false,
          colspan: 1
        },
        // {
        //   key: 'theme1',
        //   label: 'Thème 1',
        //   colspan: 1
        // },
        // {
        //   key: 'theme2',
        //   label: 'Thème 2',
        //   colspan: 1
        // },
        // {
        //   key: 'theme3',
        //   label: 'Thème 3',
        //   colspan: 1
        // }
      ],
    }
  },
  methods: {
    loadRows: function (ctx, callback) {
      let params = `page=${ctx.currentPage}&size=${ctx.perPage}&sortBy=${ctx.sortBy}`;
      axios.get(`/import-csv/?${params}`).then(
          response => {
            this.rows = response.data.rows;
            callback(this.rows);

          }
      ).catch(
          () => {
            callback([]);
          }
      );
      return null;
    },
    getRowTotalNumber: function() {
      axios.get("/import-csv/count/").then(
          response => {
            if(response.data.success) {
              this.rowTotalNumber = response.data.total;
            }
          }
      );
    },
    showRowProcessing: function (event) {
      // console.log(event);
      axios.get(`/import-csv/rows/${event.index}`).then(
          response => {
            this.result = response.data.data;
            this.refResult = response.data.ref;
            this.authorsResult = response.data.authors;
            this.authors = response.data.ref.authors;
            this.reference = response.data.ref;
            this.record = response.data.record;
            console.log(response.data.record);
          }
      );
    },

    saveAuthor: function() {

    },
    saveReference: function() {

    },
    saveRecord: function () {

    }
  },
  mounted() {
    this.getRowTotalNumber();
  }
}
</script>

<style scoped>

</style>