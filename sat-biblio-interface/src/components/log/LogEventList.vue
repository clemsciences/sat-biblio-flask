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
    <BTable striped bordered hover :provider="retrieveLogEvents" :fields="fields"
             primary-key="id" ref="logEventsTable" :per-page="perPage" :current-page="currentPage"
             :sort-by="tableSortBy" :filter="tableNameFilter" @row-dblclicked="goToLogEvent">
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
import {
  BCol,
  BContainer,
  BFormGroup,
  BFormInput,
  BPagination,
  BRow,
  BTable
} from "bootstrap-vue-next";
export default {
  name: "LogEventListView",
  components: {VueJsonPretty, BContainer, BRow, BPagination, BCol,
    BFormGroup, BFormInput, BTable, AppTitle},
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
          // bootstrap-vue-next passe un objet { value, key, item } au formatter
          // (et non l'argument positionnel « value » comme bootstrap-vue en Vue 2)
          formatter: ({ value }) => {
            if (!value) return "";
            // Normalise le format renvoyé par le backend : espace -> T et
            // microsecondes (6 chiffres) -> millisecondes (3), sinon certains
            // navigateurs (Firefox) produisent une « Invalid Date » qui fait
            // planter Intl.DateTimeFormat.format().
            const normalized = String(value).replace(" ", "T").replace(/(\.\d{3})\d+/, "$1");
            const d = new Date(normalized);
            if (isNaN(d.getTime())) return String(value);
            return new Intl.DateTimeFormat("fr-FR", {dateStyle: "short", timeStyle: "short"}).format(d);
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
    async retrieveLogEvents(ctx) {
      // Provider — ctx.sortBy est un tableau [{ key, order }] en bvn
      // currentPage et perPage ne sont pas fiables dans ctx : on utilise this.*
      const sortKey = Array.isArray(ctx.sortBy) && ctx.sortBy.length > 0
          ? ctx.sortBy[0].key
          : this.sortBy;
      let params = "?page="+this.currentPage+
          "&size="+this.perPage+
          "&sortBy="+sortKey;

      let filterParams = "";
      if(this.tableNameFilter.length > 0) {
        filterParams = filterParams+"&table_name="+encodeURI(this.tableNameFilter);
      }

      if(filterParams.length > 0) {
        params = params + filterParams;
      }
      try {
        const response = await retrieveLogEvents(params);
        if(response.data.success) {
          this.logEvents = response.data.log_events ?? [];
          // Le total vient de l'endpoint /count/ (getLogEventsTotalNumber) :
          // l'endpoint liste ne renvoie pas « total », il ne faut donc pas
          // écraser logEventsTotalNumber ici (sinon la pagination casse).
          return this.logEvents;
        }
        return [];
      } catch(reason){
        console.log(reason);
        return [];
      }
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
    },
    refreshTable: function() {
      this.$refs.logEventsTable?.refresh();
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
        this.refreshTable();
      }
    },
    // Rejoue le provider quand l'utilisateur change de page : bootstrap-vue-next
    // ne relance pas le provider de façon fiable sur le prop :current-page.
    currentPage: function () {
      this.refreshTable();
    },
  },
  computed: {
    // bootstrap-vue-next attend un tableau [{ key, order }] pour le prop sort-by
    tableSortBy: function() {
      return [{ key: this.sortBy, order: 'desc' }];
    }
  }
}
</script>

<style scoped>

</style>