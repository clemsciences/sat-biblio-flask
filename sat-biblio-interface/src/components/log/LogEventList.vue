<template>
    <BContainer>
    <AppTitle title="Liste des logs"
       info=""
       id="id-liste-logs"/>
    <BRow class="my-1">
      <BCol lg="4">
        <BFormGroup label="Tables" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BDropdown :text="tablesDropdownLabel" variant="outline-secondary"
                     size="sm" auto-close="outside" class="w-100">
            <div class="px-3 py-1" style="max-height: 260px; overflow-y: auto; min-width: 240px;">
              <BFormCheckbox v-for="name in tableNames" :key="name"
                             v-model="selectedTables" :value="name" class="text-nowrap">
                {{ name }}
              </BFormCheckbox>
              <p v-if="tableNames.length === 0" class="text-muted small mb-1">Aucune table</p>
              <hr class="my-2" v-if="tableNames.length">
              <BButton size="sm" variant="link" class="p-0"
                       :disabled="selectedTables.length === 0" @click="selectedTables = []">
                Tout décocher
              </BButton>
            </div>
          </BDropdown>
        </BFormGroup>
      </BCol>
      <BCol lg="4">
        <BFormGroup label="Type" label-cols-sm="3"
          label-align-sm="right" label-size="sm" class="mb-0">
          <BDropdown :text="eventTypesDropdownLabel" variant="outline-secondary"
                     size="sm" auto-close="outside" class="w-100">
            <div class="px-3 py-1" style="max-height: 260px; overflow-y: auto; min-width: 240px;">
              <BFormCheckbox v-for="type in eventTypes" :key="type"
                             v-model="selectedEventTypes" :value="type" class="text-nowrap">
                {{ prettyEventType(type) }}
              </BFormCheckbox>
              <p v-if="eventTypes.length === 0" class="text-muted small mb-1">Aucun type</p>
              <hr class="my-2" v-if="eventTypes.length">
              <BButton size="sm" variant="link" class="p-0"
                       :disabled="selectedEventTypes.length === 0" @click="selectedEventTypes = []">
                Tout décocher
              </BButton>
            </div>
          </BDropdown>
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
             :sort-by="tableSortBy" :filter="filterKey" @row-dblclicked="goToLogEvent">
      <template #table-caption>La liste des événements dans la base.</template>
      <template #cell(values)="data">
        <vue-json-pretty :data="JSON.parse(data.item.values)"/>
      </template>
    </BTable>
  </BContainer>
</template>

<script>
import AppTitle from "@/components/visuel/AppTitle.vue";
import {getLogEventsCount, getLogEventTableNames, getLogEventEventTypes, retrieveLogEvents} from "@/services/api.js";
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import {
  BButton,
  BCol,
  BContainer,
  BDropdown,
  BFormCheckbox,
  BFormGroup,
  BPagination,
  BRow,
  BTable
} from "bootstrap-vue-next";
export default {
  name: "LogEventListView",
  components: {VueJsonPretty, BContainer, BRow, BPagination, BCol,
    BFormGroup, BDropdown, BFormCheckbox, BButton, BTable, AppTitle},
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
      // Filtres multi-sélection (options chargées du backend)
      tableNames: [],        // noms de tables disponibles
      selectedTables: [],    // tables cochées
      eventTypes: [],        // types d'événements disponibles
      selectedEventTypes: [] // types cochés
    }
  },
  methods: {
    async retrieveLogEvents(ctx) {
      // Provider — ctx.sortBy est un tableau [{ key, order }] en bvn
      // currentPage et perPage ne sont pas fiables dans ctx : on utilise this.*
      const hasSort = Array.isArray(ctx.sortBy) && ctx.sortBy.length > 0;
      const sortKey = hasSort ? ctx.sortBy[0].key : this.sortBy;
      // Par défaut décroissant : logs du plus récent au plus ancien.
      const sortDesc = hasSort ? ctx.sortBy[0].order !== "asc" : true;
      let params = "?page="+this.currentPage+
          "&size="+this.perPage+
          "&sortBy="+sortKey+
          "&sortDesc="+sortDesc;

      if(this.selectedTables.length > 0) {
        params = params + "&table_names=" + this.selectedTables.map(encodeURIComponent).join(",");
      }
      if(this.selectedEventTypes.length > 0) {
        params = params + "&event_types=" + this.selectedEventTypes.map(encodeURIComponent).join(",");
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
      const parts = [];
      if(this.selectedTables.length > 0) {
        parts.push("table_names=" + this.selectedTables.map(encodeURIComponent).join(","));
      }
      if(this.selectedEventTypes.length > 0) {
        parts.push("event_types=" + this.selectedEventTypes.map(encodeURIComponent).join(","));
      }
      const filterParams = parts.length > 0 ? "?" + parts.join("&") : "";
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
    },
    loadTableNames: function() {
      getLogEventTableNames().then(
          (response) => {
            if(response.data.success) {
              this.tableNames = response.data.table_names ?? [];
            }
          }
      );
    },
    loadEventTypes: function() {
      getLogEventEventTypes().then(
          (response) => {
            if(response.data.success) {
              this.eventTypes = response.data.event_types ?? [];
            }
          }
      );
    },
    prettyEventType: function(type) {
      return {create: "Création", update: "Modification", delete: "Suppression"}[type] ?? type;
    }
  },
  mounted() {
    this.loadTableNames();
    this.loadEventTypes();
    this.getLogEventsTotalNumber();
  },
  watch: {
    // filterKey change quand la sélection de tables change : on met à jour le
    // total, on revient page 1 et on rejoue le provider.
    filterKey: function () {
      this.getLogEventsTotalNumber();
      this.currentPage = 1;
      this.refreshTable();
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
    },
    // Clé de filtre pour le prop :filter du BTable (déclenche le provider) et
    // pour le watcher : chaîne stable dérivée des deux sélections.
    filterKey: function() {
      return this.selectedTables.join(",") + "|" + this.selectedEventTypes.join(",");
    },
    tablesDropdownLabel: function() {
      if(this.selectedTables.length === 0) return "Toutes les tables";
      if(this.selectedTables.length === 1) return this.selectedTables[0];
      return `${this.selectedTables.length} tables sélectionnées`;
    },
    eventTypesDropdownLabel: function() {
      if(this.selectedEventTypes.length === 0) return "Tous les types";
      if(this.selectedEventTypes.length === 1) return this.prettyEventType(this.selectedEventTypes[0]);
      return `${this.selectedEventTypes.length} types sélectionnés`;
    }
  }
}
</script>

<style scoped>

</style>