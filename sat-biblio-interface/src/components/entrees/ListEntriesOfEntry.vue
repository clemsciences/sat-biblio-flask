<template>
  <b-container>
    <div v-if="totalNumber > 0">
      <b-pagination
          v-model="currentPage"
          :total-rows="totalNumber"
          :per-page="perPage"
          aria-controls="my-table"
          class="my-3"/>
      <b-table striped bordered hover :items="retrieveList" :fields="fields"
               primary-key="description" :per-page="perPage" :current-page="currentPage"
               :sort-by="sortBy" @row-dblclicked="goTo">
        <template #table-caption v-if="caption.length > 0">{{ caption }}</template>
      </b-table>
    </div>
    <p v-else>Il n'y a aucune entrée.</p>
  </b-container>
</template>

<script>

import {entries} from "@/services/entries";

export default {
  name: "ListEntriesOfEntry",

  props: {
    retrieveListRequest: {
      type: Function,
    },
    getTotalNumberRequest: {
      type: Function,
    },
    perPage: {
      type: Number,
      default: 20,
    },
    caption: {
      type: String,
      default: ""
    },
    goTo: {
      type: Function,
    },
    entryId: {
      type: Number,
    }
  },
  data: function() {
    return {
      totalNumber: 0,
      currentPage: 1,
      sortBy: "type",
      entries: [],
      fields: [
        {
          key: "type_string",
          label: "Type d'entrée",
          sortable: true
        },
        {
          key: "description",
          label: "Description",
          sortable: false
        },
      ],
    }
  },
  mounted() {
    this.getTotalNumber();
  },
  methods: {
    retrieveList(ctx, callback) {
      let params = "page="+ctx.currentPage+
          "&size="+ctx.perPage+
          "&sortBy="+ctx.sortBy+
          "&valid=1";

      this.retrieveListRequest(this.entryId, params).then(
          (response) => {
            if(response.data.success) {
              this.entries = response.data.entries;
              // if(this.authorTotalNumber< (this.currentPage-1)*ctx.perPage) {
              //   this.currentPage = 1;
              // }
              this.entries.map((value) => {
                // console.log(value);
                value.type_string = entries[value.type].string;
                return value;
              });
              callback(this.entries);
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
    getTotalNumber() {
      this.getTotalNumberRequest(this.entryId, "").then(
          (response) => {
            if(response.data.success) {
              this.totalNumber = response.data.total;
            }
          }
      ).catch(
          (reason) => {
            console.error(reason);
      }
      );
    }
  },

}
</script>

<style scoped>

</style>