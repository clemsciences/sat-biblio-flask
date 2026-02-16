<template>
    <BContainer>
    <AppTitle title="Liste des logs"
       info=""
       id="id-liste-logs"/>
    <BRow class="my-1">
      <BCol lg="4">
        <BFormGroup label="Nom de la table" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BFormInput type="search" v-model="tableNameFilter" size="sm"
                   placeholder="Filtrer en fonction du nom de la table"/>
        </BFormGroup>
      </BCol>
    </BRow>
    <BPagination
      v-model="currentPage"
      :total-rows="logEventsTotalNumber"
      :per-page="perPage"
      aria-controls="my-table"/>
    <BTable striped bordered hover :items="retrieveLogEvents" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             :sort-by="sortBy" @row-dblclicked="goToLogEvent" :filter="onFilter">
      <template #table-caption>La liste des événements dans la base.</template>
      <template #cell(values)="data">
        <vue-json-pretty :data="JSON.parse(data.item.values)"/>
      </template>
    </BTable>
  </BContainer>
</template>

<script>
import AppTitle from "@/components/visuel/AppTitle.vue";
import {getLogEventsCount, retrieveLogEvents} from "@/services/api.js";
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';

export default {
  name: "LogEventListView",

  components: {AppTitle, VueJsonPretty},
  data: function () {
    return {
      logEvents: [],
      currentPage: 1,
      perPage: 50,
      sortBy: "event_datetime",
      logEventsTotalNumber: 0,
      fields: [
        {
          key: 'event_type',
          label: "Type",
          sortable: false
        },
        {
          key: 'event_datetime',
          label: 'Date et heure',
          sortable: false,
          formatter: value => {
            let d = new Date(value);
            return new Intl.DateTimeFormat("fr-FR", {dateStyle: "short", timeStyle: "short"}).format(d)+" ("+d.getHours()+":"+d.getMinutes()+")";
          }
        },
        {
          key: "event_owner",
          label: "Utilisateur",
          sortable: false
        },
        {
          key: "table_name",
          label: "Nom de la table",
          sortable: false
        },
        {
          key: "values",
          label: "Nouvelle valeur",
          sortable: false,
          // formatter: value => {
          //   return JSON.parse(value);
          // }
        }
      ],
      tableNameFilter: ''
    }
  },
  methods: {
    retrieveLogEvents: function(ctx, callback) {
      let params = "?page="+ctx.currentPage+
          "&size="+ctx.perPage+
          "&sortBy="+ctx.sortBy;

      let filterParams = "";
      if(this.tableNameFilter.length > 0) {
        filterParams = filterParams+"&first_name="+this.firstNameFiltre;
      }

      if(filterParams.length > 0) {
        params = params + filterParams;
      }
      retrieveLogEvents(params).then(
          (response) => {
            if(response.data.success) {
              this.logEvents = response.data.log_events;
              // if(this.authorTotalNumber< (this.currentPage-1)*ctx.perPage) {
              //   this.currentPage = 1;
              // }
              callback(this.logEvents);
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
    getLogEventsTotalNumber: function() {
      let filterParams = "";
      if(this.tableNameFilter.length > 0) {

        filterParams = filterParams + "table_name=" + encodeURI(this.tableNameFilter);
      }
      // if(this.familyNameFiltre.length > 0) {
      //   if(filterParams.length > 0) {
      //     filterParams = filterParams+"&";
      //   }
      //   filterParams = filterParams + "family_name="+encodeURI(this.familyNameFiltre);
      // }
      if(filterParams.length > 0) {
        filterParams = "?" + filterParams;
      }
      getLogEventsCount(filterParams).then(
          (response) => {
            if(response.data.success) {
              this.logEventsTotalNumber = response.data.total;
            }
          }
      )
    },
    goToLogEvent: function(item) {
      console.log(item);
      // this.$router.push(`/evenements/lire/${item.id}`);
    }
  },
  mounted() {
    this.getLogEventsTotalNumber();
  },
  watch: {
    tableNameFilter: function (newValue, oldValue) {
      if(newValue !== oldValue) {
        this.getLogEventsTotalNumber();
        this.currentPage = 1;
      }
    },
  },
  computed: {
    onFilter: function() {
      return `${this.tableNameFilter}`;
    }
  }
}
</script>

<style scoped>

</style>