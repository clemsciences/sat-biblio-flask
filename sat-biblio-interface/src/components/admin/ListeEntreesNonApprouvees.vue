<template>
  <b-container>
    <div v-if="entryTotalNumber > 0">

      <b-pagination
        v-model="currentPage"
        :total-rows="entryTotalNumber"
        :per-page="perPage"
        aria-controls="my-table"
        class="my-3"/>
      <b-table striped bordered hover :items="loadEntries" :fields="fields"
               primary-key="description" :per-page="perPage" :current-page="currentPage"
               @row-dblclicked="goToEntry"
               ref="userTable">
        <template #table-caption>La liste des entrées pas encore approuvées.</template>
        <template #cell(actions)="entry">
          <b-button size="sm" @click="approve(entry)" class="mr-1" v-if="isManager">
            Approuver
          </b-button>
        </template>
      </b-table>
    </div>
    <p v-else>Il n'y a aucune entrée de type {{ entryType }} à valider.</p>
  </b-container>
</template>

<script>
import {canManage} from "@/services/rights";

export default {
  name: "ListeEntreesNonApprouvees",
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
    goTo: {
      type: Function,
    },
    entryType: {
      type: String,
      default: "",
    }
  },
  data: function() {
    return {
      entryTotalNumber: 0,
      currentPage: 1,
      entries: [],
      fields: [
        {
          key: 'contributor',
          label: 'Contributeur',
          sortable: false
        },
        {
          key: 'type',
          label: "Type",
          sortable: false
        },
        {
          key: 'description',
          label: "Description",
          sortable: false,
        },
        {
          key: 'actions',
          label: 'Actions',
          sortable: false
        }
      ],
    }
  },
  mounted() {
    this.getTotalNumber();
  },
  methods: {
    approve: function(entry) {
      // TODO
      console.log(entry);
    },
    goToEntry: function(entry) {
      // TODO
      console.log(entry);
    },
    loadEntries(ctx, callback) {
      let params = "page="+ctx.currentPage+
          "&size="+ctx.perPage;

      this.retrieveListRequest(params).then(
          (response) => {
            if(response.data.success) {
              this.entries = response.data.entries;
              // if(this.authorTotalNumber< (this.currentPage-1)*ctx.perPage) {
              //   this.currentPage = 1;
              // }
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
      this.getTotalNumberRequest("").then(
          (response) => {
            if(response.data.success) {
              this.entryTotalNumber = response.data.total;
            }
          }
      ).catch(
          (reason) => {
            console.error(reason);
      }
      );
    }
  },
  computed: {
    isManager: function() {
      return canManage(this.$store.getters.getUserRight);
    }
  }

}
</script>

<style scoped>

</style>